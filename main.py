from backup import create_backup
from system_tasks import list_processes, kill_process_safe, run_command
from services import service_action, service_status
from monitor import snapshot
from reports import log_backup, log_kill, log_command, log_service, log_monitor
from dashboard import show_dashboard
from colorama import init, Fore, Style
import os

init(autoreset=True)

def print_header():
    print(Fore.CYAN + Style.BRIGHT + "\n===== Linux Automation =====\n")

def safe_input(prompt):
    try:
        return input(prompt).strip()
    except KeyboardInterrupt:
        print(Fore.RED + "\nKeyboardInterrupt detected. Returning to main menu.")
        return "menu"

def backup_menu():
    while True:
        print("\n1. Create Backup")
        print("2. Return to Main Menu\n")
        sub = safe_input("Select an option: ")
        if sub == "2" or sub == "menu":
            return
        if sub != "1":
            print(Fore.RED + "Invalid option.")
            continue
        srcs = safe_input("Enter source folder(s) separated by comma: ").split(",")
        srcs = [s.strip() for s in srcs if s.strip()]
        dst = safe_input("Enter backup folder path: ").strip()
        z = safe_input("Create zip backup? (y/n): ").lower()
        total = sum(len(files) for s in srcs if os.path.exists(s) for _,_,files in os.walk(s))
        print(Fore.MAGENTA + f"Total files to back up: {total}")
        c = safe_input("Proceed? (y/n): ").lower()
        if c != "y":
            print(Fore.RED + "Backup cancelled.")
            return
        ok, msg = create_backup(srcs, dst, zip_backup=(z=="y"))
        print(Fore.MAGENTA + msg)
        log_backup(msg)

def processes_menu():
    while True:
        print("\n1. List Processes")
        print("2. Return to Main Menu\n")
        sub = safe_input("Select an option: ")
        if sub == "2" or sub == "menu":
            return
        if sub != "1":
            print(Fore.RED + "Invalid option.")
            continue
        sort = safe_input("Sort by cpu / ram / none: ").lower()
        filt = safe_input("Filter by name (optional): ").strip()
        procs = list_processes(sort_by=sort if sort in ["cpu","ram"] else None, filter_name=filt if filt else None)
        print(Fore.BLUE + f"\n{'PID':<8}{'Name':<20}{'User':<15}{'CPU%':<8}{'RAM(MB)':<10}{'Status':<10}{'Path'}")
        for p in procs:
            mem = p["memory_info"].rss / (1024*1024)
            path = p["exe"] if p["exe"] else ""
            print(Fore.BLUE + f"{p['pid']:<8}{p['name'][:20]:<20}{p['username']:<15}{p['cpu_percent']:<8}{mem:.2f}{p['status']:<10}{path}")

def kill_menu():
    while True:
        print("\n1. Kill Process")
        print("2. Return to Main Menu\n")
        sub = safe_input("Select an option: ")
        if sub == "2" or sub == "menu":
            return
        if sub != "1":
            print(Fore.RED + "Invalid option.")
            continue
        pids = safe_input("Enter PID(s) separated by space: ").split()
        pids = [int(x) for x in pids if x.isdigit()]
        if not pids:
            print(Fore.RED + "No valid PIDs.")
            continue
        c = safe_input(f"Kill these PIDs {pids}? (y/n): ").lower()
        if c != "y":
            print(Fore.RED + "Cancelled.")
            return
        suc, fail = kill_process_safe(pids)
        print(Fore.RED + f"Success: {suc} | Failed: {fail}")
        log_kill(pids, suc, fail)

def command_menu():
    while True:
        print("\n1. Run Command")
        print("2. Return to Main Menu\n")
        sub = safe_input("Select an option: ")
        if sub == "2" or sub == "menu":
            return
        if sub != "1":
            print(Fore.RED + "Invalid option.")
            continue
        cmds = safe_input("Enter command(s) separated by ';': ")
        out = run_command(cmds)
        print(Fore.GREEN + out)
        log_command(cmds, out)

def services_menu():
    while True:
        print("\n1. Manage a service")
        print("2. Return to Main Menu\n")
        sub = safe_input("Select an option: ")
        if sub == "2" or sub == "menu":
            return
        if sub != "1":
            print(Fore.RED + "Invalid option.")
            continue
        svc = safe_input("Enter service name (systemd): ").strip()
        print("\n1. Start")
        print("2. Stop")
        print("3. Restart")
        print("4. Status")
        print("5. Return to Previous Menu\n")
        act = safe_input("Select an action: ")
        if act == "5" or act == "menu":
            continue
        actions = {"1":"start","2":"stop","3":"restart","4":"status"}
        if act not in actions:
            print(Fore.RED + "Invalid action.")
            continue
        action = actions[act]
        if action == "status":
            ok, res = service_status(svc)
            print(Fore.GREEN if ok else Fore.RED + res)
            log_service(action, svc, res)
        else:
            ok, res = service_action(svc, action)
            print(Fore.GREEN if ok else Fore.RED + res)
            log_service(action, svc, res)

def monitor_menu():
    while True:
        print("\n1. Show System Snapshot")
        print("2. Return to Main Menu\n")
        sub = safe_input("Select an option: ")
        if sub == "2" or sub == "menu":
            return
        if sub != "1":
            print(Fore.RED + "Invalid option.")
            continue
        snap = snapshot()
        print(Fore.CYAN + f"\nTime: {snap['time']}")
        print(Fore.CYAN + f"CPU: {snap['cpu_percent']}%")
        print(Fore.CYAN + f"Memory: {snap['mem_used_mb']}/{snap['mem_total_mb']} MB ({snap['mem_percent']}%)")
        print(Fore.CYAN + f"Swap used: {snap['swap_used_mb']} MB")
        print(Fore.CYAN + f"Disk: {snap['disk_used_gb']}/{snap['disk_total_gb']} GB ({snap['disk_percent']}%)")
        print(Fore.CYAN + f"Network sent: {snap['net_bytes_sent']} bytes, recv: {snap['net_bytes_recv']} bytes")
        log_monitor(snap)

def main_menu():
    while True:
        print_header()
        print(Fore.GREEN + "1. Backup Folder")
        print(Fore.GREEN + "2. List Processes")
        print(Fore.GREEN + "3. Kill Process")
        print(Fore.GREEN + "4. Run Command")
        print(Fore.GREEN + "5. Services")
        print(Fore.GREEN + "6. System Monitor")
        print(Fore.GREEN + "7. Dashboard")
        print(Fore.GREEN + "8. Exit")
        choice = safe_input(Fore.YELLOW + "Select an option: ")
        if choice == "1":
            backup_menu()
        elif choice == "2":
            processes_menu()
        elif choice == "3":
            kill_menu()
        elif choice == "4":
            command_menu()
        elif choice == "5":
            services_menu()
        elif choice == "6":
            monitor_menu()
        elif choice == "7":
            show_dashboard()
        elif choice == "8":
            print(Fore.CYAN + "Exiting...")
            break
        else:
            print(Fore.RED + "Invalid option.")

if __name__ == "__main__":
    main_menu()
