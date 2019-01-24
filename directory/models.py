from django.db import models


class CertifiedCoach(models.Model):
    class Meta:
        db_table = 'fitpro_directory'

    id = models.AutoField(primary_key=True)
    userid = models.IntegerField(null=True)
    source = models.CharField(max_length=80, null=True, blank=True)
    fullname = models.CharField(max_length=255, null=True, blank=True)
    business_name = models.CharField(max_length=255, db_column='businessname', null=True, blank=True)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, db_column='postalcode', null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    business_phone = models.CharField(max_length=255, db_column='businessphone', null=True, blank=True)
    mobile_phone = models.CharField(max_length=255, db_column='mobilephone', null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    specialty = models.TextField()
    show_in_directory = models.IntegerField(default=0)
    level1_status = models.IntegerField(default=0)
    level2_status = models.IntegerField(default=0)
    procoach_status = models.IntegerField(default=0)
    url_last_checked = models.IntegerField(null=True)
    url_last_status = models.IntegerField(null=True)

    @property
    def location(self):
        """The location field which includes all address fields that are populated (not empty)."""
        location_fields = [
            self.address1,
            self.address2,
            self.city,
            ' '.join(filter(None, [self.province, self.postal_code])),
            self.country,
        ]
        return ', '.join(filter(None, location_fields))

    @property
    def certification_level(self):
        """Comma-separated string of certification the coach has achieved"""
        cert_level_achieved = filter(lambda status_map: status_map[1], [
            ('Level 1', self.level1_status),
            ('Level 2', self.level2_status),
            ('Procoach', self.procoach_status)
        ])
        return ','.join([cert[0] for cert in cert_level_achieved])
