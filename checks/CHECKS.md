# Check Registry

Every custom policy that exists in this repository is listed here. It includes what it enforces and where its definition/tests live. For more information, see the [README](../README.md) for steps on how to add a new policy.

## Numbering convention

The first digit of `{NUMBER}` encodes the service category; subsequent checks for that
service increment from there.

| Rule Number | Category | Check IDs |
|---|---|---|
| `1x` | S3 | `CKV_XM_AWS_S3_1` - requires server-side encryption on a bucket, either inline or via a separate encryption resource. [tests](../test/terraform/s3/test_ensure_encryption.py)<br>`CKV_XM_AWS_S3_11` - blocks `force_destroy = true`, which would allow destroying a bucket that still holds objects. [tests](../test/terraform/s3/test_deny_force_destroy.py)<br>`CKV_XM_AWS_S3_12` - requires `mfa_delete` on bucket versioning. [tests](../test/terraform/s3/test_ensure_mfa_delete.py) |
| `2x` | SM (Secrets Manager) | `CKV_XM_AWS_SM_2` - requires a secret's deletion recovery window to be 30 days. [tests](../test/terraform/sm/test_ensure_recovery_window.py) |
| `3x` | Tags | `CKV_XM_AWS_TAGS_3` - requires an `Owner` tag on EC2 instances and S3 buckets. [tests](../test/terraform/tags/test_required_tags.py) |
| `4x` | ECR | `CKV_XM_AWS_ECR_41` - requires image tag mutability to be IMMUTABLE to prevent overwriting existing image tags. [tests](../test/terraform/ecr/test_ensure_immutable_tags.py) |
