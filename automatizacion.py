import requests
import json
import pandas as pd
import sys
from bs4 import BeautifulSoup
import shutil
import datetime

#

def proceso():
    print("Hola")
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
        
    
