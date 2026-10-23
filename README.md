# my-checkov-policies

This repository is my customized [checkov](https://github.com/bridgecrewio/checkov) policies for Terraform infrastructure scanning. Built-in checkov checks run automatically alongside the custom policies defined in this repo.

#### Setup

```bash
pip install -e ".[dev]"
```
This command will ensure that you are installing all the necessary packages:
- checkov
- pytest
- the `mcp` CLI command (read more below)

#### Check ID naming convention

All custom check IDs from this repository will be required to follow this pattern:

```
CKV_XM_AWS_{SERVICE}_{NUMBER}
```

| Segment | Meaning |
|---|---|
| `CKV_` | Standard Checkov prefix |
| `XM_` | Shortened for `xtinamarie`. This uniquely namespaces these checks that I will be creating so they never clash with built-in or third-party checks |
| `AWS_` | Cloud provider |
| `{SERVICE}` | AWS service abbreviation (`S3`, `SM`, `EC2`, `IAM`, `TAGS`, …) |
| `{NUMBER}` | First digit encodes the service category; subsequent checks increment from there |

See [checks/CHECKS.md](checks/CHECKS.md) for the full check registry.

> **Note:** Please do NOT ever use the `CKV2_` prefix for custom checks — Checkov reserves that for its own graph-based checks and it will cause conflicts.


#### `mcp` CLI command

`mcp` (short for my-checkov-policies) is a thin wrapper around `checkov` that automatically loads the custom policies from this repository. Every flag that checkov accepts works exactly the same way:

```bash
# Scan a directory
mcp -d /path/to/terraform

# Scan a single file
mcp -f main.tf

# Run only specific checks
mcp -d /path/to/terraform --check CKV_XM_AWS_S3_1

# Run only checks at or above a severity
mcp -d /path/to/terraform --check HIGH

# Skip specific checks
mcp -d /path/to/terraform --skip-check CKV_AWS_18

# Change output format
mcp -d /path/to/terraform -o json

# Show all available flags (same as checkov --help)
mcp --help
```

#### Enforcement & Warning Mode (Soft-blocking)

Policies in this repository support two enforcement levels based on severity:

- **Required policies (`CRITICAL`, `HIGH`, `MEDIUM`)**: Hard-blocking gates. Failures return a non-zero exit code (`1`), preventing non-compliant infrastructure from deploying.
- **Recommended policies (`LOW`)**: Warning mode (soft-fail). Failures output full findings with official guideline documentation links, but exit with code `0` to prevent blocking deployment pipelines on recommendations.

This behavior is supported both locally and in CI/CD pipelines:

- **Local CLI (`mcp`)**: Defaults to `--soft-fail-on LOW` out of the box unless explicitly overridden with `--soft-fail`, `--soft-fail-on`, or `--hard-fail-on`.
- **CI / Pipeline integration**: The repository root `.checkov.yaml` configures `soft-fail-on: [LOW]`. Pipelines running Checkov against these policies inherit this configuration automatically or via `--config-file .checkov.yaml`.

To force hard failures on recommended checks as well, use `--hard-fail-on`:

```bash
mcp -d /path/to/terraform --hard-fail-on LOW
```
<br><br>
# Adding a new custom policy

In order to add your own custom policy, follow the steps outlined below.
#### 1. Write the check

Create a `.yaml` file under the file structure `checks/terraform/aws/{service}/`:

```yaml
metadata:
  name: "Human-readable description"
  id: "CKV_XM_AWS_{SERVICE}_{NUMBER}"
  category: "ENCRYPTION"   # or GENERAL_SECURITY, LOGGING, etc.
  severity: "HIGH"         # CRITICAL, HIGH, MEDIUM, or LOW
  guideline: "https://docs.aws.amazon.com/..." # link to official remediation docs
scope:
  provider: terraform
definition:
  and:
    - cond_type: attribute
      resource_types:
        - aws_s3_bucket
      attribute: "logging"
      operator: exists
```

For more details on creating a custom policy in YAML and understanding the structure, see [this documentation](https://www.checkov.io/3.Custom%20Policies/YAML%20Custom%20Policies.html) on checkov's docsite.

#### 2. Add test fixtures

It is essential to add both Terraform and Terraform Plan files to ensure that the check you created is working as expected in both scenarios.

```text
#compliant resources
test/resources/terraform/{service}/{check_name}/pass/main.tf
test/resources/terraform/{service}/{check_name}/pass/tfplan.json

#non-compliant resources
test/resources/terraform/{service}/{check_name}/fail/main.tf
test/resources/terraform/{service}/{check_name}/fail/tfplan.json
```

A `pass/` and a `fail/` directory are required for every check — CI fails a pull request if
either is missing, or if either lacks its `main.tf` or `tfplan.json`. Additional variant
directories (for example `pass_separate_resource/`) are allowed alongside them when a check
has more than one compliant or non-compliant shape worth covering.

Generate the `tfplan.json` files with [scripts/gen_plan.sh](scripts/gen_plan.sh), which runs
`terraform init`/`plan`/`show -json` in a temp workspace using mock credentials, so nothing
is ever authenticated or applied:

```bash
./scripts/gen_plan.sh test/resources/terraform/{service}/{check_name}/pass
```

#### 3. Write the test

When adding a test class, make sure to follow this test directory structure: `test/terraform/{service}/test_{service}.py`

Once the file has been created, the general structure for the pytest files is shown below:

```python
class TestMyNewCheck:
    CHECK_ID = "CKV_XM_AWS_{SERVICE}_{NUMBER}"

    def test_compliant_resource_passes(self):
        results = _scan(RESOURCES_DIR / "{service}/{check_name}/pass", self.CHECK_ID)
        assert results == [CheckResult.PASSED]

    def test_non_compliant_resource_fails(self):
        results = _scan(RESOURCES_DIR / "{service}/{check_name}/fail", self.CHECK_ID)
        assert results == [CheckResult.FAILED]
```

## Related

- Forked checkov repo: https://github.com/xtinamarie/checkov