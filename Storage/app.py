import connexion
import yaml
import logging
import logging.config
import datetime
from connexion import NoContent
import json
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from ticket_purchase import TicketPurchase
from music_event import MusicEvent

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

DB_ENGINE = create_engine(f'mysql+pymysql://{app_config["datastore"]["user"]}:{app_config["datastore"]["password"]}@{app_config["datastore"]["hostname"]}:{app_config["datastore"]["port"]}/{app_config["datastore"]["db"]}')
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)
logger.info(f"Connecting to DB. Hostname: {app_config['datastore']['hostname']}, Port: {app_config['datastore']['port']}")


def purchase_ticket(body):
    """ Receives a ticket purchase """
    session = DB_SESSION()

    tp = TicketPurchase(body['purchaser'],
                       body['eventDate'],
                       body['seat'],
                       body['price'],
                       body['numTickets'])

    session.add(tp)

    session.commit()
    session.close()
    logger.debug(f"Stored event purchase request with a unique id of {body['id']}")

    return NoContent, 201


def create_event(body):
    """ Receives a music event """
    logger.info(f"Connecting to DB. Hostname: {app_config['datastore']['hostname']}, Port: {app_config['datastore']['port']}")

    session = DB_SESSION()

    me = MusicEvent(body['venue'],
                   body['capacity'],
                   body['eventDate'],
                   body['headliner'],
                   body['openingAct'])

    session.add(me)

    session.commit()
    session.close()
    logger.debug(f"Stored event create request with a unique id of {body['id']}")

    return NoContent, 201

def get_ticket_purchases(timestamp):
    """ Gets new ticket purchases after the timestamp """
    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    ticket_purchases = session.query(TicketPurchase).filter(TicketPurchase.date_created >=
                                    timestamp_datetime)
    ticket_purchases_list = []
    for ticket_purchase in ticket_purchases:
        ticket_purchases_list.append(ticket_purchase.to_dict())
    session.close()
    logger.info("Query for Ticket Purchase readings after %s returns %d results" %
                (timestamp, len(ticket_purchases_list)))
    
    return ticket_purchases_list, 200

def get_music_events(timestamp):
    """ Gets new music events after the timestamp """
    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    music_events = session.query(MusicEvent).filter(MusicEvent.date_created >= timestamp_datetime)
    music_events_list = []
    for music_event in music_events:
        music_events_list.append(music_event.to_dict())
    session.close()
    logger.info("Query for Music readings after %s returns %d results" %
                (timestamp, len(music_events_list)))
    
    return music_events_list, 200

def process_messages(): 
    """ Process event messages """ 
    hostname = "%s:%d" % (app_config["events"]["hostname"],   
                          app_config["events"]["port"]) 
    client = KafkaClient(hosts=hostname) 
    topic = client.topics[str.encode(app_config["events"]["topic"])] 
     
    # Create a consume on a consumer group, that only reads new messages  
    # (uncommitted messages) when the service re-starts (i.e., it doesn't  
    # read all the old messages from the history in the message queue). 
    consumer = topic.get_simple_consumer(consumer_group=b'event_group', 
                                         reset_offset_on_start=False, 
                                         auto_offset_reset=OffsetType.LATEST) 
 
    # This is blocking - it will wait for a new message 
    for msg in consumer: 
        msg_str = msg.value.decode('utf-8') 
        msg = json.loads(msg_str) 
        logger.info("Message: %s" % msg) 
 
        payload = msg["payload"] 
 
        if msg["type"] == "tp": # Change this to your event type 
            # Store the event1 (i.e., the payload) to the DB 
            purchase_ticket(payload)
        elif msg["type"] == "me": # Change this to your event type 
            # Store the event2 (i.e., the payload) to the DB 
            create_event(payload)
        # Commit the new message as being read 
        consumer.commit_offsets() 


app = connexion.FlaskApp(__name__, specification_dir='')
# fix validate_responses
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    t1 = Thread(target=process_messages) 
    t1.setDaemon(True) 
    t1.start() 
    app.run(port=8090)
