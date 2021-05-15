from bs4 import BeautifulSoup
import csv
import requests
import os

ENDPOINT = os.environ.get("ENDPOINT")


def get_page():
    result = []

    try:
        req = requests.get(ENDPOINT)
        req.raise_for_status()
        page = req.text
    except requests.exceptions.RequestException as e:
        print("ope, failed to GET the page")
        print(str(e))
    else:
        soup = BeautifulSoup(page, 'html.parser')
        data_table = soup.find('table', {'class': 'views-table'})

        data = data_table.find('tbody')
        for table_row in data.findAll('tr'):
            row_data = []
            columns = table_row.findAll('td')
            for column in columns:
                row_data.append(column.text.strip().replace(',', ''))
            result.append(row_data)
    return result


if __name__ == "__main__":
    data = get_page()
    if data:
        with open('output.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
    else:
        print("no data found")
