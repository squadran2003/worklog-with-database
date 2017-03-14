from peewee import *
import datetime

db  = SqliteDatabase('worklog.db')


class Entry(Model):
	Date= DateField()
	employee = CharField(default='255')
	task_name = CharField(default='255')
	time_spent = TimeField()
	notes = TextField()
	created_on = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = db


def initialise():
	"""create the table"""
	db.connect()
	db.create_tables([Entry],safe = True)