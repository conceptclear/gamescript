# gamescript
## FGO py脚本
提供了几个简单的函数包括后台模拟按键，后台识别图片用以fgo刷本
[手游fgo网易mumu模拟器自动挂机py脚本](http://conceptclear.cn/mobilegame/2020/06/17/MobileGame-fgo-py.html)

## 更新
开发了一个界面，并且现在配置数据采用json格式存储于settings文件夹中，不需要修改excel文件了
## 更新2.1
修复了一些bug，改进了一下ui                                  

## 用法
将qtfgo.exe，source文件夹和settings文件夹放在同一目录下，注意当前目录中不能包含中文，然后直接运行qtfgo.exe即可（注意，有的模拟器会要求管理员权限，比如网易mumu模拟器，这时候就需要用管理员模式启动qtfgo.exe）
运行界面如下：                                  

<div align="center"><img  src="https://github.com/conceptclear/gamescript/raw/master/image/main_ui.png"></div>     

左边的文本浏览器被用于实时显示log输出，右边四个按钮分别是：                                  

- 选取设定好的脚本。v2.1提供了5个脚本选项，可以适用于不同的场景而不需要每次换副本的时候都要重新设置，选定好脚本之后之后的操作都会对所选定的脚本进行设置。                                  
- 修改基础设置。                                  
- 修改战斗设置。                                  
- 关于。一些额外说明。                                  

设定完成之后只要点击下方的开始即可进行重复刷本，注意要保证点击开始的时候，模拟器当前界面处于刷本之前的选取助战的界面上。                                  

### 基础设置
点击修改基础设置按钮可以对基础设置进行修改，如下图所示：                                  

<div align="center"><img  src="https://github.com/conceptclear/gamescript/raw/master/image/settings_ui.png"></div>     

可以设置的东西包括：                                  

- 重复刷本次数。设置完成之后会在重复运行该次数的副本之后停止，若选取不吃苹果的话则会在吃苹果的界面停止。                                  
- 是否吃苹果。现在可以选择不吃苹果，吃金苹果，吃银苹果和吃彩苹果四种选项，暂时不提供吃铜苹果的选择。                                  
- 需要寻找的助战角色。现在提供孔明，CBA，梅林，花嫁尼禄，C狐和不需要检测助战六种选项。注：如果助战角色和助战礼装都选择无会默认选择第一个助战角色，如果利用了游戏的助战筛选功能可能会出现没有角色的情况，则会引起bug，请慎用。                                  
- 需要寻找的助战礼装。现在提供午茶学妹（加羁绊礼装）和小达芬奇（加QP礼装）以及不需要检测助战礼装三种选项。注：如果是活动副本可以利用活动自带的筛选功能，这样助战礼装选取上选择“无”即可。                                  
- 模拟器窗口名称。不知道窗口名称的可以打开模拟器，将鼠标放置在任务栏的模拟器图标上，显示的文字即为窗口名称（雷电模拟器一般为“雷电模拟器”，mumu模拟器为“命运-冠位指定 - MuMu模拟器”）。                                  
- 选完角色等待时间。从选中所需要的助战角色开始，到进入战斗界面并且可以操作所需要等待的时间，单位为s。                                  
- 使用随机时间。选择是的话会给每次操作默认添加0-0.5s之间的一个随机时间。                                  
- 延迟时间。默认为0s，作用是给每次操作添加一个延迟的时间，防止有些电脑运行速度比较慢从而导致按键错误。                                  
- 战斗面数。选取战斗需要的面数，当前只支持1,2,3。                                  
- 第一/二/三面等待时间。从释放宝具到下一面战斗开始所需要的时间，单位为s。                                  
- 使用换人礼装。若选择否，则下面两个选项不起作用。                                  
- 换人功能使用面。在第1/2/3面使用换人礼装的换人功能。                                  
- 换人功能更换角色。用第4/5/6位置的角色换下1/2/3位置的角色。                                  

### 战斗设置
点击修改战斗设置可以对战斗副本进行设置，如下图所示：                                  

<div align="center"><img  src="https://github.com/conceptclear/gamescript/raw/master/image/fight_ui.png"></div>     

可以设置的东西包括：                                  

- 每一面下第1/2/3位置角色的1/2/3技能的选择，选项包括不用技能，对自己或者全体释放，对地方1,2,3位置角色释放，对己方1,2,3位置角色释放。（太空伊什塔尔宝具换色可以看作给1,2,3号角色释放技能）                                  
- 每一面下御主技能的使用，与从者技能使用类似。                                  
- 更换角色技能的使用。与前面类似。注：更换角色指的仅仅是当前面更换上来的角色，比如第一面我换下3号换上了4号角色，第二面该角色使用技能的话修改的是角色3使用技能而非换上角色使用技能。                                  
- 每一面下宝具的使用，宝具无法对己方单体使用，其他与之前类似。                                  

### 运行效果
修改完成之后，点击主页面的开始即可，运行如图所示：                                  

<div align="center"><img  src="https://github.com/conceptclear/gamescript/raw/master/image/example.png"></div>     

模拟器和脚本都可以放置在后台运行，不影响工作。                                                              
注：在选取助战的界面时，切忌用鼠标操作模拟器，因为后台模拟鼠标拖动是通过实时传递模拟鼠标当前位置实现的，若用鼠标交互则可能产生问题。                                  

提供了打包好的exe可以从百度网盘进行下载：                                  

链接：https://pan.baidu.com/s/1JPqg2Ox7Th05wZ9lu6KgLw                    
提取码：5q6j                           