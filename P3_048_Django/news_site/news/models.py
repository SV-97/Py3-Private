from django.db import models

class Report(models.Model):
    title = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    text = models.TextField("Text")

    def __str__(self):
        return self.text

class Comment(models.Model):
    report = models.ForeignKey(Report)
    author = models.CharField(max_length=70)
    text = models.TextField('Commenttext')

    def __str__(self):
        return f"{self.author} commented: {self.text}"
