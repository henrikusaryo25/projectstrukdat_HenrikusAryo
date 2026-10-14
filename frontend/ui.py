import tkinter as tk
from tkinter import ttk, messagebox
import time
import sys
import os

# Menyambungkan folder frontend ke folder backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from m1_pesanan import muat_pesanan_csv, Pesanan
from m2_antrean import ManajerAntrean, ke_postfix, hitung_postfix

class Aplikasi2EZ4U:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Delivery - M1 & M2")
        self.root.geometry("1100x700")

        # Variabel Status
        self.array_pesanan = None
        self.ll_pesanan = None
        self.manajer_q = ManajerAntrean() # Objek M2

        self.buat_antarmuka()
        self.muat_data_awal()

    def buat_antarmuka(self):
        self.tab_kontrol = ttk.Notebook(self.root)
        self.tab_kontrol.pack(side="left", fill="y", padx=5, pady=5)

        # Tab M1 (Kiri)
        self.frame_m1 = tk.Frame(self.tab_kontrol, width=300, bg="#2c3e50", padx=10, pady=10)
        self.tab_kontrol.add(self.frame_m1, text="M1: Data Array")

        # Tab M2 (Kiri)
        self.frame_m2 = tk.Frame(self.tab_kontrol, width=300, bg="#27ae60", padx=10, pady=10)
        self.tab_kontrol.add(self.frame_m2, text="M2: Stack & Queue")

        # ISI TAB M1
        tk.Label(self.frame_m1, text="--- ARRAY ---", bg="#2c3e50", fg="#f39c12").pack(pady=(5, 2))
        tk.Button(self.frame_m1, text="Tambah VIP (Head)", command=self.array_tambah_vip).pack(fill="x", pady=2)
        tk.Button(self.frame_m1, text="Hapus Pesanan (Head)", command=self.array_hapus).pack(fill="x", pady=2)
        
        tk.Label(self.frame_m1, text="--- LINKED LIST ---", bg="#2c3e50", fg="#1abc9c").pack(pady=(20, 2))
        tk.Button(self.frame_m1, text="Tambah VIP (Head)", command=self.ll_tambah_vip).pack(fill="x", pady=2)
        tk.Button(self.frame_m1, text="Hapus Pesanan (Head)", command=self.ll_hapus).pack(fill="x", pady=2)


        # ISI TAB M2: STACK DAN QUEUE
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

        # ---------------------------------------------------------
        # PANEL KANAN: Layar Output & Log Performa
        # ---------------------------------------------------------
        frame_kanan = tk.Frame(self.root, bg="#ecf0f1", padx=10, pady=10)
        frame_kanan.pack(side="right", fill="both", expand=True)

        tk.Label(frame_kanan, text="Layar Informasi", bg="#ecf0f1", font=("Arial", 10, "bold")).pack(anchor="w")
        self.layar_hasil = tk.Text(frame_kanan, height=20, font=("Consolas", 10))
        self.layar_hasil.pack(fill="both", expand=True, pady=(2, 10))

        tk.Label(frame_kanan, text="Log Eksekusi & Waktu Performa (milidetik)", bg="#ecf0f1", font=("Arial", 10, "bold")).pack(anchor="w")
        self.layar_log = tk.Text(frame_kanan, height=10, bg="#111111", fg="#00ff00", font=("Consolas", 10))
        self.layar_log.pack(fill="x", pady=(2, 0))

    # FUNGSI UTILITAS
    def muat_data_awal(self):
        self.layar_hasil.insert(tk.END, "Memuat dataset pesanan...\n")
        self.root.update()

        jalur_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'pesanan.csv'))
        mulai = time.perf_counter()
        self.array_pesanan, self.ll_pesanan = muat_pesanan_csv(jalur_csv)
        selesai = time.perf_counter()
        self.layar_hasil.insert(tk.END, f"✅ Selesai: {self.ll_pesanan.ukuran} baris terbaca.\n\n")

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
        return Pesanan(f"O-TEST", "Tamu", "Resto", "Menu", 25000, prioritas, "12:00", "", "ANTRE")

    # =========================================================
    # AKSI M1
    # =========================================================
    def array_tambah_vip(self):
        mulai = time.perf_counter(); self.array_pesanan.insert_front(self.buat_dummy(1)); self.catat_log("M1-Array", "Tambah VIP", (time.perf_counter() - mulai)*1000)
    def array_hapus(self):
        mulai = time.perf_counter(); self.array_pesanan.delete(0); self.catat_log("M1-Array", "Hapus Depan", (time.perf_counter() - mulai)*1000)
    def ll_tambah_vip(self):
        mulai = time.perf_counter(); self.ll_pesanan.insert_front(self.buat_dummy(1)); self.catat_log("M1-LL", "Tambah VIP", (time.perf_counter() - mulai)*1000)
    def ll_hapus(self):
        mulai = time.perf_counter(); self.ll_pesanan.delete(0); self.catat_log("M1-LL", "Hapus Depan", (time.perf_counter() - mulai)*1000)

    # AKSI M2 - KASIR
    def m2_hitung_kasir(self):
        ekspresi = self.entry_kasir.get()
        mulai = time.perf_counter()
        
        # 1. Konversi Infix ke Postfix
        teks_postfix = ke_postfix(ekspresi)
        
        # 2. Hitung Hasil Postfix
        hasil = hitung_postfix(teks_postfix)
        
        selesai = time.perf_counter()
        waktu = (selesai - mulai) * 1000
        
        self.layar_hasil.insert(tk.END, f"--- PERHITUNGAN KASIR (STACK) ---\n")
        self.layar_hasil.insert(tk.END, f"Struk Masuk (Infix) : {ekspresi}\n")
        self.layar_hasil.insert(tk.END, f"Dikonversi (Postfix): {teks_postfix}\n")
        self.layar_hasil.insert(tk.END, f"TOTAL BELANJA       : Rp {hasil:,}\n\n")
        self.layar_hasil.see(tk.END)
        self.catat_log("M2-Stack", "Hitung Struk Kasir", waktu)

    # AKSI M2 - ANTREAN & UNDO/REDO
    def m2_enqueue_massal(self):
        self.layar_hasil.insert(tk.END, "Memasukkan 20.000 pesanan awal ke antrean...\n")
        self.root.update()

        mulai = time.perf_counter()
        # Ambil 20.000 data dari M1 saja agar tidak terlalu memberatkan simulasi Array Naif
        batas = 20000
        for i in range(batas):
            p = self.array_pesanan.get(i)
            if p: self.manajer_q.aksi_enqueue(p)
        selesai = time.perf_counter()
        
        self.layar_hasil.insert(tk.END, f"✅ ENQUEUE Selesai!\n")
        self.cetak_status_antrean()
        self.catat_log("M2-Queue", "Enqueue Massal", (selesai - mulai) * 1000)

    def m2_dequeue_naif(self):
        # Reset pencatat geseran khusus versi Naif
        self.manajer_q.q_naif.total_geser = 0
        
        mulai = time.perf_counter()
        pesanan_keluar = self.manajer_q.q_naif.dequeue()
        selesai = time.perf_counter()
        waktu = (selesai - mulai) * 1000
        
        if pesanan_keluar:
            self.layar_hasil.insert(tk.END, f"🐢 DEQUEUE NAIF: 1 pesanan keluar.\n")
            self.layar_hasil.insert(tk.END, f"Beban Array: Menggeser {self.manajer_q.q_naif.total_geser} sisa data ke depan.\n")
            self.layar_hasil.insert(tk.END, f"Sisa Antrean Naif = {self.manajer_q.q_naif.data.ukuran}\n\n")
        self.layar_hasil.see(tk.END)
        self.catat_log("M2-Q-Naif", "Dequeue 1 Pesanan", waktu)

    def m2_dequeue_circular(self):
        mulai = time.perf_counter()
        pesanan_keluar = self.manajer_q.q_circular.dequeue()
        selesai = time.perf_counter()
        waktu = (selesai - mulai) * 1000
        
        if pesanan_keluar:
            self.layar_hasil.insert(tk.END, f"⚡ DEQUEUE CIRCULAR: 1 pesanan keluar.\n")
            self.layar_hasil.insert(tk.END, f"Beban: Menggeser 0 data. Pointer Front maju 1 langkah.\n")
            self.layar_hasil.insert(tk.END, f"Sisa Antrean Circular = {self.manajer_q.q_circular.count}\n\n")
        self.layar_hasil.see(tk.END)
        self.catat_log("M2-Q-Circ", "Dequeue 1 Pesanan", waktu)

    def m2_undo(self):
        mulai = time.perf_counter()
        berhasil = self.manajer_q.undo_last()
        waktu = (time.perf_counter() - mulai) * 1000
        
        if berhasil:
            self.layar_hasil.insert(tk.END, f"⏪ UNDO Berhasil: Aksi dikembalikan ke status sebelumnya.\n")
            self.cetak_status_antrean()
            self.catat_log("M2-Stack", "Undo Terakhir", waktu)
        else:
            self.layar_hasil.insert(tk.END, f"⚠️ Tidak ada riwayat aksi yang bisa di-Undo.\n")

    def m2_redo(self):
        mulai = time.perf_counter()
        berhasil = self.manajer_q.redo_last()
        waktu = (time.perf_counter() - mulai) * 1000
        
        if berhasil:
            self.layar_hasil.insert(tk.END, f"⏩ REDO Berhasil: Aksi yang batal diulangi kembali.\n")
            self.cetak_status_antrean()
            self.catat_log("M2-Stack", "Redo Batal", waktu)
        else:
            self.layar_hasil.insert(tk.END, f"⚠️ Tidak ada riwayat Undo yang bisa di-Redo.\n")