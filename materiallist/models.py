from django.db import models
import uuid

class Materials(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    Material_Code = models.CharField(max_length=255,blank=False,null=False,unique=True)
    Material_Name= models.CharField(max_length=255,blank=True,null=True)
    Material_Location=models.CharField(max_length=255,blank=True,null=True)
    Unit_of_Measurement=models.CharField(max_length=255,null=True, blank=True)  
    Maximum_Level=models.IntegerField(null=True, blank=True)
    Minimum_Level=models.IntegerField(null=True, blank=True)
    Re_order_Level=models.IntegerField(null=True, blank=True)
    Quantity=models.IntegerField(null=True,blank=True)

    def __unicode__(self):
        return self.Material_Code


class Transactions(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Transaction_Type=models.CharField(max_length=20,null=True)
    Received_From=models.CharField(max_length=200,null=True,blank=True)
    Number_Of_Received=models.IntegerField(null=True,blank=True)
    Issue_To=models.CharField(max_length=200,null=True,blank=True)
    Number_Of_Issued=models.IntegerField(null=True,blank=True)
    Balance=models.IntegerField(null=True,blank=True)
    Material_Name=models.ForeignKey(Materials,on_delete = models.CASCADE,related_name="display",null=True)
    Date=models.DateField(blank=True, null=True)
    Document_Number=models.IntegerField(unique=True)
    Verification_Date=models.DateField(blank=True, null=True)
    Verified_By=models.CharField(max_length=100)

    