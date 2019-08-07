from moban import repo

import fs
import fs.path
from fs.opener import Opener
from fs.opener.registry import registry
from fs.osfs import OSFS


@registry.install
class RepoFSOpener(Opener):
    protocols = ["repo"]

    def open_fs(self, fs_url, parse_result, writeable, create, cwd):
        repo_name, _, dir_path = parse_result.resource.partition("/")
        actual_repo_path = fs.path.join(repo.get_moban_home(), repo_name)
        root_path = fs.path.join(actual_repo_path, dir_path)
        osfs = OSFS(root_path=root_path)
        return osfs
