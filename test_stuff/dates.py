import re
from datetime import date

# allir sunnudagar fundnir
sunnudagar = [] # tómur listi skilgreindur fyrir dagsetningar
startdate = 733411 # númer fyrsta sunnudags ársins 2009
# lykkja sem reiknar dagsetninguna og bætir henni í dagsetningalistann
while startdate < 737062:
    dags = str(date.fromordinal(startdate))
    dags = re.sub('-0', '-', dags) # óþarfa "0" tekin út
    sunnudagar.append(dags)
    startdate += 7
# úttak prentað
for i in sunnudagar:
    print(i)
