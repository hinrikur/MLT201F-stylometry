#!/bin/bash

'''
Hinrik Hafsteinsson - Vor 2019

Biður notanda um nafn á möppu sem inniheldur .txt skrárnar sem á að sameina.
Býr líka til möppuna "combined_txt" sem inniheldur úttakskrárnar.
Ath. að þessi skripta bætur "HHG_" framan við úttakskjalið.
'''

echo 'Hvaða möppu á að sameina?'
read varname

DIRECTORY='./combined_txt'
out_filename='HHG_'$varname'.txt'

if [ ! -d "$DIRECTORY" ]; then
  mkdir $DIRECTORY
fi

cat ./$varname/* > $DIRECTORY'/'$out_filename
