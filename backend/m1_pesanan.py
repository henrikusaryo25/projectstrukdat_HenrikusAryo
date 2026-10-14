import csv

# 1. CLASS PESANAN 
class Pesanan:
    def __init__(self, oid, pelanggan, resto, menu, harga, prioritas, t_masuk, t_selesai, status):
        self.oid = oid
        self.pelanggan = pelanggan
        self.resto = resto
        self.menu = menu
        self.harga = harga
        self.prioritas = prioritas
        self.t_masuk = t_masuk
        self.t_selesai = t_selesai
        self.status = status


# 2. CLASS ARRAY 
class Array:
    def __init__(self, kapasitas_awal=4):
        self.kapasitas = kapasitas_awal
        self.ukuran = 0
        self.data = [None] * self.kapasitas 

    def _resize(self):
        kapasitas_baru = self.kapasitas * 2
        data_baru = [None] * kapasitas_baru
        for i in range(self.ukuran):
            data_baru[i] = self.data[i]
        self.data = data_baru
        self.kapasitas = kapasitas_baru

    def get(self, i):
        if 0 <= i < self.ukuran:
            return self.data[i]
        return None

    def append(self, v):
        if self.ukuran == self.kapasitas:
            self._resize()
        self.data[self.ukuran] = v
        self.ukuran += 1

    def insert_front(self, v):
        if self.ukuran == self.kapasitas:
            self._resize()
        for i in range(self.ukuran, 0, -1):
            self.data[i] = self.data[i-1]
        self.data[0] = v
        self.ukuran += 1

    def insert_middle(self, i, v):
        if self.ukuran == self.kapasitas:
            self._resize()
        for j in range(self.ukuran, i, -1):
            self.data[j] = self.data[j-1]
        self.data[i] = v
        self.ukuran += 1
        
    def delete(self, i):
        if i < 0 or i >= self.ukuran:
            return
        for j in range(i, self.ukuran - 1):
            self.data[j] = self.data[j+1]
        self.data[self.ukuran - 1] = None
        self.ukuran -= 1


# 3. CLASS SIMPUL 
class Simpul:
    def __init__(self, data):
        self.data = data
        self.next = None


# 4. CLASS LINKLIST 
class LinkList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.ukuran = 0

    def get(self, i):
        if i < 0 or i >= self.ukuran:
            return None
        sekarang = self.head
        for _ in range(i):
            sekarang = sekarang.next
        return sekarang.data

    def append(self, v):
        baru = Simpul(v)
        if not self.head:
            self.head = baru
            self.tail = baru
        else:
            self.tail.next = baru
            self.tail = baru
        self.ukuran += 1

    def insert_front(self, v):
        baru = Simpul(v)
        baru.next = self.head
        self.head = baru
        if self.tail is None:
            self.tail = baru
        self.ukuran += 1

    def insert_middle(self, i, v):
        if i == 0:
            self.insert_front(v)
            return
        if i >= self.ukuran:
            self.append(v)
            return
        
        baru = Simpul(v)
        sekarang = self.head
        for _ in range(i - 1):
            sekarang = sekarang.next
        baru.next = sekarang.next
        sekarang.next = baru
        self.ukuran += 1

    def delete(self, i):
        if i < 0 or i >= self.ukuran or self.head is None:
            return
        if i == 0:
            self.head = self.head.next
            if self.ukuran == 1:
                self.tail = None
        else:
            sekarang = self.head
            for _ in range(i - 1):
                sekarang = sekarang.next
            sekarang.next = sekarang.next.next
            if sekarang.next is None:
                self.tail = sekarang
        self.ukuran -= 1


# 5. FUNGSI MUAT CSV 
def muat_pesanan_csv(filepath):
    array_pesanan = Array()
    ll_pesanan = LinkList()
    
    with open(filepath, 'r', encoding='utf-8') as f:
        # Gunakan pembaca CSV bawaan Python
        pembaca = csv.reader(f)
        header = next(pembaca) # Lewati baris pertama (judul kolom)
        
        for kolom in pembaca:
            # Pengecekan aman, data kosong di ujung (seperti t_selesai) tetap terbaca
            if len(kolom) >= 9: 
                pesanan_baru = Pesanan(
                    kolom[0], kolom[1], kolom[2], kolom[3], 
                    kolom[4], kolom[5], kolom[6], kolom[7], kolom[8]
                )
                array_pesanan.append(pesanan_baru)
                ll_pesanan.append(pesanan_baru)
                
    return array_pesanan, ll_pesanan


# BLOK PENGUJIAN LOKAL 
if __name__ == "__main__":
    print("Memuat data...")
    # Menyesuaikan path karena m1_pesanan.py ada di dalam folder backend/
    array_ku, ll_ku = muat_pesanan_csv("../data/pesanan.csv")
    print(f"Berhasil memuat {array_ku.ukuran} data ke Array!")
    print(f"Berhasil memuat {ll_ku.ukuran} data ke Linked List!")