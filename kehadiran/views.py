from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib import messages
from datetime import datetime
from .models import Personel, Absensi

@login_required
def dashboard(request):
    # Menampilkan 50 data absen terakhir
    riwayat = Absensi.objects.select_related('personel').all()[:50]
    return render(request, 'kehadiran/dashboard.html', {'riwayat': riwayat})

@login_required
def input_absen(request):
    if request.method == 'POST':
        personel_id = request.POST.get('personel')
        tanggal = request.POST.get('tanggal')
        deskripsi = request.POST.get('deskripsi')
        
        try:
            personel = Personel.objects.get(id=personel_id)
            Absensi.objects.create(personel=personel, tanggal=tanggal, deskripsi=deskripsi)
            messages.success(request, f"Absen {personel.nama} berhasil dicatat!")
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, "Gagal menyimpan! Pastikan orang ini belum absen di tanggal tersebut.")
    
    # Kirim daftar personel aktif ke form
    personel_aktif = Personel.objects.filter(aktif=True)
    # Kirim tanggal hari ini sebagai default (format YYYY-MM-DD)
    hari_ini = datetime.now().strftime('%Y-%m-%d')
    
    return render(request, 'kehadiran/input_absen.html', {
        'personel_aktif': personel_aktif, 
        'hari_ini': hari_ini
    })

@login_required
def rekap_bulanan(request):
    # Ambil input bulan/tahun dari filter (jika tidak ada, gunakan bulan/tahun saat ini)
    bulan = int(request.GET.get('bulan', datetime.now().month))
    tahun = int(request.GET.get('tahun', datetime.now().year))
    
    # Query: Filter absen berdasarkan bulan/tahun, kelompokkan berdasar nama, hitung jumlahnya
    rekap = Absensi.objects.filter(
        tanggal__month=bulan, 
        tanggal__year=tahun
    ).values('personel__nama').annotate(total_hadir=Count('id')).order_by('-total_hadir')
    
    return render(request, 'kehadiran/rekap.html', {
        'rekap': rekap,
        'bulan_pilih': bulan,
        'tahun_pilih': tahun
    })