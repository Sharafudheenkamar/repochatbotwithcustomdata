from django.db import models

class RoomTable(models.Model):
    # LOGINID = models.ForeignKey('LoginTable', on_delete=models.CASCADE, null=True, blank=True)
    roomnumber = models.CharField(max_length=20, null=True, blank=True)
    roomtype = models.CharField(max_length=20, null=True, blank=True)
    bedtype = models.CharField(max_length=20, null=True, blank=True)
    roomimage = models.FileField(upload_to='roomimages/', null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)  # Changed to IntegerField for numeric queries
    roomservice = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=25, null=True, blank=True)

class RestaurantTable(models.Model):
    #  LOGINID =models.ForeignKey(LoginTable, on_delete=models.CASCADE)
     name=models.CharField(max_length=20, null=True,blank=True)
     place=models.CharField(max_length=20, null=True,blank=True)
     phoneno=models.BigIntegerField(null=True,blank=True)
     email=models.CharField(max_length=20, null=True,blank=True)

class RentedVehicle(models.Model):
    location = models.CharField(max_length=100, null=True, blank=True)
    contactno = models.CharField(max_length=15, null=True, blank=True)
    vehicletype = models.CharField(max_length=50, null=True, blank=True)
    rent = models.IntegerField(null=True, blank=True)  # Changed to IntegerField for numeric queries

class Spot(models.Model):
    location = models.CharField(max_length=100, null=True, blank=True)
    placename = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    ticket = models.CharField(max_length=10, choices=(('free', 'Free'), ('paid', 'Paid')))
    ticket_charge = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # For paid spots
    

    location = models.CharField(max_length=100, null=True, blank=True)
