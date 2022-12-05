from django.db import models

class SpotifyToken(models.Model):
    id=models.IntegerField(primary_key=True, auto_created=True)
    username = models.CharField(max_length=50, null=True, default="")
    user_id=models.IntegerField( null=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_token = models.CharField(max_length=300, null=True, default="")
    access_token = models.CharField(max_length=300, null=True, default="")
    expires_in = models.DateTimeField(null=True)
    token_type = models.CharField(max_length=50, null=True, default="")