from bs4 import BeautifulSoup
import csv
import requests
import os

ENDPOINT = os.environ.get("ENDPOINT")

# TODO be able to go through pages.
# ?page=1 for page 2 (page param seems 0-based)

try:
    req = requests.get(ENDPOINT)
    req.raise_for_status()
    # print(req.text[:128])
    page = req.text
except requests.exceptions.RequestException as e:
    print("ope, failed to GET the page")
    print(str(e))
else:
    soup = BeautifulSoup(page, 'html.parser')
    data_table = soup.find('table', {'class': 'views-table'})
    data = data_table.find('tbody')
    # print(data_table)

    output_rows = []
    for table_row in data.findAll('tr'):
        columns = table_row.findAll('td')
        output_row = []
        for column in columns:
            output_row.append(column.text.strip().replace(',', ''))
        output_rows.append(output_row)

    with open('output.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(output_rows)
