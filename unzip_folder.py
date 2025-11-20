import zipfile
import os


zip_path = r"/home/noe_ee/GradProject/detect (1).zip"
new_folder_path = r"/home/noe_ee/GradProject/data_folder"

os.makedirs(new_folder_path, exist_ok=True)

with zipfile.ZipFile(zip_path, "r") as z:
    z.extractall(new_folder_path)

print(f"Zip file extracted to: {new_folder_path}")