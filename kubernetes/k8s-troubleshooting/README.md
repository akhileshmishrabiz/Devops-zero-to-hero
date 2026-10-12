# Kubernetes intermittent 503 troubleshooting demo

This lab recreates a Service that looks healthy in Kubernetes while one newly
started pod returns `503` from the real payment path for 90 seconds.

The intentionally broken configuration checks `/healthz` for readiness.
`/healthz` only proves that the Python process is alive; `/payments` also needs
an initialized connection pool. The fixed configuration checks the dependency
state and adds safe rollout settings.

## What the demo proves

- `Running` and a green liveness probe do not mean an application can serve traffic.
- A pod enters a Service's EndpointSlice when its readiness condition becomes true.
- A probe can succeed while a business endpoint fails if it checks the wrong signal.
- Service backend choice is normally made per network connection, not per HTTP request.
- HTTP keep-alive can make request-level failure percentages very different from the
  fraction of unhealthy pods.
- `startupProbe`, `readinessProbe`, `minReadySeconds`, and `maxUnavailable` solve
  different parts of the problem.

The exact “one in fifty” rate is not guaranteed. It depends on connection reuse,
connection-pool size, request distribution, and kube-proxy implementation. This
lab demonstrates the mechanism rather than forcing a misleading fixed percentage.

## Files

- `kind-config.yaml`: isolated three-node Kind cluster.
- `broken-demo.yaml`: application, broken Deployment, Service, and test client.
- `fixed-demo.yaml`: strategic merge patch containing the corrected probes and rollout policy.

## 1. Create and verify the Kind context

Run all commands from this directory:

```bash
kind create cluster --config kind-config.yaml
kubectl config use-context kind-k8s-troubleshooting
kubectl config current-context
```

The final command must print exactly:

```text
kind-k8s-troubleshooting
```

Use this guard before every destructive command:

```bash
test "$(kubectl config current-context)" = "kind-k8s-troubleshooting" \
  || { echo "Wrong Kubernetes context"; exit 1; }
```

Optional context inspection:

```bash
kubectl cluster-info --context kind-k8s-troubleshooting
kubectl get nodes -o wide
```

## 2. Deploy the intentionally broken version

```bash
kubectl apply -f broken-demo.yaml
kubectl -n payment-demo rollout status deployment/payment --timeout=2m
kubectl -n payment-demo wait --for=condition=Ready pod/demo-client --timeout=2m
kubectl -n payment-demo get pods -o wide
```

The image may need to be pulled the first time. The payment pods become `Ready`
after about 10 seconds even though `/payments` needs 90 seconds. For a clean
baseline, wait until the initial pods are genuinely initialized:

```bash
sleep 95
kubectl -n payment-demo exec demo-client -- \
  python /app/load_test.py --mode new --requests 20
```

Expected result: 20 responses with status `200`.

## 3. Trigger the incident

Deleting one pod simulates a newly created pod during a rollout. The other three
remain old and fully initialized.

```bash
OLD_POD=$(kubectl -n payment-demo get pods -l app=payment \
  --sort-by=.metadata.creationTimestamp \
  -o jsonpath='{.items[0].metadata.name}')

kubectl -n payment-demo delete pod "$OLD_POD" --wait=true

NEW_POD=$(kubectl -n payment-demo get pods -l app=payment \
  --sort-by=.metadata.creationTimestamp \
  -o jsonpath='{.items[-1:].metadata.name}')

kubectl -n payment-demo wait --for=condition=Ready "pod/$NEW_POD" --timeout=45s
echo "New pod: $NEW_POD"
kubectl -n payment-demo get pods -l app=payment
```

You should see three older pods and one new pod, all shown as `1/1 Running`.
Run the remaining investigation within 90 seconds of the new pod starting. To
repeat the window, delete the newest pod again.

## 4. Start with normal cluster checks

```bash
kubectl -n payment-demo get pods -o wide
kubectl -n payment-demo get deployment payment
kubectl -n payment-demo get events --sort-by=.lastTimestamp
kubectl -n payment-demo describe pod "$NEW_POD"
```

What to point out:

- There are no restarts or `CrashLoopBackOff` events.
- The new pod passes liveness.
- Its `READY` column is `1/1`.
- Its age is much lower than the other pods.

## 5. Inspect the Service and EndpointSlices

`kubectl get endpoints` remains useful for a quick check, but EndpointSlice is
the current API to inspect in detail.

```bash
kubectl -n payment-demo get service payment
kubectl -n payment-demo get endpoints payment -o wide
kubectl -n payment-demo get endpointslices \
  -l kubernetes.io/service-name=payment -o wide
kubectl -n payment-demo get endpointslices \
  -l kubernetes.io/service-name=payment -o yaml
```

Find the new pod IP:

```bash
NEW_IP=$(kubectl -n payment-demo get pod "$NEW_POD" \
  -o jsonpath='{.status.podIP}')
echo "$NEW_IP"
```

That IP appears as a ready EndpointSlice endpoint even though `/payments` still
returns `503`. Kubernetes trusts the configured readiness probe.

For a concise pod-to-IP map:

```bash
kubectl -n payment-demo get pods -l app=payment \
  -o custom-columns='NAME:.metadata.name,IP:.status.podIP,READY:.status.containerStatuses[0].ready,STARTED:.status.startTime'
```

## 6. Bypass the Service and prove the pod is faulty

In terminal 1:

```bash
kubectl -n payment-demo port-forward "pod/$NEW_POD" 18080:8080
```

In terminal 2:

```bash
curl -i http://127.0.0.1:18080/healthz
curl -i http://127.0.0.1:18080/readyz
curl -i http://127.0.0.1:18080/payments
```

During warm-up:

- `/healthz` returns `200`.
- `/readyz` returns `503`.
- `/payments` returns `503`.

This isolates the application from Service routing, DNS, kube-proxy, and ingress.
Stop the port-forward with `Ctrl-C`.

## 7. Compare connection behavior

Fifty new TCP connections are distributed among Service backends. During the
fault window, the result is usually close to one unhealthy backend out of four,
but it is random:

```bash
kubectl -n payment-demo exec demo-client -- \
  python /app/load_test.py --mode new --requests 50
```

Example shape, not an exact promise:

```text
status counts: {200: 38, 503: 12}
requests by backend: {payment-...: ...}
```

Now send 50 requests over one persistent HTTP connection:

```bash
kubectl -n payment-demo exec demo-client -- \
  python /app/load_test.py --mode keepalive --requests 50
```

All 50 requests normally go to one backend. The batch therefore tends to be all
`200` or all `503`. Run it several times to establish new connections:

```bash
for i in 1 2 3 4 5 6 7 8; do
  kubectl -n payment-demo exec demo-client -- \
    python /app/load_test.py --mode keepalive --requests 50
done
```

Now model the post's traffic pattern directly: 46 requests reuse an established
healthy connection and four requests create new connections. Since about one in
four new connections can reach the warming pod, the expected result is roughly
one failed request out of fifty:

```bash
kubectl -n payment-demo exec demo-client -- \
  python /app/load_test.py --mode mixed --requests 50 --new-requests 4
```

Because backend selection is random, one run can produce zero, one, or several
failures. Run ten rounds to show that the aggregate rate trends toward 2%:

```bash
for i in $(seq 1 10); do
  kubectl -n payment-demo exec demo-client -- \
    python /app/load_test.py --mode mixed --requests 50 --new-requests 4
done
```

This is the defensible version of the “one in fifty” explanation. An application
with a pool of mostly long-lived healthy connections and relatively few new
connections can see a much lower request failure rate than 25%. The observed
ratio is a property of the workload and its connection pool, not round-robin
HTTP routing.

## 8. Correlate the 503s with one pod

Inspect all current payment pod logs:

```bash
kubectl -n payment-demo logs -l app=payment \
  --all-containers=true --prefix=true --since=10m
```

Show only payment failures:

```bash
kubectl -n payment-demo logs -l app=payment \
  --all-containers=true --prefix=true --since=10m \
  | grep 'path=/payments status=503'
```

Group failures by pod IP:

```bash
kubectl -n payment-demo logs -l app=payment \
  --all-containers=true --prefix=true --since=10m \
  | awk '
      /path=\/payments status=503/ {
        for (i=1; i<=NF; i++) {
          if ($i ~ /^pod_ip=/) failures[$i]++
        }
      }
      END {
        for (ip in failures) print ip, failures[ip]
      }'
```

The `503` entries should all identify the newly started pod/IP.

## 9. Prove the probe is wrong

```bash
kubectl -n payment-demo get deployment payment \
  -o jsonpath='{.spec.template.spec.containers[0].readinessProbe.httpGet.path}{"\n"}'

kubectl -n payment-demo get deployment payment -o yaml
```

The broken readiness path is `/healthz`. It answers “is the process alive?”,
not “can this instance process a payment?”

## 10. Watch a fixed rollout

Start this watch in terminal 1:

```bash
kubectl -n payment-demo get pods -w
```

Start this watch in terminal 2:

```bash
kubectl -n payment-demo get endpointslices \
  -l kubernetes.io/service-name=payment -w
```

Apply the strategic merge patch in terminal 3:

```bash
kubectl -n payment-demo patch deployment payment \
  --type=strategic --patch-file=fixed-demo.yaml

kubectl -n payment-demo rollout status deployment/payment --timeout=12m
```

The rollout is deliberately slow enough to observe:

1. A new pod starts.
2. `startupProbe` calls `/startupz` while dependencies initialize.
3. The pod stays `0/1` and does not enter the Service as a ready endpoint.
4. At roughly 90 seconds, startup succeeds and readiness starts.
5. Readiness checks `/readyz`, which reflects payment dependency state.
6. `minReadySeconds: 30` requires the pod to remain ready before it is Available.
7. `maxUnavailable: 0` prevents the rolling update from intentionally dropping
   below the desired number of available replicas.
8. `maxSurge: 1` permits one extra pod while replacement occurs.

Important nuance: `minReadySeconds` affects Deployment availability and rollout
progress. It does not delay a Ready pod from entering the Service. The corrected
readiness probe is what prevents premature traffic.

Inspect the final settings:

```bash
kubectl -n payment-demo get deployment payment \
  -o jsonpath='{.spec.minReadySeconds}{"\n"}'
kubectl -n payment-demo get deployment payment \
  -o jsonpath='{.spec.strategy.rollingUpdate}{"\n"}'
kubectl -n payment-demo get deployment payment -o yaml
```

## 11. Verify the fix

While a fixed pod is still warming, it should not appear as a ready endpoint.
After rollout completion:

```bash
kubectl -n payment-demo get pods -o wide
kubectl -n payment-demo get endpointslices \
  -l kubernetes.io/service-name=payment -o wide

kubectl -n payment-demo exec demo-client -- \
  python /app/load_test.py --mode new --requests 200
```

Expected result:

```text
status counts: {200: 200}
```

## Probe and rollout responsibilities

- `startupProbe`: protects slow startup. Until it succeeds, kubelet does not run
  readiness or liveness probes.
- `readinessProbe`: controls whether the pod is eligible for Service traffic.
- `livenessProbe`: detects a stuck process and may restart the container. It
  should not be used to model temporary dependency availability.
- `minReadySeconds`: controls when the Deployment counts a Ready pod as Available.
- `maxUnavailable: 0`: preserves desired availability during a rolling update,
  assuming enough cluster capacity exists.

## Cleanup

Delete only the demo namespace:

```bash
test "$(kubectl config current-context)" = "kind-k8s-troubleshooting" \
  && kubectl delete namespace payment-demo
```

Delete the entire dedicated cluster:

```bash
kind delete cluster --name k8s-troubleshooting
```

## Suggested live-demo narration

1. “The symptom is intermittent 503s, but Kubernetes reports four healthy pods.”
2. “One pod is much newer, so I will test whether failures correlate with it.”
3. “The Service includes all four pod IPs because all four readiness checks pass.”
4. “Direct pod access proves `/healthz` is 200 while `/payments` is 503.”
5. “Logs group every 503 under the new pod's IP.”
6. “Persistent connections explain why request percentages need not match pod percentages.”
7. “Kubernetes is following our readiness contract; the contract is wrong.”
8. “The fix models startup, traffic eligibility, and rollout availability separately.”
