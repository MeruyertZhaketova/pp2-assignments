import shutil
import os

# creating folder
os.makedirs("destination", exist_ok=True)

# moving folder
if os.path.exists("sample.txt"):
    shutil.move("sample.txt", "destination/sample.txt")