from django.db import models

# Create your models here.
class Poll(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateField()

    def __str__(self):
        return self.question_text
