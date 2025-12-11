import os
import zipfile
from datetime import datetime
import shutil

def create_backup(sources, destination, zip_backup=True):
    if isinstance(sources, str):
        sources = [sources]
    os.makedirs(destination, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    try:
        if zip_backup:
            zip_path = os.path.join(destination, f"backup_{timestamp}.zip")
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for source in sources:
                    if not os.path.exists(source):
                        continue
                    base = os.path.basename(source.rstrip(os.sep)) or os.path.basename(os.path.abspath(source))
                    for root, _, files in os.walk(source):
                        for file in files:
                            full = os.path.join(root, file)
                            arc = os.path.join(base, os.path.relpath(full, source))
                            zipf.write(full, arc)
            return True, f"Backup created at {zip_path}"
        else:
            for source in sources:
                if not os.path.exists(source):
                    continue
                dest = os.path.join(destination, f"{os.path.basename(source.rstrip(os.sep))}_{timestamp}")
                shutil.copytree(source, dest)
            return True, f"Backup copied to {destination}"
    except Exception as e:
        return False, str(e)
