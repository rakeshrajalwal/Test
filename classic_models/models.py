from django.db import models
#from django.contrib.gis.db import models

# Create your models here.
class customers(models.Model):
    customerNumber=models.IntegerField(primary_key=True,null=False)
    customerName=models.CharField(max_length=15,null=False)
    contactLastName=models.CharField(max_length=50,null=False)
    contactFirstName=models.CharField(max_length=50,null=False)
    phone=models.CharField(max_length=50,null=False)
    addressLine1=models.CharField(max_length=50,null=False)
    addressLine2=models.CharField(max_length=50,null=True)
    city=models.CharField(max_length=50,null=False)
    state=models.CharField(max_length=50,null=True)
    postalCode=models.CharField(max_length=15,null=True)
    country=models.CharField(max_length=50,null=False)
    salesRepEmployeeNumber=models.IntegerField(null=True)
    creditLimit=models.DecimalField(max_digits=32, decimal_places=8,null=True)
    class Meta:
        db_table='customers'
    def __str__(self):
        return u'%s %s %s %s %s %s' % (self.customerNumber,self.customerName,self.city,self.country,self.salesRepEmployeeNumber,self.creditLimit)

class CustomerGroup(models.Model):
    groupID=models.AutoField(primary_key=True)
    groupName=models.CharField(max_length=200)
    city=models.CharField(max_length=200,null=True,blank=True)
    country=models.CharField(max_length=200,null=True,blank=True)
    salesRepEmployeeNumber=models.CharField(max_length=200,null=True,blank=True)
    creditLimit=models.DecimalField(max_digits=32, decimal_places=8,null=True,blank=True)
    timeStamp=models.DateTimeField(auto_now=True)
    def __str__(self):
        return u'%s %s %s %s %s %s' % (self.groupID,self.groupName,self.city,self.country,self.salesRepEmployeeNumber,self.creditLimit)
    class Meta:
        db_table='customergroup'

class GroupList(models.Model):
    group_id=models.ForeignKey(CustomerGroup)
    customer_id=models.TextField("customer id")
    def __str__(self):
        return u'%s %s' % (self.group_id,self.customer_id)
    class Meta:
        db_table='grouplist'

class Campaigns(models.Model):
    campaignID=models.AutoField(primary_key=True)
    campaignName=models.CharField(max_length=200)
    timeStamp=models.DateTimeField(auto_now=True)
    def __str__(self):
        return u'%s %s' % (self.campaignID,self.campaignName)
    class Meta:
        db_table='campaigns'    

class CampaignForGroup(models.Model):
    campaignID=models.ForeignKey(Campaigns)
    groupID=models.IntegerField()
    startDate=models.DateField()
    def __str__(self):
        return u'%s %s %s' % (self.groupID,self.camapignID,self.startDate)
    class Meta:
        db_table='campaignforgroup'    
        
class campaign_targetgroup_players(models.Model):
    campaign_code=models.CharField(primary_key=True,max_length=15,null=False)
    target_group=models.CharField(max_length=15,null=False)
    wh_player_id=models.IntegerField(null=False)
    target_control_cd=models.CharField(max_length=15,null=False)
    def __str__(self):
        return u'%s %s %s %s' % (self.campaign_code,self.target_group,self.wh_player_id,self.target_control_cd)
    class Meta:
        db_table='campaign_targetgroup_players'

class campaigns_dps(models.Model):
    campaign_code=models.CharField(primary_key=True,max_length=15,null=False)
    campaign_name=models.CharField(max_length=50,null=False)
    def __str__(self):
        return u'%s %s' % (self.campaign_code,self.campaign_name)
    class Meta:
        db_table='campaigns_dps'
        
class campaigns_for_groups(models.Model):
    campaign_code=models.CharField(primary_key=True,max_length=15,null=False)
    target_group=models.CharField(max_length=15,null=False)
    start_date=models.DateField()
    def __str__(self):
        return u'%s %s %s' % (self.campaign_code,self.target_group,self.start_date)
    class Meta:
        db_table='campaigns_for_groups'
        
class daily_player_summary(models.Model):
    summary_date=models.DateField()
    wh_player_id=models.IntegerField(null=False)
    deposit_amt=models.DecimalField(max_digits=32, decimal_places=8,null=True,blank=True)
    trx_ggr_amt=models.DecimalField(max_digits=32, decimal_places=8,null=True,blank=True)
    def __str__(self):
        return u'%s %s %s %s' % (self.summary_date,self.wh_player_id,self.deposit_amt,self.trx_ggr_amt)
    class Meta:
        db_table='daily_player_summary'        
