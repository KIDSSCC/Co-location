# NAS Parallel Benchmark

### NPB-MPI

NPB的MPI实现版本。根目录NPB3.3-MPI，配置文件路径：NPB3.3-MPI/configure，目前已经准备了编译所需的make.def文件。

具体要求见README.install文件。

运行示例:

```bash
# 编译IS，问题规模为D，进程数为8
make is CLASS=D NPROCS=8
# 编译后在bin/目录下产生is.D.8文件
mpirun -np 8 --cpu-list 0-7 bin/is.D.8
```

**编译时可能部分文件存在访问权限问题，chmod解决**

### NPB-OMP

NPB的OpenMP实现版本，根目录NPB3.3-OMP，配置文件路径：NPB3.3-MPI/configure，目前已经准备了编译所需的make.def文件。

具体要求见README.install文件。

运行示例：

```bash
# 编译IS，问题鬼母为D
make is CLASS=D
# 编译后在bin/目录下产生is.D.x文件
export OMP_NUM_THREADS=8
taskset -c 0-7 bin/is.D.x
```

在新的shell中运行时需要重新设置环境变量OMP_NUM_THREADS，代表OpenMP并行程序运行时的线程数。

