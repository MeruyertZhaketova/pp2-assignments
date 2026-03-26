import os

# создаем вложенные папки
os.makedirs("test_dir/sub_dir", exist_ok=True)

# список файлов
files = os.listdir(".")
print(files)