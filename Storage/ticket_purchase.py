from sqlalchemy import Column, Integer, String, DateTime, Float
from base import Base
import datetime


class TicketPurchase(Base):
    """ Ticket Purchase """

    __tablename__ = "ticket_purchase"

    id = Column(Integer, primary_key=True)
    purchaser = Column(String(250), nullable=False)
    eventDate = Column(String(100), nullable=False)
    seat = Column(String(250), nullable=False)
    price = Column(Float(2), nullable=False)
    numTickets = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, purchaser, eventDate, seat, price, numTickets):
        """ Initializes a ticket purchase object """
        self.purchaser = purchaser
        self.eventDate = eventDate
        self.seat = seat
        self.price = price
        self.numTickets = numTickets
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of a blood pressure reading """
        dict = {}
        dict['id'] = self.id
        dict['purchaser'] = self.purchaser
        dict['eventDate'] = self.eventDate
        dict['seat'] = self.seat
        dict['price'] = self.price
        dict['numTickets'] = self.numTickets
        dict['date_created'] = self.date_created
        return dict
