



class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]



class Pluggable:

    def __init__(self, **kwargs):
        print(" -- Pluggable -- ")
        pass

# class Game(offshoot.Pluggable):
class Game(Pluggable):

    def __init__(self, **kwargs):
        print(" -- Game -- ")
        super().__init__(**kwargs)
        self.platform = kwargs.get("platform")
        self.window_name = kwargs.get("window_name")
        self.kwargs = kwargs

    def Gprint(self):
        print("Game Gprint ")

class SerpentMLAGame(Game, metaclass=Singleton):

    def __init__(self, **kwargs):
        print(" -- SerpentMLAGame -- ")
        super().__init__(**kwargs) # 运行父类init
        kwargs["platform"] = "executable"

        kwargs["window_name"] = "WINDOW_NAME44444444444444"

        kwargs["executable_path"] = "EXECUTABLE_PATH5555555555"

        self.radius = 5 #radius

    def PrintSM(self):
        print("SerpentMLAGame")

    @property # 装饰器 可以把函数变成直接读取 s = self.area
    def zPrintSM(self):
        print("SerpentMLAGame property",self.area)

    @property
    def area(self):
        return 3.14 * self.radius * self.radius

    def add(self):
        self.radius += 1 # 自定义装饰器


def f(): # metaclass=Singleton 相当于一个项目 这个类变成一个了,哪里调用都是这个类
    game = SerpentMLAGame()
    game.add()
    game.add()
    game.add()
    print("F ",game.radius)

def main():
    f()
    game = SerpentMLAGame()
    print(game.zPrintSM)
    s = game.area
    print('周长',s)
    game.add()
    print("G ", game.radius)
    game.Gprint()

    print("G ",game.window_name)


if __name__ == '__main__':
    main()





