import psutil
import subprocess

def list_processes(sort_by=None, filter_name=None):
    procs = []
    for p in psutil.process_iter(["pid","name","username","cpu_percent","memory_info","status","exe"]):
        try:
            info = p.info
            name = info.get("name") or ""
            if filter_name and filter_name.lower() not in name.lower():
                continue
            procs.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    if sort_by == "cpu":
        procs.sort(key=lambda x: x.get("cpu_percent", 0), reverse=True)
    elif sort_by == "ram":
        procs.sort(key=lambda x: x.get("memory_info").rss if x.get("memory_info") else 0, reverse=True)
    return procs

def kill_process_safe(pids):
    if isinstance(pids, int):
        pids = [pids]
    success = []
    fail = []
    for pid in pids:
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            proc.wait(timeout=5)
            success.append(pid)
        except psutil.NoSuchProcess:
            fail.append(pid)
        except psutil.AccessDenied:
            fail.append(pid)
        except Exception:
            fail.append(pid)
    return success, fail

def run_command(commands):
    if isinstance(commands, str):
        cmds = [c.strip() for c in commands.split(";") if c.strip()]
    else:
        cmds = list(commands)
    outputs = []
    for c in cmds:
        try:
            r = subprocess.run(c, shell=True, capture_output=True, text=True, timeout=60)
            out = r.stdout.strip() if r.stdout else (r.stderr.strip() if r.stderr else "")
        except Exception as e:
            out = str(e)
        outputs.append(f"$ {c}\n{out}")
    return "\n\n".join(outputs)
