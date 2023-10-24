### run.py

- run_bg_benchmark

给定一系列需要运行的BG应用以及对应的CPU核心号，在每个应用对应的容器中，规定CPU核心，运行脚本来启动BG应用。

最终返回的是每个启动的BG应用的进程号组成的字典。

下一步细节：/home/run_bg.py

- get_now_ipc

起手的for循环部分根据进程号检查了每个应用是否还在运行。似乎是如果没有在运行的话，就重新调用run_bg_benchmark。

在run_bg_benchmark中，本身已经设置了容器的CPU亲和性，随后又根据进程号或者父进程的进程号再次绑定CPU亲和性。准备了perf命令来准备进行性能的收集

while True的循环里运行perf语句收集了性能信息，并最终计算了奖励分数

- perform_resource_partitioning

具体来执行某一种资源分配方式

用taskset来设置CPU亲和性，

用CAT和MBA绑一下缓存和mb

去查一下Intel的手册

- update_APP_PID

初始时被调用一次，创建<应用，进程号>的空字典，并统计应用总数

- get_app_pid

按照特定的情况查找进程的信息，最后的for循环的目的是排除掉同一个应用所启动的多个进程

```C++
if app[:-1] in ECP_BENCHMARK:
        grep_cmd = f'ps aux | grep {ECP_BENCHMARK_GREP[app[:-1]]} | grep -v grep'
    elif app[:-1] == 'canneal' or app[:-1] == 'streamcluster' or app[:-1] == 'dedup':
        grep_cmd = f'ps aux | grep /home/pkgs/kernels/{app[:-1]}/inst | grep -v grep'
    else:
        grep_cmd = f'ps aux | grep /home/pkgs/apps/{app[:-1]}/inst | grep -v grep'
    
    for app_i in APP_PID.keys():
        if app_i[:-1] == app[:-1] and app_i != app and APP_PID[app_i] != '':
            grep_cmd += f' | grep -v {APP_PID[app_i]}'
```

设定好查询进行的指令后，执行命令行指令并对结果进行一系列的清洗，最终会获得给定应用的进程号

- refer_core

根据一个代表了分配核心数目的列表，构建出分配给每个应用具体的核心编号

其中一点是跳过了28-55的编号，目的暂时不明

- refer_llc

计算对每个应用分配的llc的16进制掩码

分配的时候是从高往低分，从大往小分。但返回的时候还是得按照应用的顺序给出列表

比如在12 cache way的情况下，三个应用采用[8,1,3]的分法

返回的列表应该是[0xff0,0x1,0xe]

- refer_mb

计算分配内存带宽的百分比，简单的乘10就可以

- gen_configs_recursively_fix

目标是计算所有可能的资源配置，大概的实现思路应该是递归的从左至右固定住某一维然后再组合结果吧

- split_averagely

将一个整数nof_units尽可能平局的分为nof_clusters份

- 初始化资源配置

## 资源分区的方式

1. 在容器中执行命令，设置CPU亲和性并运行程序

```shell
sudo docker exec laghos0 taskset -c 17,18,19 python /home/run_bg.py laghos 8
```

2. 直接为某一个进程设置CPU亲和性

```shell
sudo taskset -apc {core_allocation_list[i]} {pid}
```

#### CAT

3. 设定LLC缓存分配方案

```shell
pqos -e "llc:1=0x000f;llc:2=0x0ff0;"
```

4. 根据socket编号为socket设定COS

```shell
pqos -e "llc:1=0x000f;llc@0,1:2=0x0ff0;llc@2-3:3=0x3c"
pqos -s   #查看socket上的缓存分配方式
```

5. 为核心设定缓存分配方案COS

```shell
pqos -a "llc:1=0,2,6-10;llc:2=1;"
```

**核心的缓存方案和socket的缓存方案**？

#### MBA

设置不同的带宽方案

```shell
pqos -e "mba:1=50;mba:2=70;"
```

为不同的socket设置带宽方案

```shell
pqos -e "mba:1=80;mba@0,1:2=64;mba@2-3:3=85"
```

