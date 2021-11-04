from sqlalchemy import Column, Integer, String, DateTime, Float
from base import Base
import datetime


class MusicEvent(Base):
    """ Ticket Purchase """

    __tablename__ = "music_event"

    id = Column(Integer, primary_key=True)
    venue = Column(String(250), nullable=False)
    capacity = Column(Integer, nullable=False)
    eventDate = Column(String(100), nullable=False)
    headliner = Column(String(250), nullable=False)
    openingAct = Column(String(250), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, venue, capacity, eventDate, headliner, openingAct):
        """ Initializes a ticket purchase object """
        self.venue = venue
        self.capacity = capacity
        self.eventDate = eventDate
        self.headliner = headliner
        self.openingAct = openingAct
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of a blood pressure reading """
        dict = {}
        dict['id'] = self.id
        dict['venue'] = self.venue
        dict['capacity'] = self.capacity
        dict['eventDate'] = self.eventDate
        dict['headliner'] = self.headliner
        dict['openingAct'] = self.openingAct
        dict['date_created'] = self.date_created
        return dict
