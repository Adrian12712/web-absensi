from django.db import models
from django.utils import timezone

class Personel(models.Model):
    nama = models.CharField(max_length=150, unique=True, verbose_name="Nama Personel")
    aktif = models.BooleanField(default=True, verbose_name="Status Aktif", help_text="Hilangkan centang jika orang ini sudah tidak aktif/keluar")

    def __str__(self):
        return self.nama

class Absensi(models.Model):
    personel = models.ForeignKey(Personel, on_delete=models.CASCADE, related_name='riwayat_absen')
    tanggal = models.DateField(default=timezone.now, verbose_name="Tanggal Absen")
    waktu_input = models.TimeField(auto_now_add=True, verbose_name="Waktu Input")
    deskripsi = models.TextField(verbose_name="Deskripsi Kegiatan")

    class Meta:
        # Mencegah Admin secara tidak sengaja mengabsen orang yang sama dua kali di hari yang sama
        constraints = [
            models.UniqueConstraint(fields=['personel', 'tanggal'], name='unique_absen_harian')
        ]
        # Mengurutkan tampilan data dari yang terbaru
        ordering = ['-tanggal', '-waktu_input']

    def __str__(self):
        return f"{self.personel.nama} - {self.tanggal}"