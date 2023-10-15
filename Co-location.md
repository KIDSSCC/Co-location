# Co-location

## CPU Socket

<img src="https://raw.githubusercontent.com/KIDSSCC/MarkDown_image/main/Picture1280X1280.PNG" alt="1280X1280" style="zoom:67%;" />

一个CPU Socket可以视为一个处理器，

- core：物理核，一个CPU中可以有多个核，各个核之间相互独立，可以并行执行，每个核拥有自己的寄存器，L1，L2缓存，同一个CPu中的多个物理核共享一个L3 缓存和内存总线。多个core之间是并行
- thread：逻辑核，在一个core中可以有多个thread，逻辑核之间共享缓存和内存控制，每个逻辑核有自己的寄存器。vCPU也是指逻辑核
