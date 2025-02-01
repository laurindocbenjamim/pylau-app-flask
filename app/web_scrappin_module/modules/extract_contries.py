import requests
from bs4 import BeautifulSoup
import pandas as pd

db = 'countries.db'
table = 'countries'

csv_file = 'countries.csv'
phonenumberULR = 'https://worldpopulationreview.com/country-rankings/phone-number-length-by-country'
with_length = 'https://www.iban.com/dialing-codes'
url = 'https://countrycode.org/'

def extract_countries(url):
    count = 0
    
    if url is None:
        return None
    
    df = pd.DataFrame(columns=['Country', 'Country Code', 'ISO Code'])
    columns = []
    html_page = requests.get(url).text
    data_soup = BeautifulSoup(html_page, 'html.parser')
    thead = data_soup.find_all('thead')
    tr = data_soup.find_all('tr')
    tbody = data_soup.find_all('tbody')
    rows = tbody[0].find_all('tr')

    if thead is not None and len(thead) > 0:
        for th in thead[0].find_all('th'):
            columns.append(th.contents[0].replace('\n', '').replace('\r', '').replace(' ', '').replace('\t', ''))
        
        #df = pd.DataFrame(columns=columns)     
    if rows is not None and len(rows) > 0:
        for row in rows:
            if count < len(rows):
                col = row.find_all('td')
               
                if len(col) != 0:
                    data_dict = {
                        "Country": col[0].contents[0],
                        "Country Code": col[1].contents[0],
                        "ISO Code": col[2].contents[0],
                        "Code": col[3].contents[0],
                        "GIN": col[4].contents[0]
                    }
                    """
                    df = pd.concat([df, pd.DataFrame([[col[0].contents[0], 
                                                       col[1].contents[0], 
                                                       col[2].contents[0]
                                                       ]], 
                                                       columns=columns)
                                                       ], ignore_index=True)
                    """
                    df1 = pd.DataFrame(data_dict, index=[0])
                    df = pd.concat([df, df1], ignore_index=True)
                    
                    count += 1
            else:
                break        
        
        return df
    else:
        return None


df = extract_countries(url)
print(df)