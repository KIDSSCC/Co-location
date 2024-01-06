import subprocess
par_path = '/home/md/NPB3.3.1/NPB3.3-OMP/bin/'


def run_process(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return process

def get_result(all_command, itea=0, type='align'):
    for name, process in all_command.items():
        stdout, _ = process.communicate()
        stdout=stdout.split('\n')
        for line in stdout:
            if 'Time in seconds' in line:
                print('itea {}, {} type, {} '.format(itea+1, type, name + line))
                break
        '''
        if name == 'App_1':
            # 再运行一遍app_1
            stdout, stderr  = run_process(command_1).communicate()
            stdout=stdout.split('\n')
            for line in stdout:
                if 'Time in seconds' in line:
                    print(name + line)
                    break
        '''            

def get_process_result(process):
    stdout, _ = process.communicate()
    stdout=stdout.split('\n')
    for line in stdout:
        if 'Time in seconds' in line:
            return line


def run_app_alone(app_name):
    print('Run {} alone '.format(app_name))
    command_1 = 'taskset -c 14-17 ' + par_path + app_name
    command_2 = 'taskset -c 14,15,42,43 ' + par_path + app_name
    for i in range(3):
        print('itea {}, align result is:{}'.format(i+1, get_process_result(run_process(command_1))))
        print('itea {}, non-align result is:{}'.format(i+1, get_process_result(run_process(command_2))))

def run_app_together(app_name):
    print('Run {} together '.format(app_name))
    command_1 = 'taskset -c 14-17 ' + par_path + app_name
    command_2 = 'taskset -c 42-45 ' + par_path + app_name

    command_3 = 'taskset -c 14,15,42,43 ' + par_path + app_name
    command_4 = 'taskset -c 20,21,48,49 ' + par_path + app_name
    for i in range(2):
        alignment = {}
        alignment['App_1']=run_process(command_1)
        alignment['App_2']=run_process(command_2)
        get_result(alignment, i, 'align')
        out_alignment = {}
        out_alignment['App_1']=run_process(command_3)
        out_alignment['App_2']=run_process(command_4)
        get_result(out_alignment, i, 'out_align')

if __name__ == '__main__':
    # apps = ['ep.C.4', 'mg.C.4', 'cg.C.4', 'ft.C.4', 'is.D.4']
    apps = ['ep.C.x', 'mg.C.x', 'cg.C.x', 'ft.C.x', 'is.D.x']
    # apps = ['is.C.x']
    for app in apps:
        run_app_alone(app)
        run_app_together(app)
        print('')