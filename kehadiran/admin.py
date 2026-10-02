from django.contrib import admin
from .models import Personel, Absensi

@admin.register(Personel)
class PersonelAdmin(admin.ModelAdmin):
    list_display = ('nama', 'aktif')
    search_fields = ('nama',)
    list_filter = ('aktif',)

@admin.register(Absensi)
class AbsensiAdmin(admin.ModelAdmin):
    list_display = ('personel', 'tanggal', 'waktu_input', 'deskripsi_singkat')
    search_fields = ('personel__nama', 'deskripsi')
    list_filter = ('tanggal',)
    date_hierarchy = 'tanggal' # Memunculkan navigasi filter tanggal/bulan di atas tabel

    # Menyingkat teks deskripsi jika terlalu panjang di tabel
    def deskripsi_singkat(self, obj):
        return obj.deskripsi[:50] + '...' if len(obj.deskripsi) > 50 else obj.deskripsi
    deskripsi_singkat.short_description = 'Deskripsi'