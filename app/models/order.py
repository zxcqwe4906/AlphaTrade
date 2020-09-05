import datetime
import enum
import uuid
from decimal import Decimal

from app.database import DB

class OrderSideType(enum.Enum):
    ASK = 'ask'  # sell
    BID = 'bid'  # buy

class OrderType(enum.Enum):
    MARKET = 'market'
    LIMIT = 'limit'

class OrderStatueType(enum.Enum):
    EXECUTED = 'executed'
    OPEN = 'open'
    PARTIALLY_FILLED = 'partially_filled'
    CANCELED = 'canceled'

class Order(DB.Model):
    __tablename__ = 'order'

    id = DB.Column(DB.Integer, primary_key=True)
    created_at = DB.Column(DB.DateTime, nullable=False, default=datetime.datetime.now)
    order_id = DB.Column(DB.String(128), nullable=False, default=uuid.uuid4)
    order_type = DB.Column(DB.Enum(OrderType), nullable=False)
    order_side = DB.Column(DB.Enum(OrderSideType), nullable=False)
    amount = DB.Column(DB.DECIMAL(36, 18), nullable=False)
    price = DB.Column(DB.DECIMAL(36, 18), nullable=True)
    status = DB.Column(DB.Enum(OrderStatueType), nullable=True, default=OrderStatueType.OPEN.value)
    filled_size = DB.Column(DB.DECIMAL(36, 18), nullable=True, default=Decimal('0'))
