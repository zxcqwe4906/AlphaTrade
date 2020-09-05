import os
import sys

sys.path.append(os.getcwd())

from decimal import Decimal

from app import create_app
from app.database import DB
from app.models import Order, OrderType, OrderSideType

def main():
    app = create_app()
    # print(app.config['MYSQL_HOST'])

    # with app.app_context():
    #     order = Order(
    #         order_id='123',
    #         order_type=OrderType.LIMIT,
    #         order_side=OrderSideType.BID,
    #         amount=Decimal('10'),
    #         price=Decimal('100'),
    #     )
    #     DB.session.add(order)
    #     DB.safe_commit()

if __name__ == '__main__':
    try:
        main()
    except RuntimeError as e:
        print('Error: %s' % str(e))
    except KeyboardInterrupt:
        print('Got interrupt, quitting ...')
