import tkinter as tk
from tkinter import ttk, messagebox
import time
import sys
import os

# Menyambungkan folder frontend ke folder backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from m1_pesanan import muat_pesanan_csv, Pesanan
from m2_antrean import AntreanDapur

class Aplikasi2EZ4U:
    def __init__(self, root):
        self.root = root
        self.root.title("2EZ4U Food Delivery - M1 & M2")
        self.root.geometry("1100x650")

        # Variabel Status
        self.array_pesanan = None
        self.ll_pesanan = None
        self.dapur = AntreanDapur() # Objek M2

        self.buat_antarmuka()
        self.muat_data_awal()

    def buat_antarmuka(self):
        # ---------------------------------------------------------
        # BUKU TAB (Notebook) untuk memisah UI M1 dan M2
        # ---------------------------------------------------------
        self.tab_kontrol = ttk.Notebook(self.root)
        self.tab_kontrol.pack(side="left", fill="y", padx=5, pady=5)

        # Tab M1 (Kiri)
        self.frame_m1 = tk.Frame(self.tab_kontrol, width=300, bg="#2c3e50", padx=10, pady=10)
        self.tab_kontrol.add(self.frame_m1, text="M1: Performa Data")

        # Tab M2 (Kiri)
        self.frame_m2 = tk.Frame(self.tab_kontrol, width=300, bg="#27ae60", padx=10, pady=10)
        self.tab_kontrol.add(self.frame_m2, text="M2: Antrean Dapur")

        # ---------------------------------------------------------
        # ISI TAB M1: ARRAY VS LINKED LIST
        # ---------------------------------------------------------
        tk.Label(self.frame_m1, text="--- ARRAY ---", bg="#2c3e50", fg="#f39c12", font=("Arial", 9, "bold")).pack(pady=(5, 2))
        tk.Button(self.frame_m1, text="1. Tambah Reguler (Tail)", command=self.array_tambah_reguler).pack(fill="x", pady=2)
        tk.Button(self.frame_m1, text="2. Tambah VIP (Head)", command=self.array_tambah_vip).pack(fill="x", pady=2)
        tk.Button(self.frame_m1, text="3. Hapus Pesanan (Head)", command=self.array_hapus).pack(fill="x", pady=2)

        tk.Frame(self.frame_m1, height=2, bg="#7f8c8d").pack(fill="x", pady=10)

        tk.Label(self.frame_m1, text="--- LINKED LIST ---", bg="#2c3e50", fg="#1abc9c", font=("Arial", 9, "bold")).pack(pady=(5, 2))
        tk.Button(self.frame_m1, text="1. Tambah Reguler (Tail)", command=self.ll_tambah_reguler).pack(fill="x", pady=2)
        tk.Button(self.frame_m1, text="2. Tambah VIP (Head)", command=self.ll_tambah_vip).pack(fill="x", pady=2)
        tk.Button(self.frame_m1, text="3. Hapus Pesanan (Head)", command=self.ll_hapus).pack(fill="x", pady=2)

        # ---------------------------------------------------------
        # ISI TAB M2: ANTREAN KOKI
        # ---------------------------------------------------------
        tk.Label(self.frame_m2, text="SISTEM ANTREAN KOKI", bg="#27ae60", fg="white", font=("Arial", 12, "bold")).pack(pady=(0, 15))
        
        tk.Button(self.frame_m2, text="📥 1. Impor Semua CSV ke Dapur", bg="#f1c40f", font=("Arial", 10, "bold"), command=self.impor_ke_dapur).pack(fill="x", pady=10)
        
        tk.Button(self.frame_m2, text="👨‍🍳 2. Masak 1 Pesanan (Dequeue)", bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), command=self.masak_pesanan).pack(fill="x", pady=10)
        
        tk.Button(self.frame_m2, text="👀 3. Intip Antrean Terdepan", bg="#3498db", fg="white", command=self.intip_dapur).pack(fill="x", pady=2)
        tk.Button(self.frame_m2, text="📊 4. Lihat Status Dapur", bg="#9b59b6", fg="white", command=self.status_dapur).pack(fill="x", pady=2)


        # ---------------------------------------------------------
        # PANEL KANAN: Layar Output & Log Performa
        # ---------------------------------------------------------
        frame_kanan = tk.Frame(self.root, bg="#ecf0f1", padx=10, pady=10)
        frame_kanan.pack(side="right", fill="both", expand=True)

        tk.Label(frame_kanan, text="Layar Informasi / Data", bg="#ecf0f1", font=("Arial", 10, "bold")).pack(anchor="w")
        self.layar_hasil = tk.Text(frame_kanan, height=20, font=("Consolas", 10))
        self.layar_hasil.pack(fill="both", expand=True, pady=(2, 10))

        tk.Label(frame_kanan, text="Command Log & Catatan Performa (Waktu Eksekusi)", bg="#ecf0f1", font=("Arial", 10, "bold")).pack(anchor="w")
        self.layar_log = tk.Text(frame_kanan, height=8, bg="#111111", fg="#00ff00", font=("Consolas", 10))
        self.layar_log.pack(fill="x", pady=(2, 0))

    # =========================================================
    # FUNGSI UTILITAS
    # =========================================================
    def muat_data_awal(self):
        self.layar_hasil.insert(tk.END, "Memuat dataset 200.000 baris...\n")
        self.root.update()

        jalur_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'pesanan.csv'))
        mulai = time.perf_counter()
        self.array_pesanan, self.ll_pesanan = muat_pesanan_csv(jalur_csv)
        selesai = time.perf_counter()

        self.layar_hasil.insert(tk.END, f"✅ CSV Termuat: {self.ll_pesanan.ukuran} baris siap!\n\n")
        self.catat_log("MUAT_DATA_AWAL", "m1", (selesai - mulai) * 1000)

    def catat_log(self, perintah, modul, waktu_ms):
        teks = f"[{time.strftime('%H:%M:%S')}] {perintah:<25} -> {modul:<10} | Waktu: {waktu_ms:.4f} ms\n"
        self.layar_log.insert(tk.END, teks)
        self.layar_log.see(tk.END)

    def buat_dummy(self, prioritas):
        return Pesanan(f"O-TEST", "Tamu", "Resto", "Menu", 25000, prioritas, "12:00", "", "ANTRE")

    # =========================================================
    # FUNGSI M1 (Tetap Dipertahankan)
    # =========================================================
    def array_tambah_reguler(self):
        mulai = time.perf_counter()
        self.array_pesanan.append(self.buat_dummy(3))
        self.catat_log("ARR_ADD_REGULER", "m1-array", (time.perf_counter() - mulai)*1000)

    def array_tambah_vip(self):
        mulai = time.perf_counter()
        self.array_pesanan.insert_front(self.buat_dummy(1))
        self.catat_log("ARR_ADD_VIP", "m1-array", (time.perf_counter() - mulai)*1000)

    def array_hapus(self):
        mulai = time.perf_counter()
        self.array_pesanan.delete(0)
        self.catat_log("ARR_HAPUS_DEPAN", "m1-array", (time.perf_counter() - mulai)*1000)

    def ll_tambah_reguler(self):
        mulai = time.perf_counter()
        self.ll_pesanan.append(self.buat_dummy(3))
        self.catat_log("LL_ADD_REGULER", "m1-ll", (time.perf_counter() - mulai)*1000)

    def ll_tambah_vip(self):
        mulai = time.perf_counter()
        self.ll_pesanan.insert_front(self.buat_dummy(1))
        self.catat_log("LL_ADD_VIP", "m1-ll", (time.perf_counter() - mulai)*1000)

    def ll_hapus(self):
        mulai = time.perf_counter()
        self.ll_pesanan.delete(0)
        self.catat_log("LL_HAPUS_DEPAN", "m1-ll", (time.perf_counter() - mulai)*1000)


    # =========================================================
    # FUNGSI M2: ANTREAN DAPUR
    # =========================================================
    def impor_ke_dapur(self):
        self.layar_hasil.insert(tk.END, "Mentransfer 200.000 data ke Antrean Dapur...\n")
        self.root.update()

        mulai = time.perf_counter()
        # Transfer dari Linked List M1 ke Antrean Dapur M2
        sekarang = self.ll_pesanan.head
        while sekarang:
            self.dapur.tambah_pesanan(sekarang.data)
            sekarang = sekarang.next
        selesai = time.perf_counter()

        self.layar_hasil.insert(tk.END, "✅ Berhasil! Semua pesanan masuk dapur.\n")
        self.status_dapur()
        self.catat_log("IMPOR_MASAL_DAPUR", "m2-queue", (selesai - mulai) * 1000)

    def masak_pesanan(self):
        mulai = time.perf_counter()
        p = self.dapur.proses_pesanan()
        selesai = time.perf_counter()

        if p:
            self.layar_hasil.insert(tk.END, f"🍳 Koki Memasak: {p.pelanggan} (Prioritas {p.prioritas}) | Status: {p.status}\n")
        else:
            self.layar_hasil.insert(tk.END, "⚠️ Dapur kosong! Tidak ada pesanan untuk dimasak.\n")
        
        self.layar_hasil.see(tk.END)
        self.catat_log("DEQUEUE_MASAK", "m2-queue", (selesai - mulai) * 1000)

    def intip_dapur(self):
        p = self.dapur.intip_antrean_terdepan()
        if p:
            self.layar_hasil.insert(tk.END, f"👀 Selanjutnya dimasak: {p.pelanggan} (Prioritas {p.prioritas})\n")
        else:
            self.layar_hasil.insert(tk.END, "👀 Antrean kosong.\n")
        self.layar_hasil.see(tk.END)

    def status_dapur(self):
        teks = f"\n=== STATUS DAPUR ===\n"
        teks += f"Antrean VIP (1) : {self.dapur.q_vip.ukuran}\n"
        teks += f"Antrean Prioritas (2): {self.dapur.q_prioritas.ukuran}\n"
        teks += f"Antrean Reguler (3)  : {self.dapur.q_reguler.ukuran}\n"
        teks += f"Total Belum Dimasak  : {self.dapur.total_antrean()}\n"
        teks += f"Total Selesai Dimasak: {self.dapur.riwayat_selesai.ukuran}\n====================\n\n"
        self.layar_hasil.insert(tk.END, teks)
        self.layar_hasil.see(tk.END)