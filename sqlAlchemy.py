import sqlalchemy
from sqlalchemy import create_engine, CheckConstraint, Numeric
from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, Text, DateTime, Boolean, ForeignKey, SmallInteger
from datetime import datetime
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy.orm import relationship, Session, sessionmaker
from sqlalchemy.sql import func
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///sqlalchemy_tuts.db')
engine.connect()

print(engine)

metadata = MetaData()

customers = Table('customers', metadata,
                  Column('id', Integer(), primary_key=True),
                  Column('first_name', String(100), nullable=False),
                  Column('last_name', String(100), nullable=False),
                  Column('username', String(50), nullable=False),
                  Column('email', String(200), nullable=False),
                  Column('address', String(200), nullable=False),
                  Column('town', String(50), nullable=False),
                  Column('created_on', DateTime(), default=datetime.now),
                  Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
                  )

items = Table('items', metadata,
              Column('id', Integer(), primary_key=True),
              Column('name', String(200), nullable=False),
              Column('cost_price', Numeric(10, 2), nullable=False),
              Column('selling_price', Numeric(10, 2), nullable=False),
              Column('quantity', Integer(), nullable=False),
              CheckConstraint('quantity > 0', name='quantity_check')
              )

orders = Table('orders', metadata,
               Column('id', Integer(), primary_key=True),
               Column('customer_id', ForeignKey('customers.id')),
               Column('date_placed', DateTime(), default=datetime.now),
               Column('date_shipped', DateTime())
               )

order_lines = Table('order_lines', metadata,
                    Column('id', Integer(), primary_key=True),
                    Column('order_id', ForeignKey('orders.id')),
                    Column('item_id', ForeignKey('items.id')),
                    Column('quantity', Integer())
                    )

conn = engine.connect()

Base = declarative_base()


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer(), primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    username = Column(String(50), nullable=False)
    email = Column(String(200), nullable=False)
    address = Column(String(200), nullable=False)
    town = Column(String(50), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    orders = relationship("Order", backref='customer')


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer(), primary_key=True)
    name = Column(String(200), nullable=False)
    cost_price = Column(Numeric(10, 2), nullable=False)
    selling_price = Column(Numeric(10, 2), nullable=False)


#     orders = relationship("Order", backref='customer')


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer(), primary_key=True)
    customer_id = Column(Integer(), ForeignKey('customers.id'))
    date_placed = Column(DateTime(), default=datetime.now)
    line_items = relationship("OrderLine", secondary="order_lines", backref='order')


class OrderLine(Base):
    __tablename__ = 'order_lines'
    id = Column(Integer(), primary_key=True)
    order_id = Column(Integer(), ForeignKey('orders.id'))
    item_id = Column(Integer(), ForeignKey('items.id'))
    quantity = Column(SmallInteger())
    item = relationship("Item")

session = Session(bind=engine)

c1 = Customer(first_name='Toby',
              last_name='Miller',
              username='tmiller',
              email='tmiller@example.com',
              address='1662 Kinney Street',
              town='Wolfden'
              )

c2 = Customer(first_name='Scott',
              last_name='Harvey',
              username='scottharvey',
              email='scottharvey@example.com',
              address='424 Patterson Street',
              town='Beckinsdale'
              )

c3 = Customer(
    first_name="John",
    last_name="Lara",
    username="johnlara",
    email="johnlara@mail.com",
    address="3073 Derek Drive",
    town="Norfolk"
)

c4 = Customer(
    first_name="Sarah",
    last_name="Tomlin",
    username="sarahtomlin",
    email="sarahtomlin@mail.com",
    address="3572 Poplar Avenue",
    town="Norfolk"
)

c5 = Customer(first_name='Toby',
              last_name='Miller',
              username='tmiller',
              email='tmiller@example.com',
              address='1662 Kinney Street',
              town='Wolfden'
              )

c6 = Customer(first_name='Scott',
              last_name='Harvey',
              username='scottharvey',
              email='scottharvey@example.com',
              address='424 Patterson Street',
              town='Beckinsdale'
              )


print("{} {}".format(c1, c2))
print("{} {}".format(c1.id, c2.id))

# session.add_all([c1, c2, c3, c4, c5, c6]) commented in new commits

i1 = Item(name='Chair', cost_price=9.21, selling_price=10.81, quantity=5)
i2 = Item(name='Pen', cost_price=3.45, selling_price=4.51, quantity=3)
i3 = Item(name='Headphone', cost_price=15.52, selling_price=16.81, quantity=50)
i4 = Item(name='Travel Bag', cost_price=20.1, selling_price=24.21, quantity=50)
i5 = Item(name='Keyboard', cost_price=20.1, selling_price=22.11, quantity=50)
i6 = Item(name='Monitor', cost_price=200.14, selling_price=212.89, quantity=50)
i7 = Item(name='Watch', cost_price=100.58, selling_price=104.41, quantity=50)
i8 = Item(name='Water Bottle', cost_price=20.89, selling_price=25, quantity=50)

#session.add_all([i1, i2, i3, i4, i5, i6, i7, i8]) #commented in new commit
#session.commit() #commented in new commit

o1 = Order(customer=c1)
o2 = Order(customer=c1)

line_item1 = OrderLine(order=o1, item=i1, quantity=3)
line_item2 = OrderLine(order=o1, item=i2, quantity=2)
line_item3 = OrderLine(order=o2, item=i1, quantity=1)
line_item3 = OrderLine(order=o2, item=i2, quantity=4)

# session.add_all([o1, o2]) #commented in new commit
# session.commit() #commented in new commit

all_customers = session.query(Customer).all()
for customer in all_customers:
    print(customer)

all_items = session.query(Item).all()
for item in all_items:
    print(item)

all_orders = session.query(Order).all()
for order in all_orders:
    print(order)

print(session.query(Customer))
q = session.query(Customer)

for c in q:
    print(c.id, c.first_name)

print(session.query(Customer.id, Customer.first_name).all())

count1 = session.query(Customer).count()
print(session.query(Item).count())
print(session.query(Order).count())

print(session.query(Customer).first())
print(session.query(Item).first())
print(session.query(Order).first())

print(session.query(Customer).get(1))
print(session.query(Item).get(1))
print(session.query(Order).get(100))

