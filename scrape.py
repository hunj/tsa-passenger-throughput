from bs4 import BeautifulSoup
from datetime import datetime
import csv
import requests
import os

ENDPOINT = "https://www.tsa.gov/coronavirus/passenger-throughput"


def get_page():
    result = {}

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
            processed_data = process_row(row_data)
            result.update(processed_data)
    filtered_data = {date: count for date, count in result.items() if count}  # remove dates with no count
    print(filtered_data)
    return sorted(filtered_data.items(), key=lambda r: r[0])  # sort by date then put into a list


def process_row(row_data):
    date, count_current_year, count_one_year_ago, count_two_years_ago = row_data
    d = datetime.strptime(date, '%m/%d/%Y')
    retval = {
        d: count_current_year,
        datetime(d.year - 1, d.month, d.day): count_one_year_ago,
        datetime(d.year - 2, d.month, d.day): count_two_years_ago
    }
    return retval


if __name__ == "__main__":
    data = get_page()
    if data:
        with open('output.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in data:
                writer.writerow([datetime.strftime(row[0], '%Y-%m-%d'), row[1]])
    else:
        print("no data found")
