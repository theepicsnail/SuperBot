



from sqlalchemy import *
db = create_engine('sqlite:///test.db')
metadata = BoundMetaData(db)
users = 











###############
import sys
sys.exit(0)
###############



db_name = "test.db"

from sqlalchemy import *


from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class User(Base):
    __tablename__='users'

    id = Column(Integer,primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    state = Column(Integer)
    expire= Column(DateTime)
    def __init__(self,username,password,email=""):
        self.username=username
        self.password=password
        self.email=email
        self.expire=datetime.now()
    def __repr__(self):
        return "<User '"+self.username+"'>"
    def login(self,nick,password):
        if password==self.password:
            self.state = 1
            self.expire= datetime.datetime.now()+datetime.timedelta(days=1)
            return True
        return False
    def logout(self):
        self.state= 0
        self.expire=datetime.datetime.now()
users_table = User.__table__
metadata = Base.metadata

from sqlalchemy import create_engine
engine = create_engine('sqlite:///'+db_name)


#metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)

session = Session()
print dir(session)

session.add(User("user","pass","email"))
session.add(User("user2","pass"))
session.commit()

for i in session.query(User):
    print i.username,i.id















