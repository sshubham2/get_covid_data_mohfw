# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from pathlib import Path
from lxml import html
from datetime import datetime, date
import requests
import pandas as pd
from sqlalchemy import create_engine


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def get_india_covid_date(_url: str):
    tree = html.fromstring(requests.get(_url).content)

    _date = ''.join(tree.xpath('//*[@id="site-dashboard"]/div/div/div[1]/div[1]/h5/span/text()[1]')[0]
                    .split()[3:7]).replace(',', '')+'+05:30'
    timestamp_ = datetime.strptime(_date, '%d%B%Y%H:%M%z').isoformat()

    total_active_cases = int(tree.xpath('//*[@id="site-dashboard"]//strong[2]/text()')[0].strip())

    total_discharged = int(''.join(tree.xpath('//*[@id="site-dashboard"]//li[2]/strong[2]/text()')).strip())

    total_deaths = int(''.join(tree.xpath('//*[@id="site-dashboard"]//li[3]/strong[2]/text()')).strip())

    total_vaccination = int(''.join(tree.xpath('//*[@id="site-dashboard"]//div/span[2]/text()'))
                            .strip().replace(',', ''))

    df = pd.DataFrame(
        {'timestamp': [timestamp_], 'total_active_cases': [total_active_cases], 'total_discharged': [total_discharged],
         'total_vaccination': [total_vaccination]})

    return df


def load_data(df: pd.DataFrame):
    engine = create_engine('sqlite:///covid_data.db', echo=True)
    df.to_sql('india_covid_data', con=engine, if_exists='append', index=False)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    url = 'https://www.mohfw.gov.in/'
    load_data(get_india_covid_date(url))
