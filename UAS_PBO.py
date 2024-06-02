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
    sub_metode_dict = {
        "Bank": ["BNI", "Mandiri", "BCA", "BTN"],
        "E-Wallet": ["Dana", "GoPay", "ShopeePay"]
    }

    def __init__(self, metode):
        self.metode = metode

    @classmethod
    def get_metode(cls):
        return cls.metode_list

    @classmethod
    def get_sub_metode(cls, metode):
        return cls.sub_metode_dict.get(metode, [])
    
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
    nominal = 0
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
            while True:
                no = 0
                os.system("cls")
                print("=================================")
                print("| Donasi |")
                print("=================================")
                donasi_list = Jenis_Donasi.get_jenis_donasi_list()
                for p in donasi_list:
                    no += 1
                    print(f"{no}. {p.nama} {p.deskripsi}")
                print("=================================")
                
                donasi = input("Masukkan Jenis Donasi (0 untuk kembali): ")

                if donasi == "0":
                    break

                if not donasi.isdigit():
                    print("Input harus berupa angka. Silakan coba lagi.")
                    continue

                donasi = int(donasi)

                if donasi < 1 or donasi > len(donasi_list):
                    print("Pilihan tidak valid! Silakan coba lagi.")
                    continue
                
                angka = 0
                for p in donasi_list:
                    angka += 1
                    if donasi == angka:
                        nama = p.nama
                        break 
                break 

            if donasi == "0":
                continue

            while True:
                jenis_metode = Metode_Pembayaran.get_metode()
                no = 0
                for p in jenis_metode:
                    no += 1
                    print(f"{no}. {p}")
                
                metode = input("Masukkan Metode Pembayaran (0 untuk kembali): ")

                if metode == "0":
                    break

                if not metode.isdigit():
                    print("Input harus berupa angka. Silakan coba lagi.")
                    continue

                metode = int(metode)

                if metode < 1 or metode > len(jenis_metode):
                    print("Pilihan tidak valid! Silakan coba lagi.")
                    continue
            
                
                met = jenis_metode[metode - 1]
                print(f"Metode dipilih: {met}")

                sub_metode = Metode_Pembayaran.get_sub_metode(met)

                while True:
                    no = 0
                    for sm in sub_metode:
                        no += 1
                        print(f"{no}. {sm}")

                    sub_pilihan = input(f"Masukkan pilihan {met} (0 untuk kembali): ")

                    if sub_pilihan == "0":
                        break

                    if not sub_pilihan.isdigit():
                        print("Input harus berupa angka. Silakan coba lagi.")
                        continue

                    sub_pilihan = int(sub_pilihan)

                    if sub_pilihan < 1 or sub_pilihan > len(sub_metode):
                        print("Pilihan tidak valid! Silakan coba lagi.")
                        continue

                    sub_met = sub_metode[sub_pilihan - 1]
                    print(f"Bank Dipilih dipilih: {sub_met}")
                    break  # keluar dari loop sub-metode jika input valid

                if sub_pilihan == "0":
                    continue

                # Validasi untuk nomor kartu kredit atau nomor telepon
                if met == "Bank":
                    while True:
                        no_kartu = input("Masukkan Nomor Kartu Kredit (16 digit) (0 untuk kembali): ")

                        if no_kartu == "0":
                            break

                        if not no_kartu.isdigit() or len(no_kartu) != 16:
                            print("Nomor kartu kredit harus 16 digit angka. Silakan coba lagi.")
                            continue
                        break

                elif met == "E-Wallet":
                    while True:
                        no_telepon = input("Masukkan Nomor Telepon E-Wallet (10-12 digit) (0 untuk kembali): ")
                        if no_telepon == "0":
                            break
                        if not no_telepon.isdigit() or not (10 <= len(no_telepon) <= 12):
                            print("Nomor telepon harus 10-12 digit angka. Silakan coba lagi.")
                            continue
                        break

                    if no_telepon == "0":
                        continue

                if no_kartu == "0":
                    continue

                break  # keluar dari loop metode pembayaran jika input valid

            if metode == "0":
                continue

            # Input nominal donasi
            while True:
                nominal_input = input("Masukkan Nominal Donasi (0 untuk kembali): ")
                if nominal_input == "0":
                    break
                if not nominal_input.isdigit() or int(nominal_input) == 0:
                    print("Nominal harus berupa angka dan tidak boleh nol. Silakan coba lagi.")
                    continue
                nominal = int(nominal_input)
                break  # keluar dari loop nominal jika input valid

            if nominal_input == "0":
                continue

            # Buat objek donasi di luar loop pemeriksaan kembali
            metode_pembayaran = Metode_Pembayaran(f"{met} - {sub_met}")
            jenis_donasi = Jenis_Donasi(nama, "")
            donasi = Donasi(nominal, jenis_donasi, metode_pembayaran)
            pendonor.menyumbang(donasi)
            print("Donasi Berhasil!")

        elif pilihan == "2":
            os.system("cls")
            riwayat = pendonor.riwayat_donasi()
            print("||   Riwayat Donasi Pendonor   ||:")
            for r in riwayat:
                print(f"Nominal: Rp. {r.nominal}, Jenis Donasi: {r.jenis_donasi.nama}, Metode Pembayaran: {r.metode_pembayaran.metode}")
        elif pilihan == "3":
            os.system("cls")
            print(f"Nama: {pendonor.username}")
            total_donasi = sum(donasi.nominal for donasi in pendonor.donasi)
            print(f"Total Donasi: Rp. {total_donasi}")
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
