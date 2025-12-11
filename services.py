import subprocess

def service_exists(service):
    try:
        r = subprocess.run(["systemctl", "status", service], capture_output=True, text=True)
        return r.returncode == 0 or "Loaded: loaded" in r.stdout
    except Exception:
        return False

def service_action(service, action):
    if not service_exists(service):
        return False, f"Service '{service}' not found."
    try:
        r = subprocess.run(["systemctl", action, service], capture_output=True, text=True, timeout=20)
        out = r.stdout.strip() or r.stderr.strip()
        code = r.returncode
        if code == 0:
            return True, f"{action.capitalize()} succeeded: {service}"
        return False, f"{action.capitalize()} failed: {service}. {out}"
    except Exception as e:
        return False, str(e)

def service_status(service):
    if not service_exists(service):
        return False, f"Service '{service}' not found."
    try:
        r = subprocess.run(["systemctl", "status", service, "--no-pager"], capture_output=True, text=True, timeout=20)
        out = r.stdout.strip() or r.stderr.strip()
        return True, out
    except Exception as e:
        return False, str(e)
