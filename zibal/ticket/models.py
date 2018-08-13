from django.db import models



class Ticket(models.Model):

    subject = models.CharField(max_length=200)
    department = models.IntegerField()
    text = models.TextField(max_length=500)
    status = models.IntegerField()
    date = models.DateTimeField(null=True)
    in_reply_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

