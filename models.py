from peewee import *


db = SqliteDatabase(r'question.db')


class User(Model):
    id = PrimaryKeyField(unique=True)
    user_id = CharField(max_length=20, default='', null=True)
    username = CharField(max_length=50, default='', null=True)
    first_name = CharField(max_length=50, default='', null=True)
    last_name = CharField(max_length=50, default='', null=True)
    post = CharField(max_length=50, default='', null=True)
    expert = CharField(max_length=60, default='', null=True)
    registration_date = DateField(default='')
    quest_1 = FloatField(default=0, null=True)
    quest_2 = FloatField(default=0, null=True)
    quest_3 = FloatField(default=0, null=True)
    quest_4 = FloatField(default=0, null=True)
    quest_5 = FloatField(default=0, null=True)
    quest_6 = FloatField(default=0, null=True)
    quest_7 = FloatField(default=0, null=True)
    quest_8 = FloatField(default=0, null=True)
    avg_all_shore = FloatField(default=0)

    class Meta:
        database = db
        db_table = 'User'
        order_by = 'id'


def initialize_db():
    db.connect()
    db.create_tables([User], safe=True)
    db.close()


initialize_db()
