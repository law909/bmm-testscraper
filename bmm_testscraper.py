import requests
import datetime
import configparser
import re
import logging
from jinja2 import Environment, FileSystemLoader, select_autoescape
from bmmbackend import bmmbackend


config = configparser.ConfigParser()
config.read_file(open('config.ini'))

logging.basicConfig(
    filename=config['DEFAULT']['logfile_name'], 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s | %(module)s.%(funcName)s line %(lineno)d: %(message)s')

logging.info('TestScraper started')

backend = bmmbackend(config['DEFAULT']['monitor_url'], config['DEFAULT']['uuid'])

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape()
)
contenttpl = env.get_template('content.html')

events = backend.getEvents()
for event in events['data']:
    result = []

    if event['type'] == 1:
        result.append(['1234', '2023-07-30', 20000000, 'Ügyfél Kft.', 'Szerződés a mindenféléről'])
    else:
        result.append(['5678', '2023-07-30', 20000000, 'Ügyfél Kft.', 'ÚJ szerződés'])

    if result:
        content = ''
        for res in result:
            content = content + contenttpl.render(contract = res)
            
        backend.notifyEvent(event['id'], content)


logging.info('TesztScraper ready. Bye.')

print('Ready. Bye.')
