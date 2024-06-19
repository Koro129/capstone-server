from app import db

class Node(db.Model):
    __tablename__ = 'node'
    idNode = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idAccount = db.Column(db.Integer, db.ForeignKey('account.idAccount'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    photo = db.Column(db.String(256))
    desc = db.Column(db.String(512))
    address = db.Column(db.String(256))
    level = db.Column(db.Integer, nullable=False)
    
    account = db.relationship('Account', backref=db.backref('nodes', lazy=True))
    
    def __repr__(self):
        return '<Node {}>'.format(self.name)
