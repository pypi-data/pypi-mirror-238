import git
from dataclasses import (
    dataclass
    )

from mlpylib._util import (
    logging
    )

_logger = logging.get_logger()

@dataclass
class GitInfo:
    working_tree_dir: str
    url: str
    commit: str
    is_dirty: bool


def get_git_info(path: str) -> GitInfo:
    global _logger

    try:
        repo = git.Repo(path, search_parent_directories = True)
        current_commit = repo.commit()
        git_info = GitInfo(
            working_tree_dir = repo.working_tree_dir,
            url = repo.remotes.origin.url,
            commit = current_commit.hexsha,
            is_dirty = repo.is_dirty()
            )

    except Exception as error:
        _logger.warning(f"{error.__class__.__name__} | {error}")
        git_info = GitInfo(
            working_tree_dir = path,
            url = None,
            commit = None,
            is_dirty = None
            )

    return git_info


