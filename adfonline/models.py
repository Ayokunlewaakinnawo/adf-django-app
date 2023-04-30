from django.db import models

class ContactInfo(models.Model):
    Firstname = models.CharField(max_length=200, null=False, blank=False)
    Lastname = models.CharField(max_length=200, null=False, blank=False)
    Email = models.CharField(max_length=200, null=False, blank=False)
    Phone = models.CharField(max_length=200, null=False, blank=False)
    Description = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.Firstname
    
class RegisterEventInfo(models.Model):
    Firstname = models.CharField(max_length=200, null=False, blank=False)
    Lastname = models.CharField(max_length=200, null=False, blank=False)
    Email = models.CharField(max_length=200, null=False, blank=False)
    Phone = models.CharField(max_length=200, null=False, blank=False)
    Location = models.CharField(max_length=200, null=False, blank=False)
    RADIO_CHOICES = [
        ('student_radio', 'Student'),
        ('pro_radio', 'Professional'),
        ('content_radio', 'Content Creator'),
        ('consult_radio', 'Strategy & consulting'),
        ('business_radio', 'Business Owner'),
        ('gov_radio', 'Government/ Public Service'),
        ('other_radio', 'Other'),
    ]
    Category = models.CharField(max_length=20, choices=RADIO_CHOICES, default='other_radio')
    
    def __str__(self):
        return self.Firstname