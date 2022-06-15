import redis
from time import sleep
import subprocess
import logging

import os
from dotenv import load_dotenv

load_dotenv()

redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')
redis_pass = os.getenv('REDIS_PASS')

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)-24s] [%(levelname)-8s] Result  | %(message)s',
    handlers=[
        logging.FileHandler("server.log"),
    ]
)
logging.info('Listening ...')
while True:
    err = None
    try :
        r = redis.Redis(host=redis_host ,port=redis_port ,password=redis_pass ,decode_responses=True)
        p = r.pubsub() 
        p.subscribe('wyvern-response') 
        
        for item in p.listen():
            if type(item['data']) == str:
                print('='*50)
                print(item['data'])
                logging.info(item['data'])

        err = None
    
    except KeyboardInterrupt:
        logging.error('Exit!')
        exit(0)
    
    except Exception as e:
        if str(e) != err:
            err = str(e)
            logging.error(f'Error [{e}]')
            print(f'!! Error [{e}]')

        sleep(1)

