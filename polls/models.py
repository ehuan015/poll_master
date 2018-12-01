from django.db import models

# Create your models here.
class Poll(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateField()

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return "{} - {}".format(self.question.question_text[:25], self.choice_text[:25])
