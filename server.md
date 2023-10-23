## Docker安装

查看系统内核

```shell
uname -r
```

查看系统版本

```shell
cat /etc/os-release
```

查看docker是否启动

```shell
sudo docker version
sudo docker run hello-world
```

![image-20231022161707374](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231022161707374.png)

## 镜像命令

查看当前已经拥有的docker镜像

```shell
sudo docker images
```

查看当前正在运行的docker容器

```shell
sudo docker ps
sudo docker ps -a   #显示隐藏的docker信息，包括已经结束运行的
```

搜索在docker hub中搜索某一个镜像

```shell
sudo docker search mysql
```

 下载一个镜像

```shell
sudo docker pull mysql
```

删除一个镜像

```shell
sudo docker rmi -f (镜像的ID)
```

## 容器命令

启动并进入容器

```shell
sudo docker run -it centos /bin/bash
```

停止并退出容器

```shell
exit
```

退出但不停止容器

```
ctrl + P + Q 
```

删除容器

```shell
sudo docker rm 容器id
```

启动和停止容器

```shell
sudo docker start 容器id    # 启动容器
sudo docker restart 容器id  # 重新启动容器
sudo docker stop 容器id     # 停止一个正在运行的容器
sudo docker kill 容器id     # 强制停止当前的容器
```

