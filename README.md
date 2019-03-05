# kdLaunchPad
一个会话启动器，一键启动会话里的多个程序。可配置多个会话。

# 截图
![kdLaunchPad_screenshot](/screenshot/screen-2019-03-04-22-52-46.png.jpg "截图")

#打包
## 方法一
pyinstaller -F kdLaunchPad.py

最后复制ui文件和image目录到dist目录下即可。

## 方法二

pyinstaller --add-data="kdLaunchPad.ui;." --add-data="launchSession.ui;."  --add-data="sessionItem.ui;." -p="image;."  -c kdLaunchPad.py

最后需要复制image文件夹到dist目录
