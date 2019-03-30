import time
import os
import re
import shutil
import csv
import xml.etree.ElementTree as et
from datetime import date

'''
Hinrik Hafsteinsson - Vor 2019

Þetta er skripta sem tekur inn hrá .xml gögn um Morgunblaðið úr Risamálheildinni
og skilar út textaskrám sem innihalda einungis efni sem birtist á sunnudögum og
vistar þau í þartilgerðum möppum innan "morgunbladid_stuff" möppunnar.

Meginhlutverk skriptunnar er að búa til viðkomandi úttaksmöppur og vista gögnin
á réttum stað eftir mánuði og ári en hugmyndin er að hún taki inn ÖLL gögnin
sem Risamálheildin hefur frá Morgunblaðinu.

Með sunnudagsgögnin vistuð sérstaklega er lítið mál að finna út hvaða greinar
tilheyri Reykjavíkurbréfunum (sem er tilgangur þessarar skriptu) en það þarf
að gera handvirkt með samanburð við titla á timarit.is.
'''

''' ========================= '''
'''        Dagsetningar       '''
''' ========================= '''

# allir sunnudagar fundnir
sunnudagar = [] # tómur listi skilgreindur fyrir dagsetningar
startdate = 733411 # númer fyrsta sunnudags ársins 2009
# lykkja sem reiknar dagsetninguna og bætir henni í dagsetningalistann
while startdate < 737062:
    dags = str(date.fromordinal(startdate))
    dags = re.sub('-0', '-', dags) # óþarfa "0" tekin út
    sunnudagar.append(dags)
    startdate += 7

''' ========================= '''
'''     Flutningabreytur      '''
''' ========================= '''

# Möppurnar skilgreindar sem breytur
mbl_dir = '/Users/hinrik/Documents/skoli/MA/vor_2019/MLT201F/morgunbladid_stuff'
rmh_dir = os.path.join(mbl_dir, 'rmh_morgunbladid')
sun_dir = os.path.join(mbl_dir, 'sunnudagar_09-16')
txt_dir = os.path.join(mbl_dir, 'sunnudagar_text')
ttl_dir = os.path.join(mbl_dir, 'mbl_titlar')
# print(mbl_dir, rmh_dir, sun_dir, sep='\n')

''' ========================= '''
'''    Meginföll skilgreind   '''
''' ========================= '''

def copy_sunday():
    '''Afritar greinar í RMH-MBL möppunni sem birtust á sunnudegi í nýja möppu'''
    # Ártöl sem fengist er við
    annum = ['2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016']
    for anno in os.listdir(rmh_dir):
        year_start = time.time()
        print('Árið er {}'.format(anno))
        source_anno = os.path.join(rmh_dir, anno)
        if anno in annum and os.path.isdir(source_anno):
            dest_anno = os.path.join(sun_dir, anno)
            os.mkdir(dest_anno)
            for mensis in os.listdir(source_anno):
                month_start = time.time()
                source_mensis = os.path.join(source_anno, mensis)
                if os.path.isdir(source_mensis):
                    dest_mensis = os.path.join(dest_anno, mensis)
                    os.mkdir(dest_mensis)
                    for filename in os.listdir(source_mensis):
                        file_start = time.time()
                        if not filename.endswith('.xml'): continue
                        fullname = os.path.join(source_mensis, filename)
                        tree = et.parse(fullname)
                        root = tree.getroot()
                        # dagsetning staðsett í xml tré
                        date = root.find('./{http://www.tei-c.org/ns/1.0}teiHeader/{http://www.tei-c.org/ns/1.0}fileDesc/{http://www.tei-c.org/ns/1.0}sourceDesc/{http://www.tei-c.org/ns/1.0}biblStruct/{http://www.tei-c.org/ns/1.0}analytic/{http://www.tei-c.org/ns/1.0}date')
                        if date.text in sunnudagar:
                            shutil.copy(fullname, dest_mensis)
                        file_end = time.time()
                        #print('Tími sem fór í skrána {filename}: ', file_start - file_end)
                    month_end = time.time()
                    print('Leit í mánuði nr. {} tók'.format(mensis), month_end - month_start, 'sek.')
        year_end = time.time()
        print('Leitin í {} tók'.format(anno), year_end - year_start, 'sek. eða', (year_end - year_start)/60, 'mínútur.')

def write_sunday():
    '''Skrifar út texta greinar úr .xml skrá RMH-MBL í .txt skrá'''
    for anno in os.listdir(sun_dir):
        year_start = time.time()
        print('Árið er {}'.format(anno))
        source_anno = os.path.join(sun_dir, anno)
        if os.path.isdir(source_anno):
            dest_anno = os.path.join(txt_dir, anno)
            os.mkdir(dest_anno)
            for mensis in os.listdir(source_anno):
                month_start = time.time()
                source_mensis = os.path.join(source_anno, mensis)
                if os.path.isdir(source_mensis):
                    dest_mensis = os.path.join(dest_anno, mensis)
                    os.mkdir(dest_mensis)
                    for filename in os.listdir(source_mensis):
                        file_start = time.time()
                        if not filename.endswith('.xml'): continue
                        fullname = os.path.join(source_mensis, filename)
                        # Hér er xml-tréð parsað
                        tree = et.parse(fullname)
                        root = tree.getroot()
                        titill = root.find('./{http://www.tei-c.org/ns/1.0}teiHeader/{http://www.tei-c.org/ns/1.0}fileDesc/{http://www.tei-c.org/ns/1.0}titleStmt/{http://www.tei-c.org/ns/1.0}title/{http://www.tei-c.org/ns/1.0}title')
                        texti = root.find('./{http://www.tei-c.org/ns/1.0}text/{http://www.tei-c.org/ns/1.0}body/{http://www.tei-c.org/ns/1.0}div1/{http://www.tei-c.org/ns/1.0}p')
                        date = root.find('./{http://www.tei-c.org/ns/1.0}teiHeader/{http://www.tei-c.org/ns/1.0}fileDesc/{http://www.tei-c.org/ns/1.0}sourceDesc/{http://www.tei-c.org/ns/1.0}biblStruct/{http://www.tei-c.org/ns/1.0}analytic/{http://www.tei-c.org/ns/1.0}date')
                        # Villa í titli debugguð (villan reyndist vera í =>  G-32-5449474.xml)
                        # if date is None:
                        #     print('Villa í date => ', filename)
                        # elif titill is None:
                        #     print('Villa í texta => ', filename)
                        out_filename = '_'.join([date.text, re.sub(r'["/„”(,,)]', '', titill.text)])
                        # print(out_filename)
                        os.chdir(dest_mensis)
                        with open(out_filename, 'w') as file:
                            punktur = re.compile('\.')
                            for child in texti:
                                for elem in child:
                                    if punktur.match(elem.text):
                                        file.write(elem.text + '\n')
                                    else:
                                        file.write(elem.text + ' ')
                        # if date.text in sunnudagar:
                        #     shutil.copy(fullname, dest_mensis)
                        file_end = time.time()
                        #print('Tími sem fór í skrána {filename}: ', file_start - file_end)
                    month_end = time.time()
                    print('Ritun í mánuði nr. {} tók'.format(mensis), month_end - month_start, 'sek.')
        year_end = time.time()
        print('Ritun ársins {} tók'.format(anno), year_end - year_start, 'sek. eða', (year_end - year_start)/60, 'mínútur.')

def write_titles():
    '''Les inn titla Morgunblaðsins úr RMH og skrifar í .csv skrá'''
    for anno in os.listdir(rmh_dir):
        year_start = time.time()
        print('Árið er {}'.format(anno))
        source_anno = os.path.join(rmh_dir, anno)
        if os.path.isdir(source_anno):
            #dest_anno = os.path.join(ttl_dir, anno)
            #os.mkdir(dest_anno)
            for mensis in os.listdir(source_anno):
                month_start = time.time()
                source_mensis = os.path.join(source_anno, mensis)
                if os.path.isdir(source_mensis):
                    #dest_mensis = os.path.join(dest_anno, mensis)
                    #os.mkdir(dest_mensis)
                    os.chdir(ttl_dir) # Fært í nýja vinnumöppu
                    out_filename = (anno + '.tsv')
                    with open(out_filename, mode='w') as info_file:
                        info_writer = csv.writer(info_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        for filename in os.listdir(source_mensis):
                            #file_start = time.time()
                            if not filename.endswith('.xml'): continue
                            fullname = os.path.join(source_mensis, filename)
                            # Hér er xml-tréð parsað
                            tree = et.parse(fullname)
                            root = tree.getroot()
                            titill = root.find('./{http://www.tei-c.org/ns/1.0}teiHeader/{http://www.tei-c.org/ns/1.0}fileDesc/{http://www.tei-c.org/ns/1.0}titleStmt/{http://www.tei-c.org/ns/1.0}title/{http://www.tei-c.org/ns/1.0}title')
                            texti = root.find('./{http://www.tei-c.org/ns/1.0}text/{http://www.tei-c.org/ns/1.0}body/{http://www.tei-c.org/ns/1.0}div1/{http://www.tei-c.org/ns/1.0}p')
                            date = root.find('./{http://www.tei-c.org/ns/1.0}teiHeader/{http://www.tei-c.org/ns/1.0}fileDesc/{http://www.tei-c.org/ns/1.0}sourceDesc/{http://www.tei-c.org/ns/1.0}biblStruct/{http://www.tei-c.org/ns/1.0}analytic/{http://www.tei-c.org/ns/1.0}date')
                            # gildi dálka smíðaðir fyrir csv skrá
                            if date is None:
                                row = ['DAGSETNINGU VANTAR', filename, titill.text, mensis]
                                info_writer.writerow(row)
                            elif titill is None:
                                row = [date.text, filename, 'TITIL VANTAR', mensis]
                                info_writer.writerow(row)
                            else:
                                row = [date.text, filename, titill.text, mensis]
                                info_writer.writerow(row)
                            #file_end = time.time()
                            #print('Tími sem fór í skrána {}: '.format(date.text), file_end - file_start)
                month_end = time.time()
                print('Leit í mánuði nr. {} tók'.format(mensis), month_end - month_start, 'sek.')
        year_end = time.time()
        print('Leitin í {} tók'.format(anno), year_end - year_start, 'sek. eða', (year_end - year_start)/60, 'mínútur.')


''' ========================= '''
'''        Föll keyrð         '''
''' ========================= '''

# Byrjunartími
copy_start = time.time()
# kallað á fallið
write_titles()
# endatími
copy_end = time.time()
# tímabreytur skilgreindar
keyrsla = (copy_end - copy_start)
keyrsla_min = (copy_end - copy_start)/60
# tími prentaður
print('Keyrslu lokið. Keyrsla tók {} mínútur, eða {} sekúndur'.format(keyrsla_min, keyrsla))



''' ========================= '''
'''    Debug-/prufubreytur    '''
''' ========================= '''

# vinnumappan skilgreind sem breyta
file_dir = os.path.dirname(os.path.realpath(__file__))
# staðsetning XML skrána sem á að vinna með skilgreind (source directory)
# xml_file = os.path.join(base_path, "G-32-4247903.xml")
xml_folder = os.path.join(file_dir, 'test_stuff')
months_dir = os.listdir(xml_folder)
# staðsetning úttaksmöppunnar skilgreind
out_folder = os.path.join(file_dir, 'test_out')

''' ========================= '''
'''        Titlabreytur       '''
''' ========================= '''

# tómur listi fyrir alla titla sem finnast
titlar = []
# regex leit að réttum titli vistuð í breytu
rvk = re.compile('(REYKJAV[ÍI]KURBR[ÉE]F|[Rr]eykjav[íi]kurbr[ée]f)')

''' ========================= '''
'''     Titlafall (debug)     '''
''' ========================= '''

def finna_titla():
    for filename in fd:
        # titill staðsettur í xml tré
        date = root.find('./{http://www.tei-c.org/ns/1.0}teiHeader/{http://www.tei-c.org/ns/1.0}fileDesc/{http://www.tei-c.org/ns/1.0}sourceDesc/{http://www.tei-c.org/ns/1.0}biblStruct/{http://www.tei-c.org/ns/1.0}analytic/{http://www.tei-c.org/ns/1.0}date')
        titill = root.find('./{http://www.tei-c.org/ns/1.0}teiHeader/{http://www.tei-c.org/ns/1.0}fileDesc/{http://www.tei-c.org/ns/1.0}titleStmt/{http://www.tei-c.org/ns/1.0}title/{http://www.tei-c.org/ns/1.0}title')
        print(date.text)
        if date.text in sunnudagar: # Titlarnir settir í lista til úrvinnslu
            titlar.append(titill.text)
        # Prentar lengd titlalistans
        print(len(titlar))
        # skrifar alla fundna titla í textaskrá
        with open('titlar2.txt', 'w') as titlar_file:
            for item in titlar:
                titlar_file.write(item + '\n')

''' ========================= '''
'''    Debugfall (skraut)     '''
''' ========================= '''

def debug():
    for folder in months_dir:
        dest_folder = os.path.join(out_folder, folder)
        os.mkdir(dest_folder)
        for filename in os.listdir(folder):
            if not filename.endswith('.xml'): continue
            fullname = os.path.join(xml_folder, os.path.join(folder, filename))
            tree = et.parse(fullname)
            root = tree.getroot()
            # dagsetning staðsett í xml tré
            date = root.find('./{http://www.tei-c.org/ns/1.0}teiHeader/{http://www.tei-c.org/ns/1.0}fileDesc/{http://www.tei-c.org/ns/1.0}sourceDesc/{http://www.tei-c.org/ns/1.0}biblStruct/{http://www.tei-c.org/ns/1.0}analytic/{http://www.tei-c.org/ns/1.0}date')
            if date.text in sunnudagar:
                shutil.copy(fullname, dest_folder)
