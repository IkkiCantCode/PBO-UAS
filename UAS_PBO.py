# Tema : Non-profit

import os
class User:
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password
        self.donasi = []

    def menyumbang(self, donasi):
        self.donasi.append(donasi)

    def riwayat_donasi(self):
        return self.donasi

class Pendonor(User):
    pass

class Admin(User):
    def __init__(self, email, username, password):
        super().__init__(email, username, password)
        self.pendonor = []
        self.laporan = []

    def kelola_jenis_donasi(self, jenis_donasi):
        Jenis_Donasi.add_jenis_donasi(jenis_donasi)

    def lihat_jenis_donasi(self):
        return Jenis_Donasi.get_jenis_donasi_list()

    def lihat_pendonor(self):
        return self.pendonor

    def buat_laporan(self):
        total_pendonor = len(self.pendonor)
        total_nominal = sum(donasi.nominal for pendonor in self.pendonor for donasi in pendonor.donasi)
        return {
            "total_pendonor": total_pendonor,
            "total_nominal": total_nominal
        }

    def tambah_pendonor(self, pendonor):
        self.pendonor.append(pendonor)

class Jenis_Donasi:
    jenis_donasi_list = []
    def __init__(self, nama, deskripsi):
        self.nama = nama
        self.deskripsi = deskripsi
        
    @classmethod
    def add_jenis_donasi(self, jenis_donasi):
        self.jenis_donasi_list.append(jenis_donasi)

    @classmethod
    def get_jenis_donasi_list(self):
        return self.jenis_donasi_list

class Donasi:
    def __init__(self, nominal, jenis_donasi, metode_pembayaran):
        self.nominal = nominal
        self.jenis_donasi = jenis_donasi
        self.metode_pembayaran = metode_pembayaran

class Metode_Pembayaran:
    metode_list = ["Bank", "E-Wallet"]
    def __init__(self, metode):
        self.metode = metode

    @classmethod
    def get_metode(self):
        return self.metode_list
    
class Sistem:
    def __init__(self):
        self.admins = []
        self.pendonor = []

    def registrasi_user(self, email, username, password, is_admin=False):
        if is_admin:
            user = Admin(email, username, password)
            self.admins.append(user)
        else:
            user = Pendonor(email, username, password)
            self.pendonor.append(user)
        return user

    def login(self, username, password):
        for admin in self.admins:
            if admin.username == username and admin.password == password:
                return admin
        for pendonor in self.pendonor:
            if pendonor.username == username and pendonor.password == password:
                return pendonor
        return None

def menu_utama():
    os.system("Color B")
    print("===========================================")
    print(">>>>  SELAMAT DATANG DI DONASI CENTER  <<<<")
    print("===========================================")
    print("      .        1. Login              .     ")
    print("         .     2. Registrasi      .        ")
    print("            .  3. Keluar       .           ")
    print("===========================================")
    pilihan = input("Pilih Menu Yang Anda Inginkan: ")
    return pilihan

def menu_admin(admin):
    while True:
        os.system("Color B")
        print("======================================")
        print("       >> SELAMAT DATANG ADMIN!       ")
        print("======================================")
        print("        1.| Tambah Jenis Donasi       ")
        print("        2.| Lihat Pendonor            ")
        print("        3.| Buat Laporan              ")
        print("        4.| Keluar                    ")
        print("======================================")
        pilihan = input("Pilih Menu Yang Admin Inginkan: ")

        if pilihan == "1":
            os.system("cls")
            nama = input("Masukkan Jenis Donasi: ")
            deskripsi = input("Masukkan Deskripsi: ")
            jenis_donasi = Jenis_Donasi(nama, deskripsi)
            admin.kelola_jenis_donasi(jenis_donasi)
            print(f"Jenis Donasi '{nama}' Berhasil Ditambahkan!")
        elif pilihan == "2":
            os.system("cls")
            pendonor_list = admin.lihat_pendonor()
            print("||    Daftar Pendonor   ||: ")
            for p in pendonor_list:
                print(f"Username: {p.username}, Email: {p.email}")
        elif pilihan == "3":
            os.system("cls")
            laporan = admin.buat_laporan()
            print("||    Laporan Donasi    ||:")
            print(f"Total Pendonor: {laporan['total_pendonor']}")
            print(f"Total Nominal: {laporan['total_nominal']}")
        elif pilihan == "4":
            break
        else:
            print("Pilihan Tidak Valid. Silakan Coba Lagi :>")

def menu_pendonor(pendonor):
    while True:
        os.system("Color A")
        print("======================================")
        print("      >> SELAMAT DATANG DONATUR!      ")
        print("======================================")
        print("        1.| Beri Donasi               ")
        print("        2.| Riwayat Donasi            ")
        print("        3.| Profil                    ")
        print("        4.| Keluar                    ")
        print("======================================")
        pilihan = input("Pilih Menu Yang Pendonor Inginkan: ")

        if pilihan == "1":
            no = 0
            os.system("cls")
            print("=================================")
            print("| Donasi |")
            print("=================================")
            donasi_list = Jenis_Donasi.get_jenis_donasi_list()
            for p in donasi_list:
                no+=1
                print(f"{no}. {p.nama} {p.deskripsi}")
            print("=================================")
            donasi = int(input("Masukkan Jenis Donasi: "))
            
            angka = 0
            for p in donasi_list:
                angka+=1
                if donasi == angka:
                    nama = p.nama
                    break  
            
            jenis_metode = Metode_Pembayaran.get_metode()
            no = 0
            for p in jenis_metode:
                no+=1
                print(f"{no}. {p}")
            
            angka = 0
            metode = int(input("Masukkan Metode Pembayaran: "))
            for p in jenis_metode:
                angka+=1
                if metode == angka:
                    met = p
                    print(met)
                    break
            metode_pembayaran = Metode_Pembayaran(met)
            nominal = int(input("Masukkan Nominal Donasi: "))
            jenis_donasi = Jenis_Donasi(nama, "")
            donasi = Donasi(nominal, jenis_donasi, metode_pembayaran)
            pendonor.menyumbang(donasi)
            print("Donasi Berhasil!")
        elif pilihan == "2":
            os.system("cls")
            riwayat = pendonor.riwayat_donasi()
            print("||   Riwayat Donasi Pendonor   ||:")
            for r in riwayat:
                print(f"Nominal: {r.nominal}, Jenis Donasi: {r.jenis_donasi.nama}, Metode Pembayaran: {r.metode_pembayaran.metode}")
        elif pilihan == "3":
            os.system("cls")
            print(f"Nama: {pendonor.username}")
            total_donasi = sum(donasi.nominal for donasi in pendonor.donasi)
            print(f"Total Donasi: {total_donasi}")
            print("Tempat Donasi:")
            for donasi in pendonor.donasi:
                print(f"- {donasi.jenis_donasi.nama}")
        elif pilihan == "4":
            break
        else:
            print("Pilihan Tidak Valid. Silakan Coba Lagi :>")

def main():
    sistem = Sistem()
    # Hardcoded admin
    sistem.registrasi_user("admin@donasi.com", "admin", "admin", is_admin=True)
    sistem.registrasi_user("admin@donasi.com", "user", "user", is_admin=False)

    while True:
        pilihan = menu_utama()

        if pilihan == "1":
            os.system("cls")
            username = input("Masukkan Username: ")
            password = input("Masukkan Password: ")
            user = sistem.login(username, password)
            if user:
                if isinstance(user, Admin):
                    menu_admin(user)
                else:
                    menu_pendonor(user)
            else:
                print("Login Gagal. Username atau Password Salah :>")
        elif pilihan == "2":
            os.system("cls")
            email = input("Masukkan Email: ")
            username = input("Masukkan Username: ")
            password = input("Masukkan Password: ")
            user = sistem.registrasi_user(email, username, password, False )
            print("Registrasi Berhasil.")
        elif pilihan == "3":
            os.system("cls")
            print("                                             ")
            print("=============================================")
            print("Terima Kasih Telah Menggunakan Donasi Center!")
            print("=============================================")
            print("                                             ")
            break
        else:
            print("Pilihan Tidak Valid. Silakan Coba Lagi :>")

if __name__ == "__main__":
    main()
