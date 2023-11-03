from django.db import models

from .frame import LegacyFrame
import cv2
from tqdm import tqdm
from PIL import Image
import io
from django.core.files.base import ContentFile
from django.db import transaction

BATCH_SIZE = 1000

class LegacyVideo(models.Model):
    file = models.FileField(upload_to="legacy_videos", blank=True, null=True)
    video_hash = models.CharField(max_length=255, unique=True)
    import_date = models.DateTimeField(auto_now_add=True)
    suffix = models.CharField(max_length=255)
    fps = models.FloatField(blank=True, null=True)
    duration = models.FloatField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)

    def get_frames(self):
        """
        Retrieve all frames for this video in the correct order.
        """
        return LegacyFrame.objects.filter(video=self).order_by('frame_number')
    
    def get_frame(self, frame_number):
        """
        Retrieve a specific frame for this video.
        """
        return LegacyFrame.objects.get(video=self, frame_number=frame_number)
    
    def initialize_video_specs(self, video):
        """
        Initialize and save video metadata like framerate, dimensions, and duration.
        """
        self.fps = video.get(cv2.CAP_PROP_FPS)
        self.width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.duration = video.get(cv2.CAP_PROP_FRAME_COUNT) / self.fps
        self.save()
    
    def extract_all_frames(self):
        """
        Extract all frames from this video and save them to the database.
        Uses Django's bulk_create for more efficient database operations.
        """
        video = cv2.VideoCapture(self.file.path)

        # initialize video metadata
        self.initialize_video_specs(video)

        # Prepare for batch operation
        frames_to_create = []

        # get list of available frame_numbers
        frame_numbers = [frame.frame_number for frame in self.get_frames()]

        # extract frames
        for frame_number in tqdm(range(int(self.duration * self.fps))):
            # Skip if frame already exists
            if frame_number in frame_numbers:
                continue

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
            frame = LegacyFrame(
                video=self,
                frame_number=frame_number,
                suffix='jpg',
            )
            frame.image_file = image_file  # Temporary store the file-like object
            frames_to_create.append(frame)

            # Perform bulk create when reaching BATCH_SIZE
            if len(frames_to_create) >= BATCH_SIZE:
                with transaction.atomic():
                    LegacyFrame.objects.bulk_create(frames_to_create)

                    # After the DB operation, save the ImageField for each object
                    for frame in frames_to_create:
                        frame_name = f"video_{self.id}_frame_{str(frame.frame_number).zfill(7)}.jpg"
                        frame.image.save(frame_name, frame.image_file)

                    # Clear the list for the next batch
                    frames_to_create = []

        # Handle remaining frames
        if frames_to_create:
            with transaction.atomic():
                LegacyFrame.objects.bulk_create(frames_to_create)
                for frame in frames_to_create:
                    frame_name = f"video_{self.id}_frame_{str(frame.frame_number).zfill(7)}.jpg"
                    frame.image.save(frame_name, frame.image_file)



