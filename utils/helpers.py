import os
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def nhap_sdt():
    while True:
        sdt = input("Số điện thoại (10 số): ")
        if sdt.isdigit() and len(sdt) == 10:
            return sdt
        print("\033[91mSố điện thoại không hợp lệ. Vui lòng nhập lại.\033[0m")

def loading():
    print("\033[93mĐang xử lý...\033[0m", end="")
    for _ in range(3):
        print(".", end="", flush=True)
        time.sleep(0.4)
    print()
