# 马尔科夫链生成以及由马尔科夫链生成随机音乐

## 代码部分

### [pyMC.py](pyMC.py)

- 规定命令行参数以及调用函数

### [MChain.py](MChain.py)

- class MChain: 马尔可夫链类
- def mid_to_MChain(): mid文件转化为马尔科夫链,储存在.json文件中
- def MChain_to_chord(): 用马尔科夫链生成随机音乐

## 可执行程序部分

### pyMC.exe

- 使用命令行打开，在当前目录下，输入pyMC -h 获取帮助

### 依赖库部分

- [requirement.txt](requirement.txt)

  - [musicpy](https://rainbow-dreamer.github.io/musicpy/)

### MIDI文件素材部分

- 默认素材
  
  - [butterfly.mid](butterfly.mid)
  
- 素材来源

  - [bitmidi](https://bitmidi.com/)

- 其他素材

## 注意

- 如果想要合并多条音轨，或者几个文件的旋律音轨的序号不同，需要用python重新编写代码
