from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import io
import json

browser = webdriver.Firefox()


def sayfayaGir():
    anahtarKelime = input("Arnan Anahtar Kelimesini Yazınız : ")
    browser.get("https://www.trendyol.com/sr?q={}&qt={}&st={}&os=1".format(
        anahtarKelime, anahtarKelime, anahtarKelime))


bakilacakUrunAdeti = []
def scrollAsagiIndir():
    jsScroll = """
        window.scrollBy(0,750)
    """
    sayac = 0
    kacSaniye = int(int(input("Kaç Adet Ürüne Bakılsın :  ")))
    bakilacakUrunAdeti.append(kacSaniye)
    print("Bakılacak Ürün Adeti" , bakilacakUrunAdeti)
    kacSaniye = kacSaniye / 6
    if kacSaniye > 59:
        print("İslem Süresi : " , float(kacSaniye / 60) , " Dk")
    else:
        print("İslem Süresi : " , kacSaniye , " Saniye")
    while sayac <= kacSaniye:
        time.sleep(1)
        sayac += 1
        browser.execute_script(jsScroll)


def degerlendirmeAnalizi():
    diziBesle = []
    artiSayac = 0

    
    degerlendirmeSayisi = browser.find_elements(By.CSS_SELECTOR,".ratings-container")
    degerlendirilenUrununAdi =browser.find_elements(By.CSS_SELECTOR,".prdct-desc-cntnr-ttl-w.two-line-text")
    urunLink = browser.find_elements(By.CSS_SELECTOR,".p-card-chldrn-cntnr [href]")
    urunFiyat =browser.find_elements(By.CSS_SELECTOR,".prc-box-dscntd")
    urunResmi =browser.find_elements(By.CSS_SELECTOR,".p-card-img")


    
    for x in degerlendirmeSayisi:
        artiSayac += 1
    
    degerlendirmeDegeriSayisi = int(input("Değerlendirme Sayısı En Az Kaç Olsun : "))
    for x in range(0, artiSayac):

        gelenDegeriStrConvert = str(degerlendirmeSayisi[x].text)

        if gelenDegeriStrConvert.endswith(")"):
            degerlendirmeConvertToNumeric = gelenDegeriStrConvert.strip("()")
            analizDegeri = int(degerlendirmeConvertToNumeric)
        else:
            analizDegeri = -1



        
        if (analizDegeri != 1 and analizDegeri >= degerlendirmeDegeriSayisi or analizDegeri == degerlendirmeDegeriSayisi):
            newFiyat = str(urunFiyat[x].text)
            diziJ = {
                'degerlendirmePuani': analizDegeri,
                'urunAdi': degerlendirilenUrununAdi[x].text,
                'urunLinki': urunLink[x].get_attribute('href'),
                'urunFiyati': float(newFiyat.replace("TL","").replace(",",".")),
                'urunResmi':  urunResmi[x].get_attribute("src")
            }
            diziBesle.append(diziJ)


        






    if degerlendirmeDegeriSayisi == 0 :
        for x in range(0, bakilacakUrunAdeti[0]):
            newFiyat = str(urunFiyat[x].text)
            diziJ = {
                'degerlendirmePuani': degerlendirilenUrununAdi[x].text,
                'urunAdi': degerlendirilenUrununAdi[x].text,
                'urunLinki': urunLink[x].get_attribute('href'),
                'urunFiyati': float(newFiyat.replace("TL","").replace(",",".")),
                'urunResmi':  urunResmi[x].get_attribute("src")
            }
            diziBesle.append(diziJ)




            






    with io.open('selam.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(diziBesle, ensure_ascii=False))


def theEndWebSite():
    print("(FC Yazılım) Web Sayfamıza Yöneliyorsunuz...")
    time.sleep(1)
    urlPathProject  = "C:\\Users\\User\\OneDrive\\Masaüstü\\Programing\\Python\\trendYolAnaliz\\index.html"
    browser.get("")


sayfayaGir()
time.sleep(1)
scrollAsagiIndir()
time.sleep(2)
degerlendirmeAnalizi()
time.sleep(1)
theEndWebSite()