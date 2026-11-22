# Check Registry

Every custom policy that exists in this repository is listed here. It includes what it enforces, its severity, and where its definition/tests live. For more information, see the [README](../README.md) for steps on how to add a new policy.

## Numbering convention

The first digit of `{NUMBER}` encodes the service category; subsequent checks for that
service increment from there.

| Rule Number | Category | Check IDs |
|---|---|---|
| `1x` | S3 | `CKV_XM_AWS_S3_1` (**HIGH**) - requires server-side encryption on a bucket, either inline or via a separate encryption resource. [tests](../test/terraform/s3/test_ensure_encryption.py)<br>`CKV_XM_AWS_S3_11` (**MEDIUM**) - blocks `force_destroy = true`, which would allow destroying a bucket that still holds objects. [tests](../test/terraform/s3/test_deny_force_destroy.py)<br>`CKV_XM_AWS_S3_12` (**MEDIUM**) - requires `mfa_delete` on bucket versioning. [tests](../test/terraform/s3/test_ensure_mfa_delete.py) |
| `2x` | SM (Secrets Manager) | `CKV_XM_AWS_SM_2` (**LOW**) - requires a secret's deletion recovery window to be 30 days. [tests](../test/terraform/sm/test_ensure_recovery_window.py) |
| `3x` | Tags | `CKV_XM_AWS_TAGS_3` (**LOW**) - requires an `Owner` tag on EC2 instances and S3 buckets. [tests](../test/terraform/tags/test_required_tags.py) |
| `4x` | ECR | `CKV_XM_AWS_ECR_41` (**HIGH**) - requires image tag mutability to have strict equality of IMMUTABLE only; no other values are accepted. [tests](../test/terraform/ecr/test_ensure_immutable_tags.py)<br>`CKV_XM_AWS_ECR_4` (**MEDIUM**) - requires image scan on push to be enabled (`scan_on_push = true`) on the repository. [tests](../test/terraform/ecr/test_ensure_scan_on_push.py)<br>`CKV_XM_AWS_ECR_42` (**LOW**) - requires ECR repository encryption to be configured with KMS (`encryption_type = "KMS"`). [tests](../test/terraform/ecr/test_ensure_kms_encryption.py) |
| `5x` | EKS | `CKV_XM_AWS_EKS_5` (**MEDIUM**) - requires control plane logging on an EKS cluster to include at least `api`, `audit`, and `authenticator`. [tests](../test/terraform/eks/test_ensure_control_plane_logging.py)<br>`CKV_XM_AWS_EKS_51` (**MEDIUM**) - requires EKS cluster secrets to be encrypted with a customer managed KMS key. [tests](../test/terraform/eks/test_ensure_secrets_cmk_encryption.py)<br>`CKV_XM_AWS_EKS_52` (**HIGH**) - requires EKS public endpoint access to be disabled or restricted to non-0.0.0.0/0 CIDRs. [tests](../test/terraform/eks/test_ensure_restricted_api_endpoint.py) |

