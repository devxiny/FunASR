import os
import uuid


def list_files(directory, file_format=None):
    files_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file_format is None or file.endswith(file_format):
                files_list.append(os.path.join(root, file))
    return files_list


def generate_random_id():
    return str(uuid.uuid4())


def write_strings_with_ids(id, text, file_path):
    with open(file_path, 'a') as file:
        file.write(f"{id} {text}\n")


def remove_file_extension(file_path):
    file_name = os.path.basename(file_path)
    file_name_without_extension = os.path.splitext(file_name)[0]
    return file_name_without_extension


if __name__ == '__main__':
    directory_path = 'C:\\Users\\devxiny\\Documents\\Audacity'
    all_files = list_files(directory_path, 'wav')
    for file in all_files:
        id = generate_random_id()
        write_strings_with_ids(id, remove_file_extension(
            file), directory_path+'\\train.txt')
        write_strings_with_ids(id, file, directory_path+'\\train.scp')
