from django.db import models

# Define RoomType model with many-to-many relationships
class RoomType(models.Model):
    name = models.CharField(max_length=100)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    descriptions = models.ManyToManyField('Description')
    images = models.ManyToManyField('Image')

    def __str__(self):
        return self.name

# Define Description model
class Description(models.Model):
    text = models.TextField()

    def __str__(self):
        return f"Description: {self.pk}"


# Define a model to store image sizes
class ImageSize(models.Model):
    width = models.PositiveIntegerField()  # Store the width of the image
    height = models.PositiveIntegerField()  # Store the height of the image

    def __str__(self):
        return f"Image Size: {self.width}x{self.height}"
    
# Define Image model
class Image(models.Model):
    image = models.ImageField(upload_to='room_type_images/')

    def __str__(self):
        return f"Image: {self.pk}"

# Define Client model to store guest information
class Client(models.Model):
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=20)

    def __str__(self):
        return self.guest_name

# Define Booking model
class Booking(models.Model):
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    occupants = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.client.guest_name}'s booking for {self.room_type.name} room"
