import sys
from pathlib import Path

CHECKS_DIR = Path(__file__).resolve().parent / "checks"


def build_args(user_args: list[str]) -> list[str]:
    """Constructs the argument list for checkov, defaulting LOW severity checks to warning mode (soft-fail)."""
    default_args = ["--external-checks-dir", str(CHECKS_DIR), "--quiet"]

    # Set recommended checks (LOW severity) to warning mode (soft-fail) by default,
    # unless the user has explicitly supplied their own soft-fail or hard-fail flags.
    if not any(arg in user_args for arg in ("--soft-fail", "--soft-fail-on", "--hard-fail-on")):
        default_args.extend(["--soft-fail-on", "LOW"])

    return default_args + user_args


def main() -> None:
    sys.argv = [sys.argv[0]] + build_args(sys.argv[1:])
    from checkov.main import main as checkov_main
    checkov_main()


if __name__ == "__main__":
    main()
