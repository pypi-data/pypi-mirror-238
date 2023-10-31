import os

from lupin_grognard.core.tools.log_utils import die


def get_ci_mr_target_branch() -> str:
    mr_target_branch = os.getenv("CI_MERGE_REQUEST_TARGET_BRANCH_NAME")
    if not mr_target_branch:
        return ""
    return mr_target_branch


def is_gitlab_ci() -> bool:
    return os.getenv("GITLAB_CI") == "true"


def is_gitlab_shallow_clone_disabled() -> bool:
    return os.getenv("GIT_DEPTH") == "0"


def assert_gitlab_shallow_clone_defined() -> None:
    """Check if GIT_DEPTH is defined to 0 in GitLab CI"""
    if is_gitlab_ci() and not is_gitlab_shallow_clone_disabled():
        die(msg="GitLab shallow clone detected, please define GIT_DEPTH to 0")
