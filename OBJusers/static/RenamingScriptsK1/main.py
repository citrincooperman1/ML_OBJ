import pandas as pd
import openpyxl
import os
import time

FILETOPROCESS = "C:\\Python\\RenamingScriptsK1\\K1 name template_7pm.xlsx" #Provided excel
DIRECTORY_TO_PARSE = "\\\\SSC10422\\z-drive\\Harbor Group International\\2022\\Files to client\\Script K-1 renaming bot\\" #PROD - DON'T CHANGE
#DIRECTORY_TO_PARSE = "C:\\Python\\RenamingScriptsK1\\" #TEST

def move_file(file_name, dir):
    # Given full path of file, and directory to move that file to
    base_path = os.path.basename(file_name)
    new_path = os.path.join(dir, base_path)
    # print("base_path= " + base_path)
    # print("new_path= " + new_path)
    if os.path.exists(new_path):
        try:
            dt = time.strftime('%Y%m%d_%H%M_%S')
            backup_path = os.path.join(dir, "{}_{}".format(dt, base_path))
            os.rename(new_path, backup_path)
        except Exception as ex:
            raise Exception(ex)
    try:
        os.rename(file_name, new_path)
    except Exception as ex:
        raise Exception(ex)


def prep_dir(parent_dir, base_dir):
    # Make directory if it doesn't exist
    dir_name = os.path.join(parent_dir, base_dir)
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name, exist_ok=True)
    return dir_name


def update_filename(root_folder, file_name, client_code, folder_name):  
    error_dir = prep_dir(root_folder, 'ERROR')
    #print(reduced_string)
    current_filename = str(file_name).replace(root_folder,"")

    #Validating file - Making sure the files are not this following format: 1 ggph13-landstar manor holdings, llc-hggp capital xiii, llc-2021. Files can't end in 2021
    # count_dash = current_filename.count("-") 
    # if count_dash < 2 or count_dash > 2:
    #     print(folder_name)
    #     move_file(file_name, error_dir)
    #     return False

    #Its good! Procced to rename    
    i = current_filename.index('-')
    new_name= current_filename[:i] + "-"+client_code+"-2022-K1"
    result_prev = new_name.replace("-","_")
    result = result_prev + current_filename[i:]
    result = result.replace("-","_",2)
    one = current_filename.index('1 ')
    reduced_string = result[:one] + result[one+2:] 
    success_dir = prep_dir("\\\\SSC10422\\z-drive\\Harbor Group International\\2022\\Files to client\\K-1's to be sent\\", folder_name) #PROD - DONT CHANGE
    #success_dir = prep_dir(root_folder, 'SUCCESS') #TEST
    new_file_name = root_folder + reduced_string
    #print(new_file_name)
    #print(os.path.basename(os.path.splitext(file_name)[0]))
    try:
        os.rename(file_name, new_file_name)
    except:
        move_file(file_name, error_dir)
        return False
    else:
        move_file(new_file_name, success_dir)
        return True


if __name__ == '__main__': 
    book = openpyxl.load_workbook(FILETOPROCESS, data_only=True)
    if 'Sheet1' in book.sheetnames:
        df1 = pd.read_excel(
            FILETOPROCESS,
            sheet_name="Sheet1",
            usecols='A:B',
            index_col=None,
            header=None,
            skiprows=1
        )
    # print(df1)

    for index, row in df1.iterrows():
        folder_name = row[0]
        client_code = row[1]
        root_folder = DIRECTORY_TO_PARSE + folder_name
        #print(root_folder)
        files_to_parse = [os.path.join(DIRECTORY_TO_PARSE + folder_name , x) for x in os.listdir(DIRECTORY_TO_PARSE + folder_name) if(os.path.splitext(x)[1] == '.pdf' and not os.path.splitext(x)[0].startswith('~$'))]
        new_files_to_parse = [x for x in files_to_parse]
        #print(new_files_to_parse)
        if new_files_to_parse:
           for file in new_files_to_parse:
               # print(folder_name)
                update_filename(root_folder=root_folder, file_name=file, client_code=client_code, folder_name=folder_name)