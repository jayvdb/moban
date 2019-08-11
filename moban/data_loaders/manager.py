import moban.data_loaders.yaml  # noqa: F401
import moban.data_loaders.json_loader  # noqa: F401
from moban import utils, constants, file_system
from lml.plugin import PluginManager


class AnyDataLoader(PluginManager):
    def __init__(self):
        super(AnyDataLoader, self).__init__(constants.DATA_LOADER_EXTENSION)

    def get_data(self, file_name):
        file_extension = file_system.path_splitext(file_name)[1]
        file_type = file_extension
        if file_extension.startswith("."):
            file_type = file_type[1:]

        try:
            loader_function = self.load_me_now(file_type)
        except Exception:
            loader_function = self.load_me_now(constants.DEFAULT_DATA_TYPE)
        return loader_function(file_name)


LOADER = AnyDataLoader()


def load_data(base_dir, file_name):
    abs_file_path = search_file(base_dir, file_name)
    data = LOADER.get_data(abs_file_path)
    if data is not None:
        parent_data = None
        if base_dir and constants.LABEL_OVERRIDES in data:
            parent_data = load_data(
                base_dir, data.pop(constants.LABEL_OVERRIDES)
            )
        if parent_data:
            return utils.merge(data, parent_data)
        else:
            return data
    else:
        return None


def search_file(base_dir, file_name):
    the_file = file_name
    if not file_system.exists(the_file):
        if base_dir:
            file_under_base_dir = file_system.url_join(base_dir, the_file)
            if file_system.exists(file_under_base_dir):
                the_file = file_system.fs_url(file_under_base_dir)
            else:
                raise IOError(
                    constants.ERROR_DATA_FILE_NOT_FOUND % (file_name, the_file)
                )
        else:
            raise IOError(constants.ERROR_DATA_FILE_ABSENT % the_file)
    return the_file
