import os
import time
import re
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def nhap_sdt():
    while True:
        sdt = input("Số điện thoại (10 số): ")
        if sdt.isdigit() and len(sdt) == 10:
            return sdt
        print("\033[91mSố điện thoại không hợp lệ. Vui lòng nhập lại.\033[0m")
def kiem_tra_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def nhap_email():
    while True:
        email = input("Email: ").strip()
        if kiem_tra_email(email):
            return email
        print("\033[91mEmail không hợp lệ. Vui lòng nhập lại.\033[0m")

def nhap_ten():
    while True:
        ten = input("Tên KH: ").strip()
        if ten.replace(" ", "").isalpha():
            return ten
        print("\033[91mTên không hợp lệ. Tên chỉ được chứa chữ cái và khoảng trắng.\033[0m")


def loading(msg="Đang xử lý", dot_count=3, delay=0.4):
    print(f"\033[93m{msg}\033[0m", end="")
    for _ in range(3):
        print(".", end="", flush=True)
        time.sleep(delay)
    print()
