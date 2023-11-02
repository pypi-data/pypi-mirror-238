# 安装

```
python -m pip install vlppy
```

# 依赖

```
python>=3.4
numpy>=1.19.0
matplotlib>=3.5.0
scipy>=1.8.0
pandas>=1.3.0
```

# 例程

## 1.滤波器例程

```
from vlppy import demo
demo.demo_filter.main()
```

## 2.可见光定位例程

```
from vlppy import demo
demo.demo_main.main()
demo.demo_main.test_func()
```

# vlppy 库的使用

## 1. 模型参数定义

* 新建一个 **settings.json** 文件
* 在 **settings.json** 文件添加模型参数

```json
{
    "Room": {
        "size":{  
	    ...
        }, // 房间尺寸
        "wall":{
            ...
        } // 反射墙壁
    }, // 房间
    "PD:{  
        "PD1":{
            ...
        },
        "PD2":{
            ...
        }
    }, // 光电探测器
    "LED": {
        "LED1": {
	    ...
        }
    }  // 发光二极管 
}
```

* 加载模型参数

```python
from vlppy.setting import Settings
Args = Settings('settings.json') # 模型参数包含在字典 Args.items 中
```

## 2. 搭建模型

* 新建一个模型类 **VLP_Model**

  ```python
  import numpy as np
  import matplotlib.pyplot as plt
  from vlppy.model import LED,PD,Room
  from vlppy.signal import filter,plot

  class VLP_Model:
      def __init__(self, *args, **kwargs):
  	"""初始化模型
  	"""
  	self.room = Room(...)
  	self.pd = PD(...)
  	self.led = LED(...)

      def get_data(self):
  	"""计算PD接收LED功率
  	"""
  	P_PD = self.pd.recv_led_signal(led=self.led1, room=self.room) 
  	X, Y, Z = self.room.get_tp_pos(fmt='c')
  	return (P_PD, X, Y, Z)

      def show(self,z,savepath=...,showfig=True):
          """绘图
          z: 功率数据
  	savepath: 保存路径
  	showfig: 是否显示
          """
          xr, yr, _ = self.room.get_tp_grid()
          z = np.reshape(z, xr.shape)  
          ax = plt.axes(projection='3d')
          ax.plot_surface(xr, yr, z, cmap='viridis', edgecolor='none')
          ax.set_xlabel('X')
          ax.set_ylabel('Y')
          ax.set_zlabel('Z')
          if savepath != ...:
              plt.savefig(savepath)
          if showfig:
              plt.show()
  ```

## 3. 加载模型

```python
def main():
    cm = VLP_Model(**Args.items)
    (P,X,Y,Z) = cm.get_data()
  
    # 绘图
    cm.show(P)
```

## 4. 保存数据

```python
from vlppy.io import IO

# 保存文件路径
filepath = ...

data = {
    "P": P,
    "X": X,
    "Y": Y,
    "Z": Z
}

io = IO() 
io.save_excel(filepath, data)
```

## 5. 查看数据

```python
from vlppy.io import IO

# 文件路径
filepath = ...

# 加载数据
data = io.load_excel(filepath)

# 查看数据形状
print(data.shape)
```
