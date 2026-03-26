import shutil
import os

# copying
shutil.copy("sample.txt", "backup.txt")

# deleting
if os.path.exists("backup.txt"):
    os.remove("backup.txt")
    print("File deleted")
else:
    print("File not found")