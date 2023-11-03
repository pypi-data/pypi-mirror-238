from django.db import models
from ..label.label import Label
from ..annotation.image_classification import ImageClassificationAnnotation

class LegacyFrame(models.Model):
    video = models.ForeignKey("LegacyVideo", on_delete=models.CASCADE, related_name='frames')
    frame_number = models.IntegerField()
    image = models.ImageField(upload_to="legacy_frames", blank=True, null=True)
    suffix = models.CharField(max_length=255)
    # ImageClassificationAnnotation has a foreign key to this model (related name: image_classification_annotations)

    class Meta:
        unique_together = ('video', 'frame_number')
        indexes = [
            models.Index(fields=['video', 'frame_number']),
        ]

    def get_classification_annotations(self):
        """
        Get all image classification annotations for this frame.
        """
        return ImageClassificationAnnotation.objects.filter(legacy_frame=self)

    def get_classification_annotations_by_label(self, label:Label):
        """
        Get all image classification annotations for this frame with the given label.
        """
        return ImageClassificationAnnotation.objects.filter(legacy_frame=self, label=label)
    
    def get_classification_annotations_by_value(self, value:bool):
        """
        Get all image classification annotations for this frame with the given value.
        """
        return ImageClassificationAnnotation.objects.filter(legacy_frame=self, value=value)
    
    def get_classification_annotations_by_label_and_value(self, label:Label, value:bool):
        """
        Get all image classification annotations for this frame with the given label and value.
        """
        return ImageClassificationAnnotation.objects.filter(legacy_frame=self, label=label, value=value)
    
    def __str__(self):
        return self.video.file.path + " - " + str(self.frame_number)
