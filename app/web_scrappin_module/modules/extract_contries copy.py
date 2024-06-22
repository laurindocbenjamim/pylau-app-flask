import requests
from bs4 import BeautifulSoup
import pandas as pd

db = "countries.db"
table = "countries"

csv_file = "countries.csv"
phonenumberULR = (
    "https://worldpopulationreview.com/country-rankings/phone-number-length-by-country"
)
with_length = "https://www.iban.com/dialing-codes"
url = "https://countrycode.org/"


def extract_countries_2(url):
    count = 0
    data_dict = {}
    if url is None:
        return None

    df = pd.DataFrame()
    columns = []
    html_page = requests.get(url).text
    data_soup = BeautifulSoup(html_page, "html.parser")

    extract_tables(url)

    table = data_soup.find_all("table")
    thead = data_soup.find_all("thead")
    tr = data_soup.find_all("tr")
    tbody = data_soup.find_all("tbody")
    rows = tbody[0].find_all("tr")

    print(f"Tables: {len(table)}")

   

    columns = get_each_head_item(thead)

    if rows is not None and len(rows) > 0:
        for row in rows:
            if count < len(rows):
                col = row.find_all("td")

                if len(col) != 0:

                    try:
                        myList = []
                        for a in range(len(col)):
                            
                            if len(col) == len(columns):
                                item = get_each_tbody_item(col, a)
                                #print(f"{a} - {'N/A' if item is None else item}")
                                myList.append('null' if item is None else item)
                                data_dict[columns[a]] = 'N/A' if item is None else item
                                
                            else:
                                data_dict[columns[a]] = "null"
                        df = pd.concat(
                                [
                                    df,
                                    pd.DataFrame(
                                        [
                                            myList
                                        ],
                                        columns=columns,
                                    ),
                                ],
                                ignore_index=True,
                            )                           
                       
                    except IndexError as e:
                        print(f"IndexError: {e}")
                    except Exception as e:
                        print(f"Error {e}")
                    count += 1
                
            else:
                break

        return df
    
    print(data_dict)
    return None

def extract_tables(url):
  
    if url is None:
        return None

    html_page = requests.get(url).text
    data_soup = BeautifulSoup(html_page, "html.parser")
    table = data_soup.find_all("table")

    if len(table) > 0:
        return table
    
    return []

def get_each_head_item(thead):
    columns = []
    try:
        if thead is not None and len(thead) > 0:
            for th in thead[0].find_all("th"):
                columns.append(
                    th.contents[0]
                    .replace("\n", "")
                    .replace("\r", "")
                    .replace(" ", "")
                    .replace("\t", "")
                )
        return columns    
    except IndexError as e:
        return None
    except Exception as e:
        return None
    return None

def get_each_tbody_item(list, index):
    try:
        return list[index].contents[0].text
    except IndexError as e:
        return None
    except Exception as e:
        return None
    
print("\n")
print("Second function")
print("\n")
df = extract_countries_2(url)
print(df.head(20))
