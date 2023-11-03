import os
import pathspec
import tarfile

from mlpylib._util.gitutil import (
    GitInfo
    )

_GITIGNORE_FILE_NAME = ".gitignore"
_ADDITION_IGNORES = ["env*/", "venv*/"]


def pack_code(git_info: GitInfo, target: str):

    ignore_patterns = []
    gitignore_file = os.path.join(git_info.working_tree_dir, _GITIGNORE_FILE_NAME)

    with open(gitignore_file) as gitignore_file:
        ignore_patterns = [line for line in gitignore_file.read().splitlines() if line]

    ignore_patterns += _ADDITION_IGNORES
    ignore_patterns += [os.path.basename(target)]
    spec = pathspec.GitIgnoreSpec.from_lines(ignore_patterns)

    with tarfile.open(os.path.join(target), "w") as tar:
        for item in pathspec.util.iter_tree_entries(git_info.working_tree_dir):
            if spec.match_file(item.path) or not item.is_file():
                continue
            else:
                source = os.path.join(git_info.working_tree_dir, item.path)
                tar.add(source, item.path)
    
    pass