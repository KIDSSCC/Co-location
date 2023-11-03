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

查看日志信息

```shell
docker logs -tf --tail 10 容器进程号
# -tf 显示日志
# -tail num  显示指定数目的日志
```

查看容器内进程

```shell
docker top 进程号
```

查看元数据

```
docker inspect 进程号
```

进入正在执行的容器

```shell
docker exec -it 容器id /bin/bash
docker attach 容器id
```

将容器中的文件拷贝到服务器上：将两个路径反过来也可以实现反向传输

```shell
# 在服务器中执行
docker cp 容器id:容器内路径 服务器路径
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

# 实验可行性验证

Moses和NGINX redis

## Nginx的部署

```shell
docker search nginx
docker pull nginx
docker run -d --name nginx01 -p 3344:80 nginx

curl localhost:3344			# 尝试访问
```

正向代理：代理客户端发起请求

反向代理：代理服务器接受请求，把请求分发到对应的服务器上

先不考虑docker的部署，在服务器上直接部署

```shell
# 启动
sudo ./nginx
# 停止
sudo ./nginx -s stop
# 刷新配置文件
sudo ./nginx -s reload
# 查看nginx进程
ps aux | grep nginx
```





- 以编译安装的方式安装了nginx

- 安装了ab测试工具

  ```shell
  sudo apt-get install apache2-utils
  ```

- ab工具进行访问测试

  ```shell
  ab -c 100 -n 1000  http://localhost/
  ```



```shell
sudo taskset -c 16,17,18 ./nginx
sudo taskset -c 4 ab -c 1000 -n 2000000  http://localhost/

# 提高同时打开的文件限制
ulimit -n 65536
```



### 先测试各个资源隔离对于nginx本身的影响。

将nginx部署在一个socket上，测试用的ab程序部署在另一个socket上。



#### 先测试核心的影响

将所有核心的带宽和缓存全部放开，ab程序绑定在核心28（socket 1）上，nginx绑定在socket 0 的1，2，4，8个核心上。

记录



------

补加一个实验，nginx中的进程设置对最终的CPU运行情况会有怎样的影响

总测试数2000000，并发2000

1. workprocess设置一个进程，taskset绑定2个核心。
2. workprocess设置两个进程，taskset绑定两个核心
3. workprocess设置四个进程，taskset绑定2个核心

```shell
# 第一组实验
sudo ./nginx -s stop
# 调整好连接数2048，设置好工作进程为1个
sudo taskset -c 14,15 ./nginx 
sudo ./nginx -s reload
# 重复三次，记录时间，观察核心负载情况
sudo taskset -c 28 ab -c 2000 -n 2000000  http://localhost/


# 第二组实验
sudo ./nginx -s stop
# 调整好连接数2048，设置好工作进程为2个
sudo taskset -c 14,15 ./nginx 
sudo ./nginx -s reload
# 重复三次，记录时间，观察核心负载情况
sudo taskset -c 28 ab -c 2000 -n 2000000  http://localhost/

# 第三组实验
sudo ./nginx -s stop
# 调整好连接数2048，设置好工作进程为4个
sudo taskset -c 14,15 ./nginx
sudo ./nginx -s reload
# 重复三次，记录时间，观察核心负载情况
sudo taskset -c 28 ab -c 2000 -n 2000000  http://localhost/
```

nginx中的进程设置会影响到分配的CPU的负载量。考虑nginx中的进程设置等于或大于taskset中的设置

------

进一步提高并发量会不会影响到CPU的负载

分配两个核，nginx工作进程设置为两个，

1. 并发量2000
2. 并发量4000
3. 并发量6000

```shell
sudo ./nginx -s stop
# 调整好连接数8192，设置好工作进程为2个
sudo taskset -c 14,15 ./nginx 
sudo ./nginx -s reload
#第一组实验
sudo taskset -c 28 ab -c 2000 -n 2000000  http://localhost/
#第二组实验
sudo taskset -c 28 ab -c 4000 -n 2000000  http://localhost/
#第三组实验
sudo taskset -c 28 ab -c 6000 -n 2000000  http://localhost/
```

并发程度越高，CPU的负载会有一定程度的提升。但有限

------

### 测缓存大小和内存带宽产生的影响

#### 测缓存大小

绑定2个核，nginx内工作进程设置为2，并发先设置为4000，随后设置为10000，总测试书2000000

- 两个核的cacheway都设置为一路cache
- 两个核的cacheway都设置为6路cache
- 两个核的cacheway都设置为12路cache

```shell
sudo taskset -c 14,15 ./nginx
sudo ./nginx -s reload
sudo pqos -e "LLC@0:1=0x1"		# 调整Socket0上的COS1
sudo pqos -a "core:1=14,15"	# 将COS13应用到核心4和核心5上
sudo taskset -c 28 ab -c 4000 -n 2000000  http://localhost/

sudo pqos -e "LLC@0:1=0x3f"		# 调整Socket0上的COS1
sudo pqos -a "core:1=14,15"	# 将COS13应用到核心4和核心5上
sudo taskset -c 28 ab -c 4000 -n 2000000  http://localhost/

sudo pqos -e "LLC@0:1=0xfff"		# 调整Socket0上的COS1
sudo pqos -a "core:1=14,15"	# 将COS13应用到核心4和核心5上
sudo taskset -c 28 ab -c 4000 -n 2000000  http://localhost/

sudo pqos -e "LLC@0:1=0x1"		# 调整Socket0上的COS1
sudo pqos -a "core:1=14,15"	# 将COS1应用到核心14和核心15上
sudo taskset -c 28 ab -c 10000 -n 2000000  http://localhost/

sudo pqos -e "LLC@0:1=0x3f"		# 调整Socket0上的COS1
sudo pqos -a "core:1=14,15"	# 将COS1应用到核心14和核心15上
sudo taskset -c 28 ab -c 10000 -n 2000000  http://localhost/

sudo pqos -e "LLC@0:1=0xfff"		# 调整Socket0上的COS1
sudo pqos -a "core:1=14,15"	# 将COS1应用到核心14和核心15上
sudo taskset -c 28 ab -c 10000 -n 2000000  http://localhost/


```

观察到虽然时间变化不大，但是随着cacheway的增加，CPU的负载降下来了

#### 测内存带宽

绑定2个核，nginx内工作进程设置为2，并发先设置为4000，随后设置为10000，总测试数2000000

- 两个核的带宽设置为10%
- 两个和的带宽设置为50%
- 两个核的带宽设置为100%

```shell
sudo taskset -c 14,15 ./nginx
sudo pqos -e "mba@0:1=10"
sudo pqos -a "core:1=14,15"	# 将COS13应用到核心4和核心5上
sudo taskset -c 28 ab -c 4000 -n 2000000  http://localhost/

sudo pqos -e "mba@0:1=50"
sudo pqos -a "core:1=14,15"	# 将COS13应用到核心4和核心5上
sudo taskset -c 28 ab -c 4000 -n 2000000  http://localhost/

sudo pqos -e "mba@0:1=100"
sudo pqos -a "core:1=14,15"	# 将COS13应用到核心4和核心5上
sudo taskset -c 28 ab -c 4000 -n 2000000  http://localhost/
```

------

开始测不同socket上的情况

1. 两个核，一个在socket0，一个在socket1
2. 内存带宽分别设置为10%，30%，50%

```shell
sudo ./nginx -s stop
sudo pqos -R
sudo taskset -c 14,28 ./nginx
sudo pqos -e "mba:1=10"
sudo pqos -a "core:1=14,28"
sudo taskset -c 42 ab -c 4000 -n 2000000  http://localhost/

sudo ./nginx -s stop
sudo pqos -R
sudo taskset -c 14,15 ./nginx
sudo pqos -e "mba:1=10"
sudo pqos -a "core:1=14,15"
sudo taskset -c 42 ab -c 4000 -n 2000000  http://localhost/
```

一边80%-90%，另一边50%-60%

![image-20231028104606163](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231028104606163.png)

一边80%-90%，一边60%-70%

- 10月30日，两个核，内存带宽放10%，cache way放0x1,比较对齐和不对齐的情况

```shell
#对齐的形式
sudo pqos -R
sudo ./nginx -s stop
sudo taskset -c 14,15 ./nginx
sudo pqos -e "mba@0:1=10"
sudo pqos -e "LLC@0:1=0x1"
sudo pqos -a "core:1=14,15"

sudo taskset -c 42 ab -c 4000 -n 2000000  http://localhost/
sudo taskset -c 9 ab -c 4000 -n 2000000  http://localhost/

#不对齐的形式
sudo pqos -R
sudo ./nginx -s stop
sudo taskset -c 14,28 ./nginx
sudo pqos -e "mba:1=10"
sudo pqos -e "LLC:1=0x1"
sudo pqos -a "core:1=14,28"

sudo taskset -c 42 ab -c 4000 -n 2000000  http://localhost/
sudo taskset -c 9 ab -c 4000 -n 2000000  http://localhost/
```

- 10月31日

关于Jmeter的测试

```shell
jmeter -n -t baidu.jmx -l baidu-jmeter.jtl
```

在windows本地先配置好测试计划，然后在服务器上运行。得到的结果也能够在windows上解析。

- 11/1

测试计划是4000的并发，10秒内启动，一共运行40秒

nginx在14,15上，jmeter在2-12上，

```shell
sudo pqos -R
sudo ./nginx -s stop
sudo taskset -c 14,15 ./nginx
sudo pqos -e "mba@0:1=10"
sudo pqos -e "LLC@0:1=0x1"
sudo pqos -a "core:1=14,15"
taskset -c 2-12 jmeter -n -t nginx-test.jmx -l nginx-jmeter.jtl
```

![image-20231101224506021](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231101224506021.png)

![image-20231101230712279](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231101230712279.png)

![image-20231101230804962](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231101230804962.png)

nginx在14,28上，jmeter在42-52上，

```shell
sudo pqos -R
sudo ./nginx -s stop
sudo taskset -c 14,28 ./nginx
sudo pqos -e "mba:1=10"
sudo pqos -e "LLC:1=0x1"
sudo pqos -a "core:1=14,28"
taskset -c 42-52 jmeter -n -t nginx-test.jmx -l nginx-jmeter.jtl
```

![image-20231101232802406](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231101232802406.png)

![image-20231101232830113](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231101232830113.png)

![image-20231101232949303](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231101232949303.png)



- nginx在14，15，jmeter在2-12

![image-20231102095522736](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231102095522736.png)

![image-20231102100034966](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231102100034966.png)

![image-20231102100637490](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231102100637490.png)

- nginx在14，15，jmeter在30-40

![image-20231102101525661](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231102101525661.png)

![image-20231102102512854](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231102102512854.png)

![image-20231102103348408](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231102103348408.png)

- nginx在14，28，jmeter在2-12

![image-20231102104719460](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231102104719460.png)

![image-20231102105319688](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231102105319688.png)

![](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231102105847029.png)

- nginx在14，28，jmeter在30-40

![image-20231102110656060](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231102110656060.png)

![image-20231102111432526](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231102111432526.png)

![image-20231102112342476](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231102112342476.png)



- 11月3日

```shell
sudo ./nginx -s stop
sudo pqos -R
sudo taskset -c 14,15 ./nginx
sudo pqos -e "mba@0:1=10"
sudo pqos -e "LLC@0:1=0x1"
sudo pqos -a "core:1=14,15"
```



1. nginx在14，15；jmeter在1-11

<img src="https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231103194258939.png" alt="image-20231103194258939" style="zoom: 67%;" />

![image-20231103203957377](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231103203957377.png)

![image-20231103204035411](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231103204035411.png)

![image-20231103204159627](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231103204159627.png)

2. nginx在14，15，jmeter在30-40

<img src="https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231103195239543.png" alt="image-20231103195239543" style="zoom:67%;" />

![image-20231103223943194](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231103223943194.png)

![image-20231103224029892](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231103224029892.png)

![image-20231103224114940](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231103224114940.png)

3. nginx在14，42；jmeter在1-11

<img src="https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231103203805900.png" alt="image-20231103203805900" style="zoom:67%;" />

![image-20231103224203455](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231103224203455.png)

![image-20231103224246230](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231103224246230.png)

![image-20231103224324715](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231103224324715.png)

4. nginx在14，42；jmeter在30-40

<img src="https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231103204723235.png" alt="image-20231103204723235" style="zoom:67%;" />

![image-20231103224430665](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231103224430665.png)

![image-20231103224615129](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231103224615129.png)

![image-20231103224657029](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231103224657029.png)

5. nginx在42，43；jmeter在1-11

<img src="https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231103210138019.png" alt="image-20231103210138019" style="zoom:67%;" />

![image-20231103224755678](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231103224755678.png)

![image-20231103224903270](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231103224903270.png)

![image-20231103224943711](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231103224943711.png)

6. nginx在42，43；jmeter在30-40

<img src="https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231103211633730.png" alt="image-20231103211633730" style="zoom:67%;" />

![image-20231103225038559](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231103225038559.png)

![image-20231103225118425](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231103225118425.png)

![image-20231103225155170](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231103225155170.png)
