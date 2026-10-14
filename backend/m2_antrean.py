import sys
import os

# Menyambungkan akses ke struktur data di m1_pesanan.py
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from m1_pesanan import LinkList, Pesanan

class AntreanDapur:
    def __init__(self):
        # Menggunakan 3 Linked List terpisah sebagai wadah antrean (Queue)
        self.q_vip = LinkList()       # Prioritas 1
        self.q_prioritas = LinkList() # Prioritas 2
        self.q_reguler = LinkList()   # Prioritas 3
        
        # Wadah untuk menyimpan pesanan yang sudah selesai dimasak
        self.riwayat_selesai = LinkList()

    def tambah_pesanan(self, pesanan):
        """ENQUEUE: Memasukkan pesanan ke antrean berdasarkan prioritasnya"""
        # Penambahan di akhir (tail) senarai, performa O(1) berkat Linked List
        if pesanan.prioritas == 1:
            self.q_vip.append(pesanan)
        elif pesanan.prioritas == 2:
            self.q_prioritas.append(pesanan)
        else:
            self.q_reguler.append(pesanan)

    def proses_pesanan(self):
        """DEQUEUE: Mengeluarkan pesanan dari depan antrean tertinggi untuk dimasak"""
        pesanan_diproses = None

        # Koki selalu melihat antrean dari prioritas paling tinggi
        if self.q_vip.ukuran > 0:
            pesanan_diproses = self.q_vip.get(0)
            self.q_vip.delete(0)
        elif self.q_prioritas.ukuran > 0:
            pesanan_diproses = self.q_prioritas.get(0)
            self.q_prioritas.delete(0)
        elif self.q_reguler.ukuran > 0:
            pesanan_diproses = self.q_reguler.get(0)
            self.q_reguler.delete(0)
        
        if pesanan_diproses:
            pesanan_diproses.status = "SELESAI"
            self.riwayat_selesai.append(pesanan_diproses)
            return pesanan_diproses
        
        return None # Mengembalikan None jika semua antrean kosong

    def intip_antrean_terdepan(self):
        """PEEK: Melihat siapa yang akan dimasak selanjutnya tanpa mengeluarkannya"""
        if self.q_vip.ukuran > 0:
            return self.q_vip.get(0)
        elif self.q_prioritas.ukuran > 0:
            return self.q_prioritas.get(0)
        elif self.q_reguler.ukuran > 0:
            return self.q_reguler.get(0)
        return None

    def total_antrean(self):
        """Menghitung total keseluruhan pesanan yang belum dimasak"""
        return self.q_vip.ukuran + self.q_prioritas.ukuran + self.q_reguler.ukuran

# ==========================================
# BLOK PENGUJIAN LOKAL
# ==========================================
if __name__ == "__main__":
    dapur = AntreanDapur()
    
    print("--- SIMULASI PESANAN MASUK ---")
    dapur.tambah_pesanan(Pesanan("O-01", "Budi (Reguler)", "Resto A", "Ayam", 15000, 3, "10:00", "", "ANTRE"))
    dapur.tambah_pesanan(Pesanan("O-02", "Andi (Reguler)", "Resto B", "Soto", 12000, 3, "10:05", "", "ANTRE"))
    dapur.tambah_pesanan(Pesanan("O-03", "Siska (VIP)", "Resto C", "Steak", 50000, 1, "10:10", "", "ANTRE"))
    dapur.tambah_pesanan(Pesanan("O-04", "Rina (Prioritas)", "Resto A", "Ayam", 15000, 2, "10:15", "", "ANTRE"))
    
    print(f"Total antrean saat ini: {dapur.total_antrean()} pesanan")
    print(f"Pesanan terdepan: {dapur.intip_antrean_terdepan().pelanggan}")
    
    print("\n--- SIMULASI KOKI MEMASAK ---")
    for _ in range(4):
        p = dapur.proses_pesanan()
        if p:
            print(f"Memasak: {p.pelanggan} - Status: {p.status}")