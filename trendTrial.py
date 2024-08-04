from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import io
import json

# Define the list globally
bakilacakUrunAdeti = []

def initialize_browser():
    """Initialize the Firefox browser."""
    try:
        browser = webdriver.Firefox()
        return browser
    except Exception as e:
        print(f"Error initializing browser: {e}")
        return None

def sayfayaGir(browser):
    """Navigate to the desired page based on user input."""
    anahtarKelime = input("Aranan Anahtar Kelimesini Yazınız: ")
    url = f"https://www.trendyol.com/sr?q={anahtarKelime}&qt={anahtarKelime}&st={anahtarKelime}&os=1"
    browser.get(url)

def scrollAsagiIndir(browser):
    """Scroll down the page to load more products."""
    jsScroll = "window.scrollBy(0,750)"
    sayac = 0
    kacSaniye = int(input("Kaç Adet Ürüne Bakılsın: "))
    bakilacakUrunAdeti.append(kacSaniye)  # Use the global list
    print("Bakılacak Ürün Adeti:", bakilacakUrunAdeti)
    kacSaniye = kacSaniye / 6
    if kacSaniye > 59:
        print("İşlem Süresi:", float(kacSaniye / 60), "Dakika")
    else:
        print("İşlem Süresi:", kacSaniye, "Saniye")
    while sayac <= kacSaniye:
        time.sleep(1)
        sayac += 1
        browser.execute_script(jsScroll)

def degerlendirmeAnalizi(browser):
    """Perform analysis on product ratings and extract product data."""
    diziBesle = []

    # Selectors for various product attributes
    degerlendirmeSayisi = browser.find_elements(By.CSS_SELECTOR, ".ratings-container")
    degerlendirilenUrununAdi = browser.find_elements(By.CSS_SELECTOR, ".prdct-desc-cntnr-ttl-w")
    urunLink = browser.find_elements(By.CSS_SELECTOR, ".p-card-chldrn-cntnr [href]")
    urunFiyat = browser.find_elements(By.CSS_SELECTOR, ".prc-box-dscntd")
    urunResmi = browser.find_elements(By.CSS_SELECTOR, ".p-card-img")

    degerlendirmeDegeriSayisi = int(input("Değerlendirme Sayısı En Az Kaç Olsun: "))

    for x in range(len(degerlendirmeSayisi)):
        try:
            # Split the text to separate rating and number of reviews
            degerlendirme_text = degerlendirmeSayisi[x].text.strip()
            parts = degerlendirme_text.split()

            if len(parts) == 2:
                # Parse the rating and the review count
                rating = float(parts[0])
                review_count = int(parts[1].strip("()"))

                print(f"Rating: {rating}, Review Count: {review_count}")

                if review_count >= degerlendirmeDegeriSayisi:
                    newFiyat = urunFiyat[x].text
                    diziJ = {
                        'degerlendirmePuani': rating,
                        'degerlendirmeSayisi': review_count,
                        'urunAdi': degerlendirilenUrununAdi[x].text,
                        'urunLinki': urunLink[x].get_attribute('href'),
                        'urunFiyati': float(newFiyat.replace("TL", "").replace(",", ".")),
                        'urunResmi': urunResmi[x].get_attribute("src")
                    }
                    diziBesle.append(diziJ)
            else:
                print(f"Unexpected rating format encountered: {degerlendirme_text}")
        except ValueError as e:
            print(f"ValueError encountered: {e}")
        except IndexError:
            print("Mismatch in the number of elements. Check selectors.")
            break

    if degerlendirmeDegeriSayisi == 0:
        for x in range(min(bakilacakUrunAdeti[0], len(degerlendirmeSayisi))):
            try:
                newFiyat = urunFiyat[x].text
                diziJ = {
                    'degerlendirmePuani': degerlendirilenUrununAdi[x].text,
                    'urunAdi': degerlendirilenUrununAdi[x].text,
                    'urunLinki': urunLink[x].get_attribute('href'),
                    'urunFiyati': float(newFiyat.replace("TL", "").replace(",", ".")),
                    'urunResmi': urunResmi[x].get_attribute("src")
                }
                diziBesle.append(diziJ)
            except IndexError:
                print("Index error when processing product data.")
                break

    with io.open('selam.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(diziBesle, ensure_ascii=False))

def theEndWebSite(browser):
    """Navigate to the end website."""
    print("(FC Yazılım) Web Sayfamıza Yöneliyorsunuz...")
    time.sleep(1)
    urlPathProject = "file:///Applications/XAMPP/xamppfiles/htdocs/trendYolEntergrasyonBotu/index.html"
    browser.get(urlPathProject)

def main():
    """Main function to orchestrate the web scraping."""
    browser = initialize_browser()
    if browser is None:
        return

    try:
        sayfayaGir(browser)
        time.sleep(1)
        scrollAsagiIndir(browser)
        time.sleep(2)
        degerlendirmeAnalizi(browser)
        time.sleep(1)
        theEndWebSite(browser)
    finally:
        browser.quit()

if __name__ == "__main__":
    main()
