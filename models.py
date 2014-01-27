from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

db_url = 'sqlite:///sqlite.db'

db = create_engine(db_url)

Base = declarative_base()

class CalEntry(Base):
	__tablename__= 'calentry'

	id = Column(Integer, primary_key=True)
	user = Column(String(20))
	exchid = Column(String(200))
	icaluid = Column(String(200))

	def __repr__(self):
		return "<Entry(Username='%s', ExchID='%s', iCalUID='%s')>" % (
						self.user, self.exchid, self.icaluid)

