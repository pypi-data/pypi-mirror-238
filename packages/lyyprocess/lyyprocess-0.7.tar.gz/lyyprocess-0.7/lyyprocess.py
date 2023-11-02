import psutil
import socket
import subprocess
import time





def if_set_include_list_element(all_set, task_dict):
    """
    判断要检查的程序（在字典中的元素）是否被包含在全体进程集合中，从而不管是否子进程，都能正确找到。

    """
    print("all_set length=", len(all_set))
    result_dict = {}
    for item in all_set:
        found = False  # 标记是否找到匹配的任务
        for task in task_dict.keys():
            if task in item:
                result_dict[task] = True
                found = True
                break  # 只跳出当前的内部循环
        if found:
            continue  # 继续下一个外部循环
    return result_dict


def get_all_process_with_child():
    """
    获取当前运行的所有进程及子进程名字，存入集合中。
    """
    all_set = set()
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            proc_info = proc.as_dict(attrs=['pid', 'name'])
            process_name = proc_info['name'].lower()
            all_set.add(process_name)
            print("+", end="", flush=True)
            child_procs = psutil.Process(proc_info['pid']).children(recursive=True)
            for child_proc in child_procs:
                child_proc_info = child_proc.as_dict(attrs=['pid', 'name'])
                child_process_name = child_proc_info['name'].lower()
                all_set.add(child_process_name)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return all_set


def get_all_process_hwnd_dict():
    """
    获取当前运行的所有进程及子进程名字，存入字典中。
    """
    hwnd_dict = {}
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            proc_info = proc.as_dict(attrs=['pid', 'name'])
            process_name = proc_info['name'].lower()

            if process_name not in hwnd_dict.keys():
                hwnd_dict[process_name] = proc_info['pid']

            print("+", end="", flush=True)
            child_procs = psutil.Process(proc_info['pid']).children(recursive=True)
            for child_proc in child_procs:
                child_proc_info = child_proc.as_dict(attrs=['pid', 'name'])
                child_process_name = child_proc_info['name'].lower()
                if child_process_name not in hwnd_dict.keys():
                    hwnd_dict[child_process_name] = proc_info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return hwnd_dict

def check_processes(task_dict):
    """
    检查指定的进程是否在运行，如果没有运行，打印出来，并返回。用来通知哪些没运行。
    """
    print("enter check_processes, try to find name in all process and child process")
    false_list = []
    all_set = get_all_process_with_child()
    result_dict = if_set_include_list_element(all_set, task_dict)
    print("result_dict", result_dict)
    false_keys = [key for key in task_dict.keys() if key not in result_dict.keys()]
    print("false_keys", false_keys)
    if false_keys:
        print(" 和 ".join(false_keys) + "未运行", "请及时检查")
    false_list = [x for x in false_keys if x in task_dict.keys()]
    return false_keys


def check_port_in_use(port):
    # 检查指定端口是否被占用
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
        except OSError:
            print("# 端口被占用，查找占用端口的进程")
            for conn in psutil.net_connections():
                if conn.status == "LISTEN" and conn.laddr.port == port:
                    pid = conn.pid
                    process = psutil.Process(pid)
                    print(f"# 占用端口的进程名：{process.name()}，进程路径：{process.exe()}")
                    return process.name(), process.exe()
    return None, None


def terminate_process_using_port(port):
    try:
        command = f"netstat -ano | findstr :{port}"
        output = subprocess.check_output(command, shell=True, text=True)
        lines = output.strip().split("\n")
        for line in lines:
            parts = line.split()
            pid = int(parts[-1])
            subprocess.run(["taskkill", "/F", "/PID", str(pid)])
        print("已结束占用该端口的程序")
        return pid
    except (subprocess.CalledProcessError, ValueError) as e:
        print(f"结束占用该端口的程序时出现错误：{e}")
        return None


def run_with_error_handling(func):
    try:
        func()
    except Exception as e:
        # 处理异常，可以打印日志或执行其他操作
        print(f"模块 {func.__name__} 出现异常: {e}")


def get_child_process_number(parent_name="JY-Main.exe", debug=False):
    parent_pid = None
    # 查找主进程
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        process_info = process.info
        if parent_name.lower() in process_info['name'].lower():
            parent_pid = process_info['pid']
            break
        elif debug:
            print(process_info['name'])

    if parent_pid is None:
        print(f"没有找到名为 {parent_name} 的进程")
        return 0
    #print(f"找到名为 {parent_name} 的进程，其PID为 {parent_pid}")
    parent = psutil.Process(parent_pid)
    # 列举子进程
    children = parent.children()
    if children:
        for child in children:
            print(f"  PID: {child.pid}, 名称: {child.name()}")
    # 列举子线程


    # if main_thread:
    #     for thread_id, thread_obj in threading._active.items():
    #         if thread_obj.ident != main_thread.ident:
    #             #print(f"  Thread ID: {thread_obj.ident}")
    print("子线程数量为：", len(children))
    return len(children)


def get_hwnd(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            proc_info = proc.as_dict(attrs=['pid', 'name'])
            if process_name.lower() in proc_info['name'].lower():
                return proc_info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


def set_window_on_top(process):
    if process is not None:
        process.nice(psutil.HIGH_PRIORITY_CLASS)
        print(f"已将进程 {process.pid} 置顶")
    else:
        print("未找到名为 'kingtrade' 的进程")


# 示例：将窗口句柄为12345的窗口放在最上层
import win32gui, win32con


def set_window_top(hwnd):
    print(hwnd)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)


# 获取指定句柄的窗口标题
def get_window_title(hwnd):
    return win32gui.GetWindowText(hwnd)


# 根据窗口标题找到句柄，并置顶窗口
def find_and_set_top_window(title):
    #当前看起来不生效。不得不用pywinauto
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and title in get_window_title(hwnd):
            set_window_top(hwnd)

    win32gui.EnumWindows(callback, None)


if __name__ == '__main__':
    print(check_port_in_use(3306))

    exit()
    task_dict = {'jiepan': 'D:/Soft/_lyytools/_jiepan/_jiepan.exe', 'gui-only': 'D:/Soft/_lyytools/gui-only/gui-only.exe', 'kingtrader': 'D:/Soft/_Stock/KTPro/A.点我登录.exe'}
    stopped = check_processes(task_dict)
    print("stopped=", stopped)
