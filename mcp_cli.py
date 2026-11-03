import os
import sys
from pathlib import Path

CHECKS_DIR = Path(__file__).resolve().parent / "checks"
OVERRIDE_FLAGS = ("-s", "--soft-fail", "--soft-fail-on", "--hard-fail-on")


def build_args(user_args: list[str]) -> list[str]:
    """Constructs the argument list for checkov, defaulting LOW severity checks to warning mode (soft-fail)."""
    default_args = ["--external-checks-dir", str(CHECKS_DIR), "--quiet"]

    # Support escape hatch to suppress soft-fail injection and restore standard hard-fail default.
    # Accepts MCP_NO_SOFT_FAIL=1 from environment or command-line (stripped before passing to checkov).
    no_soft_fail = os.environ.get("MCP_NO_SOFT_FAIL") == "1"
    cleaned_args = []
    for arg in user_args:
        if arg == "MCP_NO_SOFT_FAIL=1" or arg == "--no-soft-fail":
            no_soft_fail = True
        else:
            cleaned_args.append(arg)

    # Set recommended checks (LOW severity) to warning mode (soft-fail) by default,
    # unless an override flag (-s, --soft-fail, --soft-fail-on, --hard-fail-on) is supplied
    # or the MCP_NO_SOFT_FAIL escape hatch is set.
    #
    # Why LOW works:
    # 1. Checkov compares severity as <=, so INFO is automatically included.
    # 2. Checks with no severity (e.g. built-in checks without an API key) evaluate as None
    #    and still hard-fail (exit 1), preserving security gates.
    if not no_soft_fail and not any(arg.split("=", 1)[0] in OVERRIDE_FLAGS for arg in cleaned_args):
        default_args.extend(["--soft-fail-on", "LOW"])

    return default_args + cleaned_args


def main() -> None:
    sys.argv = [sys.argv[0]] + build_args(sys.argv[1:])
    from checkov.main import Checkov

    ckv = Checkov()
    sys.exit(ckv.run())


if __name__ == "__main__":
    main()
