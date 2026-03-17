from pathlib import Path
import platform
import shutil
import subprocess

system = platform.system()
home = Path.home()
files_to_sync = ["settings.json","snippets"]
user_choice = input("Do you want to 'backup' or 'restore' ?")
print(home)
current_folder = Path.cwd()
commit_message=input("Please put your commit message here: ")

if system == "Linux":
    config_dir = home / ".config/Code/User"
    
    # 1. Check if the source folder exists FIRST
    if config_dir.exists():
        
        # 2. Now start sync 
        for filename in files_to_sync:
            if user_choice == "restore":
                source = current_folder / filename
                destination = config_dir / filename
            elif user_choice == "backup":
                source = config_dir / filename 
                destination = current_folder / filename
            else:
                print("Invalid choice!")
                break
        if source.exists():
            if source.is_dir():
                shutil.copytree(source, destination, dirs_exist_ok=True)
            else:
                shutil.copy2(source, destination)
                print(f"Successfully {user_choice}ed {filename}")
    else: print("Error: VS Code config directory not found!, Please install vscode if it's not already installed")
print(input)
status = subprocess.run(["git", "status"], cwd=current_folder)
subprocess.run(["git", "add", "."],cwd=current_folder)
subprocess.run(["git", "commit", "-m", f"{commit_message}"], cwd=current_folder, check=True)
subprocess.run(["git", "push", "origin", "master"], cwd=current_folder)
