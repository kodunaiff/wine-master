import argparse
import collections
import datetime
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_correct_year(year):
    if year[-2] == '1':
        return 'лет'
    elif year[-1] == '1':
        return 'год'
    elif year[-1] in '234':
        return 'года'
    elif year[-1] in '056789':
        return 'лет'


def get_directory(file_path_wine):
    parser = argparse.ArgumentParser(
        description='Запускает сайт с винной продукцией'
    )
    parser.add_argument(
        '-p',
        '--file_path_wine',
        help='give me path and file with wines',
        type=str,
        default=file_path_wine
    )
    args = parser.parse_args()
    return args.file_path_wine


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    load_dotenv()
    file_path_wine = os.getenv('FILE_PATH_WINE')

    now = datetime.datetime.now()
    year_of_foundation = 1920
    company_age = now.year - year_of_foundation

    production_wine = pandas.read_excel(get_directory(file_path_wine),
                                        na_values='None',
                                        keep_default_na=False)
    wines = production_wine.to_dict(orient='records')
    group_wines = collections.defaultdict(list)
    for wine in wines:
        group_wines[wine['Категория']].append(wine)

    rendered_page = template.render(
        group_wines=group_wines,
        time_title=f'Уже {company_age} '
                   f'{get_correct_year(str(company_age))} с вами',
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
