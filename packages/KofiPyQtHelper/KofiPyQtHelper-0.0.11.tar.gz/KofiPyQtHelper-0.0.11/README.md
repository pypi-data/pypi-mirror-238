# PyQtHelper

PyQt的快速布局

项目中配置放置在config文件夹中

interface放置界面文件

本项目使用pipreqs 进行依赖管理,若未安装pipreqs使用

```shell
pip install pipreqs
```

1.创建requirement.txt文件

```shell
pipreqs ./ --force
```

2.自动安装所有依赖

```shell
pip install -r requirements.txt
<!-- 强制安装 -->
pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com 
```
