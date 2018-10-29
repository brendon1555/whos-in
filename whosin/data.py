from whosin.server import db, ma

class User(db.Model):

    __tablename__ = 'users'
    name = db.Column(db.String(255), primary_key=True)
    is_in = db.Column(db.Boolean(), default=False)

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

user_schema = UserSchema()
users_schema = UserSchema(many=True)

db.create_all()