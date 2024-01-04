import os
import hashlib

def get_file_md5(file_path):
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(8192)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()

def find_duplicate_files(directory):
    file_name_dict = {}

    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            if filename in file_name_dict:
                file_name_dict[filename].append(file_path)
            else:
                file_name_dict[filename] = [file_path]

    duplicate_files = {}

    for filename, file_paths in file_name_dict.items():
        if len(file_paths) > 1:
            md5_set = set()
            for file_path in file_paths:
                md5 = get_file_md5(file_path)
                md5_set.add(md5)
            if len(md5_set) == 1:
                duplicate_files[filename] = file_paths

    return duplicate_files

def print_duplicate_files(duplicate_files):
    for filename, file_paths in duplicate_files.items():
        print(f'文件名: {filename}')
        for file_path in file_paths:
            print(f'  - {file_path}')

if __name__ == "__main__":
    target_directory = "/run/media/dahai003/download/qbt/"
    duplicate_files = find_duplicate_files(target_directory)

    if duplicate_files:
        print("以下文件具有相同的文件名和相同的MD5哈希值：")
        print_duplicate_files(duplicate_files)
    else:
        print("没有找到具有相同文件名和相同MD5哈希值的文件。")
