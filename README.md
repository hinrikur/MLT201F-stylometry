# MLT201F-stylometry

Fyrra lokaverkefni í námskeiðinu **MLT201F Málleg gagnasöfn: Í hugbúnaðargerð og rannsóknir**, kennt á vormisseri 2019 við Háskóla Íslands.

Þetta repo inniheldur gögn tengd stílmælingarathugun á _Reykjavíkurbréfum Morgunblaðsins_ sem eru vikulegir pistlar um mál líðandi stundar eftir nafnlausan höfund.

Athugunin byggðist á samanburði Reykjavíkurbréfanna á árunum 2012 til 2014 við texta þekktra höfunda frá svipuðum tíma og var  athugað hvort kerfisbundin líkindi fundust milli textanna með kósínuslíkindum. Niðurstöðurnar voru ekki afgerandi en þær benda til þess að hægt sé að vinna með viðfangsefnið lengra. 

Gögn Morgunblaðsins voru sótt úr [Risamálheildinni](malheildir.arnastofnun.is) sem er haldið úti af Stofnun Árna Magnússonar í íslenskum fræðum og má sækja af vefnum [Málföng.is](www.malfong.is).

## Uppbygging svæðis

PDF skráin `Hinrik_gagnasofn_loka.pdf` inniheldur greinargerð athugunarinnar sem heild. Þar koma fram helstu ítarupplýsingar verkefnisins.

Í grunnmöppunni eru skripturnar `parse.py` og `move.py` og sem voru notaðar til að vinna morgunblaðsgögnin úr .xml skrám Risamálheildarinnar. 

Mappan __`morgunbladid_stuff`__ inniheldur gögn úr morgunblaðinu á mismunandi stigum forvinnslu.

Mappan __`comparison`__ inniheldur samanburðartextana og skriptur sem voru notaðar til að sækja og forvinna þá. Textarnir eru annars vegar tveir textar eftir Davíð Oddsson, fyrrverandi seðlabankastjóra, og hins vegar bloggfærslur eftir Hannes Hólmstein Gissurarson, prófessor.

Mappan __`test_stuff`__ inniheldur ýmiskonar debug upplýsingar og gögn á ýmsum stigum forvinnslu.

## English

Term project #1 in the course __MLT201F Language resources for software development and research__, spring semester 2019 at the University of Iceland. Stylometric analysis of short anonymous texts in Icelandic.

_Reykjavíkurbréf_ is an anonymous, weekly column in the newspaper _Morgunblaðið_. In this project, the Reykjavíkurbréf in the period 2012-2014 were compared to texts with known authors using Cosine similarity, in an effort to shed light on their authorship. The texts in Morgunblaðið were parsed from the raw data in [the Icelandic Gigaword Corpus](malheildir.arnastofnun.is) which is run by the Árni Magnússon Institute for Icelandic Studies and can be downloaded from [Málföng.is](www.malfong.is).

Although results were inconclusive they imply that more work can be done on the subject.
