from flask_sqlalchemy import SQLAlchemy
from app import db



class Credentials(db.Model):
    uid = db.Column(db.String, primary_key=True)
    lastname = db.Column(db.String(20), nullable=True)
    firstname = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(20), nullable=True)
    pwd = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return '<New Credential %r> %self.userID'

class userID_passwdHash(db.Model):
    uid = db.Column(db.String, primary_key=True)
    passwordHash = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<New Credential %r> %self.userID'

class userID_certs(db.Model):
    serialnumber = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String, nullable=False)
    cert = db.Column(db.String(20), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    def __repr__(self):
        return '<New Credential %r> %self.userID'

class stats(db.Model):
    nIssuedCerts = db.Column(db.Integer, nullable=False)
    nRevokedCerts = db.Column(db.Integer, nullable=False)
    currentSN = db.Column(db.Integer, primary_key=True)
    def __repr__(self):
        return '<New Credential %r> %self.nIssuedCerts'
