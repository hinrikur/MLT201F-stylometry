import os
import shutil
import time

''' Þessi skrá les in lista af skráarnöfnum, ber það saman við dir af skrám og
    færir skrár með réttum nöfnum í nýja möppu  '''

mbl_dir = '/Users/hinrik/Documents/skoli/MA/vor_2019/MLT201F/morgunbladid_stuff'
txt_dir = os.path.join(mbl_dir, 'sunnudagar_text')
rvk_dir = os.path.join(mbl_dir, 'rvk_text')
names_dir = os.path.join(mbl_dir, 'rvk_filenames')


def joined(source, sub):
    ''' Hjálparfall til að tvinna saman slóðir '''
    new_dir = os.path.join(source, sub)
    return new_dir

def read_filenames(txt_dir):
    ''' Fall sem les inn skrá með skráarnöfnum og skilar lista af nöfnum '''
    global filenames
    filenames = []
    for filename in os.listdir(txt_dir):
        name_dir = joined(txt_dir, filename)
        filename_dir = joined(names_dir, filename)
        with open(filename_dir, 'r') as names:
            for i in [i.strip() for i in names.readlines()]:
                filenames.append(i)
    return filenames

def copy_files(source_dir, dest_dir, name_list):
    ''' Afritunarfall sem tekur inn dir path sem viðfang (helst bara ár í
        morgunbladid_stuff möppunni eða subfolder) '''
    for anno in os.listdir(source_dir):
        source_anno = joined(source_dir, anno)
        if os.path.isdir(source_anno):
            dest_anno = joined(dest_dir, anno)
            for mensis in os.listdir(source_anno):
                source_mensis = joined(source_anno, mensis)
                if mensis.endswith('Store') == False:
                    for txt_file in os.listdir(source_mensis):
                        txt_file_dir = joined(source_mensis, txt_file)
                        if txt_file in name_list:
                            if os.path.isdir(dest_anno):
                                pass
                            else:
                                os.mkdir(dest_anno)
                            shutil.copy(txt_file_dir, dest_anno)


copy_files(txt_dir, rvk_dir, read_filenames(names_dir))
