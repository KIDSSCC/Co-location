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

查看numa节点的分布：

```shell
numactl -H
```

## 资源隔离的测试

```shell
htop   # 监控CPU核心状态
```

测试程序：双线程的死循环

```C++
#include <iostream>
#include <thread>
using namespace std;


void function_1() {
	int i=0;
    while(true)
	{
        cout << "Thread 1 is running: " << i++ << endl;
        this_thread::sleep_for(chrono::milliseconds(50));
    }
}

void function_2() {
	int i=0;
    while(true) 
	{
        cout << "Thread 2 is running: " << i++ << endl;
        this_thread::sleep_for(chrono::milliseconds(75));
    }
}

int main() {
    thread thread_1(function_1);
    thread thread_2(function_2);

    thread_1.join();
    thread_2.join();

    cout << "Both threads have finished." << endl;

    return 0;
}

```

编译指令：

```C++
g++ -o cpu_load cpu_load.cpp -pthread
```

### 对CPU核心的隔离

在启动时绑定CPU核心

```shell
sudo taskset -c 15 ./cpu_load &            # 绑定一个
sudo taskset -c 14，15 ./cpu_load &        # 绑定两个
```

htop中可以比较明显的看到对应的核心的使用情况。如果是直接启动的话，就是随机的两个核心

在单独启动的时候，这里面好像有一个迁移的问题在里面。一开始的时候是在同一个socket上，一段时间后就变成了socket0和socket1各一个核心

运行期间换绑核心

```shell
taskset -apc 20,21 {进程号}
```

在htop上也能看到核心的使用情况发生了变换

### 对LLC和MBA的隔离

调整LLC cache way方案

```shell
sudo pqos -e "LLC:1=0xff"		# 调整所有Socket上的COS1
sudo pqos -e "LLC@0:1=0x6"		# 调整Socket0上的COS1
```

-e选项说明是对某一个COS进行配置的修改，与之相对应的-a选项代表是对核心进行分配。

需要注意的是在cacheway分配的过程中，给同一个COS分配的方案必须是连续的。0x5(101)是违规的分配。因为其中的两路cache way不是相连的

调整MBA方案

```shell
sudo pqos -e "mba:1=70"		# 调整所有Socket上的COS1
sudo pqos -e "mba@0:1=50"	# 调整Socket0上的COS1
```

将新的方案应用到指定的核心上

```shell
sudo pqos -a "core:13=4,5"	# 将COS13应用到核心4和核心5上
```

因为两个Socket上的核心编号是不一样的。所以在绑定核心时，不需要再指定Socket

### 简单流程

#### 初始配置

在核心4，5上启动进程

```shell
sudo taskset -c 4,5 ./cpu_load &
```

![image-20231024185430153](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231024185430153.png)

设定LLC 0x3f,MBA65%,

```shell
sudo pqos -e "LLC@0:4=0x3f"
sudo pqos -e "mba@0:4=65"
```

![image-20231024185703438](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231024185703438.png)

把新的COS绑定在核心4，5上，

```shell
sudo pqos -a "core:4=4,5"
```

将进程换绑到核心14，15上

```shell
sudo taskset -apc 14,15 3607674
```

![image-20231024190030147](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231024190030147.png)

调整LLC为0x3ff,MBA40%

```shell
sudo pqos -e "LLC@0:14=0x3ff"
sudo pqos -e "mba@0:14=40"
```

新的COS绑定在核心14，15上

```shell
sudo pqos -a "core:14=14,15"
```

注：以sudo taskset -c 4,5 ./cpu_load &的方式执行程序时，sudo本身也会作为一个进程存在于后台。并且，此时返回的进程号时sudo进程的进程号，而不是cpu_load的进程号。需要通过ps -a来确定cpu_load的进程号
