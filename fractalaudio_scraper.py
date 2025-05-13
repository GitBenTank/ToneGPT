import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

def scrape_amp_models(url):
    print(f"Scraping Amp Models from: {url}")
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    content_div = soup.find('div', class_='mw-parser-output')

    if not content_div:
        raise ValueError("Couldn't find the main content area on the page.")

    data = []
    for element in content_div.find_all(['p', 'li']):
        text = element.get_text(strip=True)
        if not text:
            continue

        # Heuristic: lines with '(' or mentions of 'amp' or 'model'
        if '(' in text or 'amp' in text.lower() or 'model' in text.lower():
            model_name = text.split('(')[0].strip()
            data.append({
                "Model": model_name,
                "Description": text
            })

    if not data:
        raise ValueError("No amp models found on the page.")

    df = pd.DataFrame(data)
    return df

def scrape_cab_models(url):
    print(f"Scraping Cab Models from: {url}")
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    content_div = soup.find('div', class_='mw-parser-output')

    if not content_div:
        raise ValueError("Couldn't find main content on Cab page.")

    data = []
    for li in content_div.find_all('li'):
        text = li.get_text(strip=True)
        if not text:
            continue

        # Grab cab name before first "(", else full text
        if '(' in text:
            cab_name = text.split('(')[0].strip()
        else:
            cab_name = text.strip()

        data.append({
            "Cab": cab_name,
            "Description": text
        })

    if not data:
        raise ValueError("No cab models found on the page.")

    df = pd.DataFrame(data)
    return df

def save_as_files(df, base_filename):
    df.to_csv(f"{base_filename}.csv", index=False)
    df.to_json(f"{base_filename}.json", orient='records', indent=2)
    print(f"Saved {base_filename}.csv and {base_filename}.json")

if __name__ == "__main__":
    amps_url = "https://wiki.fractalaudio.com/wiki/index.php?title=Amplifier_models_list"
    amps_df = scrape_amp_models(amps_url)
    save_as_files(amps_df, "amps_list")

    cabs_url = "https://wiki.fractalaudio.com/wiki/index.php?title=Cabinet_models_list"
    cabs_df = scrape_cab_models(cabs_url)
    save_as_files(cabs_df, "cabs_list")