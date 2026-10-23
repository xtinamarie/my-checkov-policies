import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import yaml
from mcp_cli import build_args, CHECKS_DIR


class TestMcpCli:
    """Tests for mcp CLI wrapper warning mode and Checkov configuration."""

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

    def test_build_args_preserves_explicit_soft_fail(self):
        user_args = ["-d", ".", "--soft-fail"]
        constructed = build_args(user_args)

        assert constructed.count("--soft-fail") == 1
        assert "--soft-fail-on" not in constructed

    def test_build_args_preserves_explicit_soft_fail_on(self):
        user_args = ["-d", ".", "--soft-fail-on", "CKV_XM_AWS_ECR_42"]
        constructed = build_args(user_args)

        assert constructed.count("--soft-fail-on") == 1
        idx = constructed.index("--soft-fail-on")
        assert constructed[idx + 1] == "CKV_XM_AWS_ECR_42"

    def test_build_args_preserves_explicit_hard_fail_on(self):
        user_args = ["-d", ".", "--hard-fail-on", "LOW"]
        constructed = build_args(user_args)

        assert "--hard-fail-on" in constructed
        assert "--soft-fail-on" not in constructed

    def test_checkov_yaml_config_exists_and_configured(self):
        config_file = ROOT_DIR / ".checkov.yaml"
        assert config_file.exists(), "Expected .checkov.yaml to exist in repository root"

        with open(config_file, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        assert "soft-fail-on" in config
        assert "LOW" in config["soft-fail-on"]
