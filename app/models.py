from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column('password', db.String(20))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self , username ,password):
        self.username = username
        self.password = password
        self.date_created = datetime.utcnow()
        self.date_modified = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % self.username
#
def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return (value.strftime("%Y-%m-%d") +" "+ value.strftime("%H:%M:%S"))

class Bucketlist(db.Model):
    """This class represents the bucketlist table."""

    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    # created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    items= db.relationship('Item', backref='bucketlists', lazy='dynamic')

    def __init__(self, name):
        """initialize with name."""
        self.name = name

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id' : self.id,
            'name' : self.name,
            'date_created' : dump_datetime(self.date_created),
            'date_modified' : dump_datetime(self.date_modified)
        }

    def serialize_id(self, item):
        """Return object data in easily serializeable format"""
        #self. item = b_items
        return {
            'id' : self.id,
            'name' : self.name,
            'items' : item,
            'date_created' : dump_datetime(self.date_created),
            'date_modified' : dump_datetime(self.date_modified)
        }

    def __repr__(self):
        return "<Bucketlist: {}>".format(self.name)

class Item(db.Model):
    """This class represents the items database table."""

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))

    def __init__(self, name, bucketlist_id):
        self.name = name
        self.bucketlist_id = bucketlist_id
        self.done = False

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id' : self.id,
            'name' : self.name,
            'date_created' : dump_datetime(self.date_created),
            'date_modified' : dump_datetime(self.date_modified),
            'done' : self.done,
        }

    def __repr__(self):
        return "<Item: {}>".format(self.name)
