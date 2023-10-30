# Hadder--专用蛋白质补氢工具
<img alt="Hex.pm" src="https://img.shields.io/hexpm/l/apa">

很多蛋白质数据库往往会采用去掉氢原子的方式来存储各种pdb蛋白质结构文件，
这就要求我们在实际构建力场的过程中手动去补齐氢原子，
本开源工具就可以实现这样的功能。

# 安装与使用
本软件支持pip一键安装与更新：
```bash
$ python3 -m pip install hadder --upgrade -i https://pypi.org/simple
```
支持在python中调用API接口，来完成蛋白质补氢：
```python
from hadder import AddHydrogen
AddHydrogen('input.pdb', 'output.pdb')
```
如果成功运行，会在终端窗口上打印如下文字：
```
1 H-Adding task with 3032 atoms complete in 0.116 seconds.
```
在1.4以及之后的版本中，安装完成后，也支持直接使用命令行操作来补氢：
```bash
$ python3 -m hadder -h
usage: __main__.py [-h] [-i I] [-o O]

optional arguments:
  -h, --help  show this help message and exit
  -i I        Set the input pdb file path.
  -o O        Set the output pdb file path.
  
$ python3 -m hadder -i input.pdb -o ouput.pdb # e.g. $ python3 -m hadder -i examples/case2.pdb -o examples/case2-complete.pdb
1 H-Adding task with 3032 atoms complete in 0.116 seconds.
```
不论是调用API接口的补氢，还是使用命令形式的补氢，都`建议使用绝对路径`来进行文件索引。如果在此处使用相对路径，会导致一些文件索引错误的问题。

# 示例
在`examples`路径下有一个`case2.pdb`的文件，这是一个不含氢原子的蛋白质，其结构如下图所示：

![](./examples/case2.png)

使用`Hadder`完成补氢的操作之后，得到的结果如下图所示：

![](./examples/case2-complete.png)

# 代码贡献
如果希望在本仓库贡献您的代码，为开源社区的用户提供更多的技术支持，请在按照如下操作确保代码符合PEP8规范之后，
再提交Pull Request进入审核阶段，审核结束后即可合并分支。
## 安装Flake8
Flake8是一个常用的代码规范检查工具，可以使用pip进行安装和管理。但是由于不同版本的Flake8检查出来的问题可能存在不一致的现象，
因此我们要求使用Flake8的3.8.4指定版本，安装方法如下：
```bash
$ python3 -m pip install flake8==3.8.4
```
## 使用Flake8
进入到`hadder/`路径下，执行如下指令：
```bash
$ flake8
```
如果返回的结果为空，即表明当前路径下的所有python文件符合相关的规范要求，可以提交PR进入审核阶段。

# 博客推荐
1. [从Hadder看蛋白质分子中的加氢算法](https://www.cnblogs.com/dechinphy/p/hadder.html)
2. [用脚本的形式运行Hadder](https://www.cnblogs.com/dechinphy/p/pym.html)
3. [蛋白质基础组成结构](https://www.cnblogs.com/dechinphy/p/pdb.html)
4. [氨基酸分子结构和原子命名](https://www.cnblogs.com/dechinphy/p/cnaminos.html)