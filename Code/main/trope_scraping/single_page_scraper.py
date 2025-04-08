
## 3rd party packages
import requests
from bs4 import BeautifulSoup
import pandas as pd

## python packages
import os

## homebrew packages
from Utility.toolbox import find_repo_root
root = find_repo_root()


class TropeScraper:
    def __init__(self, root):
        self.path = os.path.join(root, 'Data/home_scraped_tropes')
        os.makedirs(self.path, exist_ok=True)  # Ensure directory exists

    def trope_scrape(self, url: str) -> BeautifulSoup:
        headers = {
            "referer": "https://tvtropes.org/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers)
        return BeautifulSoup(response.text, 'lxml')
    
    def save_scrape(self, url: str, movie_name: str):
        soup = self.trope_scrape(url)
        file_path = os.path.join(self.path, f"{movie_name}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(soup.prettify())
        print(f"Scraped content saved to {file_path}")

    def save_tropes(self, url: str, movie_name: str, blank=False):
        df = self.extract_tropes(url)
        file_path = os.path.join(self.path, f"{movie_name}.csv")
        df.to_csv(file_path, index=False)
        print(f"Scraped frame saved to {file_path}")

        # now create a fake one
        if blank:
            for col in [ 
            "Inverted?/Defied?", "Averted/Subverted?", "Rough Occurence in movie",
            "Background?", "Setups?", "Start Time", "End Time", "Total Time"
            ]:
                df[col] = ""
            print(df)
            file_path = os.path.join(self.path, f"{movie_name}_blank.csv")
            df.to_csv(file_path, index=False)


    def extract_tropes(self, url: str) -> pd.DataFrame:
        soup = self.trope_scrape(url)
        tropes = []
        
        for li in soup.find_all('li'):
            trope_name_tag = li.find('a', class_='twikilink')
            if trope_name_tag:
                trope_name = trope_name_tag.get_text(strip=True)
                trope_text = ' '.join(li.stripped_strings)
                trope_text = trope_text[len(f"{trope_name} :"): ]
                tropes.append((trope_name, trope_text))

        
        df = pd.DataFrame(tropes, columns=["Trope", "Description"])
        return df
    

if __name__ == "__main__":
    ts = TropeScraper(root)
    url = input("Enter URL: ")
    movie_name = input("Enter movie name: ")
    ts.save_tropes(url, movie_name, blank=True)
