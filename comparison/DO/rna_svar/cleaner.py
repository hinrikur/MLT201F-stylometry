import re
import os

'''
Hinrik Hafsteinsson - Vor 2019

Stutt skripta sem les inn textaskrá sem var handvirkt afrituð úr PDF skrá
(hér DO_svar_raw.txt) og skilar út nokkurn veginn normaliseruðum texta þar sem
villur úr afrituninni eru hreinsaðar burt meðal annars og hver lína inniheldur
eina setningu.
'''

''' ========================= '''
'''    Breytur skilgreindar   '''
''' ========================= '''

chars = {'a' : ('á', 'á'),
         'i' : ('í', 'í'),
         'e' : ('é', 'é'),
         'u' : ('ú', 'ú'),
         'o' : ('ó', 'ó'),
         'y' : ('ý', 'ý'),
         'oe': ('ö', 'ö') }
         # Format:
         # {'key' : ('wrong', 'right')}

regex_strings = [
    ('(?<=[^(\bgr|\bbls|\d|\s|H|m\.a)]\.) ', '\n'), # insert correct newline
    ('(?<=[\.\:])\d', '\n'), # insert newline if . or : followed by digit
    ('\s\. ', ' '),
    ('((^|\n)\d\s*|^\s{1,10}|\.\))', '',), # remove miscellaneous
    ('(?=[MDCLXVI])M*(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[XV]|V?I{0,3})\.*$', '') # remove roman numerals
]

input_name = 'DO_svar_raw.txt'
output_name = 'DO_svar.txt'

''' ========================= '''
'''      Föll skilgreind      '''
''' ========================= '''

def insert_icechar(string):
    '''
    Þegar texti er afritaður handvirkt úr pdf skrá skila íslensku
    kommustafirnir sér vitlaust. Þetta fall skiptir þeim út fyrir rétta stafi.
    '''
    for char, variants in chars.items():
        print('Checking char type -', char)
        string = re.sub(variants[0], variants[1], string)
    return string

def cleanup(string):
    '''
    Keyrir í gegnum lista af regex strengjum og skiptir þeim út
    '''
    for regex in regex_strings:
        string = re.sub(regex[0], regex[1], string)
    string = insert_icechar(string)
    return(string)

def return_cleanfile(out, input):
    '''
    Býr til nýja skrá með hreinsaða textanum
    '''
    if os.path.exists(out):
        print('File already exists. Replacing file...')
        os.remove(out)
    else:
        print('Creating output file...')
    with open(out, 'w') as file:
        file.write(cleanup(input))
    print('Done.')

''' ========================= '''
'''        Föll keyrð         '''
''' ========================= '''

file = open(input_name, 'rt')
text = file.read()
file.close()
return_cleanfile(output_name, text)
