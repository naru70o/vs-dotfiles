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
commit = input("Wanna commit, yes(Y) or No(N): ").lower().strip()

if system == "Linux":
    config_dir = home / ".config/Code/User"
    print("supppppppppp")
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
elif system == "Windows":
    config_dir = home / "AppData/Roaming/Code/User"
    if config_dir.exists():
        for filename in files_to_sync:
            if user_choice == "restore":
                source = current_folder / filename
                destination = config_dir / filename
            elif user_choice == "backup":
                source = config_dir / filename 
                destination = current_folder / filename
            elif user_choice == "skip":
                break
            else:
                print("Invalid choice!")
                break
            if source.exists():
                if source.is_dir():
                    shutil.copytree(source, destination, dirs_exist_ok=True)
                    print(f"Successfully {user_choice}ed {filename}")
                else:
                    shutil.copy2(source, destination)
                    print(f"Successfully {user_choice}ed {filename}")
            else:
                print(f"Error: {filename} not found!")
    else: print("Error: VS Code config directory not found!, Please install vscode if it's not already installed")

# make the commit input all lowercase
if user_choice == "backup" or user_choice == "skip" and (commit == "yes" or commit == "y"):
    commit_message = input("Please put your commit message here: ")
    subprocess.run(["git", "add", "."], cwd=current_folder)
    subprocess.run(["git", "commit", "-m", commit_message], cwd=current_folder, check=True)
    subprocess.run(["git", "push", "origin", "master"], cwd=current_folder)
