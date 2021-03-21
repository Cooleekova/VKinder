from module_dotenv import DSN
import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = sq.create_engine(DSN)
Session = sessionmaker(bind=engine)

Base = declarative_base()
session = Session()

class VK_user(Base):
    __tablename__ = 'users'

    id = sq.Column(sq.Integer, primary_key=True)
    user_domain = sq.Column(sq.String, unique=True)


Base.metadata.create_all(engine)


