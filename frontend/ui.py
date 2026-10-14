import tkinter as tk
from tkinter import messagebox
import time
import sys
import os

# Menyambungkan folder frontend ke folder backend agar dapat memanggil m1_pesanan
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from m1_pesanan import muat_pesanan_csv, Pesanan

class Aplikasi2EZ4U:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Delivery - Project Struktur Data")
        self.root.geometry("1000x650")

        # Status pemuatan data
        self.array_pesanan = None
        self.ll_pesanan = None

        self.buat_antarmuka()
        self.muat_data_awal()

    def buat_antarmuka(self):
        # PANEL KIRI: Menu Tombol Operasi M1 
        frame_kiri = tk.Frame(self.root, width=280, bg="#2c3e50", padx=10, pady=10)
        frame_kiri.pack(side="left", fill="y")

        tk.Label(frame_kiri, text="PANEL OPERASI M1", bg="#2c3e50", fg="white", font=("Arial", 12, "bold")).pack(pady=(0, 15))

        # Sub-bagian Array
        tk.Label(frame_kiri, text=" ARRAY ", bg="#2c3e50", fg="#f39c12", font=("Arial", 9, "bold")).pack(anchor="w", pady=(5, 2))
        tk.Button(frame_kiri, text="1. Tambah Reguler (Belakang)", bg="#ecf0f1", command=self.array_tambah_reguler).pack(fill="x", pady=2)
        tk.Button(frame_kiri, text="2. Tambah VIP (Depan)", bg="#ecf0f1", command=self.array_tambah_vip).pack(fill="x", pady=2)
        tk.Button(frame_kiri, text="3. Tambah Prioritas (Tengah)", bg="#ecf0f1", command=self.array_tambah_prioritas).pack(fill="x", pady=2)
        tk.Button(frame_kiri, text="4. Hapus Pesanan (Indeks 0)", bg="#e74c3c", fg="white", command=self.array_hapus).pack(fill="x", pady=2)

        tk.Frame(frame_kiri, height=2, bg="#7f8c8d").pack(fill="x", pady=10)

        # Sub-bagian Linked List
        tk.Label(frame_kiri, text=" LINKED LIST ", bg="#2c3e50", fg="#1abc9c", font=("Arial", 9, "bold")).pack(anchor="w", pady=(5, 2))
        tk.Button(frame_kiri, text="1. Tambah Reguler (Tail)", bg="#ecf0f1", command=self.ll_tambah_reguler).pack(fill="x", pady=2)
        tk.Button(frame_kiri, text="2. Tambah VIP (Head)", bg="#ecf0f1", command=self.ll_tambah_vip).pack(fill="x", pady=2)
        tk.Button(frame_kiri, text="3. Tambah Prioritas (Tengah)", bg="#ecf0f1", command=self.ll_tambah_prioritas).pack(fill="x", pady=2)
        tk.Button(frame_kiri, text="4. Hapus Pesanan (Head)", bg="#e74c3c", fg="white", command=self.ll_hapus).pack(fill="x", pady=2)

        tk.Frame(frame_kiri, height=2, bg="#7f8c8d").pack(fill="x", pady=10)

        # Tombol Tampilkan Data Teratas
        tk.Button(frame_kiri, text="🔍 Lihat 5 Pesanan Teratas", bg="#3498db", fg="white", font=("Arial", 9, "bold"), command=self.tampilkan_data_teratas).pack(fill="x", pady=5)

        # PANEL KANAN: Layar Output & Log Performa
        frame_kanan = tk.Frame(self.root, bg="#ecf0f1", padx=10, pady=10)
        frame_kanan.pack(side="right", fill="both", expand=True)

        tk.Label(frame_kanan, text="Layar Informasi / Data", bg="#ecf0f1", font=("Arial", 10, "bold")).pack(anchor="w")
        self.layar_hasil = tk.Text(frame_kanan, height=16, font=("Consolas", 10))
        self.layar_hasil.pack(fill="both", expand=True, pady=(2, 10))

        tk.Label(frame_kanan, text="Command Log & Catatan Performa (Waktu Eksekusi)", bg="#ecf0f1", font=("Arial", 10, "bold")).pack(anchor="w")
        self.layar_log = tk.Text(frame_kanan, height=10, bg="#111111", fg="#00ff00", font=("Consolas", 10))
        self.layar_log.pack(fill="x", pady=(2, 0))

    def muat_data_awal(self):
        self.layar_hasil.insert(tk.END, "Memuat dataset 200.000 baris dari data/pesanan.csv, mohon tunggu sebentar...\n")
        self.root.update()

        jalur_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'pesanan.csv'))
        
        mulai = time.perf_counter()
        self.array_pesanan, self.ll_pesanan = muat_pesanan_csv(jalur_csv)
        selesai = time.perf_counter()

        waktu_ms = (selesai - mulai) * 1000
        self.layar_hasil.insert(tk.END, f"✅ Data berhasil dimuat!\n")
        self.layar_hasil.insert(tk.END, f"• Total Array      : {self.array_pesanan.ukuran} data\n")
        self.layar_hasil.insert(tk.END, f"• Total Linked List : {self.ll_pesanan.ukuran} data\n\n")
        
        self.catat_log("MUAT_DATASET_200K", "m1 - csv_loader", waktu_ms)

    def catat_log(self, perintah, modul, waktu_ms):
        teks = f"[{time.strftime('%H:%M:%S')}] {perintah:<30} -> {modul:<15} | Waktu: {waktu_ms:.4f} ms\n"
        self.layar_log.insert(tk.END, teks)
        self.layar_log.see(tk.END)

    def buat_pesanan_dummy(self, tipe):
        oid = f"O-TEST-{int(time.time())}"
        return Pesanan(oid, "Pelanggan Test", "Resto Test", "Menu Test", 25000, tipe, "12:00", "", "ANTRE")

    # OPERASI ARRAY
    def array_tambah_reguler(self):
        p = self.buat_pesanan_dummy(3)
        mulai = time.perf_counter()
        self.array_pesanan.append(p)
        selesai = time.perf_counter()
        self.catat_log("ARRAY_TAMBAH_REGULER", "m1 - array", (selesai - mulai) * 1000)
        self.layar_hasil.insert(tk.END, f"[Array] Added Reguler -> Total Data: {self.array_pesanan.ukuran}\n")

    def array_tambah_vip(self):
        p = self.buat_pesanan_dummy(1)
        mulai = time.perf_counter()
        self.array_pesanan.insert_front(p)
        selesai = time.perf_counter()
        self.catat_log("ARRAY_TAMBAH_VIP (FRONT)", "m1 - array", (selesai - mulai) * 1000)
        self.layar_hasil.insert(tk.END, f"[Array] Added VIP (Depan) -> Total Data: {self.array_pesanan.ukuran}\n")

    def array_tambah_prioritas(self):
        p = self.buat_pesanan_dummy(2)
        posisi = self.array_pesanan.ukuran // 2
        mulai = time.perf_counter()
        self.array_pesanan.insert_middle(posisi, p)
        selesai = time.perf_counter()
        self.catat_log("ARRAY_TAMBAH_PRIORITAS (MID)", "m1 - array", (selesai - mulai) * 1000)
        self.layar_hasil.insert(tk.END, f"[Array] Added Prioritas (Tengah) -> Total Data: {self.array_pesanan.ukuran}\n")

    def array_hapus(self):
        if self.array_pesanan.ukuran == 0:
            return
        mulai = time.perf_counter()
        self.array_pesanan.delete(0)
        selesai = time.perf_counter()
        self.catat_log("ARRAY_HAPUS_INDEX_0", "m1 - array", (selesai - mulai) * 1000)
        self.layar_hasil.insert(tk.END, f"[Array] Deleted Index 0 -> Total Data: {self.array_pesanan.ukuran}\n")

    # OPERASI LINKED LIST
    def ll_tambah_reguler(self):
        p = self.buat_pesanan_dummy(3)
        mulai = time.perf_counter()
        self.ll_pesanan.append(p)
        selesai = time.perf_counter()
        self.catat_log("LL_TAMBAH_REGULER", "m1 - linkedlist", (selesai - mulai) * 1000)
        self.layar_hasil.insert(tk.END, f"[LinkList] Added Reguler -> Total Data: {self.ll_pesanan.ukuran}\n")

    def ll_tambah_vip(self):
        p = self.buat_pesanan_dummy(1)
        mulai = time.perf_counter()
        self.ll_pesanan.insert_front(p)
        selesai = time.perf_counter()
        self.catat_log("LL_TAMBAH_VIP (FRONT)", "m1 - linkedlist", (selesai - mulai) * 1000)
        self.layar_hasil.insert(tk.END, f"[LinkList] Added VIP (Depan) -> Total Data: {self.ll_pesanan.ukuran}\n")

    def ll_tambah_prioritas(self):
        p = self.buat_pesanan_dummy(2)
        posisi = self.ll_pesanan.ukuran // 2
        mulai = time.perf_counter()
        self.ll_pesanan.insert_middle(posisi, p)
        selesai = time.perf_counter()
        self.catat_log("LL_TAMBAH_PRIORITAS (MID)", "m1 - linkedlist", (selesai - mulai) * 1000)
        self.layar_hasil.insert(tk.END, f"[LinkList] Added Prioritas (Tengah) -> Total Data: {self.ll_pesanan.ukuran}\n")

    def ll_hapus(self):
        if self.ll_pesanan.ukuran == 0:
            return
        mulai = time.perf_counter()
        self.ll_pesanan.delete(0)
        selesai = time.perf_counter()
        self.catat_log("LL_HAPUS_HEAD", "m1 - linkedlist", (selesai - mulai) * 1000)
        self.layar_hasil.insert(tk.END, f"[LinkList] Deleted Head -> Total Data: {self.ll_pesanan.ukuran}\n")
    # VIEW DATA
    def tampilkan_data_teratas(self):
        self.layar_hasil.insert(tk.END, "\n=== 5 DATA TERATAS (ARRAY) ===\n")
        for i in range(min(5, self.array_pesanan.ukuran)):
            p = self.array_pesanan.get(i)
            if p:
                self.layar_hasil.insert(tk.END, f"[{i+1}] ID: {p.oid} | Nama: {p.pelanggan} | Resto: {p.resto} | Menu: {p.menu}\n")
        self.layar_hasil.insert(tk.END, "\n")