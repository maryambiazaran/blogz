from app import db
from datetime import datetime,timedelta
from hashutils import check_pw_hash,make_pw_hash

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    post_date = db.Column(db.DateTime, nullable=True,
        default=datetime.utcnow)
    body = db.Column(db.Text())
    active = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self,title,body,owner):
        self.title = title
        self.body = body
        self.active = True
        self.date = datetime.now()
        self.owner = owner

    def __repr__(self):
        return '< Title:"{}" ,date posted: {}>'.format(self.title,str(self.date)[:16])

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    pw_hash = db.Column(db.String(200))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.pw_hash = make_pw_hash(password)

    def __repr__(self):
        list_of_blogs =''
        if self.blogs:
            for blog in self.blogs:
                list_of_blogs += blog.title
                list_of_blogs += "\n"

        return """
        id = {}
        username = {}
        blogs = {}
        """.format(self.id,self.username,list_of_blogs)

    def check_password(self,password):
        return check_pw_hash(password,self.pw_hash)