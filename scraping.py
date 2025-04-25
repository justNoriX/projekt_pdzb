import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

from data_filtr import filter_data  # <-- poprawiona ścieżka do Twojej funkcji

def scrap_data_to_excel(num_pages, output_filename="otomoto_data.xlsx"):
    """Scrapes data from otomoto.pl and saves to Excel."""
    try:
        service = Service(GeckoDriverManager().install())
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        driver = webdriver.Firefox(service=service, options=options)
    except Exception as e:
        print("❌ Błąd przy uruchamianiu przeglądarki:", e)
        return

    all_data = []

    for page_number in range(1, num_pages + 1):
        print(f"🌐 Strona {page_number}...")
        try:
            url = f"https://www.otomoto.pl/osobowe?page={page_number}"
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "article"))
            )   
            soup = BeautifulSoup(driver.page_source, "html.parser")
            articles = soup.find_all("article", attrs={"data-id": True})
            #print(f"Znaleziono {len(articles)} artykułów na stronie.")

            if not articles:
                print("⚠️ Nie znaleziono ogłoszeń na stronie.")
                continue

            for article in articles:
                link = article.find("a", href=True)
                if link:
                    try:
                        link_url = link['href']
                        driver.get(link_url)
                        
                        # Czekaj na załadowanie szczegółów ogłoszenia
                        WebDriverWait(driver, 1).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='basic_information']"))
                        )
                        
                        article_soup = BeautifulSoup(driver.page_source, "html.parser")
                        
                        # Znajdź sekcję szczegółów ogłoszenia
                        details_section = article_soup.find_all("div", {"data-testid": True})
                        data_dict = {}

                        # Pobierz cenę
                        price_element = article_soup.find("span", class_="offer-price__number")
                        if price_element:
                            price = price_element.get_text(strip=True)
                            data_dict["Cena"] = price

                        if details_section:
                            print("🔍 Szczegóły ogłoszenia znalezione.")
                            # Iteruj po wszystkich `div` z `data-testid`
                            for detail in details_section:
                                #key = detail.get("data-testid", "").strip()  # Pobierz nazwę szczegółu z `data-testid`
                                
                                # Pobierz wszystkie tagi <p> w `div`
                                paragraphs = detail.find_all("p")
                                if len(paragraphs) > 1:  # Jeśli są dwa <p>, pierwszy to nazwa, drugi to wartość
                                    key = paragraphs[0].get_text(strip=True)  # Pobierz nazwę z pierwszego <p>
                                    value = paragraphs[1].get_text(strip=True)  # Pobierz wartość z drugiego <p>
                                else:  # Jeśli brak <p>, sprawdź `aria-label`
                                    value = detail.get("aria-label", "").strip()
                                
                                if key and value:
                                    data_dict[key] = value

                        filtered_data = filter_data(data_dict)
                        all_data.append(filtered_data)
                        print(f"✅ Zebrano dane: {filtered_data}")

                    except Exception as e:
                        print(f"⚠️ Błąd podczas przetwarzania ogłoszenia: {e}")
                        continue

        except Exception as e:
            print(f"❌ Błąd na stronie {page_number}: {e}")
            continue

    driver.quit()

    if all_data:
        df = pd.DataFrame(all_data)
        current_folder = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(current_folder, output_filename)
        df.to_excel(output_path, index=False)
        print(f"📁 Dane zapisane do pliku: {output_filename}")
    else:
        print("⚠️ Nie zebrano żadnych danych. Plik nie został zapisany.")

if __name__ == "__main__":
    scrap_data_to_excel(num_pages=1)
