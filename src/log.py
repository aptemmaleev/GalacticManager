import os.path

import logging
import datetime

from config import Config

# Initialize logger
path = Config.get('log', 'path') + (datetime.datetime.now()).strftime('%y-%m-%d_%H-%M') + '.log'

logging.basicConfig(filename=path, filemode='w',format='[%(asctime)s] [%(levelname)s]: %(message)s', datefmt='%y-%m-%d %H:%M:%S', encoding='utf-8', level=20)
logging.info('Start logging')