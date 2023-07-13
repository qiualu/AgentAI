

import offshoot,sys


def install(plugin):
    print("OFFSHOOT: Attempting to install %s..." % plugin)

    # plugin_directory = offshoot.config.get("file_paths").get("plugins")

    # print(plugin_directory)

    # plugin_path = "%s/%s/plugin.py".replace("/", os.sep) % (plugin_directory, plugin)
    #
    # plugin_module_string = plugin_path.replace(os.sep, ".").replace(".py", "")
    #
    # subprocess.call([sys.executable.split(os.sep)[-1], "-m", "%s" % plugin_module_string, "install"])
    #


    # python -m plugins.SerpentMLAGamePlugin.plugin install
    # offshoot.executable_hook(SerpentGamePlugin)
    # SerpentGamePlugin(offshoot.Plugin)

    def executable_hook(plugin_class):
        command = sys.argv[1]
        if command == "install":
            plugin_class.install()
        elif command == "uninstall":
            plugin_class.uninstall()
def verify_plugin_dependencies(cls):
    print("\nOFFSHOOT PLUGIN INSTALL: Verifying that plugin dependencies are installed...\n")

    manifest = offshoot.Manifest()

    missing_plugin_names = list()

    for plugin_name in cls.plugins:
        if not manifest.contains_plugin(plugin_name):
            missing_plugin_names.append(plugin_name)

    if len(missing_plugin_names):
        raise PluginError("One or more plugin dependencies are not met: %s. Please install them before continuing..." % ", ".join(missing_plugin_names))

def testoffshootPlugin():
    kk = offshoot.Plugin()
    print(kk)
    # ---------install----------
    kk.install()
    # # verify_plugin_dependencies
    kk.verify_plugin_dependencies()



def get():
    if offshoot.config["allow"]["plugins"] is True:
        print("需要处理")
    else:
        print("已经存在")



def importTest():

    # import serpent.game
    m = "serpent.game"
    exec("import %s" % m)

    # classes = inspect.getmembers(sys.modules[m], inspect.isclass)
    # print("classes", classes)



if __name__ == '__main__':
    # install("test_package.test_module")
    # get()
    # testoffshootPlugin()

    importTest()

