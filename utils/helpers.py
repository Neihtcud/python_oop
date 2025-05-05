import os
import time
import re
import csv

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
        if len(ten) > 0 and all(c.isalpha() or c.isspace() for c in ten):
            return ten
        print("\033[91mTên không hợp lệ. Tên chỉ được chứa chữ cái và khoảng trắng.\033[0m")

def nhap_ma_khach_hang():
    while True:
        ma = input("Mã KH: ").strip().upper()
        if len(ma) > 0 and not ma.isspace():
            return ma
        print("\033[91mMã khách hàng không được để trống.\033[0m")

def loading(msg="Đang xử lý", dot_count=3, delay=0.4):
    print(f"\033[93m{msg}\033[0m", end="")
    for _ in range(dot_count):
        print(".", end="", flush=True)
        time.sleep(delay)
    print()

def xac_nhan(msg="Bạn có chắc chắn không?"):
    while True:
        choice = input(f"\033[93m{msg} (y/n): \033[0m").lower().strip()
        if choice == 'y':
            return True
        if choice == 'n':
            return False
        print("\033[91mVui lòng nhập 'y' hoặc 'n'.\033[0m")

# Thêm hai hàm mới để đọc và ghi dữ liệu khách hàng từ/vào file CSV
def read_customers_from_csv(filename):
    """
    Đọc dữ liệu khách hàng từ file CSV
    
    Args:
        filename (str): Đường dẫn đến file CSV
        
    Returns:
        list: Danh sách các dict chứa thông tin khách hàng
    """
    customers = []
    if not os.path.exists(filename):
        return customers  # Trả về danh sách rỗng nếu file không tồn tại
    
    try:
        with open(filename, mode='r', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                customers.append(row)
        return customers
    except Exception as e:
        print(f"\033[91mLỗi khi đọc file CSV: {e}\033[0m")
        return []

def write_customers_to_csv(filename, customers):
    """
    Ghi danh sách khách hàng vào file CSV
    
    Args:
        filename (str): Đường dẫn đến file CSV
        customers (list): Danh sách các đối tượng khách hàng
        
    Returns:
        bool: True nếu ghi thành công, False nếu có lỗi
    """
    # Đảm bảo thư mục tồn tại
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Chuẩn bị dữ liệu để ghi
    customer_dicts = []
    for customer in customers:
        # Giả sử mỗi đối tượng khách hàng có phương thức to_dict()
        customer_dicts.append(customer.to_dict())
    
    # Xác định các trường dữ liệu từ khách hàng đầu tiên hoặc sử dụng các trường cố định
    fieldnames = ["Loai", "MaKH", "TenKH", "SDT", "Email", "DiemTichLuy", "SoLanMua", "TongGiaTri"]
    
    try:
        with open(filename, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(customer_dicts)
        return True
    except Exception as e:
        print(f"\033[91mLỗi khi ghi file CSV: {e}\033[0m")
        return False