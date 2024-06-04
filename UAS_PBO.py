import csv
import os
from enum import Enum
from collections import defaultdict
import qrcode;
from PIL import Image


qr = qrcode.QRCode(
    version = 10,
    box_size = 7,
    border = 1
)

class JenisDonasi(Enum):
    PAKAIAN = 1
    MAKANAN = 2
    UANG = 3

class Payment(Enum):
    QRIS = 1
    BANK = 2
    SALDO = 3

class User:
    def __init__(self, email, username, password, role):
        self.email = email
        self.username = username
        self.password = password
        self.role = role
        
    def setEmail(self, email):
        self.email = email
        
    def getEmail(self):
        return self.email
    
    def setPassword(self, password):
        self.password = password
        
    def getPassword(self):
        return self.password
    
    def setSaldo(self, saldo):
        self.saldo = saldo
        
    def getSaldo(self):
        return self.saldo

class Admin(User):
    def __init__(self, email, username, password, role="Admin"):
        super().__init__(email, username, password, role)

class Donatur(User):
    def __init__(self, email, username, password, role="Donatur", saldo=0):
        super().__init__(email, username, password, role)
        self.saldo = saldo
    
    def profile(self):
        return f"Email : {self.email} \nPassword : {self.password}"

class Donasi:
    def __init__(self, nama, deskripsi, jenis_donasi_harga):
        self.nama = nama
        self.deskripsi = deskripsi
        self.jenis_donasi_harga = jenis_donasi_harga

class DonasiCenter:
    def __init__(self, file_user, file_donasi, file_riwayat):
        self.file_user = file_user
        self.file_donasi = file_donasi
        self.file_riwayat = file_riwayat
    
    def regisDonatur(self, user):
        try:
            with open(self.file_user, mode='a', newline='') as file:
                fieldnames = ['Email', 'Username', 'Password', 'Role', 'Saldo']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                # Check if file is empty to write the header
                file_is_empty = file.tell() == 0
                if file_is_empty:
                    writer.writeheader()
                
                user_data = {
                    'Email': user.email,
                    'Username': user.username,
                    'Password': user.password,
                    'Role': user.role,
                    'Saldo': user.saldo if isinstance(user, Donatur) else ''
                }
                writer.writerow(user_data)
                print(f"User {user.username} added successfully.")
                
        except Exception as e:
            print(f"An error occurred while writing to the CSV file: {e}")

    def login(self, username, password):
        try:
            with open(self.file_user, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Username'] == username and row['Password'] == password:
                        email = row['Email']
                        role = row['Role']
                        saldo = int(row['Saldo']) if row['Saldo'].isdigit() else 0
                        if role == "Admin":
                            return Admin(email, username, password)
                        else:
                            return Donatur(email, username, password, saldo=saldo)
            print("Login failed: Invalid username or password.")
        except Exception as e:
            print(f"An error occurred while reading the CSV file: {e}")
        return None
    
    def tambah_donasi(self):
        while True:
            nama = input("Masukkan nama donasi (atau '0' untuk kembali): ")
            if nama == "0":
                return  

            deskripsi = input("Masukkan deskripsi donasi (atau '0' untuk kembali): ")
            if deskripsi == "0":
                return  

            jenis_donasi_harga_input = input("Masukkan jenis donasi (pisahkan dengan '/') (atau '0' untuk kembali): ")
            if jenis_donasi_harga_input == "0":
                return  

            jenis_donasi_harga_pairs = jenis_donasi_harga_input.split('/')
            jenis_donasi_harga = {}
            
            for pair in jenis_donasi_harga_pairs:
                if ':' in pair:
                    jenis_donasi, harga = pair.split(':', 1)
                    if harga.isdigit():
                        jenis_donasi_harga[jenis_donasi] = int(harga)
                    else:
                        print(f"Error: Harga untuk jenis donasi '{jenis_donasi}' bukan angka yang valid. Input diabaikan.")
                else:
                    print(f"Error: Format jenis donasi '{pair}' tidak valid. Harus berupa 'jenis:harga'. Input diabaikan.")
            
            donasi = Donasi(nama, deskripsi, jenis_donasi_harga)
            self.simpan_donasi(donasi)
            print("Donasi berhasil ditambahkan.")
            return

    def simpan_donasi(self, donasi):
        try:
            with open(self.file_donasi, mode='a', newline='') as file:
                fieldnames = ['Nama', 'Deskripsi', 'Jenis Donasi']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                jenis_donasi_str = ';'.join([f"{jenis}:{harga}" for jenis, harga in donasi.jenis_donasi_harga.items()])
                writer.writerow({
                    'Nama': donasi.nama,
                    'Deskripsi': donasi.deskripsi,
                    'Jenis Donasi': jenis_donasi_str  # Simpan jenis donasi dan harga sebagai string dipisahkan oleh ';'
                })
                print("Donasi berhasil disimpan.")
        except Exception as e:
            print(f"An error occurred while writing to the CSV file: {e}")
            
    def ubah_donasi(self):
        while True:
            print("Daftar Donasi:")
            daftar_donasi = self.ambil_donasi()
            for idx, donasi in enumerate(daftar_donasi, start=1):
                print(f"{idx}. Nama: {donasi.nama}, Deskripsi: {donasi.deskripsi}")

            idx_donasi_input = input("Pilih donasi yang ingin diubah (atau '0' untuk kembali): ")
            if idx_donasi_input == "0":
                return  

            if not idx_donasi_input.isdigit():
                print("Masukkan nomor donasi yang valid.")
                continue
            
            idx_donasi = int(idx_donasi_input) - 1
            if idx_donasi < 0 or idx_donasi >= len(daftar_donasi):
                print("Nomor donasi tidak valid.")
                continue

            donasi_terpilih = daftar_donasi[idx_donasi]
            print("1. Nama Donasi")
            print("2. Deskripsi")
            print("3. Jenis Donasi")
            pilihan = input("Pilih data yang ingin diubah (atau '0' untuk kembali): ")
            if pilihan == "0":
                return 

            if pilihan == "1":
                nama_baru = input("Masukkan nama baru untuk donasi ini (atau '0' untuk kembali): ")
                if nama_baru == "0":
                    continue
                donasi_terpilih.nama = nama_baru
            elif pilihan == "2":
                deskripsi_baru = input("Masukkan deskripsi baru untuk donasi ini (atau '0' untuk kembali): ")
                if deskripsi_baru == "0":
                    continue 
                donasi_terpilih.deskripsi = deskripsi_baru
            elif pilihan == "3":
                jenis_donasi_baru = input("Masukkan jenis donasi baru (pisahkan dengan '/') (atau '0' untuk kembali): ")
                if jenis_donasi_baru == "0":
                    continue  
                jenis_donasi_pairs = jenis_donasi_baru.split('/')
                jenis_donasi_harga = {}
                valid_input = True
                for pair in jenis_donasi_pairs:
                    if ':' in pair:
                        jenis_donasi, harga = pair.split(':', 1)
                        if harga.isdigit():
                            jenis_donasi_harga[jenis_donasi] = int(harga)
                        else:
                            print(f"Error: Harga untuk jenis donasi '{jenis_donasi}' bukan angka yang valid. Input diabaikan.")
                            valid_input = False
                            break
                    else:
                        print(f"Error: Format jenis donasi '{pair}' tidak valid. Harus berupa 'jenis:harga'. Input diabaikan.")
                        valid_input = False
                        break
                
                if valid_input:
                    donasi_terpilih.jenis_donasi_harga = jenis_donasi_harga
                else:
                    continue 
            else:
                print("Pilihan tidak valid.")
                continue

            # Save changes to the CSV file
            try:
                with open(self.file_donasi, mode='w', newline='') as file:
                    fieldnames = ['Nama', 'Deskripsi', 'Jenis Donasi']
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    for donasi in daftar_donasi:
                        writer.writerow({
                            'Nama': donasi.nama,
                            'Deskripsi': donasi.deskripsi,
                            'Jenis Donasi': ';'.join([f"{jenis}:{harga}" for jenis, harga in donasi.jenis_donasi_harga.items()])
                        })
                print("Donasi berhasil diubah.")
            except Exception as e:
                print(f"An error occurred while writing to the CSV file: {e}")
            return  


    def hapus_donasi(self):
        while True:
            print("Daftar Donasi:")
            daftar_donasi = self.ambil_donasi()
            for idx, donasi in enumerate(daftar_donasi, start=1):
                print(f"{idx}. Nama: {donasi.nama}, Deskripsi: {donasi.deskripsi}")

            idx_donasi_input = input("Pilih donasi yang ingin dihapus (atau '0' untuk kembali): ")
            if idx_donasi_input == "0":
                return 

            if not idx_donasi_input.isdigit():
                print("Masukkan nomor donasi yang valid.")
                continue
            
            idx_donasi = int(idx_donasi_input) - 1
            if idx_donasi < 0 or idx_donasi >= len(daftar_donasi):
                print("Nomor donasi tidak valid.")
                continue

            donasi_terpilih = daftar_donasi[idx_donasi]
            confirm = input(f"Apakah Anda yakin ingin menghapus donasi {donasi_terpilih.nama}? (Y/N, atau '0' untuk kembali): ")
            if confirm == "0":
                continue  

            if confirm.lower() == 'y':
                # Hapus donasi dari daftar
                daftar_donasi.pop(idx_donasi)

                # Simpan ulang seluruh entri donasi ke dalam file CSV
                try:
                    with open(self.file_donasi, mode='w', newline='') as file:
                        fieldnames = ['Nama', 'Deskripsi', 'Jenis Donasi']
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        writer.writeheader()
                        for donasi in daftar_donasi:
                            jenis_donasi_str = ';'.join([f"{jenis}:{harga}" for jenis, harga in donasi.jenis_donasi_harga.items()])
                            writer.writerow({
                                'Nama': donasi.nama,
                                'Deskripsi': donasi.deskripsi,
                                'Jenis Donasi': jenis_donasi_str
                            })
                    print("Donasi berhasil dihapus.")
                except Exception as e:
                    print(f"An error occurred while writing to the CSV file: {e}")
                return
            else:
                print("Penghapusan donasi dibatalkan.")
                return  


    def lihat_donasi(self):
        daftar_donasi = self.ambil_donasi()
        print("Daftar Donasi:")
        for idx, donasi in enumerate(daftar_donasi, start=1):
            jenis_donasi_harga_str = ', '.join([f"{jenis} (Rp{harga})" for jenis, harga in donasi.jenis_donasi_harga.items()])
            print(f"{idx}. Nama: {donasi.nama}, Deskripsi: {donasi.deskripsi}, Jenis Donasi: {jenis_donasi_harga_str}")
        
        while True:
            print("| [1]. Ubah Donasi")
            print("| [2]. Hapus Donasi")
            print("| [3]. Kembali")
            pilihan = input("Pilih Menu Yang Anda Inginkan: ")
            if pilihan == "1":
                self.ubah_donasi()
                break
            elif pilihan == "2":
                self.hapus_donasi()
                break
            elif pilihan == "3":
                break
            else:
                print("Pilihan Tidak Valid. Silakan Coba Lagi :>")

    def ambil_donasi(self):
        try:
            with open(self.file_donasi, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                donasi_list = []
                for row in reader:
                    jenis_donasi_harga = {item.split(':')[0]: int(item.split(':')[1]) for item in row['Jenis Donasi'].split(';')}
                    donasi_list.append(Donasi(row['Nama'], row['Deskripsi'], jenis_donasi_harga))
                return donasi_list
        except Exception as e:
            print(f"An error occurred while reading the CSV file: {e}")
            return []

    def menu_donasi(self):
        while True:
            os.system("Color B")
            print("===========================================")
            print("Kelola Donasi")
            print("===========================================")
            print("[1]. Tambah Donasi")
            print("[2]. Lihat Donasi")
            print("[3]. Kembali")
            print("===========================================")
            pilihan = input("Pilih Menu Yang Anda Inginkan: ")
            if pilihan == "1":
                self.tambah_donasi()
            elif pilihan == "2":
                self.lihat_donasi()
            elif pilihan == "3":
                break
            else:
                print("Pilihan Tidak Valid. Silakan Coba Lagi :>")
                
    def simpan_riwayat_donasi(self, donatur, donasi_tujuan, deskripsi_donasi,banyak, jumlah):
        try:
            with open(self.file_riwayat, mode='a', newline='') as file:
                fieldnames = ['Username', 'Nama Donasi', 'Jenis Donasi', 'Banyak', 'Total']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                # Check if file is empty to write the header
                file_is_empty = file.tell() == 0
                if file_is_empty:
                    writer.writeheader()
                donasi_user = ({
                    'Username': donatur.username,
                    'Nama Donasi': donasi_tujuan,
                    'Jenis Donasi': deskripsi_donasi,
                    'Banyak': banyak,
                    'Total': jumlah
                })
                writer.writerow(donasi_user)
                print("Riwayat donasi berhasil disimpan.")
        except Exception as e:
            print(f"An error occurred while writing to the CSV file: {e}")
            
    def lihat_alldonatur(self):
        donatur_dict = defaultdict(int)
        try:
            with open(self.file_riwayat, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    username = row['Username']
                    jumlah_donasi = int(row['Total'])
                    donatur_dict[username] += jumlah_donasi
        except Exception as e:
            print(f"An error occurred while reading the CSV file: {e}")
            return
        
        # Sort donatur by total donation amount in descending order
        sorted_donatur = sorted(donatur_dict.items(), key=lambda x: x[1], reverse=True)
        
        print("Penyumbang Tertinggi:")
        for idx, (username, total_donasi) in enumerate(sorted_donatur[:10], start=1):
            print(f"{idx}. Username: {username}, Total Donasi: {total_donasi}")
        
    def update_user_data_in_csv(self, donatur):
        try:
            with open(self.file_user, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                users = list(reader)
            
            with open(self.file_user, mode='w', newline='') as file:
                fieldnames = ['Email', 'Username', 'Password', 'Role', 'Saldo']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                
                for user in users:
                    if user['Username'] == donatur.username:
                        user['Email'] = donatur.email
                        user['Password'] = donatur.password
                        user['Saldo'] = donatur.saldo
                    writer.writerow(user)
            
            print("Data pengguna berhasil diperbarui di file CSV.")
        except Exception as e:
            print(f"Terjadi kesalahan saat menyimpan data ke file CSV: {e}")
            
    def ubah_profil(self, donatur):
        print(" [1]. Email")
        print(" [2]. Password")
        pilihan = input("Pilih data yang ingin diubah: ")
        if pilihan == "1":
            email = input("Masukkan Email Baru: ")
            donatur.setEmail(email)
        elif pilihan == "2":
            password = input("Masukkan Password Baru: ")
            donatur.setPassword(password)
        
        self.update_user_data_in_csv(donatur)
        print("Profil berhasil diubah.")     
            
    def riwayat_donasi(self, donatur):
        no = 0
        total = 0  # Inisialisasi total di luar loop
        try:
            with open(self.file_riwayat, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                print("Riwayat Donasi:")
                for row in reader:
                    if row['Username'] == donatur.username:
                        no += 1
                        print(f"{no}. Nama Donasi: {row['Nama Donasi']}\nJenis Donasi: {row['Jenis Donasi']}\nBanyak: {row['Banyak']}\nTotal: {row['Total']}")
                        total += int(row['Total'])  # Tambahkan nilai total setiap donasi ke total keseluruhan
                print(f"Total Donasi: {total}")
        except Exception as e:
            print(f"An error occurred while reading the CSV file: {e}")

    def laporan_donasi(self):
        donasi_stats = defaultdict(lambda: {'jumlah_orang': 0, 'total_donasi': 0})
        try:
            with open(self.file_riwayat, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                donatur_set = defaultdict(set)
                for row in reader:
                    nama_donasi = row['Nama Donasi']
                    jumlah_donasi = int(row['Total'])
                    username = row['Username']
                    
                    donasi_stats[nama_donasi]['total_donasi'] += jumlah_donasi
                    if username not in donatur_set[nama_donasi]:
                        donasi_stats[nama_donasi]['jumlah_orang'] += 1
                        donatur_set[nama_donasi].add(username)
        except Exception as e:
            print(f"An error occurred while reading the CSV file: {e}")
            return
        
        print("Laporan Donasi:")
        for nama_donasi, stats in donasi_stats.items():
            print(f"Nama Donasi: {nama_donasi}, Jumlah Orang: {stats['jumlah_orang']}, Total Donasi: {stats['total_donasi']}")

    def beri_donasi(self, donatur):
        daftar_donasi = self.ambil_donasi()
        if not daftar_donasi:
            print("Belum ada donasi yang tersedia.")
            return

        while True:
            print("Daftar Donasi:")
            for idx, donasi in enumerate(daftar_donasi, start=1):
                print(f"{idx}. Nama: {donasi.nama}, Deskripsi: {donasi.deskripsi}")

            pilihan_donasi_input = input("Pilih donasi yang ingin Anda sumbangkan (atau '0' untuk kembali): ")
            if pilihan_donasi_input == "0":
                return  

            if not pilihan_donasi_input.isdigit():
                print("Masukkan nomor yang valid.")
                continue
            
            pilihan_donasi = int(pilihan_donasi_input)
            if pilihan_donasi < 1 or pilihan_donasi > len(daftar_donasi):
                print("Pilihan tidak valid.")
                continue

            donasi_tujuan = daftar_donasi[pilihan_donasi - 1]

            while True:
                print("Jenis Donasi yang tersedia:")
                for idx, (jenis, harga) in enumerate(donasi_tujuan.jenis_donasi_harga.items(), start=1):
                    print(f"{idx}. {jenis} (Rp{harga})")

                pilihan_jenis_input = input("Pilih jenis donasi (atau '0' untuk kembali): ")
                if pilihan_jenis_input == "0":
                    break  

                if not pilihan_jenis_input.isdigit():
                    print("Masukkan nomor yang valid.")
                    continue
                
                pilihan_jenis = int(pilihan_jenis_input)
                if pilihan_jenis < 1 or pilihan_jenis > len(donasi_tujuan.jenis_donasi_harga):
                    print("Pilihan tidak valid.")
                    continue

                jenis_donasi = list(donasi_tujuan.jenis_donasi_harga.keys())[pilihan_jenis - 1]
                harga = donasi_tujuan.jenis_donasi_harga[jenis_donasi]

                while True:
                    banyak_donasi_input = input("Masukkan jumlah donasi (atau '0' untuk kembali): ")
                    if banyak_donasi_input == "0":
                        break 

                    if not banyak_donasi_input.isdigit():
                        print("Masukkan jumlah yang valid.")
                        continue

                    banyak_donasi = int(banyak_donasi_input)
                    if banyak_donasi < 1:
                        print("Jumlah donasi harus lebih dari 0.")
                        continue

                    total_harga = harga * banyak_donasi
                    print(f"Total yang harus dibayar: Rp{total_harga}")

                    while True:
                        print("Pilih metode pembayaran:")
                        print("1. QRIS")
                        print("2. Bank")
                        print("3. Saldo")
                        pilihan_pembayaran = input("Pilih metode pembayaran (atau '0' untuk kembali): ")
                        if pilihan_pembayaran == "0":
                            break  

                        if pilihan_pembayaran == "1":
                            qr.add_data(donasi_tujuan)
                            qr.make(fit=True)
                            img = qr.make_image(fill="black", back_color="white")
                            img.show()
                        elif pilihan_pembayaran == "2":
                            print("Pilih bank:")
                            print("1. Bank A - 1234567890")
                            print("2. Bank B - 0987654321")
                            input("Masukkan bank pilihan Anda: ")
                            print("Silakan transfer ke nomor rekening yang tertera.")
                        elif pilihan_pembayaran == "3":
                            if donatur.saldo < total_harga:
                                print("Saldo Anda tidak mencukupi.")
                                continue
                            else:
                                donatur.saldo -= total_harga
                                print(f"Saldo berhasil digunakan. Sisa saldo Anda: {donatur.saldo}")
                                self.update_user_data_in_csv(donatur)
                        else:
                            print("Pilihan tidak valid.")
                            continue

                        self.simpan_riwayat_donasi(donatur, donasi_tujuan.nama, jenis_donasi, banyak_donasi, total_harga)
                        return  
                    break
                break
            break

    def update_saldo(self, donatur):
        try:
            with open(self.file_user, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                users = [row for row in reader]

            for user in users:
                if user['Username'] == donatur.username:
                    user['Saldo'] = donatur.saldo

            with open(self.file_user, mode='w', newline='') as file:
                fieldnames = ['Email', 'Username', 'Password', 'Role', 'Saldo']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(users)

            print("Saldo berhasil diperbarui.")
        except Exception as e:
            print(f"An error occurred while updating the CSV file: {e}")
        
    def top_up_saldo(self, donatur):
        try:
            jumlah = int(input("Masukkan jumlah saldo yang ingin ditop-up: "))
            donatur.saldo += jumlah
            self.update_saldo(donatur)
            print(f"Top-up berhasil. Saldo Anda sekarang: Rp{donatur.saldo}")
        except ValueError:
            print("Masukkan jumlah yang valid.")
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
        
    def menu_profil(self,donatur):
        while True:
            print(donatur.profile())
            print(" [1]. Ubah")
            print(" [2]. Keluar")
            pilihan = input("Pilihan : ")
            if pilihan == "1":
                self.ubah_profil(donatur)
            elif pilihan == "2":
                break
            else:
                print("tidak tersedia")
    
    def menu_admin(self):
        while True:
            os.system("Color B")
            print("======================================")
            print("       >> SELAMAT DATANG ADMIN!       ")
            print("======================================")
            print("        1.| Kelola Donasi             ")
            print("        2.| Lihat Donatur             ")
            print("        3.| Laporan Donasi            ")
            print("        4.| Keluar                    ")
            print("======================================")
            pilihan = input("Pilih Menu Yang Admin Inginkan: ")

            if pilihan == "1":
                self.menu_donasi()
            elif pilihan == "2":
                self.lihat_alldonatur()
            elif pilihan == "3":
                self.laporan_donasi()
            elif pilihan == "5":
                break
            else:
                print("Pilihan Tidak Valid. Silakan Coba Lagi :>")       
                
    def menu_donatur(self, donatur):
        nominal = 0
        while True:
            print(f"Saldo : {donatur.saldo}")
            os.system("Color A")
            print("======================================")
            print("      >> SELAMAT DATANG DONATUR!      ")
            print("======================================")
            print("        1.| Beri Donasi               ")
            print("        2.| Riwayat Donasi            ")
            print("        3.| Profil                    ")
            print("        4.| Top Up Saldo              ")
            print("        5.| Keluar                    ")
            print("======================================")
            pilihan = input("Pilih Menu Yang Donatur Inginkan: ")
            if pilihan == "1":
                self.beri_donasi(donatur)
            elif pilihan == "2":
                self.riwayat_donasi(donatur)
            elif pilihan == "3":
                self.menu_profil(donatur)
            elif pilihan == "4":
                self.top_up_saldo(donatur)
            elif pilihan == "5":
                break
            else:
                print("Pilihan Tidak Valid. Silakan Coba Lagi :>")

    def menu_regis(self):
        os.system("cls")
        email = input("Masukkan Email: ")
        username = input("Masukkan Username: ")
        password = input("Masukkan Password: ")
        newDonatur = Donatur(email, username, password)
        self.regisDonatur(newDonatur)
        print("Registrasi Berhasil.")

    def login_menu(self):
        os.system("cls")
        username = input("Masukkan Username: ")
        password = input("Masukkan Password: ")
        userLogin = self.login(username, password)
        if userLogin:
            print(f"Login successful")
            if isinstance(userLogin, Donatur):
                self.menu_donatur(userLogin)
            else:
                self.menu_admin()
        else:
            print("Login failed.")

    def main_menu(self):
        while True:
            os.system("Color B")
            print("===========================================")
            print(">>>>  SELAMAT DATANG DI DONASI CENTER  <<<<")
            print("===========================================")
            print("      .        1. Login              .     ")
            print("         .     2. Registrasi      .        ")
            print("            .  3. Keluar       .           ")
            print("===========================================")
            pilihan = input("Pilih Menu Yang Anda Inginkan: ")
            if pilihan == "1":
                self.login_menu()
            elif pilihan == "2":
                self.menu_regis()
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

def main():
    user_file = 'dataU.csv'
    donasi_file = 'donasi.csv'
    riwayat_donasi_file = 'riwayat_donasi.csv'
    donasi_center = DonasiCenter(user_file, donasi_file, riwayat_donasi_file)
    donasi_center.main_menu()

if __name__ == "__main__":
    main()

