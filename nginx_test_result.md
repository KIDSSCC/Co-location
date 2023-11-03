用Jmeter对nginx进行压测

- Jmeter设置线程组数量为50000，在5s内全部启动，持续运行25秒
- nginx准备100000个静态文件，设置工作进程数量为1
- 在jmeter测试计划启动后10s中启动perf，进行10s的观察
- 对应核心的cache way设置为0x1，MB设置为10%

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