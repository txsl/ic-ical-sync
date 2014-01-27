from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

db = create_engine('sqlite:///sqlite.db')

Base = declarative_base()

class CalEntry(Base):
	__tablename__= 'calentry'

	id = Column(Integer, primary_key=True)
	user = Column(String)
	exchid = Column(String)
	icaluid = Column(String)

	def __repr__(self):
		return "<Entry(Username='%s', ExchID='%s', iCalUID='%s')>" %
						self.user, self.exchid, self.icaluid