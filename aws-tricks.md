
`
aws ssm start-session --target ssm-managed-instance-id \
--document-name AWS-StartPortForwardingSessionToRemoteHost \
--parameters '{"portNumber":["5432"],"localPortNumber":["5432"],"host":[" remote-database-host-name"]}'

psql -h 127.0.0.1 -U postgres



`
