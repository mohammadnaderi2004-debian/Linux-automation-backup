from datetime import datetime
import csv
import os

backup_history = []
kill_history = []
command_history = []
service_history = []
monitor_history = []

def log_backup(msg):
    t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{t}] {msg}"
    backup_history.append(entry)
    _append_txt("backup_log.txt", entry)

def log_kill(pids, success, fail):
    t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for pid in success:
        entry = f"[{t}] PID:{pid} Result:Success"
        kill_history.append(entry)
        _append_txt("kill_log.txt", entry)
    for pid in fail:
        entry = f"[{t}] PID:{pid} Result:Failed"
        kill_history.append(entry)
        _append_txt("kill_log.txt", entry)

def log_command(cmds, output):
    t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{t}] Command: {cmds}\n{output}"
    command_history.append(entry)
    _append_txt("command_log.txt", entry)

def log_service(action, service, result):
    t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{t}] Service:{service} Action:{action} Result:{result}"
    service_history.append(entry)
    _append_txt("service_log.txt", entry)

def log_monitor(snapshot):
    t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{t}] {snapshot}"
    monitor_history.append(entry)
    _append_txt("monitor_log.txt", entry)

def _append_txt(filename, entry):
    try:
        os.makedirs("logs", exist_ok=True)
        path = os.path.join("logs", filename)
        with open(path, "a") as f:
            f.write(entry + "\n")
    except Exception:
        pass

def export_csv(list_name, filename):
    try:
        os.makedirs("logs", exist_ok=True)
        path = os.path.join("logs", filename)
        data = globals().get(list_name, [])
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            for line in data:
                writer.writerow([line])
        return True, path
    except Exception as e:
        return False, str(e)
