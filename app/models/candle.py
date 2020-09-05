from app.database import DB

class PriceCandle(DB.Model):
    open = DB.Column(DB.DECIMAL(36, 18), nullable=False)
    high = DB.Column(DB.DECIMAL(36, 18), nullable=False)
    low = DB.Column(DB.DECIMAL(36, 18), nullable=False)
    close = DB.Column(DB.DECIMAL(36, 18), nullable=False)
    volume = DB.Column(DB.DECIMAL(36, 18), nullable=False)
    # exchange name
    # CandleTimeframeType
    # server time
    # datetime
