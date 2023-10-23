import subprocess as sp
import os
import time
import subprocess
import csv
import itertools
import numpy as np
from typing import List, Dict, Tuple
import datetime
from copy import deepcopy
import pandas as pd
from scipy.stats.mstats import gmean

FNULL = open(os.devnull, 'w')

BG_APP_NAMES    = [
                'blackscholes' ,
                'canneal',
                'fluidanimate',
                'freqmine',
                'streamcluster',
                'swaptions',
                'vips',
                'bodytrack',
                'dedup',
                'facesim',
                'ferret',
                'raytrace',
                'x264',
                'amg',
                'comd',
                'laghos',
                'miniamr',
                'minife',
                'nekbone',
                'sw4lite',
                'swfft',
                'xsbench',
                ] 

ECP_BENCHMARK = [
                'amg',
                'comd',
                'laghos',
                'miniamr',
                'minife',
                'nekbone',
                'sw4lite',
                'swfft',
                'xsbench',
                ]

ECP_BENCHMARK_GREP = {
                'amg': "'amg -n 300'",
                'comd': 'CoMD-mpi',
                'laghos': 'laghos-1.0',
                'miniamr': 'miniamr-1.4.0',
                'minife': 'minife-2.1.0',
                'nekbone': 'nekbone-17.0',
                'sw4lite': 'sw4lite-1.0',
                'swfft': 'swfft-1.0',
                'xsbench': 'xsbench-14',
}

# THREAD_NUM_APP = {
#                 'blackscholes' : 3,
#                 'canneal'      : 3,
#                 'fluidanimate' : 8,
#                 'freqmine'     : 3,
#                 'streamcluster': 1,
#                 'swaptions'    : 5,
#                 'vips'         : 1,
#                 'bodytrack'    : 3,
#                 'dedup'        : 8,
#                 'facesim'      : 8,
#                 'ferret'       : 3,
#                 'raytrace'     : 1,
#                 'x264'         : 8,
#                 'amg'          : 8,
#                 'comd'         : 1,
#                 'laghos'       : 1,
#                 'miniamr'      : 1,
#                 'minife'       : 1,
#                 'nekbone'      : 1,
#                 'sw4lite'      : 8,
#                 'swfft'        : 1,
#                 'xsbench'      : 8
#             }

# BG_APP_ISO_IPC   = {
#                 'blackscholes' : 7.7, 
#                 'canneal'      : 1.9, 
#                 'fluidanimate' : 18.0, 
#                 'freqmine'     : 3.6, 
#                 'streamcluster': 0.77, 
#                 'swaptions'    : 12.4, 
#                 'vips'         : 3.3,  
#                 'bodytrack'    : 7.6,
#                 'dedup'        : 10.9,
#                 'facesim'      : 22.2,
#                 'ferret'       : 5.3,
#                 'raytrace'     : 1.7,
#                 'x264'         : 11.5,
#                 'amg'          : 12.6,
#                 'comd'         : 1.9,
#                 'laghos'       : 3.5,
#                 'miniamr'      : 0.95,
#                 'minife'       : 1.3,
#                 'nekbone'      : 3.1,
#                 'sw4lite'      : 27.1,
#                 'swfft'        : 0.8,
#                 'xsbench'      : 6.3,
#                 }

THREAD_NUM_APP = {
                'blackscholes' : 8,
                'canneal'      : 1,
                'fluidanimate' : 8,
                'freqmine'     : 1,
                'streamcluster': 1,
                'swaptions'    : 8,
                'vips'         : 1,
                'bodytrack'    : 1,
                'dedup'        : 1,
                'facesim'      : 8,
                'ferret'       : 1,
                'raytrace'     : 1,
                'x264'         : 8,
                'amg'          : 8,
                'comd'         : 1,
                'laghos'       : 1,
                'miniamr'      : 1,
                'minife'       : 1,
                'nekbone'      : 1,
                'sw4lite'      : 8,
                'swfft'        : 1,
                'xsbench'      : 8
            }

BG_APP_ISO_IPC   = {
                'blackscholes' : 20.6, 
                'canneal'      : 0.65, 
                'fluidanimate' : 17.7, 
                'freqmine'     : 1.2, 
                'streamcluster': 0.76, 
                'swaptions'    : 19.7, 
                'vips'         : 3.3,  
                'bodytrack'    : 2.5,
                'dedup'        : 1.5,
                'facesim'      : 22.0,
                'ferret'       : 1.8,
                'raytrace'     : 1.7,
                'x264'         : 8.2,
                'amg'          : 10.9,
                'comd'         : 1.95,
                'laghos'       : 3.5,
                'miniamr'      : 0.7,
                'minife'       : 1.2,
                'nekbone'      : 3.1,
                'sw4lite'      : 27.1,
                'swfft'        : 0.86,
                'xsbench'      : 6.2,
                }

# THREAD_NUM_APP = {
#                 'blackscholes' : 8,
#                 'canneal'      : 8,
#                 'fluidanimate' : 8,
#                 'freqmine'     : 8,
#                 'streamcluster': 1,
#                 'swaptions'    : 8,
#                 'vips'         : 1,
#                 'bodytrack'    : 8,
#                 'dedup'        : 1,
#                 'facesim'      : 8,
#                 'ferret'       : 1,
#                 'raytrace'     : 1,
#                 'x264'         : 8,
#                 'amg'          : 8,
#                 'comd'         : 1,
#                 'laghos'       : 1,
#                 'miniamr'      : 1,
#                 'minife'       : 1,
#                 'nekbone'      : 1,
#                 'sw4lite'      : 8,
#                 'swfft'        : 1,
#                 'xsbench'      : 8
#             }

# BG_APP_ISO_IPC   = {
#                 'blackscholes' : 20.6, 
#                 'canneal'      : 5.2, 
#                 'fluidanimate' : 17.9, 
#                 'freqmine'     : 9.9, 
#                 'streamcluster': 0.78, 
#                 'swaptions'    : 19.8, 
#                 'vips'         : 3.3,  
#                 'bodytrack'    : 20.388,
#                 'dedup'        : 1.5,
#                 'facesim'      : 23.1,
#                 'ferret'       : 1.7,
#                 'raytrace'     : 1.7,
#                 'x264'         : 9.4,
#                 'amg'          : 12.2,
#                 'comd'         : 1.95,
#                 'laghos'       : 3.5,
#                 'miniamr'      : 0.93,
#                 'minife'       : 1.3,
#                 'nekbone'      : 3.0,
#                 'sw4lite'      : 25.7,
#                 'swfft'        : 0.86,
#                 'xsbench'      : 6.7,
#                 }

# sudo docker exec fluidanimate0 taskset -c 21,22,23,24 python /home/run_bg.py fluidanimate 2
# sudo taskset -apc 22,23 pid

APP_PPID        = {
                'blackscholes' : 311842,
                'canneal'      : 311690,
                'fluidanimate' : 311977,
                'freqmine'     : 312133,
                'streamcluster': 312268,
                'swaptions'    : 312409,
                'vips'         : 312549,
                'bodytrack'    : 312683,
                'dedup'        : 312813,
                'facesim'      : 312954,
                'ferret'       : 313092,
                'raytrace'     : 313225,
                'x264'         : 313365,
                'amg'          : 319955,
                'comd'         : 320107,
                'laghos'       : 320265,
                'miniamr'      : 320435,
                'minife'       : 320590,
                'nekbone'      : 320750,
                'sw4lite'      : 320905,
                'swfft'        : 321064,
                'xsbench'      : 321221
                }


SLEEP_TIME = 0.01
NUM_PERF_FAIL = 0

PATH_SHARE = "/home/pwq/atc/tailbench/share"
PATH_RUN = '/home/pwq/lsp/lsp'


def update_APP_PID(app_list:List[str]) -> None:
    """
    create a new APP_PID dictionary
    """
    global APP_PID
    APP_PID = {}.fromkeys(app_list, '')
    global NUM_APPS
    NUM_APPS = len(app_list)

def get_app_pid(app:str) -> str:
    """
    get running app's pid
    input: app name
    return: app's pid
    """
    # sudo docker exec fluidanimate0 taskset -c 18 python /home/run_bg.py fluidanimate 1
    # ps aux | grep /home/tailbench.inputs/img-dnn/ | grep -v grep
    print(f'start get {app} pid')
    if app[:-1] in ECP_BENCHMARK:
        grep_cmd = f'ps aux | grep {ECP_BENCHMARK_GREP[app[:-1]]} | grep -v grep'
    elif app[:-1] == 'canneal' or app[:-1] == 'streamcluster' or app[:-1] == 'dedup':
        grep_cmd = f'ps aux | grep /home/pkgs/kernels/{app[:-1]}/inst | grep -v grep'
    else:
        grep_cmd = f'ps aux | grep /home/pkgs/apps/{app[:-1]}/inst | grep -v grep'
    
    for app_i in APP_PID.keys():
        if app_i[:-1] == app[:-1] and app_i != app and APP_PID[app_i] != '':
            grep_cmd += f' | grep -v {APP_PID[app_i]}'
    while True:
        try:
            r = subprocess.run(grep_cmd, shell=True, check=True, capture_output=True)
            r_ = str(r.stdout.decode())
            r_ = "".join(r_)
            rs = r_.split(' ')
            cnt = 0
            for m in range(len(rs)):
                if rs[m] == '':
                    cnt += 1
            for x in range(cnt):
                rs.remove('')
            print(f'{app}\'s PID: {rs[1]}')
            return rs[1]
        except:
            continue

def run_bg_benchmark(app_list:List[str], core_allocation_list:List[str]) -> Dict[str, str]:
    """
    run bg app list
    input: bg app list, app's core
    return: None
    """
    # 这个持久化运行
    total_command = []
    for i in range(len(app_list)):
        bg_app_name = app_list[i][:-1]
        # sudo docker exec laghos0 taskset -c 17,18,19 python /home/run_bg.py laghos 8
        # ps aux | grep /home/pkgs/apps/fluidanimate/inst | grep -v grep
        command = f"sudo docker exec {app_list[i]} taskset -c {core_allocation_list[i]} python /home/run_bg.py {bg_app_name} 8 &"
        total_command.append(command)
    subprocess.call(" ".join(total_command), shell=True, stdout=open(os.devnull, 'w'))
    # time.sleep(3.0)
    for i in range(len(app_list)):
        print(f'start run {app_list[i]}')
        APP_PID[app_list[i]] = get_app_pid(app=app_list[i])
    return APP_PID

def get_now_ipc(app_list:List[str], core_allocation_list:List[str]) -> Tuple[float, List[float]]:
    """
    get average of app list's ips speedup, as reward
    input: app list, app's core
    return: average of ips speedup(as reward), ips speedup list
    """
    # core_allocation_list = refer_core(core_config=[3, 4, 5, 2, 2, 2, 1, 7, 1, 4, 4, 2, 1, 1, 1, 1, 3, 2, 1, 3])
    
    now = datetime.datetime.now()
    total_command = []
    rep_total_command = []

    insn_tmp = []

    for i in range(len(app_list)):
        # 检查每个bg app是否还在运行
        cmd_run = f"sudo ps aux | grep ' {APP_PID[app_list[i]]} '"  # 查看当前target的进程情况
        out = os.popen(cmd_run).read()
        print(cmd_run)
        print(out)
        if len(out.splitlines()) <= 2:
            print(f"==============bg app {app_list[i]} rerun==============")
            run_bg_benchmark(app_list=[app_list[i]], core_allocation_list=[core_allocation_list[i]])

        # 似乎没什么用，绑定一次就够了
        # KIDSSCC:为目标进程或者其父进程设置CPU亲和性
        pid = APP_PID[app_list[i]]
        ppid = APP_PPID[app_list[i][:-1]]
        try:
            subprocess.call(f"sudo taskset -apc {core_allocation_list[i]} {pid} > /dev/null",
                            shell=True)
        except:
            subprocess.call(f'sudo taskset -apc {core_allocation_list[i]} {ppid} > /dev/null',
                            shell=True)
        # perf测量每个正在运行的app的22个性能数据
        # sudo docker exec x2640 taskset -c 0,1,2 python /home/run_bg.py fluidanimate 8
        # sudo perf stat -e cycles,instructions,inst_retired.prec_dist,uops_retired.retire_slots,L1-dcache-loads,dTLB-loads,l2_rqsts.all_demand_miss,offcore_requests.demand_data_rd,dTLB-load-misses,LLC-loads,branch-misses,L1-dcache-stores,branch-loads,branch-load-misses,LLC-store-misses,cpu_clk_unhalted.thread_p,L1-dcache-load-misses,ld_blocks.store_forward,ld_blocks.no_sr -C 0,1,2 sleep 0.5
        perf_command = f"sudo perf stat -e cycles,instructions -p {pid} sleep {SLEEP_TIME}"  # perf工具获取该app运行的22个指标
        rep_perf_command = f"sudo perf stat -e cycles,instructions -p {ppid} sleep {SLEEP_TIME}"
        total_command.append(perf_command)
        rep_total_command.append(rep_perf_command)
        # print(perf_command)
        insn_tmp.append(f"ipc_{str(app_list[i])}")

    while True:
        r_ = []
        for i in range(len(app_list)):
            try:
                r = subprocess.run(total_command[i], shell=True, check=True, capture_output=True)
                if i%5 == 4: time.sleep(1.5)
            except:
                r = subprocess.run(rep_total_command[i], shell=True, check=True, capture_output=True)
                if i%5 == 4: time.sleep(1.5)

            r_.append(str(r.stderr.decode()))
        r_ = "".join(r_)
        rs = r_.split('\n')
        label = dict.fromkeys(insn_tmp, 0)

        # 用于储存究竟属于哪个app
        app_name = -1
        app_id = 0
        for index, line in enumerate(rs):
            rr = line.split(' ')
            rr = [i for i in rr if i != ""]
            # print(rr)
            if len(rr) < 2 or "elapsed" in rr or 'Some' in rr or '\techo' in rr or '\tperf' in rr\
                or 'echo' in rr or '...' in rr:
                continue
            if "Performance" in line:
                app_name = app_list[app_id]
                app_id += 1
                # 字典label记录每个app运行时核内产生的指令数
                try:

                    # label[f"ipc_{app_name}"] = float(instruction[0].replace(',', '')) \
                    #                            / BG_APP_ISO_IPS[app_name[:-1]]
                    label[f"ipc_{app_name}"] = float(rs[index + 3][55:59])
                except:
                    print(f'\n=========={app_name} can not get ips==========\n')
                    label[f"ipc_{app_name}"] = 0.15

        ipc_list = list(label.values())
        core_num = []
        for i in range(len(core_allocation_list)):
            core_allocation = core_allocation_list[i].split(',')
            if int(core_allocation[-1]) > 27:
                r = int(core_allocation[-1]) - 28
            else:
                r = int(core_allocation[-1])

            if int(core_allocation[0]) > 27:
                l = int(core_allocation[0]) - 28
            else:
                l = int(core_allocation[0])

            core_num.append(r - l + 1)
        ipc_list_core = [ipc_list[i] * min(core_num[i], THREAD_NUM_APP[app_list[i][:-1]]) / BG_APP_ISO_IPC[app_list[i][:-1]] \
                    for i in range(len(ipc_list))]

        reward = gmean(ipc_list_core)
        # reward = sum(ips_list) / len(ipc_list)
        break


    times = datetime.datetime.now() -now
    print("==================================getnowipc",times)
    print(f'ips_list:{ipc_list}')
    print(f'ipc_list_core:{ipc_list_core}')
    print(f'core_num:{core_num}')
    print(f'app_list:{app_list}')
    return reward, ipc_list_core


def refer_core(core_config:List[int], unit_scale:int = 1) -> List[str]:    # len(core_config) = NUM_APPS
    """
    translate core config to core command, [2,4,3] => ["0,1","2,3,4,5","6,7,8"]
    input: core config list
    output: core command list
    """
    
    core_config = [c * unit_scale for c in core_config]
    core_allocation_list = [""] * len(core_config)
    endpoint_left = 0
    for i in range(len(core_config)):
        endpoint_right = endpoint_left + core_config[i] - 1
        core_list = list(range(endpoint_left, endpoint_right+1))
        for j in range(len(core_list)):
            if core_list[j] > 27:
                core_list[j] += 28
        core_allocation_list[i] = ",".join([str(c) for c in core_list])
        endpoint_left = endpoint_right + 1
    return core_allocation_list

# def refer_llc(llc_config:List[int]) -> List[str]: 
#     """
#     translate llc config to llc command, [2, 5, 3] -> ['0x003', '0x07b', '0x380']
#     input: llc config list
#     output: llc command list
#     """
#     nof_llc = np.array(llc_config).sum()
#     i = nof_llc - 1
#     llc_allocation_list = []
#     for j in range(len(llc_config)):
#         ini_list = [0 for k in range(nof_llc)]
#         count = llc_config[j]
#         while count > 0:
#             ini_list[i] = 1
#             i -= 1
#             count -= 1
#         llc_allocation_list.append(hex(int(''.join([str(item) for item in ini_list]), 2)))
#     return llc_allocation_list

def refer_llc(llc_config:List[int], num_llc:int) -> List[str]:
    llc = [-1] * num_llc
    group_id = np.argsort(-np.array(llc_config)).tolist()
    llc_config = (-np.sort(-np.array(llc_config))).tolist()  # 从大到小排列
    llc_allocation_list_nosorted = []
    for app in range(len(llc_config)):
      ini_list = [0] * num_llc
      size_config = llc_config[app]
      now_config = 0

      while now_config < size_config:
            min_llc = min(llc)
            for i in range(len(llc)):
                  if llc[i] == min_llc and ini_list[i] == 0:
                        ini_list[i] = 1
                        now_config += 1
                        llc[i] += 1
                        if now_config == size_config:
                              break
      llc_allocation_list_nosorted.append(hex(int(''.join([str(item) for item in ini_list]), 2)))        

    llc_allocation_list = []
    for i in range(len(llc_config)):
      for j in range(len(group_id)):
            id = group_id[j]
            if i == id:
                  llc_allocation_list.append(llc_allocation_list_nosorted[j])
    return llc_allocation_list

def refer_mb(mb_config:List[int]) -> List[int]:    
    """
    translate mb config to mb command, [2, 5, 3] -> [20, 50, 30]
    input: mb config list
    output: mb command list
    """
    mb_allocation_list = [i * 10 for i in mb_config]
    return mb_allocation_list

def gen_configs_recursively_fix(num_res:int, num_apps:int) -> List[List[int]]:
    """
    get a resource's allocation space.
    input: resource id, num of groups/apps
    return: a list contains all allocation plans of a resource
    """
    def gen_configs_recursively(u, num_res, a, num_apps):
        if (a == num_apps - 1):
            return None
        else:
            ret = []
            for i in range(1, num_res - u + 1 - num_apps + a + 1):
                confs = gen_configs_recursively(u + i, num_res, a + 1, num_apps)
                if not confs:
                    ret.append([i])
                else:
                    for c in confs:
                        ret.append([i])
                        for j in c:
                            ret[-1].append(j)
            return ret
    res_config = gen_configs_recursively(0, num_res, 0, num_apps)
    for i in range(len(res_config)):
        other_source = np.array(res_config[i]).sum()
        res_config[i].append(num_res - other_source)
    return res_config

# Use taskset, and intel CAT and MBA tools to partition resources among co-running applications
def perform_resource_partitioning(core_allocation_list, llc_allocation_list, mb_allocation_list, 
                                  group_list, app_list, is_group):
    """
    implement the resource allocation command on system
    input: core, llc and mb allocation command, groups/apps list
    return: None
    """
    # 先用taskset绑核
    for i in range(len(app_list)):
        pid = APP_PID[app_list[i]]
        print(f'core_list[i]: {core_allocation_list[i]}')
        print(f'pid: {pid}')
        sp.call(f'sudo taskset -apc {core_allocation_list[i]} {pid} > /dev/null',
                shell=True)
    # 再用CAT/MBA绑llc和mb
    g_core_allocation = []
    for group in group_list:
        group_cores = []
        for app in group:
            for a in range(len(app_list)):
                if app == app_list[a]:
                    group_cores.append(core_allocation_list[a])
        g_core_allocation.append(','.join(group_cores))

    print(f'g_core_allocation: {g_core_allocation}')

    for i in range(len(group_list)):
        sp.run('sudo pqos -a "llc:{}={}"'.format(i+1, g_core_allocation[i]), shell=True, capture_output=True)
        # sp.run('sudo pqos -e "llc:{}={}"'.format(i+1, g_llc_allocation[i]),
        #        shell=True, capture_output=True)
        sp.run('sudo pqos -e "llc@0:{}={}"'.format(i+1, llc_allocation_list[i]),
               shell=True, capture_output=True)
        sp.run('sudo pqos -a "core:{}={}"'.format(i+1, g_core_allocation[i]), shell=True, capture_output=True)
        # sp.run('sudo pqos -e "mba:{}={}"'.format(i+1, int(g_mb_allocation[i])), shell=True,
        #        capture_output=True)
        sp.run('sudo pqos -e "mba@0:{}={}"'.format(i+1, mb_allocation_list[i]), shell=True,
               capture_output=True)

def gen_init_config(app_num:int=0, num_core:int=0, num_llc:int=0, num_mb:int=0,
                    core_space:List[List[int]]=[], llc_space:List[List[int]]=[], mb_space:List[List[int]]=[]) \
                    -> Tuple[List[int], List[int], List[int], int, List[int], List[int]]:
    """
    create an initial resource plan.
    input: app number, core, llc and mb number
    return: all resources' config, and corrsponding arms
    """
    nof_core = num_core; nof_llc = num_llc; nof_mb = num_mb
    core_arm = 0; llc_arm = 0; mb_arm = 0
    
    core_config = split_averagely(nof_units=nof_core, nof_clusters=app_num)
    for config_id in range(len(core_space)):
        if core_config == core_space[config_id]:
            core_arm = config_id
            break
    print(f'core_config:{core_config}')

    if nof_llc != 0:
        llc_config = split_averagely(nof_units=nof_llc, nof_clusters=app_num)
        print(f'llc_config:{llc_config}')
    for config_id in range(len(llc_space)):
        if llc_config == llc_space[config_id]:
            llc_arm = config_id
            break

    if nof_mb != 0:
        mb_config = split_averagely(nof_units=nof_mb, nof_clusters=app_num)
        print(f'mb_config:{mb_config}')
    for config_id in range(len(mb_space)):
        if mb_config == mb_space[config_id]:
            mb_arm = config_id
            break

    if nof_llc != 0 and nof_mb != 0:
        return core_config, llc_config, mb_config, core_arm, llc_arm, mb_arm
    else:
        return core_config, core_arm

def split_averagely(nof_units:int, nof_clusters:int) -> List[int]:
    each_clu_units = nof_units // nof_clusters
    res_clu_units = nof_units % nof_clusters
    units_clu = [each_clu_units] * (nof_clusters-1)
    if res_clu_units >= each_clu_units:
        for i in range(res_clu_units):
            units_clu[i]+=1
        units_clu.append(each_clu_units)
    else:
        units_clu.append(each_clu_units+res_clu_units)
    return units_clu

# def group2app_allocation(g_core_allocation_list:List[str], g_llc_allocation_list:List[str], g_mb_allocation_list:List[int],
#                          group_list:List[List[str]], app_list:List[str]) -> Tuple[List[str], List[str], List[str]]:
#     """
#     将面对group的allocation格式转为面向单个app的allocation格式
#     """
#     core_allocation_list = []
#     llc_allocation_list = []
#     mb_allocation_list = []
#     for app in app_list:
#         for g in range(len(group_list)):
#             if app in group_list[g]:
#                 core_allocation_list.append(g_core_allocation_list[g])
#                 llc_allocation_list.append(g_llc_allocation_list[g])
#                 mb_allocation_list.append(g_mb_allocation_list[g])
#                 break
#     return core_allocation_list, llc_allocation_list, mb_allocation_list

# def config2allocation(core_unit_scale:int, core_config:List[int], llc_config:List[int], mb_config:List[int],
#                     group_list:List[List[str]], app_list:List[str]) -> Tuple[List[str], List[str], List[str]]:
#     """
#     将面向group的config格式，处理再refer成面向单个app的allocation格式
#     """
    
#     g_core_allocation_list = refer_core(core_config=core_config, unit_scale=core_unit_scale)
#     g_llc_allocation_list = refer_llc(llc_config=llc_config)
#     g_mb_allocation_list = refer_mb(mb_config=mb_config)
#     core_allocation_list, llc_allocation_list, mb_allocation_list = \
#     group2app_allocation(g_core_allocation_list, g_llc_allocation_list, g_mb_allocation_list,
#                          group_list=group_list, app_list=app_list)
def group2app_allocation(g_llc_allocation_list:List[str], g_mb_allocation_list:List[int],
                         group_list:List[List[str]], app_list:List[str]) -> Tuple[List[str], List[str], List[str]]:
    """
    将面对group的allocation格式转为面向单个app的allocation格式
    """
    llc_allocation_list = []
    mb_allocation_list = []
    for app in app_list:
        for g in range(len(group_list)):
            if app in group_list[g]:
                llc_allocation_list.append(g_llc_allocation_list[g])
                mb_allocation_list.append(g_mb_allocation_list[g])
                break
    return llc_allocation_list, mb_allocation_list

def config2allocation(core_unit_scale:int, core_config:List[int], llc_config:List[int], mb_config:List[int],
                    group_list:List[List[str]], app_list:List[str], num_llc:int) -> Tuple[List[str], List[str], List[str]]:
    """
    将面向group的config格式，处理再refer成面向单个app的allocation格式
    """
    # group内部core平分
    g_aver_core_config = []; aver_core_config = []
    core_config = [c * core_unit_scale for c in core_config]
    for c in range(len(core_config)):
        each_core_config = core_config[c] // len(group_list[c])
        res_core_config = core_config[c] % len(group_list[c])
        c_core_config = [each_core_config] * (len(group_list[c])-1)
        if res_core_config >= each_core_config:
            for i in range(res_core_config):
                c_core_config[i]+=1
            c_core_config.append(each_core_config)
        else:
            c_core_config.append(each_core_config+res_core_config)
        g_aver_core_config.append(c_core_config)
    for app in app_list:
        for g in range(len(group_list)):
            for a in range(len(group_list[g])):
                if app == group_list[g][a]:
                    aver_core_config.append(g_aver_core_config[g][a])
                    
    core_allocation_list = refer_core(core_config=aver_core_config)
    
    g_llc_allocation_list = refer_llc(llc_config=llc_config, num_llc=num_llc)
    g_mb_allocation_list = refer_mb(mb_config=mb_config)
    # llc_allocation_list, mb_allocation_list = \
    # group2app_allocation(g_llc_allocation_list, g_mb_allocation_list,
    #                      group_list=group_list, app_list=app_list)

    return core_allocation_list, g_llc_allocation_list, g_mb_allocation_list



def app2group_ips_list(ips_list:List[float], group_list:List[List[str]], app_list:List[str]) -> List[float]:
    """
    将获取的单个app的ips_list，转为group的ips_list(准确说是reward)
    """
    group_ips_list = []
    for group in group_list:
        g_ips = []
        for i in range(len(app_list)):
            if app_list[i] in group:
                g_ips.append(ips_list[i])
        group_ips_list.append(gmean(g_ips))
    return group_ips_list

def sort_group_configs(nonsort_all_core_config:List[List[int]], group_list:List[List[str]], app_list:List[str])\
                       -> Tuple[List[int], List[str]]:
    """
    已经获取到各个group的config，拼接起来使之符合app_list排序，并转为allocation命令
    """
    all_core_config = []
    for app in app_list:
        for g in range(len(group_list)):
            for a in range(len(group_list[g])):
                if group_list[g][a] == app:
                    all_core_config.append(nonsort_all_core_config[g][a])
    all_core_allocation_list = refer_core(all_core_config)
    return all_core_config, all_core_allocation_list

def ips2greward(ips_list:List[float], group_list:List[List[str]], app_list:List[str]) \
                -> Tuple[List[float], List[List[float]]]:
    """
    将获得的所有ips，分别计算每个group的reward，以及组合成各个group的ips_list
    """
    group_reward = []
    group_ips_lists = []
    for group in group_list:
        ips = []
        g_ips_list = []
        for g_app in group:
            for a in range(len(app_list)):
                if g_app == app_list[a]:
                    ips.append(ips_list[a])
                    g_ips_list.append(ips_list[a])
        group_reward.append(gmean(ips))
        group_ips_lists.append(g_ips_list)
    return group_reward, group_ips_lists

# NUM_CORES = 80
# def refer_core(core_config:List[int], unit_scale:int = 1) -> List[str]:    # len(core_config) = NUM_APPS
#     """
#     translate core config to core command, [2,4,3] => ["0,1","2,3,4,5","6,7,8"]
#     input: core config list
#     output: core command list
#     """
#     socket_core = int(NUM_CORES / 2)
#     core_config = [c * unit_scale for c in core_config]
#     core_allocation_list = [""] * len(core_config)
#     endpoint_left = 0
#     for i in range(len(core_config)):
#         endpoint_right = endpoint_left + core_config[i] - 1
#         core_list = list(range(endpoint_left, endpoint_right+1))
#         # 物理核0：0~27，56~83
#         # 物理核1：28~55，84~111
#         for j in range(len(core_list)):
#             if core_list[j] < socket_core:
#                 if core_list[j] > 27:
#                     core_list[j] += 28
#                 else:
#                     core_list[j] += 0
#             else:
#                 core_list[j] = core_list[j] - socket_core + 28
#                 if core_list[j] > 28 + 27:
#                     core_list[j] += 28
#                 else:
#                     core_list[j] += 0
#         core_allocation_list[i] = ",".join([str(c) for c in core_list])
#         endpoint_left = endpoint_right + 1
#     return core_allocation_list
