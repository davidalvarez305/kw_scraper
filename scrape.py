import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import re
from sheets import write_values

def scrape():
    load_dotenv()
    WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/List_of_sports"
    resp = requests.get(WIKIPEDIA_URL).text
    html = BeautifulSoup(resp, 'html.parser')

    values_to_write = [['keyword', 'group', 'completed', 'products crawled']]
    rows = []

    main_content = html.find("div", { "id": "bodyContent" })
    list_elements = main_content.find_all("li")

    for li in list_elements:
        r = bool(re.match(r'''<li><a href="\/wiki\/([A-Za-z0-9])\w+" title="([0-9A-Za-z ]*)">([A-Za-z ]*)<\/a><\/li>''', str(li)))
        if r:
            rows.append([li.find('a').string, 'sport', 'FALSE', 0])
    
    values_to_write += rows

    write_values(spreadsheet_id=str(os.environ.get('SPREADSHEET')), range="Amazon!A:D", values=values_to_write)

scrape()