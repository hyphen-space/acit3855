import connexion
import json
import datetime
from pykafka import KafkaClient
from connexion import NoContent
from time import sleep
import requests
import yaml
import logging
import logging.config
import os 
 
if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test": 
    print("In Test Environment") 
    app_conf_file = "/config/app_conf.yml" 
    log_conf_file = "/config/log_conf.yml" 
else: 
    print("In Dev Environment") 
    app_conf_file = "app_conf.yml" 
    log_conf_file = "log_conf.yml" 
 
with open(app_conf_file, 'r') as f: 
    app_config = yaml.safe_load(f.read()) 
 
# External Logging Configuration 
with open(log_conf_file, 'r') as f: 
    log_config = yaml.safe_load(f.read()) 
    logging.config.dictConfig(log_config) 
 
logger = logging.getLogger('basicLogger') 
 
logger.info("App Conf File: %s" % app_conf_file) 
logger.info("Log Conf File: %s" % log_conf_file)

# with open('app_conf.yml', 'r') as f:
#     app_config = yaml.safe_load(f.read())

# with open('log_conf.yml', 'r') as f:
#     log_config = yaml.safe_load(f.read())
#     logging.config.dictConfig(log_config)

# logger = logging.getLogger('basicLogger')

    
num_retries = 0
while num_retries <= app_config["kafka"]["max_retries"]:
    logger.info(f"Trying to connect to Kafka. Attempt #{num_retries + 1}")
    try:
        client = KafkaClient(hosts=f'{app_config["events"]["hostname"]}:{app_config["events"]["port"]}') 
        topic = client.topics[str.encode(app_config["events"]["topic"])]
    except:
        logger.error("Cannot connect to Kafka. Retrying...")
        sleep(app_config["kafka"]["sleep_duration"])
        num_retries += 1
    else:
        logger.info(f"Connected to Kafka")
        break



def purchase_ticket(body):
    # url = app_config["eventstore1"]["url"]
    logger.info(f"Received event 'purchase' request with a unique id of {body['id']}")
    # res = requests.post(url, json=body)
    
    # client = KafkaClient(hosts=f'{app_config["events"]["hostname"]}:{app_config["events"]["port"]}') 
    # topic = client.topics[str.encode(app_config["events"]["topic"])]
    producer = topic.get_sync_producer() 
    
    msg = { "type": "tp",  
            "datetime" :    
            datetime.datetime.now().strftime( 
                "%Y-%m-%dT%H:%M:%S"),  
            "payload": body } 
    msg_str = json.dumps(msg) 
    producer.produce(msg_str.encode('utf-8'))
    logger.info(f"Returned event 'purchase' response (Id: {body['id']}) with status {201}")

    return NoContent, 201 

def create_event(body):
    # url = app_config["eventstore2"]["url"]
    logger.info(f"Received event 'purchase' request with a unique id of {body['id']}")
    # res = requests.post(url, json=body)

    # client = KafkaClient(hosts=f'{app_config["events"]["hostname"]}:{app_config["events"]["port"]}') 
    # topic = client.topics[str.encode(app_config["events"]["topic"])]
    producer = topic.get_sync_producer() 
    
    msg = { "type": "me",  
            "datetime" :    
            datetime.datetime.now().strftime( 
                "%Y-%m-%dT%H:%M:%S"),  
            "payload": body } 
    msg_str = json.dumps(msg) 
    producer.produce(msg_str.encode('utf-8')) 

    logger.info(f"Returned event 'purchase' response (Id: {body['id']}) with status {201}")

    return NoContent, 201 

app = connexion.FlaskApp(__name__, specification_dir='')
#app.add_api("openapi.yml", strict_validation=True, validate_responses=False)
app.add_api("openapi.yml", base_path="/receiver", strict_validation=True, validate_responses=False)

if __name__ == "__main__":
    app.run(port=8080)
