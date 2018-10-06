import argparse
import warnings

from bs4 import BeautifulSoup
from tabulate import tabulate
from unidecode import unidecode
import requests


URL_TEAMS = 'https://ipsc.ksp.sk/2018/teams'
URL_RESULTS = 'https://ipsc.ksp.sk/2018/results'
TABLE_HEADERS = ['Rank', 'Name', 'Pts', 'Time', 'Members', 'Division']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('COUNTRY', help='e.g. Hong Kong')
    args = parser.parse_args()
    country = args.COUNTRY

    users = {}

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')

        req = requests.get(URL_TEAMS)
        req.raise_for_status()
        soup = BeautifulSoup(req.text, 'html.parser')
        table = soup.find_all('table')[0]
        for row in table.find_all('tr')[1:]:
            data = row.find_all('td')
            name = data[1].get_text().strip()
            user = {
                'members': unidecode(data[2].get_text().strip()),
                'institution': unidecode(data[3].get_text().strip()),
                'country': data[4].get_text().strip(),
                'division': data[5].get_text().strip()
            }
            if name in users:
                print unidecode(name), 'repeated'
            users[name] = user

        req = requests.get(URL_RESULTS)
        req.raise_for_status()
        soup = BeautifulSoup(req.text, 'html.parser')
        table = soup.find_all('tbody')[0]
        result = []
        for row in table.find_all('tr'):
            data = row.find_all('td')
            rank = data[0].get_text().strip()[:-1]
            name = data[1].get_text().strip()
            pts = data[2].get_text().strip()
            penalty = data[3].get_text().strip()
            if name not in users:
                print unidecode(name), 'not found'
            user = users[name]
            if user['country'] == country:
                name = unidecode(name)
                result.append([rank, name, pts, penalty, user['members'], user['division']])

    print tabulate(result, headers=TABLE_HEADERS)


if __name__ == '__main__':
    main()
