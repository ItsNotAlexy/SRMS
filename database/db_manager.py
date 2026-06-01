from flask_sqlalchemy import SQLAlchemy


class DatabaseManager:
	def __init__(self):
		self.db = SQLAlchemy()

	def __getattr__(self, name):
		return getattr(self.db, name)

	def init_app(self, app):
		self.db.init_app(app)

	def create_all(self):
		self.db.create_all()

	def drop_all(self):
		self.db.drop_all()

	def add(self, model):
		self.db.session.add(model)

	def add_all(self, models):
		self.db.session.add_all(models)

	def delete(self, model):
		self.db.session.delete(model)

	def commit(self):
		self.db.session.commit()

	def rollback(self):
		self.db.session.rollback()


db = DatabaseManager()

