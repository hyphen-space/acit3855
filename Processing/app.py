import connexion
from connexion import NoContent
import requests
import yaml
import json
import logging
import logging.config
from apscheduler.schedulers.background import BackgroundScheduler
import os.path
import datetime

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

def get_stats():
    logger.info("Request started")
    try:
        with open(app_config["datastore"]["filename"], "r") as f:
            current_stats = json.load(f)
            logger.debug(current_stats)
    except(FileNotFoundError):
        return "File does not exist", 400
    
    logger.info("Request completed")
    return current_stats, 200

def populate_stats(): 
    """ Periodically update stats """ 
    current_datetime = datetime.datetime.now()
    logger.info("Start Periodic Processing")
    if os.path.isfile(app_config["datastore"]["filename"]):
        with open(app_config["datastore"]["filename"], "r") as f:
            current_stats = json.load(f)
    else:
        current_stats = {
                        "num_ticket_purchases": 0,
                        "max_ticket_price": 0,
                        "num_music_events": 0,
                        "max_music_event_capacity": 0,
                        "last_updated": current_datetime}

    r1 = requests.get(app_config["eventstore"]["url"] + f"?timestamp={current_datetime}")

    if r1.status_code != 200:
        logger.error("Something went wrong, could not retrieve purchase events")
    else:
        logger.info(f"Received {len(r1.json())} purchase events")
    
    r2 = requests.get(app_config["eventstore"]["url2"] + f"?timestamp={current_datetime}") 
    if r2.status_code != 200:
        logger.error("Something went wrong, could not retrieve music events")
    else:
        logger.info(f"Received {len(r2.json())} music events")

    new_stats = {}
    # new_stats["num_ticket_purchases"] = current_stats["num_ticket_purchases"] + len(r1.json())
    # new_stats["num_music_events"] = current_stats["num_music_events"] + len(r2.json())

    if len(r1.json()) == 0:
        new_stats["num_ticket_purchases"] = current_stats["num_ticket_purchases"]
        new_stats["num_music_events"] = current_stats["num_music_events"]
        new_stats["max_ticket_price"] = current_stats["max_ticket_price"]
        new_stats["max_music_event_capacity"] = current_stats["max_music_event_capacity"]

    else:
        new_stats["num_ticket_purchases"] = len(r1.json())
        new_stats["num_music_events"] = len(r2.json())

        max_ticket_price = current_stats["max_ticket_price"]
        max_music_event_capacity = current_stats["max_music_event_capacity"]
        for event in r1.json():
            if event["price"] > max_ticket_price:
                max_ticket_price = event["price"]
        for event in r2.json():
            if event["capacity"] > max_music_event_capacity:
                max_music_event_capacity = event["capacity"]  
        new_stats["max_ticket_price"] = max_ticket_price
        new_stats["max_music_event_capacity"] = max_music_event_capacity
    new_stats["last_updated"] = current_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")

    with open(app_config["datastore"]["filename"] ,"w") as f:
        json.dump(new_stats, f, indent=2)
    
    logger.debug(new_stats)

    logging.info("Period processing has ended")


def init_scheduler(): 
    sched = BackgroundScheduler(daemon=True) 
    sched.add_job(populate_stats,    
                  'interval', 
                  seconds=app_config['scheduler']['period_sec']) 
    sched.start()


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    # run our standalone gevent server
    init_scheduler()
    app.run(port=8100, use_reloader=False)
