from pyexchange import Exchange2010Service, ExchangeNTLMAuthConnection
from datetime import datetime
from pytz import timezone
import getpass
from sqlalchemy.orm import sessionmaker

from models import db, CalEntry

Session = sessionmaker(bind=db)
session = Session()

# This modification: https://code.google.com/p/python-ntlm/issues/detail?id=17 needs to be made to NTLM, otherwise this code fails.

URL = u'https://exchange.imperial.ac.uk/EWS/Exchange.asmx'

try:
	from credentials import *
except ImportError:
	print "Credentials file not found. Please enter your details below..."
	USERNAME = u'ic\\' + raw_input("Imperial College Username: ")
	PASSWORD = getpass.getpass("Imperial College Password:")

# Set up the connection to Exchange
connection = ExchangeNTLMAuthConnection(url=URL,
                                     username=USERNAME,
                                     password=PASSWORD)

service = Exchange2010Service(connection)

event= service.calendar().new_event(
	subject= u"This is a test",
	location= u"EEE",
	start=datetime(2014,2,1,15,0,0, tzinfo=timezone("Europe/London")),
	end=datetime(2014,2,1,16,0,0, tzinfo=timezone("Europe/London")),
	text_body= u"does this appear"
)

event.create()

entry = CalEntry(user=USERNAME, exchid=event.id, icaluid='test')

session.add(entry)
session.commit()