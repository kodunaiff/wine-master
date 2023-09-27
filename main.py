import collections
import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

now = datetime.datetime.now()
company_age = int(now.year) - 1920


def true_statement(year):
    if year[-2] == '1':
        return 'лет'
    elif year[-1] == '1':
        return 'год'
    elif year[-1] in '234':
        return 'года'
    elif year[-1] in '056789':
        return 'лет'


wines_db = pandas.read_excel('wine3.xlsx',
                             na_values='None', keep_default_na=False)
wines = wines_db.to_dict(orient='records')
group_wines = collections.defaultdict(list)
for wine in wines:
    group_wines[wine['Категория']].append(wine)

rendered_page = template.render(
    group_wines=group_wines,
    time_title='Уже ' + str(company_age) + ' ' +
               f'{true_statement(str(company_age))}' + ' с вами',
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
