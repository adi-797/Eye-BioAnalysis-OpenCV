from django.db import models

class Auth(models.Model):
	username_db = models.TextField(default = "NA")
	password_db = models.TextField(default = "NA")

	def __str__(self):
		return self.username_db + "#" + self.password_db