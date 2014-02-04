from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
import datetime

db_url = 'sqlite:///sqlite.db'

db = create_engine(db_url)

Base = declarative_base()

class CalEntry(Base):
	__tablename__= 'calentry'

	id = Column(Integer, primary_key=True)
	user = Column(String(20))
	exchid = Column(String(200))
	icaluid = Column(String(200))
	entrytime = Column(DateTime, default=datetime.datetime.now(), server_default="NOW()", nullable=False)
	removaltime = Column(DateTime)

	def __repr__(self):
		return "<Entry(Username='%s', ExchID='%s', iCalUID='%s')>" % (
						self.user, self.exchid, self.icaluid)

