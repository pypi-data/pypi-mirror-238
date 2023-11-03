from django.db import models

class Prediction(models.Model):
    """
    A class representing a prediction.

    Attributes:
        name (str): The name of the prediction.
        description (str): A description of the prediction.

    """
    label = models.ForeignKey("Label", on_delete=models.CASCADE, related_name="predictions")
    frame = models.ForeignKey("Frame", on_delete=models.CASCADE, related_name="predictions")
    confidence = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('label', 'frame')