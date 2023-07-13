

from offshootplugin import Plugin


def DebugPlugin():
    ps = Plugin()
    print(ps.name,ps.version)

    # install 函数
    ps.install()




if __name__ == '__main__':
    # 调试offshootplugin 文件 Plugin类
    DebugPlugin()








