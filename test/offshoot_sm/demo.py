


# class ExportFormat:
#     def __init__(self):
#         self.name = "Export Format"
#
#     def export(self, data):
#         raise NotImplementedError()
#
#     @classmethod
#     def is_an_export_format(cls):
#         return True

import offshoot

class ExportFormat(offshoot.Pluggable):
    def __init__(self):
        self.name = "Export Format"

    @offshoot.expected
    def export(self, data):
        raise NotImplementedError()

    @classmethod
    @offshoot.forbidden
    def is_an_export_format(cls):
        return True

import offshoot

class YAMLExportFormatPlugin(offshoot.Plugin):
    name = "YAMLExportFormatPlugin"
    version = "0.1.0"

    libraries = ["PyYAML"]

    files = [
        {"path": "export_formats/yaml.py", "pluggable": "ExportFormat"}
    ]

    config = {
        "export_options": {
            "width": 80
        }
    }

    @classmethod
    def on_install(cls):
        print("\n\n%s was installed successfully!" % cls.__name__)

    @classmethod
    def on_uninstall(cls):
        print("\n\n%s was uninstalled successfully!" % cls.__name__)

if __name__ == "__main__":
    offshoot.executable_hook(YAMLExportFormatPlugin)

