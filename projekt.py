import re
from urllib.request import urlopen

link = 'https://seer.cancer.gov/statfacts/'
spletna_stran = urlopen(link).read().decode('UTF-8')

prvi_indeks = spletna_stran.find('alphaList')
zadnji_indeks = spletna_stran.find('</main>')

podatek1 = spletna_stran[prvi_indeks:zadnji_indeks].replace('\r', '').replace('\t', '').replace('\n', '')
neuporaben_seznam = re.split(r'<li>|</li>', podatek1)

slovar = {}
for li in neuporaben_seznam:
    if '</a>' in li:
        tema = re.search(r'(<a.*>)(.*)(</a>)',li).group(2)
        povezave_neuporabne = re.search(r'(<a.*>)(.*)(</a>)',li).group(1)
        povezave = re.search(r'(<a href=")(.*)(">)',povezave_neuporabne).group(2)
        slovar[tema] = povezave
#print(slovar['Tongue'])  

link_tema = 'https://seer.cancer.gov'   
print(urlopen(link_tema + slovar['Tongue']).read().decode('UTF-8'))     

