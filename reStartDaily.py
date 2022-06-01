import os, subprocess
from server2user.logout import logout


# 1.获取指定进程的pid
def getPid(procName, *args):

    # 接参,拼接指令
    parameter = [procName]
    for key in args:
        parameter.append(key)
    inst = "ps -ef"
    for para in parameter:
        inst = inst + " | grep " + para
    logout("reStartDaily", f"执行指令：{inst}")
    proc = os.popen(inst)

    # os.popen执行linux-ps命令会把命令本身进程一起输出，所以过滤处理
    pid = proc.readlines()
    index = 0
    for output in pid:
        if "grep" in output:
            break
        index += 1
    pid.pop(index)
    logout("reStartDaily", f"指令<{inst}>返回：{pid}")

    # 返回进程pid
    if len(pid) == 0:
        return
    return pid[0][9:14].replace(" ", "")


# 2.杀掉指定pid的进程
def killPid(pid):
    if pid is None:
        return 
    subprocess.call(["kill", "-9", pid])


# 3.启动程序
def startProc(proc):
    try:
        if proc not in ["recheck", "schedule"]:
            raise ValueError("参数错误")
    except Exception as e:
        return
    subprocess.Popen(f"nohup python proxyPool.py {proc}&", bufsize=0, shell=True)
    logout("reStartDaily", f"proxyPool-{proc} 程序启动成功！")


# 0.主程序
def main(proc):
    killPid(getPid("python", proc))
    startProc(proc)
    getPid(proc)


if __name__ == '__main__':
    main("schedule")
    main("recheck")
    print("#"*50)
    print("\n")