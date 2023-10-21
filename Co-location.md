# Co-location

## CPU Socket

<img src="https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Picture1280X1280.PNG" alt="1280X1280" style="zoom: 50%;" />

一个CPU Socket可以视为一个处理器，

- core：物理核，一个CPU中可以有多个核，各个核之间相互独立，可以并行执行，每个核拥有自己的寄存器，L1，L2缓存，同一个CPu中的多个物理核共享一个L3 缓存和内存总线。多个core之间是并行
- thread：逻辑核，在一个core中可以有多个thread，逻辑核之间共享缓存和内存控制，每个逻辑核有自己的寄存器。vCPU也是指逻辑核，逻辑核之间是并发



## Parties

多种交互应用下的QoS感知资源分区方法

### 摘要

背景：现有的多租户架构，一个LC与若干个BE，目前的云应用逐渐从批处理作业变 为了LC业务

### 1.介绍

多租户的软件架构策略因为资源争夺问题存在性能损失

对于微小的框架和应用，其延迟时间的要求比大型的应用更为严格

原有的三种方法：

- 禁止LC业务和其他业务共享资源，保证了QoS，损失了性能（<span style="background-color:red">是指运行LC业务是不能运行其他业务吗</span>）
- 避免可能发生干扰的应用之间的协同调度，提高了利用率，但限制了可以共同调度的情况
- 使用隔离技术进行资源分区，保证了QoS同时提高了BE的吞吐量，但只允许一个LC

Parties的运行粒度：几百毫秒，检测QoS违规

- 没有先验知识
- 容器，线程固定，缓存分区，频率缩放，内存容量分区，磁盘分区，网络带宽分区

#### 论文工作

1. 描述LC业务对不同资源分配的敏感度，对资源干扰的敏感度
2. 资源可交换性
3. 在LC业务和输入负载的多种组合下测试并与Heracles进行对比，

### 2.相关工作

原有工作的两种策略

- 集群调度器根据给定的应用预测干扰，在运行时进行资源调度或者禁止资源共享，保证了QoS但限制了共享
- 内粒度的资源分配，但需要对体系结构或者应用进行更改

parties相比Heracles额外支持内存容量隔离和磁盘带宽隔离

### 3.特征描述

平台规格 ：

![image-20231015195226004](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231015195226004.png)

- 每个socket中分配了8个核心作为IRQ内核，用于网络中断。
- 8GB内存用于操作系统
- 每个应用一个单独的容器
- 启用了超线程和超频

#### 3.1 实验中使用的 LC应用

1. Memcached：高性能内存对象缓存系统，调整了它的数据集配置，包含3200万项，每个项30B的键和200B的值
2. Xapian：web搜索引擎，根据wiki英文版快照构建成了叶子节点
3. Nginx：http服务器，数据集100万个大小为1KB的html文件
4. Moses：一个翻译系统
5. MongoDB：NoSQL数据库，数据集包含10亿条记录，每条记录10个字段，每个字段100B
6. Sphinx：语音识别系统

#### 最大负载和QoS目标的确定

逐渐提高请求数，来测试服务器的承载能力和延迟的情况。

![image-20231015202348459](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231015202348459.png)

对于每一个应用，逐渐增加输入负载，其尾部延迟也随之增加。（每个应用横轴数值范围不一样）通常在整个横轴的60%到80%的范围内，延迟的增加达到拐点，从拐点之后，延迟就快速增长

Qos设置**为拐点的第99百分位**（<span style="background-color:red">不完全理解，似乎是指将0到拐点之间的99百分位作为QoS</span>）

最大负载：拐点处的RPS

![image-20231015203325794](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231015203325794.png)

对于各个应用的更为具体的QoS与负载情况

- 用户空间，内核空间，IO处理的CPU时间占比
- 每千条指令 i_cache miss次数
- 每千条指令LLC miss次数
- 内存
- 内存带宽
- 磁盘带宽
- 网络带宽

#### 3.2 测试策略

使用开环负载生成器

对memcached，使用开环的内部负载生成器，对NGINX和MongoDB，使用开环的wrk2和YCSB，对于Moses，Sphinx，和Xapian，使用Tailbench

采用指数间隔到达时间分布来模拟泊松过程

在三台服务器上实例化足够的客户端避免饱和，保证测量到的延迟是服务器延迟。

每个实验运行5次，每次1分钟

#### 3.3 干扰的研究

将每个LC应用与一系列对系统施加不同影响的microbenchmark组合

![image-20231015211748656](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231015211748656.png)

左侧是测试的各种共享资源以及怎样进行的测试

实验中使用的每个物理核中都有两个逻辑核用于两个超线程。应用本身在8个物理核心上，使用8个线程（对应8个逻辑核）

- 为了测试超线程干扰对应用延迟的影响，将8个计算密集型程序与应用部署在了相同的逻辑核上，此时待测应用会与microbenchmark共享同样的超线程中的资源（一共8个超线程）
- 测试CPU干扰的影响，将8个计算密集程序部署在和待测应用相同的物理核上（每个物理核上两个超线程，一个待测应用，一个microbenchmark）
- 测试电源功率的影响，一个socket中22个物理核，8个用于网络中断，8个用于待测应用，在剩下的6个上跑满病毒（**占用了部分电源**）
- 测试LLC 容量的影响，在与待测应用相同的socket上运行缓存抖动程序。（**相当于ban掉了待测应用在LLC上的缓存数据？**）
- 测试LLC带宽的影响，启动12个缓存抖动程序（**占掉了全部的LLC带宽**）
- 测试内存带宽，启动12个内存波动测试程序（**占掉了部分内存带宽**）
- 测试内存容量，用一个内存冲击程序，占用128GB中的120GB（**占掉了部分内存**）
- 测试硬盘带宽，（**不是很理解**）
- 测试网络带宽的影响，运行iperf3客户端将网络带宽占掉

##### 对于干扰的分析

![image-20231015213706618](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231015213706618.png)

结合之前各个应用的延迟变换情况，应用对自己利用率较高的资源较为敏感。在该资源被占用时，收到的影响较大。

有些应用是因为自己对某个资源利用率高才对该资源敏感

而有些应用是因为其QoS过于严格所以对某些资源敏感（即便其本身可能对该资源没有很高的使用率）

#### 3.4 隔离的研究

两个结论：

1. 每个应用程序都受到一定资源的干扰
2. 每种共享资源都会影响一些程序

采用软硬件隔离机制

区分资源分配敏感型和资源争用敏感型

两类资源：计算和存储

##### 资源隔离的实验设计

首先单独采用隔离策略运行待测应用，区分出资源分配敏感和资源争用敏感（<span style="background-color:red">为什么会有资源争用敏感？</span>）

然后再将待测应用和microbenchmark放在一起，探究隔离机制消除干扰的程度

分为计算资源和存储资源两类

具体的隔离机制：

![image-20231015211748656](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231015211748656.png)

可以给应用分配特定的核心，并设定特定核心的频率。Intel CAT可以调整分配的带宽。

Linux上工具可以限制某个容器的 内存容量，磁盘带宽。以上这些是具体的资源隔离方案。即预先分配好一定的资源。在单独运行待测应用的情况下，就可以观察出待测应用是否是因为资源的分配而受到了干扰。

###### 3.4.1对于计算资源

![image-20231016105444491](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231016105444491.png)

在30%和90%负载下，对资源的敏感程度。图中代表了三个维度的资源。横纵轴代表对应的核心与LLC的分配，每个格子中的颜色代表满足QoS所需要的频率（Power）

1. 除MongoDB外，其他应用都需要满足特定的内核数量要求，否则无论LLC怎样分配，都会违反QoS
2. 内核给的够多，LLC和频率都可以放宽要求
3. 低负载下多数应用对LLC分配不敏感。（基本没有说满足特定cache way的需要，cacheway为1也可以满足QoS）

在采用CAT技术隔离cache时，同时也会间接影响内存带宽。因此可能无法区分出应用到底是对cache敏感还是对内存带宽敏感。加了一组实验

![image-20231016110835513](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231016110835513.png)

在空闲的核心上运行了占用内存带宽的microbenchmark，发现应用对LLC的需求进一步提高

###### 3.4.2对于存储资源

仅考虑了MongoDB

![image-20231016111205762](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231016111205762.png)

增大内存容量，对带宽的需求就会相应的减小

###### 3.4.3 资源可替代性

资源的可替代性是的parties可以更快的找到满足要求的配置，原因：

1. 配置方案相对灵活
2. 启发式搜索找到一个解就可以

### 4. parties的设计

#### 4.1 设计原则

1. 动态细粒度的资源分配：细粒度的决策避免在敏感资源上导致QoS违规
2. 不需要先验知识
3. 控制器需要快速的从错误的决策中恢复
4. 最后再考虑工作负载迁移

#### 4.2 控制器

##### 4.2.1 主控制器操作

1. 初始化时所有资源均等分配，每500ms采样一次
2. 当一个应用空闲很小或为负时，为其分配更多的资源
3. 满足所有应用的QoS之后，找到延迟松弛最高的应用减少其资源
4. 设置计时器追踪发生QoS的时间，1min内没有找到解决违规问题就会进行工作负载迁移

应用迁移的原则

应用迁移的步骤

##### 4.2.2 分配的调整

调整一个资源，观察是否满足要求，不满足要求的话就选择调整另一个资源

- 增加资源：目标是减少延迟时间。当增加了某一个资源仍然不满足要求时，不会撤回当前的资源，会继续的追加资源
- 减少资源：目标是仍然保证QoS，当减少资源的操作导致QoS违规时，可以快速的进行恢复，并在30s内禁止再次进行减少资源的操作

##### 4.2.3资源的排序

<增加/减少，核心数量/缓存大小/CPU频率/内存容量/磁盘带宽>，一共10种操作

在没有先验知识的情况下，第一次调整是随机选择资源的，随后的调整按照下图中开始轮转。避免总是增加或者减少同一种资源

![image-20231016202536224](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231016202536224.png)

计算资源发生改变后的结果不能及时观察到，因此在计算轮转完一圈后会检查一下内存的松弛情况。如果内存比较松弛，就再转一圈计算轮

需要跳过的情况：

1. 某一个应用已经拿到最多份额或最小份额的当前资源，会跳过本次调整
2. 对于内存中的服务，不会一直减少对其的内存分配

##### 4.2.4 执行资源分配

当需要给一个应用增加资源时。

1. 先从BE业务处回收，否则再从LC业务回收
2. 如果需要回收的是内存资源，则尽量找内存松弛最大的。否则就找延迟松弛最大的 

#### 4.3 一些讨论

1. 通过监控来分类出哪些应用是内存中的应用。避免其出现内存相关的问题
2. 测量延迟的方法
3. 控制器的参数设置：多长时间调整一次，增加资源和回收资源的阈值，负载迁移的触发时间，资源调整的粒度
4. 增加一个应用的资源可能对另一个应用产生的影响
5. 一个应用不会因为长期的回收资源而一直违背QoS
6. 负载迁移的频率
7. parties与作业调度器

### 5 实验评估

#### 5.1 方法论

在多节点部署

运行LC应用之外，同时运行BE业务，以BE业务的吞吐量作为测试

**实验方案：**

1. 先以恒定负载运行，再考虑日常的负载变化
2. 对于每个应用，负载从10%到100%，以10%为增量，这样对于每个应用就是10种负载，（N个应用，测试空间就是10的N方）
3. 30s预热，60s运行，重复3次

#### 5.2 恒定负载

##### 5.2.1 parties的性能

###### 两个应用协同运行

![image-20231017110857968](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231017110857968.png)

横轴代表的是待测应用的负载。纵轴六条线代表和当前待测应用一起运行的其他应用。图中能看出mongoDB协同运行比较好，能够和其他的应用都以较大负载运行

###### 三至六个应用协同运行

![image-20231017113912703](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231017113912703.png)

前四张图是待测应用和Memcached，Xapian协同运行，最后一张图是六个应用一起运行，Moses：10%，Sphinx：10%，MongoBD：100%

##### 5.2.2 与Heracles的比较

Heracles适用于一个LC与多个BE，对比的方案为，以一个待测应用作为LC业务，剩下的几个应用作为BE业务

![image-20231017145600514](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231017145600514.png)

1. 当LC业务QoS违规时，Heracles会挂起BE，但如果BE也是一个延迟敏感的业务，会导致更严重的QoS违规
2. Heracles在BE业务中不进行资源分区
3. Heracles中的资源控制器比较独立。在进行分配时比较激进或保守
4. Heracles不支持对内存容量和磁盘带宽的操作

##### 5.2.3 与其他资源控制器的比较

比较了另外的两种资源控制器，

- unmanaged：不进行任何资源隔离，仅依靠操作系统来进行资源的调度
- Oracle：通过在线的分析来确定可行方案，（**可能是指最理想的情况？**）

![image-20231017150648170](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231017150648170.png)

#### 5.3 波动负载

![image-20231017151405020](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231017151405020.png)

1. 第一幅图，Moses保持负载为10%，Xapian保持负载为20%，memcached负载从10%开始，逐渐增长到60%，再衰减回10%
2. 第二幅图，再unmanaged下，各应用延迟的波动，Xapian和Moses还能保证正常的业务，memcached随着负载的增长，Qos严重违规
3. 第三幅图，在Heracles下，保证了Memcached的QoS，但是挂起了另外两个应用
4. 第四幅图，在Parties下，各个应用表现均较好，不存在一个应用长期QoS违规
5. 第五幅图，BE业务的吞吐量
6. 第六幅图，Parties给各个应用分配的核心数量
7. 第七幅图和第八幅图，（**不理解为什么会产生这样的 变化**）

#### 5.4 Parties的开销

![image-20231017153036379](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231017153036379.png)

随着并行应用的增加，总的搜索空间会大幅增加，但是Parties总的搜索时间增长速度较慢





## CLite

### 摘要

基于贝叶斯优化的多资源分区

开源：https://github.com/GoodwillComputingLab/CLITE.

### 1. 介绍

和Parties时比较类似。

Parties缺乏最优性，健壮性，和效率

1. parties忽视了资源之间的复杂关系
2. 忽视了BG任务对资源的敏感程度

#### 文章的贡献

将贝叶斯方法用到的资源分区之中。并对基础的贝叶斯方法进行了一些调整。

与parties相比获得了一定的性能提升

### 2. 挑战与机遇

![image-20231017171310311](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231017171310311.png)

各种资源以及将其分配或隔离的方式

用于分配资源的方法已经有了，但是决定怎样分配很困难

![image-20231017172045582](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231017172045582.png)

应用对资源A的敏感程度要取决于另一种资源B分配了多少

![image-20231017172748790](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231017172748790.png)

用于论证Parties中那种每一次保持其他资源不变，只调整一种资源的方法，可能没办法找到最优解，只能得到次优解

### 3. CLite概述

Clite的设计准则，以及其不采用十分精确的模型，而是just-accurate-enough

Clite使用BO来加速对配置空间的探索

#### 3.1 贝叶斯优化

![image-20231017204734635](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231017204734635.png)

贝叶斯优化的一个阶段的快照

![image-20231017205947699](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231017205947699.png)

探索与开发过程

#### 3.2 为什么使用贝叶斯优化

总结就是BO方法不需要考虑部分细节以及复杂的关系。可以直接用于求解最优问题

和其他模拟黑盒函数的算法相比，BO需要少量的采样就可以获得较高的准确度

#### 3.3 CLite中BO的挑战

空间过大，目标函数不是一个简单的标量。受初始配置的影响

### 4. Clite的设计和实现

1. 代理模型选择GP，同时减少了采样点的数量来减少GP在推理上的开销

2. 需求函数的要求：1. 开销小，2. 平衡探索和开发

​	选择EI作为需求函数，![image-20231018140451281](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231018140451281.png)

以E（x）最大的x作为下一步的探索（**需求函数用于指导下一轮迭代的采样点选择**）

3. 评分函数的设计，将LC业务满足QoS的情况与BE业务的表现整合为一个值。（需要是平滑的分布，以便于指导需求函数的探索）

![image-20231018141741368](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231018141741368.png)

4. 初始配置的设置

5. 缓解多维空间探索的压力
6. 动态的中止条件

### 5. CLite的实验评估分析

#### 5.1 实验方法论

实验平台：

![image-20231019111426464](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231019111426464.png)

实验中运行的LC和BE业务

![image-20231019111836758](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231019111836758.png)

- 还是先测了LC业务的QoS目标与最大负载，不断增加负载观察延迟变化情况，CLIte是以95百分位作为QoS目标

![image-20231019112157213](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231019112157213.png)

（认为CPU功率不重要）

#### 5.2 实验结果分析

<img src="https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231019142209098.png" alt="image-20231019142209098" style="zoom:50%;" />

在没有BE业务的情况下，各种方法，在三个应用协同调度下能达到的最大负载。横轴为masstree的负载，纵轴为imgdnn的负载，每一格代表在不违反QOS的情况下，memcached能达到的最大负载。

![image-20231019142710634](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231019142710634.png)

和上图比较类似，还是协同调度三个LC，同时额外加了一个BE业务

![image-20231019143622976](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231019143622976.png)

(a)是Parties方法和CLite方法在不同资源山给出的分配方案。即便二者都是满足了LC业务的Qos目标。他们给出的方案是不同的。

具体的原因是Parties在找到满足QoS的目标之后就停止了。开始回收资源用于BE业务。但CLite方法在达到QoS目标之后，仍在不断的调整方法。根据资源的等价性以及应用对资源的敏感程度，来寻找怎样最大会BE业务的吞吐量

(b)是parties方法和CLite方法在多次进行采样之后对资源分配的调整。Parties在采样100次内陷入了循环，认为当前的应用不能被协同调度。需要进行负载迁移。而CLite在30次内就找到了可行解

![image-20231019144802624](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231019144802624.png)

在固定两个应用的负载，动态调整第三个应用的负载。各个方法与Oracle之间的差距。（但这里没看懂这个最终的性能表现是指BE的吞吐量还是其他什么目标）

![image-20231019153413718](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231019153413718.png)

同样的方案多次运行，CLite在性能表现上的方差最小。表现较为稳定，方差小

![image-20231019153820272](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231019153820272.png)

协同调度两个LC和一个BE，比较BE的性能表现。CLite的结果更接近于最优解。

![image-20231019154112267](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231019154112267.png)

协同运行三个LC和一个BE，观察各种资源分配方案下，BE业务的性能。Clite也是最优的

![image-20231019154414574](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231019154414574.png)

两个LC也三个BE，CLite在多BE业务下也能够达到较优的效果

![image-20231019154802774](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231019154802774.png)

在采样上需要的开销，CLite略高于Parties，在找到满足QoS要求的资源配置方案之后，CLite会继续进行优化

![image-20231019155757116](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231019155757116.png)

三个LC和一个BE，固定了两个LC的负载，动态调整第三个LC的负载，观察CLite对资源的分配以及BE业务的吞吐量。CLite是可以感知到负载的变化并及时调整达到新的最优方案的

**总的实验流程**

- 先测定QoS目标和最大负载标准
- figure7：3个LC，0个BE，观察协同调度下某一个LC能达到的最大负载。证明CLite提高LC的负载能力
- figure8：3个LC，1个BE，观察协同调度下某一个LC能达到的最大负载。证明CLite提高LC的负载能力
- figure9：3个LC，1个BE，比较了不同方法给出的分配方案。证明CLite为什么较优
- figure10：3个LC，0个BE，固定两个LC的负载，调整第三个LC的负载，比较三个LC的平均性能，证明Clite能提高LC的性能
- figure11：3个LC，0个BE，固定两个LC的负载，调整第三个LC的负载，多次运行，比较每次之间的差距。证明CLite的可变性小
- figure12：2个LC，1个BE，观察在两个LC不同的负载之下，BE能达到的性能。证明LC能提高BE的性能
- figure13：3个LC，1个BE，观察在三个LC均恒定负载的情况下，BE的性能。证明LC能提高BE的性能
- figure14：2个LC，3个BE，观察在两个LC均恒定负载的情况下，三个BE的平均性能。证明CLite在多BE下表现较好
- figure15：不同的LC也BE配比，验证CLite的采样开销
- figure16：3个LC，1个BE，固定了两个LC的负载，动态调整第三个LC的负载，比较资源的分配方案以及BE的性能。证明CLite的动态调整能力
- CLite对BO参数调优不敏感
- Clite优于其他的空间探索算法

### 6. 相关工作

1. unmanaged

不进行分区，探索使业务之间不争夺共同资源还能满足QoS的并置方案。

缺点是需要先验知识，不能动态调整。同时减少了可共存的应用方案

Cooper和Hound不能保证QoS

2. 单LC多BE的分区策略

只考虑一个LC和多个BE协同调度。

缺点是只保证了LC的QoS，忽视了BE的性能

3. 多LC多BE的分区策略

Parties，不能找到最优解



## OLPart

### 摘要

以性能计数器来近似衡量应用的资源敏感性

采用上下文多臂赌博机来设计分区方案

开源：https://github.com/oksdfncsj/OLPart.

### 1. 介绍

- 算法应该能获得最优解
- 高效性和鲁棒性
- 不需要先验知识

之前方法的问题：在搜索过程中忽视了应用对资源敏感性的问题

运行时性能计数器可以在一定程度上指示应用对资源的敏感程度

### 2. 动机

#### 2.1 资源分区的难点

应用对于资源的敏感性是动态变化的，会收到多种因素的影响。比如另一种资源分配的多少，应用负载的多少

![](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231019213353824.png)

- figure1：说明应用对资源的敏感性存在的一个复杂情况

#### 2.2 已有方法的限制

Parties：parties在给应用增加资源时有一个做法。如果新分配了资源并没有缓解应用的QoS违规问题。parties不会回收刚刚分配的资源，而是会继续追加其他类型的资源（甚至还是当前的资源）。但这种做法本身存在问题。OLPart实验过程中观察到，例如在某一种资源A没有达到要求时，一味的增加B资源是没用的。

CLite：Clite的问题是缺乏对应用具体状态的感知，Clite中有一项设置是当有任意一个应用QoS违规时，评分函数不会超过0.5。但决策时只是知道了有应用QoS违规，但是不知道具体是哪个应用违规。此时再进行决策。是有可能给正常运行的应用追加资源的。同样，仅靠一个标量值，CLite也无法感知到应用对资源的敏感性。

![image-20231019213713784](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231019213713784.png)

- figure2：说明CLite在探索过程中还是存在低效的问题

#### 2.3 存在的机会

通过性能计数器来指示应用对资源的敏感程度

![image-20231019214151839](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231019214151839.png)

- figure3：不断改变LLC cacheway的分配，左边是延迟的变化，右边是cache miss率的变化。二者十分相近。

寻找应用j对资源r的敏感性表现为哪一个性能计数器，实验设计

1. 针对应用r，设计1000种资源分配方案
2. 在若干资源方案之中，是资源r从最小变化到最大。其他配置保持不变，
3. 记录下每一次的延迟和所有待定的性能计数器
4. 计算延迟的变化和哪一个性能计数器的变化相关性最大。

总共测了6个LC应用，3种资源，100个待定的性能计数器

![image-20231019214826527](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231019214826527.png)

最左侧是6个应用，测试了每个应用对三个资源的敏感性，可以通过哪些性能计数器表现出来。

**这里各个性能计数器的含义稍后查一下**

### 3. 对OLPart的总览

设计准则

- 多资源的联合搜索
- 轻量级，高响应
- 不需要先验知识
- 采用性能计数器指示配置空间的探索

CMAB：在一系列实验中，选择一组动作，最大化所选行动的总收益

#### 3.1 多臂赌博机

MAB和UCB

CMAB和LinUCB

#### 3.2 为什么CMAB使用与资源分区问题

阐述了四个方面的原因

#### 3.3 应用CMAB的挑战

探索空间过大

奖励函数的设计

### 4. OLPart的设计

#### 4.1 Bandits和arm的设计

bandits代表老虎机，问题模型本身，

arm代表每一步的动作

采用分散化的策略，为不同的资源和应用建立独立的bandits。在决策时，由所有bandits协同决策

- 完全隔离与部分共享

每一个bandits负责一个应用和一个资源。每一个bandit的arm数量代表了资源的总数

#### 4.2 上下文特征

对每个应用，维护一个集合，包含了能代表资源敏感性的性能计数器的集合。

针对于每个bandit（维护一个应用和一个资源的关系），在决策过程中使用的上下文信息，还包含了其他应用的性能计数器信息。因为在决策过程中，对每一个应用资源的分配是会收到其他应用当前资源分配方式的干扰的。

#### 4.3 摇臂选择策略

部分共享：采用标准的LinUCB

完全隔离：基于贪心算法的束搜索法

束搜索法这里没有完全理解

![image-20231021144628114](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231021144628114.png)

#### 4.4 奖励函数的设计

违反QoS的情况

满足QoS的情况

#### 4.5 多版本

定期构建一个新的bandits

#### 4.6 对旧的bandit的利用

利用旧的bandit的相关参数来初始化新到来的应用业务

如果一个应用之前在当前服务器节点上部署过，则可以直接用之前与这个应用相关的bandit来初始化新的bandit

否则，可以用之前所有bandit的平均值来初始化新的应用的bandit

#### 4.7 整合

![image-20231021163542229](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231021163542229.png)

OLPart的整一个运行流程

### 5. 实验评估

#### 5.1 实验设置

##### 实验环境

![image-20231021163657367](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231021163657367.png)

禁止超线程和超频。

应该是10个物理核，每个物理核上两个逻辑核，一共20个核心。分了一个CPU core跑操作系统，其他的跑应用

##### 分配的资源

CPU核心，缓存大小和内存带宽。CPU核心采用完全隔离的策略，缓存大小和内存带宽采用部分共享

CAT可以用于分配cache way，但需要是连续的

MBA可以给应用分配指定比例的带宽

##### 待测应用

![image-20231021165046997](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231021165046997.png)

实验中使用的LC和BE业务

工作中的负载使用的是tailbench套件，BE的负载通过PARSEC套件获得

QoS的确定和CLite中使用的方法近似

##### OLPart的配置

- 三秒做一次决策
- 每个应用选择五个性能计数器
- 最多维持三个版本的bandits
- 束搜索算法中为每个bandit选择5个arm
- 到达给定的搜索时间就结束

#### 5.2 Baselines

选择了parties，Clite和离线分析的oracles

#### 5.3 结果和分析

##### 5.3.1 算法的最优性

![image-20231021170310547](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231021170310547.png)

- figure5：3个LC，0个BE，测试在前两个应用的不同负载下，第三个应用能达到的最高负载，用于验证OLPart等处的分配方案的最优性

![image-20231021191334177](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231021191334177.png)

- figure6：3个LC，1个BE，比较在不同负载下，BE业务的吞吐量：验证OLPart能最大化BE业务的性能

![image-20231021191349737](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231021191349737.png)

- figure7：3个LC，1个BE，比较在同一个负载下，BE吞吐量随时间的变化。验证OLPart探索空间的效率更高

![image-20231021191427822](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231021191427822.png)

- figure8：3个LC，一个BE，LC的应用的负载都是随机的。来比较不同方法下BE业务的吞吐量。验证OLPart能最大化BE吞吐量

##### 5.3.2 可扩展性

![image-20231021191939870](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231021191939870.png)

- figure9：在不同规模的协同调度作业下，OLPart能以较快的速度找到最优解。同时BE的吞吐量也是最高的

##### 5.3.3 上下文特征的有效性

![image-20231021193158033](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231021193158033.png)

在使用上下文特征和不使用上下文特征的两种情况下，BE业务的吞吐性能和找到最优解的时间都存在一定的差距

##### 5.3.4 bandits重用的有效性

![image-20231021193824177](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231021193824177.png)

做了三组实验，每组实验分两个阶段。第一个阶段跑60s，第二个阶段跑60s，以第二个阶段中BE的吞吐量作为衡量指标。

其中，第一组实验，前后两个阶段运行的是完全不同的应用。第二组实验，前后两个阶段运行的应用有部分相同。而在第三组实验，前后两个阶段运行的应用则完全相同。三组实验下，第三组实验的性能表现是最好的。说明了bandit重用这一机制确实能缓解冷启动的问题。在某些应用场景下，能够更迅速的找到新部署的协同调度任务的最优解。

##### 5.3.5 采用多版本bandits的有效性

![image-20231021194643213](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231021194643213.png)

对于LC和BE以及LC负载的设置。选择了3个LC和1个BE的组合。LC业务的负载随时间进行变化。来模拟实际应用中，负载的波动情况。

对于多版本bandits这一机制。主要包含两个方面。保存bandits的版本数量和创建新的bandits的频率。做了两组实验，分别是固定这两个因素中的一个，然后动态调整另外一个。

左图是不同频率下的表现。过高和过低都不太行

右图是固定了频率，然后调整版本数的表现，同样也是过高和过低都不太行。但同时，K=3的情况总是优于K=1的情况。说明多版本bandits这一机制本身，还是有效的。

#### 5.4 OLPart的开销

![image-20231021195426017](https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Pictureimage-20231021195426017.png)

类似线性的时间开销，比较高效

### 总的实验设计

总体先验证了最优性，分为两部分，没有BE下LC能达到多高的负载。和LCBE混合调度下，BE能有多高的吞吐量。

1. 三个LC调度。比较能够达到的最大负载（figure5）。
2. 三个LC和1个BE调度。保证不同方法下LC以相同的负载运行，比较BE能达到的吞吐量（figure6）。再扩展到若干应用之间的调度。在任何情况下，OLPart的BE业务都能有最大的吞吐量（figure8）.

然后验证了高效性.

3. 在某一种负载下，比较不同的方法找到最优解需要的时间，同时从侧面也验证了BE吞吐量的最优（figure7）

然后验证了可扩展性

4. 不仅仅是3个LC，实验中检测了在更多的LC与BE进行协同调度的情况下，OLPart的查询速度和BE业务的表现也都是较优的（figure9）

然后验证了算法设计中，部分模块的有效性

5. 类似于消融实验的方式，验证了OLPart中使用上下文特征是有效的（figure10）
6. 验证了bandits重用是有效的
7. 验证了多版本bandits是有效的（figure11）
