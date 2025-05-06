from datetime import datetime
from models.customer import LoyalCustomer

def ghi_log(hanh_dong, khach_hang, log_file='log.txt'):
    try: 
        with open(log_file, 'a', encoding='utf-8') as f:
            thoi_gian = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            loai = "Loyal" if isinstance(khach_hang, LoyalCustomer) else "Casual"
            f.write(f"[{thoi_gian}] {hanh_dong} khách hàng: {khach_hang.ma_khach_hang} - {khach_hang.ten_khach_hang} - {loai}\n")
    except Exception as e:
        print(f"\033[91mLỗi ghi log: {e}\033[0m")
