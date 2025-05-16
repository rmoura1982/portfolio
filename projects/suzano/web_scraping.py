from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd


url_chinese_caixin = "https://br.investing.com/economic-calendar/chinese-caixin-services-pmi-596"
url_usd_cny = "https://br.investing.com/currencies/usd-cny-historical-data"
chrome_driver_path = "files\chromedriver.exe"

def web_conection(url_string, chrome_driver_path):
    url = url_string
    chrome_driver = chrome_driver_path
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    service = Service(chrome_driver)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    return driver

def scrape_chinese_caixin():
    driver = web_conection(url_chinese_caixin, chrome_driver_path)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "eventHistoryTable596")))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.find("table", {"id": "eventHistoryTable596"})
        data = []
        if table:
            rows = table.find_all("tr")
            for row in rows:
                columns = row.find_all("td")
                if columns:
                    date = columns[0].text.strip()
                    actual_state = columns[2].text.strip()
                    forecast = columns[3].text.strip()
                    previous = columns[4].text.strip()
                    data.append({
                        "Date": date,
                        "Actual": actual_state,
                        "Forecast": forecast,
                        "Previous": previous
                    })
            df = pd.DataFrame(data)
        else:
            print("Tabela não encontrada!")
    except Exception as e:
        print({e})
    driver.quit()
    return df


def scrape_usd_cny():
    driver = web_conection(url_usd_cny, chrome_driver_path)
    try:
        date_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.relative'))
        )
        date_button.click()
        date_input_start = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.relative'))
        )
        date_input_start.click()
        driver.execute_script("arguments[0].value = arguments[1]", date_input_start, '1991-01-01')
        apply_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'cursor-pointer')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", apply_button)
        driver.execute_script("arguments[0];", apply_button)
        apply_button.click()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.find("table")
        data = []
        if table:
            rows = driver.find_elements(By.CSS_SELECTOR, 'tbody tr')
            for row in rows:
                columns = row.find_elements(By.TAG_NAME, 'td')
                if len(columns) >= 7:
                    date = columns[0].text.strip()
                    close = columns[1].text.strip()
                    opening = columns[2].text.strip()
                    high = columns[3].text.strip()
                    low = columns[4].text.strip()
                    volume = columns[5].text.strip()
                    variation = columns[6].text.strip()
                    data.append({
                        "Date": date,
                        "Último": close,
                        "Abertura": opening,
                        "Máxima": high,
                        "Mínima": low,
                        "Vol.": volume,
                        "Var%": variation
                    })
            df = pd.DataFrame(data)  
    except Exception as e:
        print({e})
    driver.quit()
    return df
