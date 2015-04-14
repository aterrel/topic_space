from django.db import models


class WordCloudRequest(models.Model):
    start_year = models.CharField(max_length=4)
    end_year = models.CharField(max_length=4)
    stop_words = models.TextField()

