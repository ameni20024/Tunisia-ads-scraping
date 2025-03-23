import pandas as pd
from bs4 import BeautifulSoup as soup
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Fonction de scraping
def scrape_tayara():
    service = Service(r"C:\webdrivers\chromedriver.exe")
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)

    urls = [f"https://www.tayara.tn/ads/c/Immobilier/?page={i}" for i in range(1, 11)]
    
    data = []

    for url in urls:
        print(f"Scraping : {url}")
        driver.get(url)
        time.sleep(2)  # Pause pour permettre le chargement du contenu

        # Parser le contenu HTML avec BeautifulSoup
        page = soup(driver.page_source, 'html.parser')
        house_containers = page.find_all("article", class_="mx-0")

        for house in house_containers:
            # Titre de l'article
            nom_article = house.find('h2', class_="card-title font-arabic text-sm font-medium leading-5 text-gray-800 max-w-min min-w-full line-clamp-2 my-2")
            nom_article = nom_article.text.strip() if nom_article else "Non spécifié"
            
            # Prix
            prix = house.find('data', class_="font-bold font-arabic text-red-600 undefined")
            prix = prix.text.strip() if prix else "Non spécifié"
            
            # Catégorie
            categorie = house.find('span', class_="truncate text-3xs md:text-xs lg:text-xs w-3/5 font-medium text-neutral-500")
            categorie = categorie.text.strip() if categorie else "Non spécifiée"
            
            # Localisation
            localisation = house.find_all('span', class_="line-clamp-1 truncate text-3xs md:text-xs lg:text-xs w-3/5 font-medium text-neutral-500")
            localisation = localisation[-1].text.strip() if localisation else "Non spécifiée"
            
            # Ajouter à la liste des données
            data.append({
                'Nom': nom_article,
                'Prix': prix,
                'Catégorie': categorie,
                'Localisation': localisation
            })

    driver.quit()

    # Créer un fichier CSV si des données sont disponibles
    if data:
        df = pd.DataFrame(data)
        df.to_csv('annonces_tayara.csv', index=False)
        print(f"{len(df)} articles extraits et sauvegardés dans 'annonces_tayara.csv'")
    else:
        print("Aucune donnée trouvée lors du scraping.")

    return data
