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


def extract_countries(url):
    count = 0

    if url is None:
        return None

    df = pd.DataFrame()
    columns = []
    html_page = requests.get(url).text
    data_soup = BeautifulSoup(html_page, "html.parser")
    thead = data_soup.find_all("thead")
    tr = data_soup.find_all("tr")
    tbody = data_soup.find_all("tbody")
    rows = tbody[0].find_all("tr")

    if thead is not None and len(thead) > 0:
        for th in thead[0].find_all("th"):
            columns.append(
                th.contents[0]
                .replace("\n", "")
                .replace("\r", "")
                .replace(" ", "")
                .replace("\t", "")
            )

        # df = pd.DataFrame(columns=columns)
    if rows is not None and len(rows) > 0:
        for row in rows:
            if count < len(rows):
                col = row.find_all("td")

                if len(col) != 0:
                    data_dict = {}
                    try:
                        #myList = []
                        #for i in range(len(col)):
                            #myList.append(col[i].contents[0])
                        #print(myList)
                    
                        
                        
                        data_dict = {
                            "Country": col[0].contents[0],
                            "Country Code": col[1].contents[0],
                            "ISO Code": col[2].contents[0],
                            "Population": col[3].contents[0],
                            "Area": col[4].contents[0],
                        }

                        df1 = pd.DataFrame(data_dict, index=[0])
                        df = pd.concat([df, df1], ignore_index=True)
                        

                        """
                        
                        df = pd.concat(
                            [
                                df,
                                pd.DataFrame(
                                    [
                                        [
                                            col[0].contents[0],
                                            col[1].contents[0],
                                            col[2].contents[0],
                                            col[3].contents[0],
                                            col[4].contents[0],
                                            col[5].contents[0],
                                        ]
                                    ],
                                    columns=columns,
                                ),
                            ],
                            ignore_index=True,
                        )
                        """
                    except IndexError as e:
                        print(f"IndexError: {e}")
                    except Exception as e:
                        print(f"Error {e}")
                    count += 1
                
            else:
                break

        return df
    else:
        return None



def extract_countries_2(url):
    count = 0
    data_dict = {}
    if url is None:
        return None

    df = pd.DataFrame()
    columns = []
    html_page = requests.get(url).text
    data_soup = BeautifulSoup(html_page, "html.parser")
    thead = data_soup.find_all("thead")
    tr = data_soup.find_all("tr")
    tbody = data_soup.find_all("tbody")
    rows = tbody[0].find_all("tr")

    if thead is not None and len(thead) > 0:
        for th in thead[0].find_all("th"):
            columns.append(
                th.contents[0]
                .replace("\n", "")
                .replace("\r", "")
                .replace(" ", "")
                .replace("\t", "")
            )

        # df = pd.DataFrame(columns=columns)
        
    if rows is not None and len(rows) > 0:
        for row in rows:
            if count < len(rows):
                col = row.find_all("td")

                if len(col) != 0:
                    

                    """
                    if 'Antarctica' in col[0].contents[0]:
                        print("+================ Antarctica ===============+")
                        for a in range(len(col)):
                            item = get_each_item(col, a)
                            print(f"{a} - {'N/A' if item is None else item}")
                        
                        break
                    """

                    try:
                        myList = []
                        for a in range(len(col)):
                            
                            if len(col) == len(columns):
                                item = get_each_item(col, a)
                                print(f"{a} - {'N/A' if item is None else item}")
                                myList.append('null' if item is None else item)
                                data_dict[columns[a]] = 'N/A' if item is None else item
                                
                            else:
                                data_dict[columns[a]] = "N/A"
                                #myList.append("N/A")
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

                        if count == 20:
                            
                            print(df)
                            break
                        """    
                        print(" ================ Data Dictionary ================")
                        

                        df1 = pd.DataFrame(data_dict, index=[0])
                        df = pd.concat([df, df1], ignore_index=True)
                        #print("+================ Data Frame ===============+")
                        #print(df.head(11))
                        for i in range(len(col)):
                            #myList.append(col[i].contents[0])
                            a = 1
                        #print(myList)
                        

                        
                        
                        df = pd.concat(
                            [
                                df,
                                pd.DataFrame(
                                    [
                                        [
                                            col[0].contents[0],
                                            col[1].contents[0],
                                            col[2].contents[0],
                                            col[3].contents[0],
                                            col[4].contents[0],
                                            col[5].contents[0],
                                        ]
                                    ],
                                    columns=columns,
                                ),
                            ],
                            ignore_index=True,
                        )
                        """
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
    

df = extract_countries(url)
print("\n")
#print(df)

def get_each_item(list, index):
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
#print(df)
