# coding=utf-8

import os
import re
from bs4 import BeautifulSoup
import requests
import urllib3
from dateutil.parser import parse

'''
Hinrik Hafsteinsson - Vor 2019

Skripta sem skrapar færslur af bloggsíðu Hannesar Hólmsteins Gissurarsonar og
skrifar þær út í .txt skrár sem ber hver nafn eftir dagsetningu og titli
viðkomandi færslu.
Eins og er miðar skriptan einungis við árið 2014 en hana má aðlaga til að
skrapa allar færslur af síðunni til dæmis.
'''

''' ========================= '''
'''    Breytur skilgreindar   '''
''' ========================= '''

starts = {
    '2012' : '/blog/hannesgi/entry/1216126/',
    '2013' : '/blog/hannesgi/entry/1280891/',
    '2014' : '/blog/hannesgi/entry/1404246/'
}

# start = '/blog/hannesgi/entry/1404246/' # 2014
# start = '/blog/hannesgi/entry/1280891/' # 2013
start = '/blog/hannesgi/entry/1216126/' # 2012
wd = os.getcwd()
target_years = ['2012', '2013', '2014']

error_list = []

''' ========================= '''
'''      Föll skilgreind      '''
''' ========================= '''

def make_dirs():
    '''
    Býr til yfirmöppuna 'hhg_blogg' og undirmöppuna 201X, fyrir úttakskrár, ef
    þær eru þegar ekki til.
    '''
    if os.path.isdir(target_dir):
        if os.path.isdir(target_dest):
            pass
        else:
            os.mkdir(target_dest)
    else:
        os.mkdir(target_dir)
        os.mkdir(target_dest)

def get_soup(url):
    '''
    Hjálparfall sem býr til BeuatifulSoup object úr vefsíðu með url sem viðfang.
    Skilar úttakinu sem breytu.
    '''
    blogg = requests.get(url)
    blogg_soup = BeautifulSoup(blogg.content, 'html.parser')
    return blogg_soup

def get_info(num):
    '''
    Viðeigandi upplýsingar fundnar á vefsíðu með hjálp get_soup() fallsins
    Ath viðfang fallsins en það tekur við ítarupplýsingum um vefsíðu
    Sjá breytuna 'start' hér fyrir ofan sem geymir uppl. um upphafssíðu

    Nokkrar bloggfærslur innihalda villur í meginmáli og því inniheldur
    fallið try-except likkju, þar sem 'body' er sleppt ef villa kemur upp.

    Fallið skilar alltaf af sér dictið 'info'.
    '''
    url = 'https://hannesgi.blog.is' + num
    soup = get_soup(url)
    entry = soup.find('div', class_ = 'blog-entry')
    try:
        info = {
            'date' : entry.find('p', class_='entry-date').string,
            'title' : entry.find('h2').string,
            'body' : entry.find('div', class_='entry-body').p.text,
            'next' : entry.find('span', class_='next').a['href']
        }
        return info
    except:
        info = {
            'date' : entry.find('p', class_='entry-date').string,
            'title' : entry.find('h2').string,
            'next' : entry.find('span', class_='next').a['href']
        }
        return info


def make_file(info):
    '''
    Tekur inn dictið info (úttak get_info() falls), undirbýr gögnin og
    skrifar þau í skrá með nafni byggðu á metadata úr bloggfærslunni.

    Ath. vegna villu í body í nokkrum fræslum er varnagli í vinnslu 'body'
    gagna á tveimur stöðum innan fallsins.

    Ef villa kemur upp er nafni villuskránnar bætt við listann 'error_list'
    til vistunar.
    '''
    try:
        body = re.sub(r'(?=[(.?!,:%)])(?<=[^\s])', r' ', info['body'])
        body = re.sub(r'(?<=[^\d] \.\s)', r'\n', body)
    except:
        print('Villa - eitthvað er að færslunni')
        body = False
    date = re.sub(r' \| ', r' ', info['date'])
    date = str(parse(date))[:10]
    file_title = date + ' ' + info['title']
    # file_title = re.sub(r' ', r'_', file_title)
    print(file_title)
    if body:
        with open('HHG_' + file_title + '.txt', 'w') as file:
            file.write(body)
    else:
        print('Villa - upplýsingar skrár:', file_title)
        error_list.append(file_title)
        print(len(error_list))

    # global num
    next = info['next']
    if file_title[:4] == target_year:
        make_file(get_info(next))
    else:
        return

def write_error_filenames():
    '''
    Skrifar nöfn bloggfærslna sem náðist ekki að afrita í sérstakt skjal.
    '''
    with open('2014_villufærslur.txt', 'w') as file:
        for i in error_list:
            file.write(i)
            file.write('\n')

''' ========================= '''
'''        Föll keyrð         '''
''' ========================= '''

for target_year in target_years:
    target_dir = os.path.join(wd, 'hhg_blogg')
    target_dest = os.path.join(target_dir, target_year)
    make_dirs()
    os.chdir(target_dest)
    make_file(get_info(starts[target_year]))
    os.chdir(os.path.abspath('../..'))
write_error_filenames()



# print(num)
