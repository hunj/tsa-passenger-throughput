from bs4 import BeautifulSoup
import csv
import requests
import os

ENDPOINT = os.environ.get("ENDPOINT")

output_rows = []
# Iterate through multiple pages
for i in range(5):
    url = ENDPOINT+f"?page={i}"
    try:
        req = requests.get(url)
        req.raise_for_status()
        # print(req.text[:128])
        page = req.text
    except requests.exceptions.RequestException as e:
        print("ope, failed to GET the page")
        print(str(e))
    else:
        soup = BeautifulSoup(page, 'html.parser')
        data_table = soup.find('table', {'class': 'views-table'})
        try: # If no table, we are done scraping
            data = data_table.find('tbody')
        except AttributeError:
            print("Finished scraping")
            break
        # print(data_table)
    
        for table_row in data.findAll('tr'):
            columns = table_row.findAll('td')
            output_row = []
            for column in columns:
                output_row.append(column.text.strip().replace(',', ''))
            output_rows.append(output_row)
    
with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(output_rows)
