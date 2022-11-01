import os


class SoundfontLoader:
    _instance = None

    @staticmethod
    def get_instance():
        if not SoundfontLoader._instance:
            SoundfontLoader()
        return SoundfontLoader._instance

    def __init__(self):
        if (SoundfontLoader._instance is None):
            self.file_list = {}
            self.reload_soundfont()
            self.default = "Jazz_Guitar"
            SoundfontLoader._instance = self

    def get(self, name=""):
        if (name == ""):
            return self.file_list[self.default]
        return self.file_list[name]

    def get_name_from_path(self, path):
        return [v for v in self.file_list.keys() if self.file_list[v] == path][0]

    def get_idx_from_path(self, path):
        return [i for i, v in enumerate(self.file_list.keys()) if self.file_list[v] == path][0]

    def get_names(self):
        return list(self.file_list.keys())

    def reload_soundfont(self, path="data/soundfonts"):
        for file in os.listdir(path):
            p = os.path.join(path, file)
            if (os.path.isfile(p) and file.split(".")[-1] == "sf2"):
                self.file_list[file.split(".")[0]] = p
