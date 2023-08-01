# 使用可视化调试器 (Visual Debugger)

Serpent.AI 框架附带了一个名为 Visual Debugger 的可视化调试器应用程序。它的功能很简单:在开发者在游戏代理运行时，帮助其针对内存中的图像数据进行可视化调试。举例来说，Visual Debugger 就像一个针对图像的 print 功能。

## 使用可视化调试器 (Visual Debugger)

像框架中的大多数功能一样，通过 serpent 命令就可以启动可视化调试器。
运行 ``` serpent visual_debugger ```
你将会看到一个如下图所示界面的应用:

## 向可视化调试器中传递图像

Visual Debugger 实例提供了接下来应用程序要处理的图像数据的存储函数接口。

**self.store_image_data**

**方法签名** store_image_data(self, image_data, image_shape, bucket="debug")

* image_data: 一个存储形状 (rows, cols, color_channels) 的 numpy ndarray 数组，dtype 为 np.uint8
* image_shape: image_data 的形状
* bucket: 在可视化调试器内，要显示该图像的指定分组标签

**示例**

```
import skimage.io
from serpent.visual_debugger.visual_debugger import VisualDebugger

image = skimage.io.imread("image.png")

visual_debugger = VisualDebugger()
visual_debugger.store_image_data(
    image_data = image,
    image_shape = image.shape,
    bucket = "0"
)

```

VisualDebugger 实例可在你的代码的任何位置实例化。游戏代理已经内含了一个 self.visual_debugger 实例了。

## 自定义可视化调试器分组

默认情况下，可视化调试器会将待显示的图像显示在对应为 “0”，“1”，“2” 和 “3” 的标签桶内。这些桶标签可以通过编辑 config/config.yml 文件进行定制。相关的代码段如下所示:

```
 visual_debugger:
    redis_key_prefix: SERPENT:VISUAL_DEBUGGER
    available_buckets:
        - "0"
        - "1"
        - "2"
        - "3"
        
```

你可以很简单的将 available_buckets 更改为任何你想要的标签。可视化调试器会将其进行适配调整并为每个配置标签的桶分配空间。



