from django.db import models

# Create your models here.
class molbank(models.Model):
    ID = models.CharField(default='DUMMY_ID',primary_key=True,max_length=10)
    SMILES = models.CharField(default='DUMMY_SMILES',max_length=150)
    SAMPLE_CODE = models.CharField(default='DUMMY_SAMPLE_CODE',max_length=20)
    class Meta:
    	permissions = (
    		('is_admin','MB: ADMIN'),
            ('is_chem','MB: CHEM'),
            ('is_bio','MB: BIO'),
            ('is_slab','MB: SLAB'),
    		)
class status(models.Model):
    name = models.CharField(default='NoName', max_length = 100)
    chemist = models.BooleanField(default=False)
    biologist = models.BooleanField(default=False)
    spectral = models.BooleanField(default=False)

    @classmethod
    def create(cls, name):
        file = cls(name=name)
        return file

class allplates(models.Model):
    Project = models.CharField(max_length=4)
    Position_in_Array = models.CharField(null=True, blank=True, max_length=4)
    sub_project = models.CharField(null=True, blank=True, max_length=4)
    MTP_Plate_No = models.CharField(null=True, blank=True, max_length=4)
    Structure = models.CharField(null=True, blank=True, max_length=1)
    Solution_PT_Barcode = models.IntegerField(null=True, blank=True)
    Array_PT_Barcode = models.CharField(null=True, blank=True, max_length=10)
    Tray_PT_Barcode = models.IntegerField(null=True, blank=True)
    Neat_sample_Barcode = models.IntegerField(null=True, blank=True)
    Array_NS_Barcode = models.IntegerField(null=True, blank=True)
    Tray_NS_Barcode = models.IntegerField(null=True, blank=True)
    Smiles = models.CharField(max_length=500)
    Sample_code = models.CharField(db_column='sample_code', primary_key=True, max_length=20)
    Molecular_Weight = models.DecimalField(decimal_places=3, max_digits=10)
    Molecular_Formula = models.CharField(max_length=500)
    CLogP = models.DecimalField(decimal_places=3, max_digits=10)
    Name = models.CharField(max_length=500)
    NMR = models.DecimalField(null=True, blank=True, decimal_places=3, max_digits=10)
    Mass = models.DecimalField(null=True, blank=True, decimal_places=3, max_digits=10)
    HPLC_or_LCMS = models.DecimalField(null=True, blank=True, decimal_places=3, max_digits=10)
    Solubility = models.DecimalField(null=True, blank=True, decimal_places=3, max_digits=10)
    No_of_Rings = models.IntegerField()
    No_of_nitrogens = models.IntegerField()
    No_of_Oxygens = models.IntegerField()
    TPSA = models.DecimalField(decimal_places=3, max_digits=10)
    No_of_Sulphur = models.IntegerField()
    Sample_Weight_submitted = models.CharField(max_length=10)
    Purity = models.DecimalField(null=True, blank=True, decimal_places=3, max_digits=10)
    IUPAC_Name = models.CharField(null=True, blank=True, max_length=500)
    Date_of_approval = models.DateField(null=True, blank=True)
    Date_of_Submission = models.DateField(null=True, blank=True)
    Scientist_name = models.CharField(max_length=30)
    Reference_syn_or_bio = models.CharField(null=True, blank=True, max_length=4)
    Known_bio_activity = models.CharField(null=True, blank=True, max_length=4)
    Natural_or_Synthetic = models.CharField(null=True, blank=True, max_length=4)
    Physical_state = models.CharField(null=True, blank=True, max_length=4)
    Sample_in = models.CharField(null=True, blank=True, max_length=4)
    Sample_out = models.CharField(null=True, blank=True, max_length=4)
    Miscellaneous = models.CharField(null=True, blank=True, max_length=4)
    Optical_Rotation = models.CharField(null=True, blank=True, max_length=4)
    Institute = models.CharField(max_length=10)