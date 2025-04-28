# GitHub Actions Pipeline with SonarQube, Trivy, tfsec, and Checkov

Here's a comprehensive GitHub Actions workflow that integrates these security scanning tools for a robust DevSecOps pipeline. I'll provide the workflow file and setup instructions.

## The Workflow File

Create a file named `.github/workflows/devsecops-pipeline.yml` in your repository:

```yaml
name: DevSecOps Pipeline

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  code-security-scan:
    name: Code Security Scan
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Required for SonarQube to get all history for coverage and blame information

      - name: Set up JDK 17
        uses: actions/setup-java@v3
        with:
          distribution: 'temurin'
          java-version: '17'

      - name: SonarQube Scan
        uses: SonarSource/sonarqube-scan-action@master
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}

      - name: SonarQube Quality Gate
        uses: SonarSource/sonarqube-quality-gate-action@master
        timeout-minutes: 5
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}

  container-security-scan:
    name: Container Security Scan
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'table'
          exit-code: '1'
          ignore-unfixed: true
          severity: 'CRITICAL,HIGH'

  iac-security-scan:
    name: Infrastructure as Code Security Scan
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: tfsec
        uses: aquasecurity/tfsec-action@v1.0.0
        with:
          soft_fail: true

      - name: Checkov
        uses: bridgecrewio/checkov-action@master
        with:
          directory: .
          framework: terraform
          soft_fail: true
          output_format: github_failed_only
          download_external_modules: true
          quiet: false
          log_level: WARNING

  security-scan-summary:
    name: Security Scan Summary
    needs: [code-security-scan, container-security-scan, iac-security-scan]
    runs-on: ubuntu-latest
    steps:
      - name: Summary
        run: |
          echo "## Security Scan Summary" >> $GITHUB_STEP_SUMMARY
          echo "✅ All security scans completed" >> $GITHUB_STEP_SUMMARY
          echo "Please check individual job logs for detailed results" >> $GITHUB_STEP_SUMMARY
```

## Setup Instructions

### 1. SonarQube Setup

1. **Set up SonarQube server**:
   - Either use SonarCloud (cloud-based option) or set up your own SonarQube server
   - If self-hosted, ensure it's accessible from GitHub Actions

2. **Create a SonarQube project**:
   - Log in to SonarQube
   - Create a new project and generate a token

3. **Add GitHub Secrets**:
   - Go to your GitHub repository → Settings → Secrets → Actions
   - Add two secrets:
     - `SONAR_HOST_URL`: Your SonarQube server URL (e.g., `https://sonarqube.yourcompany.com`)
     - `SONAR_TOKEN`: Your SonarQube authentication token

4. **Create a sonar-project.properties file** in your repository root:
   ```properties
   sonar.projectKey=your-project-key
   sonar.projectName=Your Project Name
   sonar.sources=.
   sonar.exclusions=**/*.test.js,**/*.spec.js,**/node_modules/**,**/vendor/**
   sonar.sourceEncoding=UTF-8
   # If you have specific test directories:
   sonar.tests=tests
   sonar.test.inclusions=**/*.test.js,**/*.spec.js
   ```

### 2. Trivy Configuration

Trivy will scan your codebase for vulnerabilities in dependencies and container images. No additional configuration is needed, but if you have Docker images, you might want to customize the scan:

For Docker images, modify the Trivy action:
```yaml
- name: Run Trivy vulnerability scanner for Docker
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: 'your-docker-image:tag'
    format: 'sarif'
    output: 'trivy-results.sarif'
```

### 3. tfsec and Checkov Setup

These tools will scan your Terraform files for security issues. They work out of the box, but you can add custom configuration:

For tfsec:
- Create a `.tfsec/config.yaml` file for custom rules or to exclude specific checks:
  ```yaml
  exclude:
    - AWS018  # Example: exclude check for enabling S3 access logging
  ```

For Checkov:
- Create a `.checkov.yaml` or `.checkov.yml` file:
  ```yaml
  skip-check:
    - CKV_AWS_116  # Example: skip check for S3 bucket encryption
  ```

## Making It Work for Your Project

Depending on your project's structure, you may need to adjust:

1. **Language-specific configurations**:
   - For Node.js projects, you might add `npm install` before scans
   - For Java projects, you might need Maven or Gradle steps

2. **CI pipeline customization**:
   - Add build and test steps before security scans
   - Configure notifications (Slack, email) for security findings

3. **Terraform specific settings**:
   - If your Terraform files are in a subdirectory, adjust the paths in the tfsec and Checkov steps

## Handling Scan Results

By default, this pipeline will:
- Fail on critical and high severity issues detected by Trivy
- Soft fail (continue but report issues) for tfsec and Checkov
- Gate deployments based on SonarQube quality gates

To make the pipeline less strict for initial implementation:
- Change `exit-code: '1'` to `exit-code: '0'` in the Trivy step
- Set `soft_fail: true` for all tools (already set in the example)

## Additional Tips

1. **Start with soft failures**: While implementing, set all tools to "soft fail" so pipelines complete while you fix issues.

2. **Baseline current state**: Run the pipeline once and document all current issues before enforcing stricter policies.

3. **Incrementally enforce**: Gradually increase the strictness as your team addresses security findings.

4. **Documentation**: Create documentation for your team on how to interpret and fix common findings from each tool.

5. **Custom policy development**: Once familiar with the tools, develop custom policies specific to your organization's needs.

This pipeline provides a solid foundation for implementing DevSecOps practices in your project. The combination of SonarQube (code quality), Trivy (container security), tfsec and Checkov (IaC security) gives you comprehensive coverage across different aspects of your application security.
