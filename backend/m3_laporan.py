import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from m1_pesanan import Pesanan

class PenghitungLangkah:
    """Objek sederhana untuk mencatat jumlah perbandingan dan pemindahan data"""
    def __init__(self):
        self.banding = 0
        self.pindah = 0
        
    def reset(self):
        self.banding = 0
        self.pindah = 0

def dapatkan_kunci(pesanan, nama_kunci):
    """Fungsi pembantu untuk mengambil atribut objek berdasarkan nama kunci"""
    if nama_kunci == 'oid': return pesanan.oid
    if nama_kunci == 'harga': return pesanan.harga
    if nama_kunci == 'selesai': return pesanan.waktu_selesai
    return pesanan.oid

# ==========================================
# ALGORITMA PENGURUTAN (SORTING)
# ==========================================
def insertion_sort(larik, kunci_urut="harga", batas=None):
    """O(n^2) - Stabil. Digunakan untuk data kecil."""
    stats = PenghitungLangkah()
    
    # Ambil elemen mentah ke dalam list biasa
    data_list = []
    total = batas if batas else larik.ukuran
    for i in range(total):
        data_list.append(larik.get(i))
        
    # Proses Insertion Sort
    for i in range(1, len(data_list)):
        elemen_saat_ini = data_list[i]
        nilai_saat_ini = dapatkan_kunci(elemen_saat_ini, kunci_urut)
        j = i - 1
        
        while j >= 0:
            stats.banding += 1
            # Syarat > memastikan kestabilan (elemen sama tidak digeser)
            if dapatkan_kunci(data_list[j], kunci_urut) > nilai_saat_ini:
                data_list[j + 1] = data_list[j]
                stats.pindah += 1
                j -= 1
            else:
                break
                
        data_list[j + 1] = elemen_saat_ini
        stats.pindah += 1
        
    return data_list, stats.banding, stats.pindah


def merge_sort(larik, kunci_urut="oid", batas=None):
    """O(n log n) - Stabil. Digunakan untuk data besar."""
    stats = PenghitungLangkah()
    
    # Ambil elemen mentah
    data_list = []
    total = batas if batas else larik.ukuran
    for i in range(total):
        data_list.append(larik.get(i))
        
    def _merge_sort_rekursif(data):
        if len(data) <= 1:
            return data
            
        mid = len(data) // 2
        kiri = _merge_sort_rekursif(data[:mid])
        kanan = _merge_sort_rekursif(data[mid:])
        
        return _gabungkan(kiri, kanan)
        
    def _gabungkan(kiri, kanan):
        hasil = []
        i = j = 0
        
        while i < len(kiri) and j < len(kanan):
            stats.banding += 1
            # Syarat <= memastikan elemen kiri didahulukan (stabil)
            if dapatkan_kunci(kiri[i], kunci_urut) <= dapatkan_kunci(kanan[j], kunci_urut):
                hasil.append(kiri[i])
                stats.pindah += 1
                i += 1
            else:
                hasil.append(kanan[j])
                stats.pindah += 1
                j += 1
                
        # Sisa elemen
        while i < len(kiri):
            hasil.append(kiri[i])
            stats.pindah += 1
            i += 1
        while j < len(kanan):
            hasil.append(kanan[j])
            stats.pindah += 1
            j += 1
            
        return hasil

    data_terurut = _merge_sort_rekursif(data_list)
    return data_terurut, stats.banding, stats.pindah


# ==========================================
# ALGORITMA PENCARIAN (SEARCHING)
# ==========================================
def linear_search(larik, target_oid):
    """O(n) - Tidak butuh data terurut"""
    banding = 0
    for i in range(larik.ukuran):
        banding += 1
        p = larik.get(i)
        if p.oid == target_oid:
            return i, banding, p
    return -1, banding, None

def binary_search(data_terurut_list, target_oid):
    """O(log n) - Wajib data terurut"""
    banding = 0
    lo = 0
    hi = len(data_terurut_list) - 1
    
    while lo <= hi:
        banding += 1
        mid = (lo + hi) // 2
        
        if data_terurut_list[mid].oid == target_oid:
            return mid, banding, data_terurut_list[mid]
        elif data_terurut_list[mid].oid < target_oid:
            lo = mid + 1
        else:
            hi = mid - 1
            
    return -1, banding, None