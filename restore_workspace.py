import os
import shutil

def main():
    archive_dir = os.path.abspath(os.path.join(os.getcwd(), "..", "robertpelloni"))
    workspace_root = os.getcwd()
    
    if not os.path.exists(archive_dir):
        print("Archive dir does not exist.")
        return

    items = os.listdir(archive_dir)
    for item in items:
        item_path = os.path.join(archive_dir, item)
        target_path = os.path.join(workspace_root, item)
        
        if os.path.exists(target_path):
             print(f"Target {target_path} already exists. Skipping.")
             continue
             
        print(f"Moving {item} back to workspace...")
        try:
            shutil.move(item_path, target_path)
        except Exception as e:
            print(f"  Failed to move {item}: {e}")

if __name__ == "__main__":
    main()
