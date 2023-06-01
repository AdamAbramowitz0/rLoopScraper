import pandas as pd
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select
from PIL import Image
import requests, sys

print(sys.argv[0])


dataframe = pd.read_excel(sys.argv[1])
print(len(dataframe.GeneID))
dataframe2 = pd.DataFrame({
    "GeneID": [],
    "Control":[],
    "Bigger": [],
    "BiggerEqual1":[],
    "BiggerEqual2":[]})

#for i in range(0,len(dataframe.GeneID)):
for i in range(0,len(dataframe.GeneID)):
    
    browser = webdriver.Firefox()
    x=dataframe.GeneID[i]
    try:

    
        server = "https://rest.ensembl.org"
        ext = '/lookup/symbol/homo_sapiens/'+x+'?content-type=application/json'

        r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
        
        if not r.ok:
            r.raise_for_status()
            sys.exit()
        
        decoded = r.json()
        print(decoded)
        x=decoded['id']
        print(x)
        print("ENS")
        browser.get("http://r-loop.org/?gene="+x+"&org=human")
        time.sleep(12)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        browser.maximize_window()
        browser.save_screenshot('screenie.png')


        with Image.open("screenie.png") as im:
            px = im.load()

        print(px[1848, 420])
        ppl = 0
        for l in range(0,3584):
            for h in range(0,1942):
                if px[l,h] == (148,0,211,255):
                    ppl+=1
                h+=1
            l+=1

    
    except:
        ppl = -1
    dataframe1 = pd.DataFrame({
    "GeneID": [dataframe.GeneID[i]],
    "Purple":[ppl]})
    print(dataframe.GeneID[i])
    print(ppl)
        
    dataframe2 = pd.concat([dataframe2, dataframe1])

    dataframe2.to_excel(sys.argv[2])
    browser.delete_all_cookies()
    browser.close()
