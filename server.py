import redis
import logging
import os

import os
from dotenv import load_dotenv

load_dotenv()

redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')
redis_pass = os.getenv('REDIS_PASS')

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)-24s] [%(levelname)-8s] Command | %(message)s',
    handlers=[
        logging.FileHandler("server.log"),
    ]
)

r = redis.Redis(host=redis_host ,port=redis_port ,password=redis_pass ,decode_responses=True)
client = input('Connect to client : ')

while True:
    try :
        text = input('> ').split(' ')
        s_text = [letter for letter in text if letter != ''] 
        
        if s_text[0] == 'go' :
            text = ' '.join(s_text[1:])
            text = 'go @#@ cmd @#@ /c @#@ ' + text
        
        else :
            text = ' '.join(s_text)
            text = 'cmd @#@ /c @#@ ' + text
        logging.info(text)
        r.publish(f'wyvern-{client}-command' ,text )

    except KeyboardInterrupt:
        logging.error('Exit!')
        exit(0)
    except Exception as e :
        print(f'!! Error[{e}]')
        logging.error(f'Error [{e}]')
