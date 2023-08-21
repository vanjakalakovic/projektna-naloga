import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio

link = 'https://seer.cancer.gov'
link_podrocja = link + '/statfacts/'

spletna_stran = urlopen(link_podrocja).read().decode('UTF-8')
bs_spletna_stran = BeautifulSoup(spletna_stran,'html.parser')


seznam_podrocij = bs_spletna_stran.find('div',attrs={'class':'alphaList'})

slovar = {}

nepotrebne_teme = ["Female Breast Subtypes","Chronic Lymphocytic Leukemia/Small Lymphocytic Lymphoma (CLL/SLL)",'Diffuse Large B-Cell Lymphoma (DLBCL)',
'Follicular Lymphoma','Lip']
for l in seznam_podrocij.find_all('a'):
    #if(l.get_text() == "Esophagus"):
     #   break
    if l.get_text() in nepotrebne_teme: continue
    slovar[l.get_text()] = l.get('href')


#funkcija za pobiranje podatkov iz spletne strani
#od 51 dam lahko v slovar, kot kljuc mu dam ime stolpca(All races M) in kot vrednost podatki_o_novih_moskih, to dam lahko v if zanko
def get_podatki(povezava):
    podatki = {}

    def novi_in_smrtni_primeri(vrsta,podatek):
        for p in podatek.find_all('p'):
            naslov = p.find('span').get_text()
            vrednost = p.find('span').find_next().get_text().replace(',','')
            estimated = re.search(r'^Estimated',naslov)

            if estimated:
                podatki["prb_"+ vrsta] = vrednost
            else:
                podatki["delez_"+ vrsta] = vrednost

    def ostali_podatki(kljuc, podatek):
        tag = 'td'
        if 'povp_starost' in kljuc:
            tag = 'strong'
        podatek_spol = podatek.find(tag).get_text().replace(',','')
        podatki[kljuc] =  podatek_spol 


    link_tema = link + povezava
    spletna_podrocje = BeautifulSoup(urlopen(link_tema).read().decode('UTF-8'),'html.parser')

    def spletna_povezava(oznaka, tip, sez):
        podatki_za_predelavo = spletna_podrocje.find(oznaka, attrs={tip: sez})
        return podatki_za_predelavo

#novi primeri
    if spletna_povezava('div', 'class', ['new', 'glanceBox']): 
        novi_in_smrtni_primeri('novi', spletna_povezava('div', 'class', ['new', 'glanceBox']))

#smrtni primeri
    if spletna_povezava('div', 'class', ['death']):
        novi_in_smrtni_primeri('smrtni',spletna_povezava('div', 'class', ['death'])) 

#podatki o relativnem prezivetje
    if spletna_povezava('div', 'class', ['col-lg-4','offset-lg-1']):
        for div in spletna_povezava('div', 'class', ['col-lg-4','offset-lg-1']).find_all('div'):
            podatki_prezivetje = div.find('strong').get_text()
            podatki["5_letno_realtivno_prezivetje_stevilo"] = podatki_prezivetje

#podatki o novih primerih moski
    if spletna_povezava('table', 'id', ['scrapeTable_04']):
        ostali_podatki('All_races_M', spletna_povezava('table', 'id', ['scrapeTable_04']))

#podatki o novih primerih zenske          
    if spletna_povezava('table', 'id', ['scrapeTable_05']):
        ostali_podatki('All_races_Z',spletna_povezava('table', 'id', ['scrapeTable_05']))

#podatki o povprečni starosti za nove primere    
    if spletna_povezava('div', 'class', ['statSurv']):
        ostali_podatki('povp_starost', spletna_povezava('div', 'class', ['statSurv']))

#podatki o smrtnih primerih moski
    if spletna_povezava('table', 'id', ['scrapeTable_07']):
        ostali_podatki('Death_cases_All_races_M', spletna_povezava('table', 'id', ['scrapeTable_07']))

#podatki o smrtnih primerih zenske
    if spletna_povezava('table', 'id', ['scrapeTable_08']):
        ostali_podatki('Death_cases_All_races_Z', spletna_povezava('table', 'id', ['scrapeTable_08']))

#podatki o povprecni starosti smrti
    if spletna_povezava('div', 'class', ['col-lg-4','offset-lg-1']):
        ostali_podatki('povp_starost_smrti', spletna_povezava('div', 'class', ['statDie']))
        

    return podatki

#podatke damo v prvotni slovar
for k,v in slovar.items():
    #print("Fetching data for: ", k, "(",list(slovar.keys()).index(k) + 1,"/",len(slovar.keys()),")")
    slovar[k] = get_podatki(v)

#sestavimo csv datoteko  
csv_ime_datoteke = "output.csv"

with open(csv_ime_datoteke, mode="w", newline='') as file:
    writer = csv.writer(file)
    
    header = ['Type Of Cancer', 'Estimated New Cases in 2023','(%) of All New Cancer Cases','Estimated Deaths in 2023',
              '(%) of All Cancer Deaths','5-Year Relative Survival ',
              'New Cases Male', 'New Cases Female','Median Age At Diagnosis',
              'Death Cases Male', 'Death Cases Female', 'Median Age At Death']
    writer.writerow(header)
    
    for name, values in slovar.items():
        prb_novi = values.get("prb_novi")
        delez_novi = values.get("delez_novi")
        prb_smrti = values.get("prb_smrtni")
        delez_smrti = values.get("delez_smrtni")
        relativno_prezivetje_stevilo = values.get("5_letno_realtivno_prezivetje_stevilo")
        All_races_M = values.get('All_races_M')
        All_races_Z = values.get('All_races_Z')
        povp_starost = values.get('povp_starost')
        Death_cases_All_races_M = values.get('Death_cases_All_races_M')
        Death_cases_All_races_Z = values.get('Death_cases_All_races_Z')
        povp_starost_smrti = values.get('povp_starost_smrti')

        row = [name, prb_novi, delez_novi, prb_smrti, delez_smrti, relativno_prezivetje_stevilo, 
                All_races_M, All_races_Z, povp_starost, Death_cases_All_races_M ,
               Death_cases_All_races_Z, povp_starost_smrti]
        writer.writerow(row)    


#preberemo csv datoteko, zamenjamo vse podatke ki mankajo z 0 in odstranimo tiste, ki imajo premalo podatkov za obdelavo
vsi_podatki = pd.read_csv('output.csv', encoding='cp1252',index_col= 'Type Of Cancer')
vsi_podatki = vsi_podatki.fillna(0)
vsi_podatki.replace('Sex-specific cancer type', 0, inplace=True)


#številčne podatke spremenimo v numerične za lažjo obdelavo
stolpci = ['Estimated New Cases in 2023','Estimated Deaths in 2023']
vsi_podatki[stolpci] = vsi_podatki[stolpci].applymap(pd.to_numeric, errors='coerce')

#tukaj nevem a je to oki ali je treba dati v CSV datoteke
estimated_new_cases = vsi_podatki[['Estimated New Cases in 2023']].sort_values('Estimated New Cases in 2023', ascending=False)
estimated_new_cases = estimated_new_cases[estimated_new_cases['Estimated New Cases in 2023'] != 0]
estimated_death_cases = vsi_podatki[['Estimated Deaths in 2023']].sort_values('Estimated Deaths in 2023', ascending=False)
estimated_death_cases = estimated_death_cases[estimated_death_cases['Estimated Deaths in 2023'] != 0]
who_gets_this_cancer = vsi_podatki[['New Cases Male', 'New Cases Female','Median Age At Diagnosis']].replace(0 , '/')
who_dies_from_this_cancer = vsi_podatki[['Death Cases Male', 'Death Cases Female', 'Median Age At Death']].replace(0 , '/')
survival_rate = vsi_podatki[[ '5-Year Relative Survival ']].replace(0 , '/')



#Stolpicni diagrami za novi primeri in smrtni primeri za 2023

ax1 = estimated_new_cases.plot(kind='barh', legend=False, figsize=(25,8), width = 0.8, color = '#4169E1')
ax1.set_title('Estimated New Cases in 2023')
ax1.set_ylabel(' ')
plt.savefig('Estimated New Cases in 2023.jpg', format='jpeg')
plt.close()

ax2 = estimated_death_cases.plot(kind='barh', legend=False, figsize=(25,8), width = 0.8, color = '#4169E1')
ax2.set_title('Estimated Deaths in 2023')
ax2.set_ylabel(' ')
plt.savefig('Estimated Deaths in 2023.jpg', format='jpeg')
plt.close()


#stolpični diagrami za tipe raka ločeno glede na moške in ženske...novi primeri in smrtni primeri
moski_zenske_novi = vsi_podatki[['New Cases Male', 'New Cases Female']]
moski_zenske_novi.loc[:, ['New Cases Male', 'New Cases Female']] = moski_zenske_novi[['New Cases Male', 'New Cases Female']].applymap(pd.to_numeric, errors='coerce')

for index, row in moski_zenske_novi.iterrows():
    values = row.values
    
    plt.bar(range(len(values)), values, color = ['#A4D3EE','#FFAEB9'])
    
    plt.ylim(bottom=0)
    plt.title(f'Type of cancer: {index}')
    
    plt.savefig(f'bar_plot_new_cases_{index}.jpg', format='jpeg')
    plt.clf()


moski_zenske_smrtni = vsi_podatki[['Death Cases Male', 'Death Cases Female']]
moski_zenske_smrtni.loc[:, ['Death Cases Male', 'Death Cases Female']] = moski_zenske_smrtni[['Death Cases Male', 'Death Cases Female']].applymap(pd.to_numeric, errors='coerce')

for index, row in moski_zenske_smrtni.iterrows():
    values = row.values
    
    plt.bar(range(len(values)), values, color = ['#A4D3EE','#FFAEB9'])
    
    plt.ylim(bottom=0)
    plt.title(f'Type of cancer: {index}')
    
    plt.savefig(f'bar_plot_death_cases_{index}.jpg', format='jpeg')
    plt.clf()


#podatki za risanje stolpičnih diagramov: sem probala yrisat ampak pride dost čudn 
procenti = vsi_podatki[['(%) of All New Cancer Cases','(%) of All Cancer Deaths']]
procenti = procenti[procenti['(%) of All New Cancer Cases'] != 0]

procenti.loc[:, '(%) of All New Cancer Cases'] = procenti['(%) of All New Cancer Cases'].str.replace('%','')
procenti.loc[:, '(%) of All Cancer Deaths'] = procenti['(%) of All Cancer Deaths'].str.replace('%','')
procenti.loc[:,['(%) of All New Cancer Cases','(%) of All Cancer Deaths']] = procenti[['(%) of All New Cancer Cases','(%) of All Cancer Deaths']].applymap(pd.to_numeric, errors='coerce')

procenti_novi = procenti[['(%) of All New Cancer Cases']]
procenti_smrtni = procenti[['(%) of All Cancer Deaths']]

ax3 = procenti_novi.plot(kind='barh', legend=False, figsize=(25,8), width = 0.8, color = '#4169E1')
ax3.set_title('(%) of All New Cancer Cases')
ax3.set_ylabel('')
plt.savefig('(%) of All New Cancer Cases.jpg', format='jpeg')
plt.close()

ax4 = procenti_smrtni.plot(kind='barh', legend=False, figsize=(25,8), width = 0.8, color = '#4169E1')
ax4.set_title('(%) of All Cancer Deaths')
ax4.set_ylabel(' ')
plt.savefig('(%) of All Cancer Deaths.jpg', format='jpeg')
plt.close()