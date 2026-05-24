from tools.dev_ops_tools import (
    inspect_dependencies,
    package_vulnerability_warning,
    git_branch_detector,
    git_commit_summarizer,
    git_safe_status_mode,
    git_diff_reader,
    git_commit_assistant,
    git_ignore_inspector,
    read_error_logs,
    analyze_laravel_log,
)


def handle_dev_ops_routes(user_input: str, text: str, clean_text: str):
    if text in ["inspect dependencies", "dependency inspector", "dependencies"]:
        return inspect_dependencies()

    if text in ["package vulnerability warning", "vulnerability warning", "check package risks"]:
        return package_vulnerability_warning()

    if text in ["git branch", "git branch detector", "current branch"]:
        return git_branch_detector()

    if text in ["git commits", "git commit summarizer", "recent commits"]:
        return git_commit_summarizer()

    if text in ["git status", "safe git status", "git safe status"]:
        return git_safe_status_mode()

    if text in ["git diff", "read git diff", "git diff reader"]:
        return git_diff_reader()

    if text in ["git commit assistant", "commit assistant", "suggest commit"]:
        return git_commit_assistant()

    if text in ["gitignore inspector", "git ignore inspector", "inspect gitignore"]:
        return git_ignore_inspector()

    if text in ["read error logs", "error log reader", "show error logs"]:
        return read_error_logs()

    if text in ["laravel log analyzer", "analyze laravel log", "laravel logs"]:
        return analyze_laravel_log()

    return None
