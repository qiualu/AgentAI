# 定义及定位精灵 (Sprite)

如果你正在为一个基于精灵的游戏开发插件的话，跟高兴告诉你 Serpent.AI 框架内已经内置了很多针对这种用例的强大模块。

## 针对 Sprite 精灵的开发
Sprite 类旨在代表精灵图像数据。我们同样支持动画状态和 Alpha 通道。一个 Sprite 实例本身没有太多的作用，但它是一些更高级别系统的输入存在的。它还预先计算了动画状态中每幅图像数据的各种重要指标，如特征颜色和像素坐标等信息。 Sprite 实例有两种生成方式:一种是在游戏插件中打包时自动生成的精灵，或者是在运行时手动生成。

## 游戏插件自动打包精灵
就像在 The Game Class, bundled game sprites 章节中提到的，在运行阶段游戏精灵会被自动转化为精灵实例，表现为在 Game 实例中完成一个self.sprites的映射。这些通常最终会成为用于识别和比较的精灵的参考指标。

## 精灵实例的手动生成
SpriteIdentifier 实例和 SpriteLocator 实例都以 Sprite 精灵对象为基本操作单元，所以你必须将你的输入图像转化为精灵对象才能使用这些功能。

### 从图像数据创建精灵
将图像数据转换为 Sprite 精灵对象很简单，你只需要记住一点: 输入应该是一个图像堆栈，而不是单张图像。 正因为我们的 Sprite 实例支持动画状态，所以输入才可以处理多张图像。如果你想将普通的三通道 (rows, cols, channels) 图像转化为带动画标签的 (rows, cols, channels, animation_state) 图像，你可以使用以下代码段:
```
import numpy as np
image_data = image[..., np.newaxis]
```
然后，你将创建如下的 Sprite 精灵:

```
from serpent.sprite import Sprite
sprite = Sprite("MY SPRITE", image_data=image_data)
```
这样就全部搞定啦！

### 向精灵中添加额外图像信息
如果你发现你的精灵需要添加更多的图像数据的话（新的变量，新的动画帧等），你可以使用以下代码段来添加额外信息:
```
sprite.append_image_data(extra_image[..., np.newaxis])
```
## 定位 Sprite 精灵
游戏代理中针对这个任务的常见方法是查看屏幕的特定区域，并尝试识别该区域内可能是哪个精灵的画面。其实在所有打包了精灵实例的游戏插件中，其 GameAgent 实例都预加载了一个 SpriteIdentifier 实例。利用该实例可以让定位与识别精灵的工作事半功倍。

在 Serpent.AI 框架中，有两种识别精灵的方法: Signature Colors 颜色签名和 Constellation of Pixels 像素星座。

## 使用颜色签名识别精灵
在大多数情况下我们都强烈建议使用这种解决方案。 任何Sprite对象在初始化时都会对其图像数据进行分析，分析过程中就包括一组颜色签名的确定。这些颜色签名就是图像数据中具有主要信息量的色彩信息。

简而言之: 在尝试查询识别精灵时，系统会将目标颜色签名与游戏实例内打包的精灵的颜色签名进行比较。 返回超过某个阈值的最佳分数的匹配对象。这个方法真的很棒，因为它抵消了图像缩放和变换带来的干扰。这种方法的唯一短板就是难以区分那些色彩相近的精灵。

利用颜色签名对 GameAgent 中的精灵进行识别:
```
query_sprite = Sprite("QUERY", image_data=query_image[])
sprite_name = self.sprite_identifier.identify(query_sprite, mode="SIGNATURE_COLORS")  # Will be "UNKNOWN" if no match
```
## 使用像素星座识别精灵
提供这种方法仅仅是作为当颜色签名方法不好用时候的备份。该方法本身并不灵活:所查询的精灵必须与目标的大小完全匹配。在创建 Sprite 精灵对象时，在构建其颜色签名的基础上，同时也会构建其像素坐标。像素星座是像素坐标和颜色签名之间的映射。

简而言之:在尝试查询识别精灵时，系统会将目标的像素星座与游戏实例内打包的精灵的像素星座进行比较。返回超过某个阈值的最佳分数的匹配对象。

利用像素星座对 GameAgent 中的精灵进行识别:

query_sprite = Sprite("QUERY", image_data=query_image[])
sprite_name = self.sprite_identifier.identify(query_sprite, mode="CONSTELLATION_OF_PIXELS")  # Will be "UNKNOWN" if no match
## 在游戏帧中定位精灵
使用我们的框架可以让你不会吹灰之力就能在 GameFrame 游戏帧中定位到你想要的图像信息:
```
from serpent.sprite_locator import SpriteLocator

# Assuming the existance of "image"
sprite_to_locate = Sprite("QUERY", image_data=image[..., np.newaxis])

sprite_locator = SpriteLocator()
location = sprite_locator.locate(sprite=sprite_to_locate, game_frame=game_frame)
location 会将是一个 (y0, x0, y1, x1) 四元组或者是 None 空。
```
