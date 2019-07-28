import os
import sys

from moban import constants
PY2 = sys.version_info[0] == 2


class GitRequire(object):
    def __init__(
        self, git_url=None, branch=None, submodule=False, reference=None
    ):
        self.git_url = git_url
        self.submodule = submodule
        self.branch = branch
        self.reference = reference

    def clone_params(self):
        clone_params = {
            "single_branch": True,
            "depth": constants.DEFAULT_CLONE_DEPTH,
        }
        if self.branch is not None:
            clone_params["branch"] = self.branch
        elif self.reference is not None:
            clone_params["reference"] = self.reference
        return clone_params

    def __eq__(self, other):
        return (
            self.git_url == other.git_url
            and self.submodule == other.submodule
            and self.branch == other.branch
            and self.reference == other.reference
        )

    def __repr__(self):
        return "%s,%s,%s" % (self.git_url, self.branch, self.submodule)


class TemplateTarget(object):
    def __init__(
        self,
        template_file,
        data_file,
        output,
        template_type=constants.DEFAULT_TEMPLATE_TYPE,
    ):
        self.template_file = to_unicode(template_file)
        self.data_file = to_unicode(data_file)
        self.original_output = to_unicode(output)
        self.template_type = template_type
        self.output = self.original_output

        self.set_template_type(template_type)

    def set_template_type(self, new_template_type):
        self.template_type = new_template_type
        if self.original_output.endswith(to_unicode(self.template_type)):
            self.output, _ = os.path.splitext(self.original_output)
        else:
            self.output = self.original_output

    def __eq__(self, other):
        return (
            self.template_file == other.template_file
            and self.data_file == other.data_file
            and self.output == other.output
            and self.template_type == self.template_type
        )

    def __repr__(self):
        return "%s,%s,%s,%s" % (
            self.template_file,
            self.data_file,
            self.output,
            self.template_type,
        )


def to_unicode(path):
    if PY2 and path.__class__.__name__ != "unicode":
        return u"".__class__(path)
    return path
