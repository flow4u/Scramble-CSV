'''
Generic functions used in FAIRification Notebooks
'''

import time
from datetime import datetime
import shutil
import os
import glob
import zipfile
import sys


# try to stop elegantly
class StopExecution(Exception):
    def _render_traceback_(self):
        pass

    
def correct_date(a,b):
    '''
    Dates are usually an issue, this function converts certain given formats into ISO8601, %Y-%m-%d format
    '''
    if a == '': return ''
    try:
        a = datetime.strptime(str(a), b)
        return datetime.strftime(a, '%Y-%m-%d')
    except:
        return 'ERR: ' + str(a)
    
    
def duration_days(x, con):
    '''
    Duration in days, requires that dates are in ISO 8601 format
    '''
    try:
        end = datetime.strptime(x[mv], '%Y-%m-%d')
        start = datetime.strptime(x[con], '%Y-%m-%d')
        return (end-start).days
    except:
        return 'ERR'    
        

def find_unpack_zips(folder, correction=0):
    '''
    find_unpack_zips takes the arguments:
    - folder: for where the zips
    - correction: to trunc the zip name with more characters than .zip (4) this is optional
    
    If the target directory already exists, it will be deleted.
    
    The zip will be unzipped in a subfolder called <zipfile.zip> minus (4 + correction)
    e.g. find_unpack_zips('./myfolder/', 2)  unzips myzip01.zip in subfolder myzip
    
    When finished unzipping the zipfile is deleted
    
    The function returns a list with processed zipfiles
    
    '''
    files = []
    path = folder + '/'
    correction=-4-correction
    for file in glob.glob(path +'/*.zip'):
        source = file
        target = file[:correction]
        if os.path.exists(target):
            shutil.rmtree(target)
                          
        with zipfile.ZipFile(source, 'r') as zip_ref:
            os.mkdir(target)
            zip_ref.extractall(target)
        os.remove(source)
        files.append(file)
    return files


def move_files(file_name, source_folder, target_folder):
    '''
    Mover zips from the source folder to the target folder
    '''
    try:
        for item in os.listdir(source_folder):
            if os.path.isdir(source_folder+'/'+item):
                for file in glob.glob(source_folder + '/' + item + '/'+file_name):
                    shutil.move(file, target_folder)
                try:
                    os.rmdir(source_folder + '/' + item)
                except:
                    pass
    except:
        pass


def choose_dir_item(folder, type='folders', what='All'):
    '''
    Pick a subfolder or file from a folder.
    
    '''
    all_items = get_all_items(folder, type)
    print_title('Choose source by number')
    # create dictionary with all folders
    items = {}
    if what != 'All':
        temp_all_items = []
        for item in all_items:
            if what in item and 'EMPTY' not in item and 'ERRORS' not in item and 'NON_MAPPED' not in item and 'MISSING_KEYS' not in item and '~'not in item:
                temp_all_items.append(item)
        all_items = temp_all_items

    count = 0
    for count1, item in enumerate(all_items):
        items[count1+1] = item
        extra =''
        if count1+1 < 10: extra = ' '
        print(f'[{count1+1}]{extra} {items[count1+1]}', end = '\t')
        if (count1+1) %3 == 0: print('')
        count = count1
    print('\n')
    
    item_choosen = False
    while item_choosen == False:
        this_answer = choose_retry(str(1) + ' and ' + str(count + 1))
        try:
            if int(this_answer) > 0 and int(this_answer) <= count + 1:
                item_choosen = True
                return all_items[int(this_answer)-1]
        except:
            if this_answer.lower()=='q':
                print_title('Quiting the notebook run on instruction of the user')
                item_choosen = True
                raise StopExecution #SystemExit("Stop right there!")
                # return ''


def get_all_items(folder, type='folders'):
    '''
    This function gets by default all the subfolders from folder
    If type == files, then it gets all the files in that folder
    '''
    all_outputs = []
    for item in os.listdir(folder):
        if type == 'folders':
            if os.path.isdir(folder + item): all_outputs.append(item)
        if type == 'files':
            if os.path.isfile(folder + item): all_outputs.append(item)
    return sorted(all_outputs, reverse=True)


def title_wrapper(func):
    '''
    This function wraps the title with * and -.
    
    Used by print_title
    '''
    def wrapper(*args, **kwargs):
        print('*'*90)
        func(*args, **kwargs)
        print('-'*90)
    return wrapper


@title_wrapper
def print_title(text):
    '''
    This function wraps the text in the title_wrapper
    '''
    print(text)

    
def choose_retry(text):
    '''
    This generic function returns the input from the user.
    '''
    return input('Please choose Q(uit) or between '+ text + ': ')


# function to quickly output DF to temp.csv comma separated
def output_csv(df, name, timestamp=True):
    '''
    Quickly create a temp CSV, comma separated
    
    output_csv(df, target_folder, name, timestamp)
    df: dataframe to be saved as CSV
    target_folder: folder to save the csv to
    name: name of the csv file
    timestamp: True or False, default True
    '''
    stamp = time.strftime('%Y%m%d-%H%M%S', time.localtime()) + '-'
    if not timestamp:
        stamp = ''
    # if target_folder[-1] != '/': target_folder += '/'
    # name = stamp + name[i+1:] + '.csv'
    # if name[:-4] != '.csv':
    #     if name[0:1] != '.':
    #         name = './Result/' + stamp + name + '.csv'
    #     else:
    i = name.rfind('/')
    name = name[0:i+1] + stamp + name[i+1:] +'.csv'
    try:
        df.to_csv(name, header=True, index=False, sep=',')
        print('saved: ' + name)
        return 'saved: ' + name
    except:
        print_title('Close ' + name + ' and Continue, or Stop  ')
        pyanswer = answer('Respond with C(ontinue) or S(top) ')
        if not pyanswer:
            print('You have halted the operation, please rerun this notebook when you are ready.')
            raise StopExecution #sys.exit(1)
        else:
            output_csv(df, name)

            
# function for yes/no result based on the answer proded as argument
def answer(reply):
    '''
    To prompt the user to accept the next step, false results in halting the script
    True: C(onctiue), or c(continue)
    False: S(top), s(top), ''
    '''
    yes = set (['C', 'c'])
    no = set (['S', 's', ''])
    
    while True:
        choice = input(reply).lower()
        if choice in yes:
            print('\nScript continues....')
            return True
        elif choice in no:
            print('\nScript has halted, please make changes and rerun the notebook.')
            print('\n\n\n\n')
            return False
        else:
            print("Please respond with 'C' or 'S'\n")