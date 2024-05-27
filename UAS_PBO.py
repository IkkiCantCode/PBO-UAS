# Tema : Non-profit

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
        self.jenis_donasi = []
        self.pendonor = []
        self.laporan = []

    def kelola_jenis_donasi(self, jenis_donasi):
        self.jenis_donasi.append(jenis_donasi)

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
    def __init__(self, nama, deskripsi):
        self.nama = nama
        self.deskripsi = deskripsi

class Donasi:
    def __init__(self, nominal, jenis_donasi, metode_pembayaran):
        self.nominal = nominal
        self.jenis_donasi = jenis_donasi
        self.metode_pembayaran = metode_pembayaran

class Metode_Pembayaran:
    def __init__(self, metode):
        self.metode = metode

class Sistem:
    def __init__(self):
        self.admin = []
        self.pendonor = []

    def registrasi_user(self, email, username, password, is_admin=False):
        if is_admin:
            user = Admin(email, username, password)
            self.admin.append(user)
        else:
            user = Pendonor(email, username, password)
            self.pendonor.append(user)
        return user

    def login(self, username, password):
        for admin in self.admin:
            if admin.username == username and admin.password == password:
                return admin
        for pendonor in self.pendonor:
            if pendonor.username == username and pendonor.password == password:
                return pendonor
        return None

def menu_utama():
    print("   .   SELAMAT DATANG DI DONASI CENTER  .  ")
    print("      .        1. Login              .     ")
    print("         .     2. Registrasi      .        ")
    print("            .  3. Keluar       .           ")
    pilihan = input("Pilih Menu Yang Anda Inginkan: ")
    return pilihan

def menu_admin(admin):
    while True:
        print("       >> SELAMAT DATANG ADMIN!       ")
        print("        1.| Tambah Jenis Donasi       ")
        print("        2.| Lihat Pendonor            ")
        print("        3.| Buat Laporan              ")
        print("        4.| Keluar                    ")
        pilihan = input("Pilih Menu Yang Admin Inginkan: ")

        if pilihan == "1":
            nama = input("Masukkan Jenis Donasi: ")
            deskripsi = input("Masukkan Deskripsi: ")
            jenis_donasi = Jenis_Donasi(nama, deskripsi)
            admin.kelola_jenis_donasi(jenis_donasi)
            print(f"Jenis Donasi '{nama}' Berhasil Ditambahkan!")
        elif pilihan == "2":
            pendonor_list = admin.lihat_pendonor()
            print("||    Daftar Pendonor   ||: ")
            for p in pendonor_list:
                print(f"Username: {p.username}, Email: {p.email}")
        elif pilihan == "3":
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
        print("     >> SELAMAT DATANG PENDONOR!      ")
        print("        1.| Beri Donasi               ")
        print("        2.| Riwayat Donasi            ")
        print("        3.| Keluar                    ")
        pilihan = input("Pilih Menu Yang Pendonor Inginkan: ")

        if pilihan == "1":
            nominal = int(input("Masukkan Nominal Donasi: "))
            nama_jenis = input("Masukkan Jenis Donasi: ")
            metode = input("Masukkan Metode Pembayaran: ")
            metode_pembayaran = Metode_Pembayaran(metode)
            jenis_donasi = Jenis_Donasi(nama_jenis)
            donasi = Donasi(nominal, jenis_donasi, metode_pembayaran)
            pendonor.menyumbang(donasi)
            print("Donasi Berhasil!")
        elif pilihan == "2":
            riwayat = pendonor.riwayat_donasi()
            print("||   Riwayat Donasi Pendonor   ||:")
            for r in riwayat:
                print(f"Nominal: {r.nominal}, Jenis Donasi: {r.jenis_donasi.nama}, Metode Pembayaran: {r.metode_pembayaran.metode}")
        elif pilihan == "3":
            break
        else:
            print("Pilihan Tidak Valid. Silakan Coba Lagi :>")


def main():
    sistem = Sistem()
    while True:
        pilihan = menu_utama()

        if pilihan == "1":
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
            email = input("Masukkan Email: ")
            username = input("Masukkan Username: ")
            password = input("Masukkan Password: ")
            is_admin = input("Apakah Anda Admin? (yes/no): ").lower() == "yes"
            user = sistem.registrasi_user(email, username, password, is_admin)
            if is_admin:
                print("Admin Berhasil Didaftarkan.")
            else:
                print("Pendonor Berhasil Didaftarkan.")
        elif pilihan == "3":
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