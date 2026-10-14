import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from m1_pesanan import Array, LinkList, Pesanan

# ==========================================
# BAGIAN A: STACK UNTUK KASIR (INFIX -> POSTFIX & UNDO/REDO)
# ==========================================
class Stack:
    """Implementasi Stack sederhana di atas Array murni"""
    def __init__(self):
        self.data = Array()
        
    def push(self, x):
        self.data.append(x)
        
    def pop(self):
        if self.data.ukuran == 0:
            return None
        teratas = self.data.get(self.data.ukuran - 1)
        self.data.delete(self.data.ukuran - 1)
        return teratas
        
    def peek(self):
        if self.data.ukuran == 0:
            return None
        return self.data.get(self.data.ukuran - 1)
        
    def is_empty(self):
        return self.data.ukuran == 0

def tingkat_operator(op):
    if op in ('*', '/'): return 2
    if op in ('+', '-'): return 1
    return 0

def tokenisasi(ekspresi):
    """Memecah teks "(3*12000)+(2*8500)-5000" menjadi daftar token yang benar"""
    token = []
    angka_sementara = ""
    for char in ekspresi:
        if char.isdigit():
            angka_sementara += char
        else:
            if angka_sementara:
                token.append(angka_sementara)
                angka_sementara = ""
            if char in "()+-*/":
                token.append(char)
    if angka_sementara:
        token.append(angka_sementara)
    return token

def ke_postfix(ekspresi):
    """Mengubah notasi Infix menjadi Postfix"""
    stack_op = Stack()
    postfix = []
    tokens = tokenisasi(ekspresi)
    
    for t in tokens:
        if t.isdigit():
            postfix.append(t)
        elif t == '(':
            stack_op.push(t)
        elif t == ')':
            while not stack_op.is_empty() and stack_op.peek() != '(':
                postfix.append(stack_op.pop())
            stack_op.pop() # Buang '('
        else:
            while (not stack_op.is_empty() and stack_op.peek() != '(' and 
                   tingkat_operator(stack_op.peek()) >= tingkat_operator(t)):
                postfix.append(stack_op.pop())
            stack_op.push(t)
            
    while not stack_op.is_empty():
        postfix.append(stack_op.pop())
        
    return " ".join(postfix)

def hitung_postfix(postfix_str):
    """Mengevaluasi hasil Postfix menjadi total angka"""
    stack_angka = Stack()
    tokens = postfix_str.split()
    
    for t in tokens:
        if t.isdigit():
            stack_angka.push(int(t))
        else:
            b = stack_angka.pop() # Keluaran pertama adalah operand kanan
            a = stack_angka.pop()
            if t == '+': stack_angka.push(a + b)
            elif t == '-': stack_angka.push(a - b)
            elif t == '*': stack_angka.push(a * b)
            elif t == '/': stack_angka.push(a // b)
            
    return stack_angka.pop()

# ==========================================
# BAGIAN B: QUEUE (NAIF VS CIRCULAR)
# ==========================================
class AntreanNaif:
    """O(n) per dequeue karena menggeser sisa array"""
    def __init__(self):
        self.data = Array()
        self.total_geser = 0
        
    def enqueue(self, x):
        self.data.append(x)
        
    def dequeue(self):
        if self.data.ukuran == 0:
            return None
        keluar = self.data.get(0)
        
        # Simulasi pop(0) yang lambat
        self.data.delete(0)
        self.total_geser += self.data.ukuran # Mencatat beban kerja
        return keluar

class AntreanMelingkar:
    """O(1) per dequeue karena hanya memutar pointer"""
    def __init__(self, kapasitas=350000):
        # Kapasitas dibuat statis besar agar cukup untuk 200rb data
        self.kapasitas = kapasitas
        self.data = [None] * self.kapasitas
        self.front = 0
        self.rear = 0
        self.count = 0 # Pencacah untuk mencegah kebingungan penuh/kosong
        
    def enqueue(self, x):
        if self.count == self.kapasitas:
            return False # Tolak jika penuh
        self.data[self.rear] = x
        self.rear = (self.rear + 1) % self.kapasitas
        self.count += 1
        return True
        
    def dequeue(self):
        if self.count == 0:
            return None
        keluar = self.data[self.front]
        self.data[self.front] = None # Bersihkan memori (opsional)
        self.front = (self.front + 1) % self.kapasitas
        self.count -= 1
        return keluar

# ==========================================
# MANAJER ANTREAN (MENGHUBUNGKAN QUEUE DENGAN UNDO/REDO)
# ==========================================
class ManajerAntrean:
    def __init__(self):
        self.q_naif = AntreanNaif()
        self.q_circular = AntreanMelingkar()
        
        # Stack untuk riwayat
        self.stack_undo = Stack()
        self.stack_redo = Stack()
        
    def aksi_enqueue(self, pesanan):
        self.q_naif.enqueue(pesanan)
        self.q_circular.enqueue(pesanan)
        
        # Catat untuk undo
        self.stack_undo.push({"aksi": "ENQUEUE", "data": pesanan})
        # Kosongkan redo setiap ada aksi baru
        while not self.stack_redo.is_empty():
            self.stack_redo.pop()
            
    def aksi_dequeue(self, jumlah=1):
        keluaran_naif = []
        keluaran_circular = []
        
        for _ in range(jumlah):
            if self.q_naif.data.ukuran > 0:
                keluaran_naif.append(self.q_naif.dequeue())
                keluaran_circular.append(self.q_circular.dequeue())
                
        if keluaran_circular:
            # Catat keseluruhan daftar yang dihapus ke dalam stack
            self.stack_undo.push({"aksi": "DEQUEUE", "data": keluaran_circular})
            while not self.stack_redo.is_empty():
                self.stack_redo.pop()
                
        return keluaran_circular
        
    def undo_last(self):
        aksi_terakhir = self.stack_undo.pop()
        if not aksi_terakhir: return False
        
        # Jika sebelumnya enqueue, batalkan dengan mengeluarkannya dari antrean
        if aksi_terakhir["aksi"] == "ENQUEUE":
            # (Untuk simulasi naif, menghapus elemen paling belakang)
            self.q_naif.data.ukuran -= 1 
            self.q_circular.count -= 1
            self.q_circular.rear = (self.q_circular.rear - 1) % self.q_circular.kapasitas
            
        # Jika sebelumnya dequeue, kembalikan data ke DEPAN antrean circular
        elif aksi_terakhir["aksi"] == "DEQUEUE":
            daftar_pesanan = aksi_terakhir["data"]
            # Kembalikan dengan arah terbalik agar urutannya tetap benar di depan
            for p in reversed(daftar_pesanan):
                self.q_circular.front = (self.q_circular.front - 1) % self.q_circular.kapasitas
                self.q_circular.data[self.q_circular.front] = p
                self.q_circular.count += 1
                
                # Kembalikan juga ke Antrean Naif (di indeks 0)
                self.q_naif.data.insert_front(p)
                
        self.stack_redo.push(aksi_terakhir)
        return True
        
    def redo_last(self):
        aksi_batal = self.stack_redo.pop()
        if not aksi_batal: return False
        
        # Kerjakan ulang aksi aslinya
        if aksi_batal["aksi"] == "ENQUEUE":
            self.q_naif.enqueue(aksi_batal["data"])
            self.q_circular.enqueue(aksi_batal["data"])
        elif aksi_batal["aksi"] == "DEQUEUE":
            jumlah = len(aksi_batal["data"])
            for _ in range(jumlah):
                self.q_naif.dequeue()
                self.q_circular.dequeue()
                
        self.stack_undo.push(aksi_batal)
        return True