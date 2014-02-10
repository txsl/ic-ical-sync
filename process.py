from pyexchange import Exchange2010Service, ExchangeNTLMAuthConnection
from datetime import datetime
from pytz import timezone
import getpass
from sqlalchemy.orm import sessionmaker
import sqlalchemy
from icalendar import Calendar, Event

from models import db, CalEntry

# This modification: https://code.google.com/p/python-ntlm/issues/detail?id=17 
# needs to be made to NTLM, otherwise this code fails.


class ExchangeCal:

	URL = u'https://exchange.imperial.ac.uk/EWS/Exchange.asmx'

	def __init__(self, db, username, password):
		# Set up the connection to Exchange
		connection = ExchangeNTLMAuthConnection(url=self.URL,
		                                     username=username,
		                                     password=password)
		self.username = username
		self.service = Exchange2010Service(connection)

		self.db = db

	def create_event(self, subject, location, start, end, text_body):
		event= self.service.calendar().new_event(
			subject= subject.decode('unicode-escape'),
			location= location.decode('unicode-escape'),
			start=start,
			end=end,
			text_body= text_body.decode('unicode-escape')
			)
		event.create()

		entry = CalEntry(user=self.username, exchid=event.id, icaluid='test')

		self.db.add(entry)
		self.db.commit()

	def cancel_event(self, event):
		exch_event = self.service.calendar().get_event(id=event.exchid)
		exch_event.cancel()
		event.removaltime = sqlalchemy.func.now()
		self.db.commit()

	def list_current_events(self):
		return self.db.query(CalEntry).filter_by(removaltime=None, user=self.username).all()

	def cancel_current_events(self):
		for e in self.list_current_events():
			self.cancel_event(e)

def open_cal(cal):
	g = open(cal,'rb')
	gcal = Calendar.from_ical(g.read())
	for component in gcal.walk():
	    if component.name == "VEVENT":
        	for c in component.keys():
        		print c, component.get(c).to_ical()
        	# print component.get('dtstart').to_ical()
        	# print component.get('dtend')
        	# print component.get('dtstamp')
	g.close()

if __name__ == '__main__':
	Session = sessionmaker(bind=db)
	session = Session()

	try:
		from credentials import *
	except ImportError:
		print "Credentials file not found. Please enter your details below..."
		USERNAME = u'ic\\' + raw_input("Imperial College Username: ")
		PASSWORD = getpass.getpass("Imperial College Password:")

	c = ExchangeCal(session, USERNAME, PASSWORD)

	open_cal('/Users/txsl/Downloads/calendar.ics')

	# c.create_event('test', 'EEE408', datetime(2014,2,10,15,0,0, tzinfo=timezone("Europe/London")), datetime(2014,2,10,15,0,0, tzinfo=timezone("Europe/London")), 'Sending some stuff')
	# c.cancel_current_events()
	#