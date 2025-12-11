import psutil
from datetime import datetime

def snapshot():
    cpu = psutil.cpu_percent(interval=0.5)
    v = psutil.virtual_memory()
    swap = psutil.swap_memory()
    disks = psutil.disk_usage('/')
    net = psutil.net_io_counters()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "time": now,
        "cpu_percent": cpu,
        "mem_total_mb": v.total // (1024*1024),
        "mem_used_mb": v.used // (1024*1024),
        "mem_percent": v.percent,
        "swap_used_mb": swap.used // (1024*1024),
        "disk_total_gb": disks.total // (1024*1024*1024),
        "disk_used_gb": disks.used // (1024*1024*1024),
        "disk_percent": disks.percent,
        "net_bytes_sent": net.bytes_sent,
        "net_bytes_recv": net.bytes_recv
    }
