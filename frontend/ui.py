import tkinter as tk
from tkinter import ttk, messagebox
import time
import sys
import os

# Menyambungkan folder frontend ke folder backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from m1_pesanan import muat_pesanan_csv, Pesanan
from m2_antrean import ManajerAntrean, ke_postfix, hitung_postfix
from m3_laporan import insertion_sort, merge_sort, linear_search, binary_search

class Aplikasi2EZ4U:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Delivery - Project Struktur Data")
        self.root.geometry("1100x700")

        # Variabel Status Backend
        self.array_pesanan = None
        self.ll_pesanan = None
        self.manajer_q = ManajerAntrean() 
        self.data_terurut_oid = None      

        self.buat_antarmuka()
        self.muat_data_awal()

    def buat_antarmuka(self):
        self.tab_kontrol = ttk.Notebook(self.root)
        self.tab_kontrol.pack(side="left", fill="y", padx=5, pady=5)

        # TAB NAVIGASI KIRI
        self.frame_m1 = tk.Frame(self.tab_kontrol, width=300, bg="#2c3e50", padx=10, pady=10)
        self.tab_kontrol.add(self.frame_m1, text="M1: Data Array")

        self.frame_m2 = tk.Frame(self.tab_kontrol, width=300, bg="#27ae60", padx=10, pady=10)
        self.tab_kontrol.add(self.frame_m2, text="M2: Stack & Queue")
        
        self.frame_m3 = tk.Frame(self.tab_kontrol, width=300, bg="#8e44ad", padx=10, pady=10)
        self.tab_kontrol.add(self.frame_m3, text="M3: Sort & Search")

        # M1: ARRAY VS LINKED LIST
        tk.Label(self.frame_m1, text="--- ARRAY ---", bg="#2c3e50", fg="#f39c12", font=("Arial", 9, "bold")).pack(pady=(5, 2))
        tk.Button(self.frame_m1, text="Lihat Pesanan (Indeks ke-100k)", command=self.array_lihat).pack(fill="x", pady=2)
        tk.Button(self.frame_m1, text="Tambah Reguler (Tail)", command=self.array_tambah_reguler).pack(fill="x", pady=2)
        tk.Button(self.frame_m1, text="Tambah Prioritas (Tengah)", command=self.array_tambah_prioritas).pack(fill="x", pady=2)
        tk.Button(self.frame_m1, text="Tambah VIP (Head)", command=self.array_tambah_vip).pack(fill="x", pady=2)
        tk.Button(self.frame_m1, text="Hapus Pesanan (Head)", command=self.array_hapus).pack(fill="x", pady=2)
        
        tk.Frame(self.frame_m1, height=2, bg="#7f8c8d").pack(fill="x", pady=15)
        
        tk.Label(self.frame_m1, text="--- LINKED LIST ---", bg="#2c3e50", fg="#1abc9c", font=("Arial", 9, "bold")).pack(pady=(5, 2))
        tk.Button(self.frame_m1, text="Lihat Pesanan (Indeks ke-100k)", command=self.ll_lihat).pack(fill="x", pady=2)
        tk.Button(self.frame_m1, text="Tambah Reguler (Tail)", command=self.ll_tambah_reguler).pack(fill="x", pady=2)
        tk.Button(self.frame_m1, text="Tambah Prioritas (Tengah)", command=self.ll_tambah_prioritas).pack(fill="x", pady=2)
        tk.Button(self.frame_m1, text="Tambah VIP (Head)", command=self.ll_tambah_vip).pack(fill="x", pady=2)
        tk.Button(self.frame_m1, text="Hapus Pesanan (Head)", command=self.ll_hapus).pack(fill="x", pady=2)

        # M2: KASIR, UNDO/REDO, DAN DAPUR
        tk.Label(self.frame_m2, text="--- KASIR (STACK) ---", bg="#27ae60", fg="white", font=("Arial", 10, "bold")).pack(pady=(0, 2))
        self.entry_kasir = tk.Entry(self.frame_m2, font=("Arial", 10))
        self.entry_kasir.insert(0, "(3*12000)+(2*8500)-5000")
        self.entry_kasir.pack(fill="x", pady=5)
        tk.Button(self.frame_m2, text="Hitung Struk (Infix -> Postfix)", bg="#f1c40f", command=self.m2_hitung_kasir).pack(fill="x", pady=2)

        tk.Frame(self.frame_m2, height=2, bg="white").pack(fill="x", pady=15)

        tk.Label(self.frame_m2, text="--- RIWAYAT (UNDO/REDO) ---", bg="#27ae60", fg="white", font=("Arial", 10, "bold")).pack(pady=2)
        tk.Button(self.frame_m2, text="⬅️ UNDO", bg="#e67e22", fg="white", command=self.m2_undo).pack(fill="x", pady=2)
        tk.Button(self.frame_m2, text="➡️ REDO", bg="#d35400", fg="white", command=self.m2_redo).pack(fill="x", pady=2)

        tk.Frame(self.frame_m2, height=2, bg="white").pack(fill="x", pady=15)

        tk.Label(self.frame_m2, text="--- DAPUR (QUEUE) ---", bg="#27ae60", fg="white", font=("Arial", 10, "bold")).pack(pady=2)
        tk.Button(self.frame_m2, text="📥 ENQUEUE (Massal 20rb)", bg="#3498db", fg="white", command=self.m2_enqueue_massal).pack(fill="x", pady=5)
        tk.Button(self.frame_m2, text="🐢 DEQUEUE (Array)", bg="#e74c3c", fg="white", command=self.m2_dequeue_naif).pack(fill="x", pady=2)
        tk.Button(self.frame_m2, text="⚡ DEQUEUE (Circular)", bg="#9b59b6", fg="white", command=self.m2_dequeue_circular).pack(fill="x", pady=2)

        # M3: SORT DAN SEARCH
        tk.Label(self.frame_m3, text="--- SORTING (PENGURUTAN) ---", bg="#8e44ad", fg="white", font=("Arial", 10, "bold")).pack(pady=(0, 2))
        
        tk.Label(self.frame_m3, text="Jumlah Data (Max 200rb untuk Merge):", bg="#8e44ad", fg="white").pack(anchor="w")
        self.entry_jumlah_sort = tk.Entry(self.frame_m3)
        self.entry_jumlah_sort.insert(0, "4000")
        self.entry_jumlah_sort.pack(fill="x", pady=2)
        
        tk.Label(self.frame_m3, text="Kunci Urut (oid / harga / selesai):", bg="#8e44ad", fg="white").pack(anchor="w")
        self.entry_kunci_sort = tk.Entry(self.frame_m3)
        self.entry_kunci_sort.insert(0, "harga")
        self.entry_kunci_sort.pack(fill="x", pady=5)

        tk.Button(self.frame_m3, text="Insertion Sort O(n²)", bg="#f1c40f", command=self.m3_insertion_sort).pack(fill="x", pady=2)
        tk.Button(self.frame_m3, text="Merge Sort O(n log n)", bg="#e67e22", command=self.m3_merge_sort).pack(fill="x", pady=2)

        tk.Frame(self.frame_m3, height=2, bg="white").pack(fill="x", pady=15)

        tk.Label(self.frame_m3, text="--- SEARCHING (PENCARIAN) ---", bg="#8e44ad", fg="white", font=("Arial", 10, "bold")).pack(pady=2)
        tk.Label(self.frame_m3, text="Cari Nomor OID (Misal: O-137442):", bg="#8e44ad", fg="white").pack(anchor="w")
        
        self.entry_cari_oid = tk.Entry(self.frame_m3)
        self.entry_cari_oid.insert(0, "O-137442")
        self.entry_cari_oid.pack(fill="x", pady=5)

        tk.Button(self.frame_m3, text="Linear Search O(n)", bg="#3498db", fg="white", command=self.m3_linear_search).pack(fill="x", pady=2)
        tk.Button(self.frame_m3, text="Binary Search O(log n)", bg="#2980b9", fg="white", command=self.m3_binary_search).pack(fill="x", pady=2)

        # PANEL KANAN UTAMA: Output & Log
        frame_kanan = tk.Frame(self.root, bg="#ecf0f1", padx=10, pady=10)
        frame_kanan.pack(side="right", fill="both", expand=True)

        tk.Label(frame_kanan, text="Layar Informasi / Output", bg="#ecf0f1", font=("Arial", 10, "bold")).pack(anchor="w")
        self.layar_hasil = tk.Text(frame_kanan, height=20, font=("Consolas", 10))
        self.layar_hasil.pack(fill="both", expand=True, pady=(2, 10))

        tk.Label(frame_kanan, text="Command Log & Eksekusi (Milidetik)", bg="#ecf0f1", font=("Arial", 10, "bold")).pack(anchor="w")
        self.layar_log = tk.Text(frame_kanan, height=10, bg="#111111", fg="#00ff00", font=("Consolas", 10))
        self.layar_log.pack(fill="x", pady=(2, 0))

    # FUNGSI UTILITAS
    def muat_data_awal(self):
        self.layar_hasil.insert(tk.END, "Memuat dataset pesanan 200.000 baris...\n")
        self.root.update()

        jalur_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'pesanan.csv'))
        mulai = time.perf_counter()
        self.array_pesanan, self.ll_pesanan = muat_pesanan_csv(jalur_csv)
        selesai = time.perf_counter()
        
        self.layar_hasil.insert(tk.END, f"✅ Selesai: {self.ll_pesanan.ukuran} baris terbaca ke Array & Linked List.\n\n")
        self.catat_log("Sistem", "Load CSV 200k", (selesai - mulai) * 1000)

    def catat_log(self, modul, perintah, waktu_ms):
        teks = f"[{modul:<10}] {perintah:<25} | Waktu: {waktu_ms:.4f} ms\n"
        self.layar_log.insert(tk.END, teks)
        self.layar_log.see(tk.END)

    def cetak_status_antrean(self):
        q_n = self.manajer_q.q_naif.data.ukuran
        q_c = self.manajer_q.q_circular.count
        u = self.manajer_q.stack_undo.data.ukuran
        r = self.manajer_q.stack_redo.data.ukuran
        self.layar_hasil.insert(tk.END, f"-> Status Antrean saat ini: Naif = {q_n}, Circular = {q_c}\n")
        self.layar_hasil.insert(tk.END, f"-> Stack Undo = {u} catatan, Redo = {r} catatan.\n\n")
        self.layar_hasil.see(tk.END)

    def buat_dummy(self, prioritas):
        return Pesanan(f"O-TEST", "Tamu VIP", "Restoran XYZ", "Kopi", 25000, prioritas, "12:00", "", "ANTRE")

    # AKSI M1: ARRAY VS LINKED LIST 
    def array_lihat(self):
        mulai = time.perf_counter()
        p = self.array_pesanan.get(100000)
        waktu = (time.perf_counter() - mulai) * 1000
        self.catat_log("M1-Array", "Lihat Indeks 100k", waktu)
        self.layar_hasil.insert(tk.END, f"🔍 ARRAY Lihat (Indeks 100k): Ditemukan {p.pelanggan} ({waktu:.4f} ms)\n")
        self.layar_hasil.see(tk.END)
        
    def array_tambah_reguler(self):
        mulai = time.perf_counter()
        self.array_pesanan.append(self.buat_dummy(3))
        waktu = (time.perf_counter() - mulai) * 1000
        self.catat_log("M1-Array", "Tambah Reguler", waktu)
        self.layar_hasil.insert(tk.END, f"➕ ARRAY Tambah Reguler di Belakang ({waktu:.4f} ms)\n")
        self.layar_hasil.see(tk.END)

    def array_tambah_prioritas(self):
        mulai = time.perf_counter()
        self.array_pesanan.insert(100000, self.buat_dummy(2))
        waktu = (time.perf_counter() - mulai) * 1000
        self.catat_log("M1-Array", "Tambah Prioritas", waktu)
        self.layar_hasil.insert(tk.END, f"⚡ ARRAY Tambah Prioritas di Tengah/Indeks 100k ({waktu:.4f} ms)\n")
        self.layar_hasil.see(tk.END)

    def array_tambah_vip(self):
        mulai = time.perf_counter()
        self.array_pesanan.insert_front(self.buat_dummy(1))
        waktu = (time.perf_counter() - mulai) * 1000
        self.catat_log("M1-Array", "Tambah VIP", waktu)
        self.layar_hasil.insert(tk.END, f"👑 ARRAY Tambah VIP di Depan/Head ({waktu:.4f} ms)\n")
        self.layar_hasil.see(tk.END)
        
    def array_hapus(self):
        mulai = time.perf_counter()
        self.array_pesanan.delete(0)
        waktu = (time.perf_counter() - mulai) * 1000
        self.catat_log("M1-Array", "Hapus Depan", waktu)
        self.layar_hasil.insert(tk.END, f"❌ ARRAY Hapus Pesanan Terdepan ({waktu:.4f} ms)\n")
        self.layar_hasil.see(tk.END)

    def ll_lihat(self):
        mulai = time.perf_counter()
        p = self.ll_pesanan.get(100000)
        waktu = (time.perf_counter() - mulai) * 1000
        self.catat_log("M1-LL", "Lihat Indeks 100k", waktu)
        self.layar_hasil.insert(tk.END, f"🔍 LINKED LIST Lihat (Indeks 100k): Ditemukan {p.pelanggan} ({waktu:.4f} ms)\n")
        self.layar_hasil.see(tk.END)
        
    def ll_tambah_reguler(self):
        mulai = time.perf_counter()
        self.ll_pesanan.append(self.buat_dummy(3))
        waktu = (time.perf_counter() - mulai) * 1000
        self.catat_log("M1-LL", "Tambah Reguler", waktu)
        self.layar_hasil.insert(tk.END, f"➕ LINKED LIST Tambah Reguler di Belakang ({waktu:.4f} ms)\n")
        self.layar_hasil.see(tk.END)

    def ll_tambah_prioritas(self):
        mulai = time.perf_counter()
        self.ll_pesanan.insert(100000, self.buat_dummy(2))
        waktu = (time.perf_counter() - mulai) * 1000
        self.catat_log("M1-LL", "Tambah Prioritas", waktu)
        self.layar_hasil.insert(tk.END, f"⚡ LINKED LIST Tambah Prioritas di Tengah/Indeks 100k ({waktu:.4f} ms)\n")
        self.layar_hasil.see(tk.END)

    def ll_tambah_vip(self):
        mulai = time.perf_counter()
        self.ll_pesanan.insert_front(self.buat_dummy(1))
        waktu = (time.perf_counter() - mulai) * 1000
        self.catat_log("M1-LL", "Tambah VIP", waktu)
        self.layar_hasil.insert(tk.END, f"👑 LINKED LIST Tambah VIP di Depan/Head ({waktu:.4f} ms)\n")
        self.layar_hasil.see(tk.END)
        
    def ll_hapus(self):
        mulai = time.perf_counter()
        self.ll_pesanan.delete(0)
        waktu = (time.perf_counter() - mulai) * 1000
        self.catat_log("M1-LL", "Hapus Depan", waktu)
        self.layar_hasil.insert(tk.END, f"❌ LINKED LIST Hapus Pesanan Terdepan ({waktu:.4f} ms)\n")
        self.layar_hasil.see(tk.END)
 
    # AKSI M2: KASIR, UNDO/REDO, QUEUE
    def m2_hitung_kasir(self):
        ekspresi = self.entry_kasir.get()
        mulai = time.perf_counter()
        
        teks_postfix = ke_postfix(ekspresi)
        hasil = hitung_postfix(teks_postfix)
        
        waktu = (time.perf_counter() - mulai) * 1000
        
        self.layar_hasil.insert(tk.END, f"--- PERHITUNGAN KASIR (STACK) ---\n")
        self.layar_hasil.insert(tk.END, f"Struk Masuk (Infix) : {ekspresi}\n")
        self.layar_hasil.insert(tk.END, f"Dikonversi (Postfix): {teks_postfix}\n")
        self.layar_hasil.insert(tk.END, f"TOTAL BELANJA       : Rp {hasil:,}\n\n")
        self.layar_hasil.see(tk.END)
        self.catat_log("M2-Stack", "Hitung Struk Kasir", waktu)

    def m2_enqueue_massal(self):
        self.layar_hasil.insert(tk.END, "Memasukkan 20.000 pesanan awal ke Antrean Naif & Circular...\n")
        self.root.update()

        mulai = time.perf_counter()
        for i in range(20000):
            p = self.array_pesanan.get(i)
            if p: self.manajer_q.aksi_enqueue(p)
        waktu = (time.perf_counter() - mulai) * 1000
        
        self.layar_hasil.insert(tk.END, f"✅ ENQUEUE Selesai!\n")
        self.cetak_status_antrean()
        self.catat_log("M2-Queue", "Enqueue Massal", waktu)

    def m2_dequeue_naif(self):
        self.manajer_q.q_naif.total_geser = 0
        mulai = time.perf_counter()
        pesanan = self.manajer_q.q_naif.dequeue()
        waktu = (time.perf_counter() - mulai) * 1000
        
        if pesanan:
            self.layar_hasil.insert(tk.END, f"🐢 DEQUEUE NAIF: 1 pesanan keluar.\n")
            self.layar_hasil.insert(tk.END, f"Beban Array: Menggeser {self.manajer_q.q_naif.total_geser} sisa data ke depan.\n")
            self.layar_hasil.insert(tk.END, f"Sisa Antrean Naif = {self.manajer_q.q_naif.data.ukuran}\n\n")
        self.layar_hasil.see(tk.END)
        self.catat_log("M2-Q-Naif", "Dequeue 1 Pesanan", waktu)

    def m2_dequeue_circular(self):
        mulai = time.perf_counter()
        pesanan = self.manajer_q.q_circular.dequeue()
        waktu = (time.perf_counter() - mulai) * 1000
        
        if pesanan:
            self.layar_hasil.insert(tk.END, f"⚡ DEQUEUE CIRCULAR: 1 pesanan keluar.\n")
            self.layar_hasil.insert(tk.END, f"Beban: Menggeser 0 data. Pointer Front maju 1 langkah.\n")
            self.layar_hasil.insert(tk.END, f"Sisa Antrean Circular = {self.manajer_q.q_circular.count}\n\n")
        self.layar_hasil.see(tk.END)
        self.catat_log("M2-Q-Circ", "Dequeue 1 Pesanan", waktu)

    def m2_undo(self):
        mulai = time.perf_counter(); berhasil = self.manajer_q.undo_last(); waktu = (time.perf_counter() - mulai) * 1000
        if berhasil:
            self.layar_hasil.insert(tk.END, f"⏪ UNDO Berhasil: Aksi dikembalikan ke status sebelumnya.\n")
            self.cetak_status_antrean()
            self.catat_log("M2-Stack", "Undo Terakhir", waktu)

    def m2_redo(self):
        mulai = time.perf_counter(); berhasil = self.manajer_q.redo_last(); waktu = (time.perf_counter() - mulai) * 1000
        if berhasil:
            self.layar_hasil.insert(tk.END, f"⏩ REDO Berhasil: Aksi yang batal diulangi kembali.\n")
            self.cetak_status_antrean()
            self.catat_log("M2-Stack", "Redo Batal", waktu)


    # AKSI M3: SORTING DAN SEARCHING
    def m3_insertion_sort(self):
        batas_teks = self.entry_jumlah_sort.get().strip()
        kunci = self.entry_kunci_sort.get().strip()
        batas = int(batas_teks) if batas_teks else self.array_pesanan.ukuran
        
        # Cegah Insertion Sort untuk memproses data terlampau besar agar UI tidak macet
        if batas > 20000:
            messagebox.showwarning("DITOLAK", "Batas Insertion Sort maksimal 20.000. Gunakan Merge Sort untuk data besar!")
            return
            
        mulai = time.perf_counter()
        hasil, banding, pindah = insertion_sort(self.array_pesanan, kunci_urut=kunci, batas=batas)
        waktu = (time.perf_counter() - mulai) * 1000
        
        self.cetak_hasil_sort("Insertion Sort", len(hasil), kunci, hasil, banding, pindah)
        self.catat_log("M3-Sort", "Insertion Sort", waktu)

    def m3_merge_sort(self):
        batas_teks = self.entry_jumlah_sort.get().strip()
        kunci = self.entry_kunci_sort.get().strip()
        batas = int(batas_teks) if batas_teks else self.array_pesanan.ukuran
        
        mulai = time.perf_counter()
        hasil, banding, pindah = merge_sort(self.array_pesanan, kunci_urut=kunci, batas=batas)
        waktu = (time.perf_counter() - mulai) * 1000
        
        self.cetak_hasil_sort("Merge Sort", len(hasil), kunci, hasil, banding, pindah)
        self.catat_log("M3-Sort", "Merge Sort", waktu)
        
        if kunci == "oid":
            self.data_terurut_oid = hasil

    def cetak_hasil_sort(self, nama, total_data, kunci, hasil, banding, pindah):
        self.layar_hasil.delete(1.0, tk.END)
        self.layar_hasil.insert(tk.END, f"=== HASIL {nama.upper()} ===\n")
        self.layar_hasil.insert(tk.END, f"{total_data} pesanan diurutkan menurut '{kunci}'.\n")
        self.layar_hasil.insert(tk.END, f"Beban Algoritma: {banding:,} perbandingan, {pindah:,} pemindahan.\n\n")
        
        for i in range(min(10, len(hasil))):
            p = hasil[i]
            self.layar_hasil.insert(tk.END, f"[{i+1}] OID: {p.oid} | Harga: {p.harga} | Selesai: {p.waktu_selesai} | {p.pelanggan}\n")
        self.layar_hasil.see(tk.END)

    def m3_linear_search(self):
        target = self.entry_cari_oid.get().strip()
        
        mulai = time.perf_counter()
        idx, banding, p = linear_search(self.array_pesanan, target)
        waktu = (time.perf_counter() - mulai) * 1000
        
        self.layar_hasil.delete(1.0, tk.END)
        self.layar_hasil.insert(tk.END, f"=== HASIL LINEAR SEARCH (Pencarian Kasar) ===\n")
        if p:
            self.layar_hasil.insert(tk.END, f"Ditemukan pada indeks awal {idx}.\n")
            self.layar_hasil.insert(tk.END, f"Beban: {banding:,} kali perbandingan baris per baris.\n\n")
            self.layar_hasil.insert(tk.END, f"Data: {p.oid} | {p.pelanggan} | {p.menu} | Rp {p.harga}\n")
        else:
            self.layar_hasil.insert(tk.END, f"Pesanan '{target}' tidak ditemukan di sistem.\n")
            
        self.catat_log("M3-Search", "Linear Search", waktu)

    def m3_binary_search(self):
        target = self.entry_cari_oid.get().strip()
        
        # PERLINDUNGAN OTOMATIS
        if getattr(self, "data_terurut_oid", None) is None:
            self.layar_hasil.insert(tk.END, "⚠️ Daftar terurut belum tersedia di memori.\nSedang membangun indeks dengan Merge Sort otomatis...\n")
            self.root.update()
            hasil, banding, pindah = merge_sort(self.array_pesanan, kunci_urut="oid", batas=self.array_pesanan.ukuran)
            self.data_terurut_oid = hasil
            
        mulai = time.perf_counter()
        idx, banding, p = binary_search(self.data_terurut_oid, target)
        waktu = (time.perf_counter() - mulai) * 1000
        
        self.layar_hasil.delete(1.0, tk.END)
        self.layar_hasil.insert(tk.END, f"=== HASIL BINARY SEARCH (Pencarian Cerdas) ===\n")
        if p:
            self.layar_hasil.insert(tk.END, f"Ditemukan pada baris ke-{idx} di dalam daftar terurut.\n")
            self.layar_hasil.insert(tk.END, f"Beban SUPER RINGAN: Hanya butuh {banding:,} kali perbandingan!\n\n")
            self.layar_hasil.insert(tk.END, f"Data: {p.oid} | {p.pelanggan} | {p.menu} | Rp {p.harga}\n")
        else:
            self.layar_hasil.insert(tk.END, f"Pesanan '{target}' tidak ditemukan dalam memori.\n")
            
        self.layar_hasil.see(tk.END)
        self.catat_log("M3-Search", "Binary Search", waktu)