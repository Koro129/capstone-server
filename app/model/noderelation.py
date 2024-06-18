from app import db

class NodeRelation(db.Model):
    __tablename__ = 'node_relation'
    idNode1 = db.Column(db.Integer, db.ForeignKey('node.idNode'), primary_key=True)
    idNode2 = db.Column(db.Integer, db.ForeignKey('node.idNode'), primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    
    node1 = db.relationship('Node', foreign_keys=[idNode1])
    node2 = db.relationship('Node', foreign_keys=[idNode2])
    
    def __repr__(self):
        return '<NodeRelation {}-{}>'.format(self.idNode1, self.idNode2)
