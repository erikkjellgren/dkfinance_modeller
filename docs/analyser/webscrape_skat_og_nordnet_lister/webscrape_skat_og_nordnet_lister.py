import os

import dkfinance_modeller.utility.webscrape as webscrape

f = open(f"{os.path.dirname(__file__)}/../template_skat_positiv_liste.csv", "r")
isiner = []
for i, line in enumerate(f):
    if i == 0:
        continue
    isiner.append(line.strip("\n"))
f.close()
out = open("skat_positiv_liste_info.csv", "w")
out.write("ISIN;Navn;Index;ÅOP;Replication;Domicil\n")
infoer = webscrape.få_etf_info(isiner, 4)
for info in infoer:
    if info["succes"]:
        out.write(
            f"{info['isin']};{info['navn']};{info['indeks']};"
            f"{info['åop']};{info['replication']};{info['domicile']}\n"
        )
out.close()


f = open(f"{os.path.dirname(__file__)}/../template_nordnet_liste.csv", "r")
isiner = []
skat = {}
for i, line in enumerate(f):
    if i == 0:
        continue
    isiner.append(line.strip("\n").split(";")[1])
    skat[line.strip("\n").split(";")[1]] = line.strip("\n").split(";")[0]
f.close()
out = open("nordnet_liste_info.csv", "w")
out.write("ISIN;Navn;Index;ÅOP;Replication;Domicil;Beskatning\n")
infoer = webscrape.få_etf_info(isiner, 4)
for info in infoer:
    if info["succes"]:
        out.write(
            f"{info['isin']};{info['navn']};{info['indeks']};"
            f"{info['åop']};{info['replication']};{info['domicile']};{skat[str(info['isin'])]}\n"
        )
out.close()
