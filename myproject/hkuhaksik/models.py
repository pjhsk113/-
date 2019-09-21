from django.db import models

class HakMenu(models.Model):
	id = models.AutoField(primary_key=True)
	cafe_name = models.CharField(max_length=30, default="")
	menu = models.CharField(max_length=100, default="")
	is_new = models.BooleanField(default=False)

class KyoMenu(models.Model):
	id = models.AutoField(primary_key=True)
	cafe_name = models.CharField(max_length=30, default="")
	menu = models.CharField(max_length=100, default="")
	is_new = models.BooleanField(default=False)