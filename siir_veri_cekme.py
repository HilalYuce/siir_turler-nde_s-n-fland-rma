import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import random
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

lock = threading.Lock()

def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=chrome_options)

def get_poem_content(url, driver):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "pd-title-a")))

    soup = BeautifulSoup(driver.page_source, "html.parser")

    try:
        title_div = soup.find("div", class_="pd-title-a")
        title = title_div.find("h3").get_text()

        text_div = soup.find("div", class_="pd-text")
        paragraphs = text_div.find_all("p")
        poem_text = "\n".join([paragraph.get_text().strip() for paragraph in paragraphs])

        return title, poem_text

    except Exception as e:
        print("Bir hata oluştu:", e)
        return None, None

def save_poems_bulk(poems_data, filename="category_agac.csv"):
    rows = []
    titles_set = set()  

    for title, poem_lines in poems_data:
        if title in titles_set:
            continue  
        titles_set.add(title)
        rows.append({"title": title, "poem": ""})
        rows.extend([{"title": "", "poem": line} for line in poem_lines])
        rows.append({"title": "", "poem": ""})  
    
    df = pd.DataFrame(rows)
    with open(filename, 'a', encoding="utf-8-sig", newline='') as f:
        df.to_csv(f, header=f.tell()==0, index=False)
    print(f"{len(poems_data)} adet şiir '{filename}' dosyasına topluca kaydedildi.")

def collect_poems(base_url, categories):
    driver = initialize_driver()

    for category in categories:
        page = 1
        processed_urls = set()  
        while True:
            page_url = f"{base_url}/{category}/siirleri/" if page == 1 else f"{base_url}/{category}/siirleri/sayfa-{page}/"
            print(f"İşlenen URL: {page_url}")
            driver.get(page_url)

           
            try:
                WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "more-button")))
            except:
                print(f"Sayfa yüklenirken zaman aşımı: {page_url}")
                break

            soup = BeautifulSoup(driver.page_source, "html.parser")
            links = soup.find_all("a", class_="more-button btn", href=True)
            
            if not links:  
                print(f"'{category}' kategorisi için son sayfa: {page}")
                break
            
            category_urls = []
            for link in links:
                full_url = urljoin(page_url, link["href"])

                with lock:
                    if full_url not in processed_urls:
                        processed_urls.add(full_url)
                        category_urls.append(full_url)

            poems_data = []
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = {executor.submit(get_poem_content, url, driver): url for url in category_urls}
                for future in as_completed(futures):
                    title, poem_text = future.result()
                    if title and poem_text:
                        poem_lines = poem_text.splitlines()
                        poems_data.append((title, poem_lines))
            
            if poems_data:
                save_poems_bulk(poems_data)
            
            page += 1

    driver.quit()

base_url = "https://antoloji.com"
categories = ["agac"]

collect_poems(base_url, categories)
