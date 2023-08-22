# projektna-naloga
V python datoteki je zapisana koda mojega projekta. V prvih 7 vrsticah so uvožene vse knjižnjice, ki sem jih potrebovala.
V naslednjih vrsticah sem uvozila linke za spletno stran iz katere sem želela vzeti podatke. 
V vrstici 15 sem z .find poiskala vse podatke, zajete v razredu alphaList, ker sem opazila da se vsi moji podatki nahajajo tam.
Nato sem naredila slovar_podrocij, kamor sem shranila povezave do spletnih mest z mojimi podatki.
Prav tako sem se odločila, da bom nekatere teme, ki niso imele dovolj podatkov izpustila.
Za pridobivanje samih podatkov sem napisala funkcijo pridobi_podatke, ki gre ćez vse povezave in poišče željene podatke te pa nato shrani v slovar ppodatki.
Podatke sem nato shranila v večji slovar, kjer so ključi tipi raka, vrednosti pa so podatki iz prejšnjega slovarja.
Vnaslednjih vrsticah sem ustvarila mapo grafi, kamor se bodo shranjevali izrisani grafi, da bo naloga bolj pregledna.
Potem sem iz slovarja ustvarila csv datoteko, da bodo podatki bolj pregledni.
Za predelavo podatkov sem v vrstici 150 napisala funkcijo predelaj_csv_podatke, ki naredi vse potrebne izboljšave, ki so potrebni za predstavitev podatkov.
Nato sem ustvarila tabele, kjer sem podatke ustrezno razvrstila in uredila morebitne težave.
Poleg tabel sem želela podatke še grafično predstaviti, zato sem napisala funkcijo generiraj graf, ki izriše grafe za pričakovane nove primere, pričakovane smrtne primere, delež novih primerov in delež smrtnih primerov.
Z funkcijo generiraj_graf_primerjave sem  ustvarila grafe, ki za vsak tip raka posebaj primerjajo delež moških in delež žensk, ki dobijo in umrejo za tem rakom.
V vrsticah od 210 do 219 sem še popravila podatke, tako da so bili ustrezne oblike za funkcijo.
