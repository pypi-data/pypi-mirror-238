from django.db import models
from datetime import date
import cv2
from tqdm import tqdm
from PIL import Image
import io
from django.core.files.base import ContentFile
from django.db import transaction
from ..label.label import Label
from ..annotation.image_classification import ImageClassificationAnnotation

BATCH_SIZE = 1000

class Video(models.Model):
    file = models.FileField(upload_to="raw_videos", blank=True, null=True)
    video_hash = models.CharField(max_length=255, unique=True)
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE, blank=True, null=True, related_name='videos')
    date = models.DateField(blank=True, null=True)
    suffix = models.CharField(max_length=255)
    fps = models.FloatField()
    duration = models.FloatField()
    width = models.IntegerField()
    height = models.IntegerField()

    meta = models.JSONField(blank=True, null=True)

    def get_frames(self):
        """
        Retrieve all frames for this video in the correct order.
        """
        return Frame.objects.filter(video=self).order_by('frame_number')
    
    def get_frame(self, frame_number):
        """
        Retrieve a specific frame for this video.
        """
        return Frame.objects.get(video=self, frame_number=frame_number)
    
    def initialize_metadata_in_db(self, video_meta=None):
        if not video_meta:
            video_meta = self.meta
        self.set_examination_date_from_video_meta(video_meta)
        self.patient, created = self.get_or_create_patient(video_meta)
        self.save()

    def get_or_create_patient(self, video_meta=None):
        from ..persons import Patient
        if not video_meta:
            video_meta = self.meta

        patient_first_name = video_meta['patient_first_name']
        patient_last_name = video_meta['patient_last_name']
        patient_dob = video_meta['patient_dob']

        # assert that we got all the necessary information
        assert patient_first_name and patient_last_name and patient_dob, "Missing patient information"

        patient, created = Patient.objects.get_or_create(
            first_name=patient_first_name,
            last_name=patient_last_name,
            dob=patient_dob
        )

        return patient, created

    def set_examination_date_from_video_meta(self, video_meta=None):
        if not video_meta:
            video_meta = self.meta
        date_str = video_meta['examination_date'] # e.g. 2020-01-01
        if date_str:
            self.date = date.fromisoformat(date_str)
            self.save()

    def extract_all_frames(self):
        """
        Extract all frames from the video and store them in the database.
        Uses Django's bulk_create for more efficient database operations.
        """
        # Open the video file
        video = cv2.VideoCapture(self.file.path)

        # Initialize video properties
        self.initialize_video_specs(video)

        # Prepare for batch operation
        frames_to_create = []

        # Extract frames
        for frame_number in tqdm(range(int(self.duration * self.fps))):
            # Read the frame
            success, image = video.read()
            if not success:
                break

            # Convert the numpy array to a PIL Image object
            pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            # Save the PIL Image to a buffer
            buffer = io.BytesIO()
            pil_image.save(buffer, format='JPEG')

            # Create a file-like object from the byte data in the buffer
            image_file = ContentFile(buffer.getvalue())

            # Prepare Frame instance (don't save yet)
            frame = Frame(
                video=self,
                frame_number=frame_number,
                suffix='jpg',
            )
            frame.image_file = image_file  # Temporary store the file-like object
            frames_to_create.append(frame)

            # Perform bulk create when reaching BATCH_SIZE
            if len(frames_to_create) >= BATCH_SIZE:
                with transaction.atomic():
                    Frame.objects.bulk_create(frames_to_create)

                    # After the DB operation, save the ImageField for each object
                    for frame in frames_to_create:
                        frame_name = f"video_{self.id}_frame_{str(frame.frame_number).zfill(7)}.jpg"
                        frame.image.save(frame_name, frame.image_file)

                    # Clear the list for the next batch
                    frames_to_create = []

        # Handle remaining frames
        if frames_to_create:
            with transaction.atomic():
                Frame.objects.bulk_create(frames_to_create)
                for frame in frames_to_create:
                    frame_name = f"video_{self.id}_frame_{str(frame.frame_number).zfill(7)}.jpg"
                    frame.image.save(frame_name, frame.image_file)

    def initialize_video_specs(self, video):
        """
        Initialize and save video metadata like framerate, dimensions, and duration.
        """
        self.fps = video.get(cv2.CAP_PROP_FPS)
        self.width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.duration = video.get(cv2.CAP_PROP_FRAME_COUNT) / self.fps
        self.save()


class Frame(models.Model):
    video = models.ForeignKey(Video, related_name='frames', on_delete=models.CASCADE)
    frame_number = models.IntegerField()
    # Add any other fields you need to store frame-related information
    image = models.ImageField(upload_to="frames")  # Or some other field type, depending on how you're storing the frame
    suffix = models.CharField(max_length=255)
    # ImageClassificationAnnotation has a foreign key to this model (related name: image_classification_annotations)

    class Meta:
        # Ensure that for each video, the frame_number is unique
        unique_together = ('video', 'frame_number')
        # Optimize for retrieval in frame_number order
        indexes = [models.Index(fields=['video', 'frame_number'])]

    def get_classification_annotations(self):
        """
        Get all image classification annotations for this frame.
        """
        return ImageClassificationAnnotation.objects.filter(frame=self)
    
    def get_classification_annotations_by_label(self, label:Label):
        """
        Get all image classification annotations for this frame with the given label.
        """
        return ImageClassificationAnnotation.objects.filter(frame=self, label=label)
    
    def get_classification_annotations_by_value(self, value:bool):
        """
        Get all image classification annotations for this frame with the given value.
        """
        return ImageClassificationAnnotation.objects.filter(frame=self, value=value)
    
    def get_classification_annotations_by_label_and_value(self, label:Label, value:bool):
        """
        Get all image classification annotations for this frame with the given label and value.
        """
        return ImageClassificationAnnotation.objects.filter(frame=self, label=label, value=value)
    

