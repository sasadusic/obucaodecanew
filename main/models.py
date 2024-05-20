from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

class Marka(models.Model):
    imeMarke = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.imeMarke
    
class Tip(models.Model):
    tip = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.tip

class Boja(models.Model):
    boja = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.boja
    
class VelicinaObuce(models.Model):
    velicina = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return str(self.velicina)

class VelicinaOdece(models.Model):
    velicina = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return str(self.velicina)

class SlikaObuce(models.Model):
    obuca = models.ForeignKey('Obuca', related_name='slike_obuce', on_delete=models.CASCADE)
    slika = models.ImageField(null=True, blank=True, upload_to='obuca_slike')

    def __str__(self):
        return str(self.slika)

class SlikaOdece(models.Model):
    odeca = models.ForeignKey('Odeca', related_name='slike_odece', on_delete=models.CASCADE)
    slika = models.ImageField(null=True, blank=True, upload_to='odeca_slike')

    def __str__(self):
        return f'Image for {self.odeca.naziv}'
    
@receiver(post_delete, sender=SlikaObuce)
def delete_slikaobuce_file(sender, instance, **kwargs):
    # Delete file from filesystem when corresponding `SlikaObuce` object is deleted.
    if instance.slika:
        if os.path.isfile(instance.slika.path):
            os.remove(instance.slika.path)

@receiver(post_delete, sender=SlikaOdece)
def delete_slikaodece_file(sender, instance, **kwargs):
    # Delete file from filesystem when corresponding `SlikaObuce` object is deleted.
    if instance.slika:
        if os.path.isfile(instance.slika.path):
            os.remove(instance.slika.path)

class Obuca(models.Model):
    naziv = models.CharField(max_length=100)
    sifra = models.PositiveIntegerField(null=True, blank=True, unique=True)
    cena = models.PositiveIntegerField()
    marka = models.ForeignKey(Marka, on_delete=models.CASCADE)
    boja = models.ManyToManyField(Boja)
    velicina = models.ManyToManyField(VelicinaObuce)
    stanje = models.CharField(max_length=50, null=True, blank=True)
    opis = models.TextField(null=True, blank=True)
    glavnaSlika = models.ImageField(upload_to='obuca_slike', null=True, blank=True)
    slike = models.ManyToManyField(SlikaObuce, related_name='obuce', null=True, blank=True)

    def prati(self, korisnik):
        Praćenje.objects.get_or_create(korisnik=korisnik, obuca=self)
    
    def odprati(self, korisnik):
        Praćenje.objects.filter(korisnik=korisnik, obuca=self).delete()

    def __str__(self):
        return self.naziv

class Odeca(models.Model):
    naziv = models.CharField(max_length=100)
    sifra = models.PositiveIntegerField(null=True, blank=True, unique=True)
    tip = models.ForeignKey(Tip, on_delete=models.CASCADE)
    cena = models.PositiveIntegerField()
    marka = models.ForeignKey(Marka, on_delete=models.CASCADE)
    boja = models.ManyToManyField(Boja)
    velicina = models.ManyToManyField(VelicinaOdece)
    stanje = models.CharField(max_length=50)
    opis = models.TextField()
    glavnaSlika = models.ImageField(upload_to='odeca_slike', null=True, blank=True)
    slike = models.ManyToManyField(SlikaOdece, related_name='odece')

    def prati(self, korisnik):
        Praćenje.objects.get_or_create(korisnik=korisnik, odeca=self)
    
    def odprati(self, korisnik):
        Praćenje.objects.filter(korisnik=korisnik, odeca=self).delete()

    def __str__(self):
        return self.naziv
    
class NacinKupovine(models.Model):
    naziv = models.CharField(max_length=100, null=True, blank=True, unique=True)
    text = models.CharField(max_length=1000, null=True, blank=True, unique=True)

    def __str__(self):
        return self.naziv
    
class Praćenje(models.Model):
    korisnik = models.ForeignKey(User, on_delete=models.CASCADE)
    obuca = models.ForeignKey(Obuca, on_delete=models.CASCADE, null=True, blank=True)
    odeca = models.ForeignKey(Odeca, on_delete=models.CASCADE, null=True, blank=True)
    prati = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.korisnik.username} prati {self.obuca or self.odeca}'