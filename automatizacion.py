import requests
import json
import pandas as pd
import sys
from bs4 import BeautifulSoup
import shutil
import datetime
import os

#
def getURL(id):
    url = f'https://seia.sea.gob.cl/reportes/publico/rpt_proyectos_comunasAction.php?comuna={id}&presentacion=AMBOS&sector='

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')

    records = []
    columns = []
    for tr in table.findAll("tr"):
        ths = tr.findAll("th")
        if ths != []:
            for each in ths:
                columns.append(each.text)
        else:
            trs = tr.findAll("td")
            record = []
            for each in trs:
                try:
                    link = each.find('a')['href']
                    text = each.text
                    record.append(link)
                    record.append(text)
                except:
                    text = each.text
                    record.append(text)
            records.append(record)
    columns.insert(1, 'Link')
    df = pd.DataFrame(data=records, columns = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])#, columns = columns)
    df2 = df[["2","3"]]
    return df2

def proceso():
    print("Hola")
    ref = pd.read_excel("referenciaSEIA.xlsx")
    for i in range(len(ref)):    
        idComuna = ref["codigo"][i]
        comuna = ref["comunas"][i]
        print(comuna)
        df = getURL(idComuna)
        df2 = df.drop([0],axis=0)
        df3 = pd.read_html(f"https://seia.sea.gob.cl/reportes/publico/rpt_proyectos_comunasAction.php?comuna={idComuna}&presentacion=AMBOS&sector=")
        dfFinal = df3[1]
        dfFinal["URL"] = list(df2["2"])
        dfFinal["Comuna"] = comuna
        #print(len(df2))
        #print(len(dfFinal))
        #break
        dfFinal.to_excel(f"data/{comuna}.xlsx", index=False)
        ejemplo_dir = 'data/'
        with os.scandir(ejemplo_dir) as ficheros:
            ficheros = [fichero.name for fichero in ficheros if fichero.is_file()]


        salida = []
        for i in ficheros:
            if(".xlsx" in i):
                url = f'data/{i}'
                df = pd.read_excel(url)
                #print(len(df))
                #print(i)
                salida.append(df)
        
        dfFinal = pd.concat(salida)
        dfFinal.to_excel(r"Consolidado/Consolidado.xlsx", index=False)
        shutil.copy (r'Consolidado/Consolidado.xlsx', f"Legacy/Consolidado_{datetime.datetime.now().strftime('%Y-%m-%d')}.xlsx")
        return 

if __name__ == '__main__':
    try:
        proceso()
    except:
        try:
            proceso()
        except:
            error = sys.exc_info()[1]
            print(error)
        
    
