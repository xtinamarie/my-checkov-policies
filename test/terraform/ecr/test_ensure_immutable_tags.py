from pathlib import Path

from checkov.common.models.enums import CheckResult
from checkov.runner_filter import RunnerFilter
from checkov.terraform.runner import Runner
from checkov.terraform.plan_runner import Runner as TFPlanRunner

CHECKS_DIR = Path(__file__).parents[3] / "checks"
RESOURCES_DIR = Path(__file__).parents[2] / "resources" / "terraform" / "ecr" / "ensure_immutable_tags"


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


class TestEnsureImmutableTags:
    """CKV_XM_AWS_ECR_41 — aws_ecr_repository must have image_tag_mutability set to IMMUTABLE."""

    CHECK_ID = "CKV_XM_AWS_ECR_41"

    def test_repository_with_immutable_tags_passes(self):
        results = _scan(RESOURCES_DIR / "pass", self.CHECK_ID)
        assert results == [CheckResult.PASSED]

    def test_repository_non_compliant_cases_fail(self):
        results = _scan_by_resource(RESOURCES_DIR / "fail", self.CHECK_ID)
        assert results["aws_ecr_repository.fail_mutable"] == CheckResult.FAILED
        assert results["aws_ecr_repository.fail_missing_mutability"] == CheckResult.FAILED
        assert results["aws_ecr_repository.fail_immutable_with_exclusion"] == CheckResult.FAILED
        assert results["aws_ecr_repository.fail_mutable_with_exclusion"] == CheckResult.FAILED

    def test_repository_with_immutable_tags_passes_plan(self):
        results = _scan_plan(RESOURCES_DIR / "pass" / "tfplan.json", self.CHECK_ID)
        assert results == [CheckResult.PASSED]

    def test_repository_non_compliant_cases_fail_plan(self):
        results = _scan_plan_by_resource(RESOURCES_DIR / "fail" / "tfplan.json", self.CHECK_ID)
        assert results["aws_ecr_repository.fail_mutable"] == CheckResult.FAILED
        assert results["aws_ecr_repository.fail_missing_mutability"] == CheckResult.FAILED
        assert results["aws_ecr_repository.fail_immutable_with_exclusion"] == CheckResult.FAILED
        assert results["aws_ecr_repository.fail_mutable_with_exclusion"] == CheckResult.FAILED
