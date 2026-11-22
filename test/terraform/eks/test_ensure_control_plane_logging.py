from pathlib import Path

from checkov.common.models.enums import CheckResult
from checkov.runner_filter import RunnerFilter
from checkov.terraform.runner import Runner
from checkov.terraform.plan_runner import Runner as TFPlanRunner

CHECKS_DIR = Path(__file__).parents[3] / "checks"
RESOURCES_DIR = Path(__file__).parents[2] / "resources" / "terraform" / "eks" / "ensure_control_plane_logging"


def _scan(tf_dir: Path, check_id: str) -> list[CheckResult]:
    runner = Runner()
    report = runner.run(
        root_folder=str(tf_dir),
        external_checks_dir=[str(CHECKS_DIR)],
        runner_filter=RunnerFilter(checks=[check_id]),
    )
    return [r.check_result["result"] for r in report.passed_checks + report.failed_checks]


def _scan_plan(plan_file: Path, check_id: str) -> list[CheckResult]:
    runner = TFPlanRunner()
    report = runner.run(
        files=[str(plan_file)],
        external_checks_dir=[str(CHECKS_DIR)],
        runner_filter=RunnerFilter(checks=[check_id]),
    )
    return [r.check_result["result"] for r in report.passed_checks + report.failed_checks]


def _scan_by_resource(tf_dir: Path, check_id: str) -> dict[str, CheckResult]:
    runner = Runner()
    report = runner.run(
        root_folder=str(tf_dir),
        external_checks_dir=[str(CHECKS_DIR)],
        runner_filter=RunnerFilter(checks=[check_id]),
    )
    return {r.resource: r.check_result["result"] for r in report.passed_checks + report.failed_checks}


def _scan_plan_by_resource(plan_file: Path, check_id: str) -> dict[str, CheckResult]:
    runner = TFPlanRunner()
    report = runner.run(
        files=[str(plan_file)],
        external_checks_dir=[str(CHECKS_DIR)],
        runner_filter=RunnerFilter(checks=[check_id]),
    )
    return {r.resource: r.check_result["result"] for r in report.passed_checks + report.failed_checks}


class TestEnsureControlPlaneLogging:
    """CKV_XM_AWS_EKS_5 — aws_eks_cluster must set enabled_cluster_log_types to include api, audit, and authenticator."""

    CHECK_ID = "CKV_XM_AWS_EKS_5"

    def test_cluster_with_control_plane_logging_passes(self):
        results = _scan_by_resource(RESOURCES_DIR / "pass", self.CHECK_ID)
        assert len(results) == 2
        assert results["aws_eks_cluster.pass_exact"] == CheckResult.PASSED
        assert results["aws_eks_cluster.pass_all"] == CheckResult.PASSED

    def test_cluster_non_compliant_cases_fail(self):
        results = _scan_by_resource(RESOURCES_DIR / "fail", self.CHECK_ID)
        assert len(results) == 3
        assert CheckResult.PASSED not in results.values()
        assert results["aws_eks_cluster.fail_missing_all"] == CheckResult.FAILED
        assert results["aws_eks_cluster.fail_partial"] == CheckResult.FAILED
        assert results["aws_eks_cluster.fail_empty"] == CheckResult.FAILED

    def test_cluster_with_control_plane_logging_passes_plan(self):
        results = _scan_plan_by_resource(RESOURCES_DIR / "pass" / "tfplan.json", self.CHECK_ID)
        assert len(results) == 2
        assert results["aws_eks_cluster.pass_exact"] == CheckResult.PASSED
        assert results["aws_eks_cluster.pass_all"] == CheckResult.PASSED

    def test_cluster_non_compliant_cases_fail_plan(self):
        results = _scan_plan_by_resource(RESOURCES_DIR / "fail" / "tfplan.json", self.CHECK_ID)
        assert len(results) == 3
        assert CheckResult.PASSED not in results.values()
        assert results["aws_eks_cluster.fail_missing_all"] == CheckResult.FAILED
        assert results["aws_eks_cluster.fail_partial"] == CheckResult.FAILED
        assert results["aws_eks_cluster.fail_empty"] == CheckResult.FAILED

    def test_cluster_inside_module_passes(self):
        results = _scan_by_resource(RESOURCES_DIR / "module", self.CHECK_ID)
        assert len(results) == 1
        assert list(results.values()) == [CheckResult.PASSED]
        assert any("aws_eks_cluster.module_cluster" in k for k in results)

    def test_non_eks_resources_ignored(self):
        # Confirms check does not inadvertently evaluate non-EKS resources if resource_types is modified
        results = _scan_by_resource(RESOURCES_DIR / "non_eks", self.CHECK_ID)
        assert results == {}

    def test_unresolved_variable_fails_directory_scan(self):
        # Unresolved variable without default fails the required log types check in directory scans
        results = _scan_by_resource(RESOURCES_DIR / "unresolved_var", self.CHECK_ID)
        assert results == {"aws_eks_cluster.unresolved_var_cluster": CheckResult.FAILED}
