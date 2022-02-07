import os, re, shutil, sys

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANS = {}
TRANSLATION = (
    "a", "b", "v", "g", "d", "e", "e", "j",
    "z", "i", "j", "k", "l", "m", "n", "o",
    "p", "r", "s", "t", "u", "f", "h", "ts",
    "ch", "sh", "sch", "", "y", "", "e", "yu",
    "u", "ja", "je", "ji", "g"
    )

    
dict_extensions = {

    'image': ['jpg', 'png', 'jpeg','svg'],

    'video': ['avi', 'mp4' 'mov', 'mkv'],

    'documents': ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],

    'audio': ['mp3', 'ogg', 'wav', 'amr'],

    'archive': ['zip', 'gz', 'tar'],
    
    'other': []
    
    }

list_known_exten = []
list_unknown_exten = []

def get_list_files(path):

    list_of_files = []
    
    for i in os.walk(path):
        list_of_files.append(i)
        
    return list_of_files


def delete_ds_store_only_for_mac(adress, file):

    file_path = os.path.join(adress, file)
    
    if file == ".DS_Store":
            
        os.remove(file_path)
            

def normilize(file_name):

    correct_file_name = re.sub(r"\W", "_", file_name)

    check_cyrillic = re.search(r"[а-яА-ЯёЁ]", correct_file_name)

    if check_cyrillic != None:

        for c, l in zip(tuple(CYRILLIC_SYMBOLS), TRANSLATION):
        
            TRANS[ord(c)] = l
            TRANS[ord(c.upper())] = l.upper()

        correct_file_name = correct_file_name.translate(TRANS)
        
    return correct_file_name

def unpack_archive(correct_file_name, new_file_path, new_file_name, folder_path):

    file_achv_path = os.path.join(folder_path, correct_file_name)

    shutil.unpack_archive(new_file_path, file_achv_path)
    
    os.remove(new_file_path)
    
    return file_achv_path


def sorts_files(adress, file, path):

    current_file_path = os.path.join(adress, file)

    file_name, file_exten = os.path.splitext(file)

    file_exten = file_exten.replace('.', '')

    correct_file_name = normilize(file_name)

    new_file_name = correct_file_name + "." + file_exten
    
    for dict_key, dict_exten in dict_extensions.items():

        flag = 0

        if file_exten in dict_exten:

            folder_path = os.path.join(path, dict_key)

            if not os.path.exists(folder_path):
                os.mkdir(folder_path)

            new_file_path = os.path.join(folder_path, new_file_name)
            
            if not os.path.exists(new_file_path):
                os.replace(current_file_path, new_file_path)

                if not file_exten in list_known_exten:
                    list_known_exten.append(file_exten)
        
            if file_exten in ['zip', 'gz', 'tar']:
                new_file_path = unpack_archive(correct_file_name, new_file_path, new_file_name, folder_path)
                
            flag = 1
            break
        
    if flag == 0:

        folder_path = os.path.join(path, 'other')

        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
            
        new_file_path = os.path.join(folder_path, new_file_name)
        
        if not os.path.exists(new_file_path):
            os.replace(current_file_path, new_file_path)

            if not file_exten in list_unknown_exten:
                list_unknown_exten.append(file_exten)
    
    return list_known_exten, list_unknown_exten

def delete_empty_folders(path):

    while True:
        
        a = 0
        
        for paths, folders, files in os.walk(path):
            
            if not files and not folders:
                
                os.rmdir(paths)
                a = 1

        if a != 1:
            break


def main():

    try:
        path = sys.argv[1]

    except IndexError:
        
        print("Аргументов нет")
        path = input("Введите путь сюда: ")
        

    if os.path.isdir(path) == False:
        
        print(f'"{path}" - не является существующиим путем к папке. Попробуйте еще раз!')
        path = input("Введите корректный путь к папке: ")
    
    for adress, folder, files in get_list_files(path):
        
        for file in files:
            
            delete_ds_store_only_for_mac(adress, file)
            
            if file != ".DS_Store":
                
                sorts_files(adress, file, path)
                
    delete_empty_folders(path)

    print(f'Список всех извесных программе расширений: {list_known_exten}\n'
          f'Список неизвесных программе расширений: {list_unknown_exten}')
    
if __name__ == '__main__':
    main()
