import json
import os
import requests
from dotenv import load_dotenv
from gmail import send_mail

from sheets import get_values, write_values

def main():
    load_dotenv()
    SHEET_ID = str(os.environ.get('SPREADSHEET'))
    keywords = get_values(SHEET_ID, "Amazon!A:D")

    url = os.environ.get('REVIEW_POST_API')
    headers = {'Content-Type': 'application/json',
               'X-SECRET-AGENT': str(os.environ.get('X_SECRET_AGENT')),
               'Authorization': 'Bearer ' + os.environ.get('AUTH_HEADER_STRING')}

    for keyword in keywords:

        # Keyword status 'FALSE' means this keyword group has never been used before.
        if keyword['completed'] == 'FALSE':
            data = {
                'group_name': keyword['group'],
                'keyword': keyword['keyword'],
            }
            resp = requests.post(url, data=json.dumps(data), headers=headers)
            products = resp.json()
            print('RESP: ', products['data'])
            # send_mail(len(products['data']))

if __name__ == "__main__":
    main()
