import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from application import get_sqlalchemy_db_url

database_url = get_sqlalchemy_db_url()
engine = create_engine(database_url)

Session = sessionmaker(bind=engine)
session = Session()

Base = sqlalchemy.orm.declarative_base()


class TableCreation(Base):
    __tablename__ = 'test_table2'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    birth_date = Column(String, nullable=False)
    tc = Column(String, nullable=False)
    credit_card_number = Column(String, nullable=False)
    password = Column(String, nullable=False)
    url = Column(String, nullable=False)
    number = Column(String, nullable=False)
    mix_content = Column(String, nullable=False)


Base.metadata.create_all(engine)


def add_to_table():
    for i in range(10):
        data = TableCreation(username="user123",
                             email="abcde@gmail.com ",
                             birth_date="16-07-2002 45/85/1991 19/10/1981",
                             tc="12205887980",
                             credit_card_number="4123456789012 4912345678901234 5624332432432432",
                             password="user:password math:95",
                             url="https://chat.openai.com/",
                             number="0555915647 555-555-5555 +90 555 555 5555 ",
                             mix_content="12hfsjkhfd@gmail.com user1:12345 +90 555 555 5555 user2: 123456 "
                                    "21dsf@hotmail.io js slafd 54658998444 555-555-555")

        session.add(data)
    session.commit()


if __name__ == "__main__":
    add_to_table()
