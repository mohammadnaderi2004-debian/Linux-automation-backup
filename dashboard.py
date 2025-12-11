from colorama import Fore, Style
from reports import backup_history, kill_history, command_history, service_history, monitor_history

def show_dashboard():
    print(Fore.CYAN + Style.BRIGHT + "\n===== DASHBOARD =====\n")
    
    print(Fore.GREEN + "Backup History:")
    if backup_history:
        for e in backup_history[-10:]:
            print(Fore.GREEN + e)
    else:
        print(Fore.GREEN + "No backup records.")
    print()
    
    print(Fore.YELLOW + "Kill History:")
    if kill_history:
        for e in kill_history[-10:]:
            print(Fore.YELLOW + e)
    else:
        print(Fore.YELLOW + "No kill records.")
    print()
    
    print(Fore.MAGENTA + "Command History:")
    if command_history:
        for e in command_history[-10:]:
            print(Fore.MAGENTA + e.splitlines()[0])
    else:
        print(Fore.MAGENTA + "No command records.")
    print()
    
    print(Fore.BLUE + "Service History:")
    if service_history:
        for e in service_history[-10:]:
            print(Fore.BLUE + e)
    else:
        print(Fore.BLUE + "No service records.")
    print()
    
    print(Fore.CYAN + "Monitor History:")
    if monitor_history:
        for e in monitor_history[-5:]:
            print(Fore.CYAN + e)
    else:
        print(Fore.CYAN + "No monitor records.")
    print()
