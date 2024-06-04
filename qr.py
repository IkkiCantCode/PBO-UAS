import qrcode;
import image;

qr = qrcode.QRCode(
    version = 10,
    box_size = 7,
    border = 1
)

qr.add_data("https://github.com/IkkiCantCode/PBO-UAS")
qr.make(fit = True)
img = qr.make_image(fill = "black", back_color = "white")
img.show()


# def addCsvUser(regis):
#     file_exists = os.path.exists('dataU.csv')
#     file_empty = not file_exists or os.stat('dataU.csv').st_size == 0
    
#     try:
#         with open('dataU.csv', mode='a', newline='') as file:
#             fieldnames = ['Email', 'Username', 'Password', 'Saldo', 'Role']
#             writer = csv.DictWriter(file, fieldnames=fieldnames)
            
#             if file_empty:
#                 writer.writeheader()
#             writer.writerow({
#                 'Email': regis[0],
#                 'Username': regis[1],
#                 'Password': regis[2],
#                 'Saldo': regis[3],
#                 'Role': regis[4]
#             })
#     except Exception as e:
#         print(f"An error occurred while writing to the CSV file: {e}")
        
# def openCsvUser():
#     try:
#         with open('dataU.csv', mode='r', newline='') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 print(row['Email'], row['Username'], row['Password'], row['Saldo'], row['Role'])
#                 Admin.pendonor.append(Pendonor(row))
#     except Exception as e:
#         print(f"An error occurred while reading the CSV file: {e}")

# email = input("Masukkan Email: ")
# username = input("Masukkan Username: ")
# password = input("Masukkan Password: ")
# regis = (email, username, password, 0, 'donatur')
# print("Registrasi Berhasil.")
# addCsvUser(regis)
# openCsvUser()