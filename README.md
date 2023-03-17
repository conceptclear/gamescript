# gamescript
## FGO py脚本
提供了几个简单的函数包括后台模拟按键，后台识别图片用以fgo刷本
[手游fgo网易mumu模拟器自动挂机py脚本](http://conceptclear.cn/mobilegame/2020/06/17/MobileGame-fgo-py.html)

## 更新3.2
- 更新鼠标选择模拟器功能，可以在“模拟器窗口名称”处填写“鼠标选择”，脚本会根据5s后鼠标所处位置自动获取该处句柄
- 更新奥伯龙（双宝具）
- 增加吃青苹果
- 延长了吃苹果及选助战的等待时间，减少卡顿带来的问题
## 更新3.1
- 实装技能加速功能
- 增添奥伯龙杀狐小芬奇
- 增添自选角色（非提供助战），可在1280*720分辨率下对宝具部分进行截图，以“user.jpg”为名存放在source文件夹下
## 更新3.0
针对刷本中出现的几个问题对程序进行了较大的修改：
- 模拟器的匹配问题
- CAB的宝具名不同的问题
- 按键顺序问题
- json文件名问题
- 释放技能等待时间问题
- 增加铜苹果支持
- 战斗结束延长等待时间防止黑屏过长
- 换人时间问题
## 更新2.1.1
增添了CAB
## 更新2.1
修复了一些bug，改进了一下ui     
## 更新
开发了一个界面，并且现在配置数据采用json格式存储于settings文件夹中，不需要修改excel文件了
                            
### 模拟器的匹配问题
当前只能使用雷电模拟器；
MuMu模拟器，之前可用但是在一次更新之后更改了模拟器软件架构，新的架构没有深入研究；
夜神模拟器，主窗口句柄有32个子句柄，其中包含游戏画面的子句柄在子句柄序列中的位置不固定，且包含游戏画面的子句柄还包含了菜单栏，游戏画面为该子句柄的子句柄，需要寻找方法确定每次有游戏画面的子句柄的顺序；
其余模拟器，待测试；
### CAB宝具名问题
将CAB改为CAB1和CAB2两张图，匹配时先匹配图1，若无法匹配则匹配图2，再进行判断。
### 增加铜苹果支持
增加吃铜苹果功能，通过先拖动菜单，再选择P点实现
### 战斗结束延长等待时间问题
将选择继续战斗之后的等待时间从3s延长为5s
### 其余问题
其余问题通过修改存储格式来实现修改。原文件结构通过分离基础设定和战斗按键设置，将设置分为两个json文件，且文件没有采用格式化json的存储方式。
最大的问题在于战斗按键设置采用的是每个按键都进行判断的方式，且默认为3s的按键延迟，对于不同的角色按键时间适用性不强。而且默认采用的是123号位所有技能都要按顺序释放完成，这样对于一些有技能释放先后顺序的情况并不适用。
将两个文件合并为一个文件，并且采用格式化存储的方式。对战斗设置采用序列化存储方式。改进后的json文件详见fgo1.json。
## UI更新
UI进行了一些更新，主界面的选取脚本界面从原来的只能选给定的5个设定好的脚本更换为可以自己打开文件夹选择（注意，原json文件现不可使用。）
主要进行变更的为战斗设置界面，从原来的每个技能设定更换为序列化设定，具体如下图。

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

- 每一面下第1/2/3位置角色的1/2/3技能的选择，选项包括对自己或者全体释放，对地方1,2,3位置角色释放，对己方1,2,3位置角色释放。（太空伊什塔尔宝具换色可以看作给1,2,3号角色释放技能）                                  
- 每一面下御主技能的使用，与从者技能使用类似。                                  
- 更换角色技能的使用。与前面类似。注：更换角色指的仅仅是当前面更换上来的角色，比如第一面我换下3号换上了4号角色，第二面该角色使用技能的话修改的是角色3使用技能而非换上角色使用技能。                                  
- 每一面下宝具的使用，宝具无法对己方单体使用，其他与之前类似。                                  

### 运行效果
修改完成之后，点击主页面的开始即可，运行如图所示：                                  

<div align="center"><img  src="https://github.com/conceptclear/gamescript/raw/master/image/example.png"></div>     

模拟器和脚本都可以放置在后台运行，不影响工作。                                                              
注：在选取助战的界面时，切忌用鼠标操作模拟器，因为后台模拟鼠标拖动是通过实时传递模拟鼠标当前位置实现的，若用鼠标交互则可能产生问题。                                  

### 依赖项
- pywin32
- opencv-python
- numpy
- pyqt5