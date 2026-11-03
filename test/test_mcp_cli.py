import os
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml
from mcp_cli import build_args, CHECKS_DIR

ROOT_DIR = Path(__file__).resolve().parents[1]
RESOURCES_DIR = ROOT_DIR / "test" / "resources" / "terraform"
FAIL_KMS_DIR = RESOURCES_DIR / "ecr" / "ensure_kms_encryption" / "fail"
CLI_SCRIPT = ROOT_DIR / "mcp_cli.py"


class TestMcpCliUnit:
    """Unit tests for mcp CLI argument construction and configuration."""

    def test_build_args_defaults_to_soft_fail_on_low(self):
        user_args = ["-d", "/path/to/terraform"]
        constructed = build_args(user_args)

        assert "--external-checks-dir" in constructed
        assert str(CHECKS_DIR) in constructed
        assert "--quiet" in constructed
        assert "--soft-fail-on" in constructed
        idx = constructed.index("--soft-fail-on")
        assert constructed[idx + 1] == "LOW"
        assert constructed[-2:] == ["-d", "/path/to/terraform"]

    def test_build_args_handles_equals_syntax_for_soft_fail_on(self):
        user_args = ["-d", ".", "--soft-fail-on=CKV_XM_AWS_TAGS_3"]
        constructed = build_args(user_args)

        assert "--soft-fail-on=CKV_XM_AWS_TAGS_3" in constructed
        assert constructed.count("--soft-fail-on") == 0
        assert "LOW" not in constructed

    def test_build_args_handles_short_flag_s(self):
        user_args = ["-d", ".", "-s"]
        constructed = build_args(user_args)

        assert "-s" in constructed
        assert "--soft-fail-on" not in constructed

    def test_build_args_preserves_explicit_soft_fail(self):
        user_args = ["-d", ".", "--soft-fail"]
        constructed = build_args(user_args)

        assert constructed.count("--soft-fail") == 1
        assert "--soft-fail-on" not in constructed

    def test_build_args_preserves_explicit_hard_fail_on(self):
        user_args = ["-d", ".", "--hard-fail-on", "LOW"]
        constructed = build_args(user_args)

        assert "--hard-fail-on" in constructed
        assert "--soft-fail-on" not in constructed

    def test_build_args_handles_equals_syntax_for_hard_fail_on(self):
        user_args = ["-d", ".", "--hard-fail-on=LOW"]
        constructed = build_args(user_args)

        assert "--hard-fail-on=LOW" in constructed
        assert "--soft-fail-on" not in constructed

    def test_build_args_escape_hatch_env_var(self, monkeypatch):
        monkeypatch.setenv("MCP_NO_SOFT_FAIL", "1")
        user_args = ["-d", "/path/to/terraform"]
        constructed = build_args(user_args)

        assert "--soft-fail-on" not in constructed

    def test_build_args_escape_hatch_cli_args(self):
        # Passed as MCP_NO_SOFT_FAIL=1 argument (stripped from checkov args)
        constructed_env_arg = build_args(["-d", ".", "MCP_NO_SOFT_FAIL=1"])
        assert "--soft-fail-on" not in constructed_env_arg
        assert "MCP_NO_SOFT_FAIL=1" not in constructed_env_arg

        # Passed as --no-soft-fail argument (stripped from checkov args)
        constructed_flag = build_args(["-d", ".", "--no-soft-fail"])
        assert "--soft-fail-on" not in constructed_flag
        assert "--no-soft-fail" not in constructed_flag

    def test_checkov_yaml_config_exists_and_configured(self):
        config_file = ROOT_DIR / ".checkov.yaml"
        assert config_file.exists(), "Expected .checkov.yaml to exist in repository root"

        with open(config_file, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        assert "soft-fail-on" in config
        assert "LOW" in config["soft-fail-on"]


class TestMcpCliExitCodes:
    """Integration tests validating real Checkov exit codes through mcp_cli."""

    def test_exit_code_soft_fail_low_check_passes_with_zero(self):
        # Scoped to LOW severity check CKV_XM_AWS_ECR_42: warning mode activates and exits 0
        with tempfile.TemporaryDirectory() as tmpdir:
            cmd = [
                sys.executable,
                str(CLI_SCRIPT),
                "-d",
                str(FAIL_KMS_DIR),
                "--check",
                "CKV_XM_AWS_ECR_42",
                "--framework",
                "terraform",
            ]
            proc = subprocess.run(cmd, cwd=tmpdir, capture_output=True, text=True)
            assert proc.returncode == 0, (
                f"Expected exit code 0 when soft-failing on LOW check, got {proc.returncode}.\n"
                f"Stdout: {proc.stdout}\nStderr: {proc.stderr}"
            )

    def test_exit_code_unscoped_fail_directory_hard_fails_with_one(self):
        # Unscoped directory scan: CKV_XM_AWS_ECR_4 (MEDIUM severity) also fails and causes hard exit 1
        with tempfile.TemporaryDirectory() as tmpdir:
            cmd = [
                sys.executable,
                str(CLI_SCRIPT),
                "-d",
                str(FAIL_KMS_DIR),
                "--framework",
                "terraform",
            ]
            proc = subprocess.run(cmd, cwd=tmpdir, capture_output=True, text=True)
            assert proc.returncode == 1, (
                f"Expected exit code 1 when unscoped check failures include MEDIUM, got {proc.returncode}.\n"
                f"Stdout: {proc.stdout}\nStderr: {proc.stderr}"
            )

    def test_exit_code_escape_hatch_hard_fails_with_one(self):
        # With escape hatch MCP_NO_SOFT_FAIL=1, soft-fail is suppressed so even LOW checks exit 1
        with tempfile.TemporaryDirectory() as tmpdir:
            env = os.environ.copy()
            env["MCP_NO_SOFT_FAIL"] = "1"
            cmd = [
                sys.executable,
                str(CLI_SCRIPT),
                "-d",
                str(FAIL_KMS_DIR),
                "--check",
                "CKV_XM_AWS_ECR_42",
                "--framework",
                "terraform",
            ]
            proc = subprocess.run(cmd, cwd=tmpdir, env=env, capture_output=True, text=True)
            assert proc.returncode == 1, (
                f"Expected exit code 1 when MCP_NO_SOFT_FAIL=1 suppresses soft-fail, got {proc.returncode}.\n"
                f"Stdout: {proc.stdout}\nStderr: {proc.stderr}"
            )
