### run.py

- run_bg_benchmark

给定一系列需要运行的BG应用以及对应的CPU核心号，在每个应用对应的容器中，规定CPU核心，运行脚本来启动BG应用。

最终返回的是每个启动的BG应用的进程号组成的字典。

下一步细节：/home/run_bg.py

- get_now_ipc

起手的for循环部分根据进程号检查了每个应用是否还在运行。似乎是如果没有在运行的话，就重新调用run_bg_benchmark。

在run_bg_benchmark中，本身已经设置了容器的CPU亲和性，随后又根据进程号或者父进程的进程号再次绑定CPU亲和性。准备了perf命令来准备进行性能的收集

