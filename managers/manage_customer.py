import csv
import os
import shutil
import datetime
import matplotlib.pyplot as plt
from models.customer import LoyalCustomer, CasualCustomer
from utils.logger import ghi_log

class ManageCustomer:
    def __init__(self, filename='khachhang.csv'):
        self.danh_sach_khach_hang = []
        self.filename = filename
        self.doc_file()

    def backup_file(self):
        if os.path.exists(self.filename):
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{self.filename}.backup_{timestamp}"
            try:
                shutil.copy(self.filename, backup_filename)
                print(f"\033[92mĐã tạo bản sao lưu: {backup_filename}\033[0m")
            except Exception as e:
                print(f"\033[91mLỗi sao lưu file: {e}\033[0m")

    def doc_file(self):
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['Loai'] == 'Loyal':
                       kh = LoyalCustomer.from_dict(row)
                    else:
                       kh = CasualCustomer.from_dict(row)
                    self.danh_sach_khach_hang.append(kh)
        except Exception as e:
              print(f"\033[91mLỗi đọc file: {e}\033[0m")         

    def ghi_file(self):
        self.backup_file()
        try:
            with open(self.filename, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['Loai', 'MaKH', 'TenKH', 'SDT', 'Email', 'SoLanMua', 'TongGiaTri', 'DiemTichLuy']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for kh in self.danh_sach_khach_hang:
                    writer.writerow(kh.to_dict())
            print("\033[92mLưu file thành công\033[0m")
        except Exception as e:
            print(f"\033[91mLỗi ghi file: {e}\033[0m")

    def tim_kiem_nang_cao(self, loai=None, ten_chua=None, tong_gia_min=None, tong_gia_max=None, so_lan_mua_min=None, ma_kh=None, sdt_chua=None, email_chua=None):
        ket_qua = []
        for kh in self.danh_sach_khach_hang:
            if loai and not ((loai == 'Loyal' and isinstance(kh, LoyalCustomer)) or (loai == 'Casual' and isinstance(kh, CasualCustomer))):
                continue
            if ten_chua and ten_chua.lower() not in kh.ten_khach_hang.lower():
                continue
            if ma_kh and kh.ma_khach_hang != ma_kh:
                continue
            if sdt_chua and sdt_chua not in kh.so_dien_thoai:
                continue
            if email_chua and email_chua.lower() not in kh.email.lower():
                continue
            if isinstance(kh, CasualCustomer):
                if tong_gia_min is not None and kh.tong_gia_tri_mua_hang < tong_gia_min:
                    continue
                if tong_gia_max and kh.tong_gia_tri_mua_hang > tong_gia_max:
                   continue
                if so_lan_mua_min and kh.so_lan_mua_hang < so_lan_mua_min:
                   continue
            ket_qua.append(kh)
        return ket_qua

    def them_khach_hang(self, khach_hang):
        # Kiểm tra thông tin bắt buộc
        if not khach_hang.ma_khach_hang or not khach_hang.so_dien_thoai:
            print("\033[91mMã khách hàng và Số điện thoại là bắt buộc!\033[0m")
            return

        # Kiểm tra trùng lặp
        for kh in self.danh_sach_khach_hang:
            if kh.ma_khach_hang == khach_hang.ma_khach_hang:
               print("\033[91mMã khách hàng đã tồn tại!\033[0m")
               return
            if kh.so_dien_thoai == khach_hang.so_dien_thoai:
               print("\033[91mSố điện thoại đã tồn tại!\033[0m")
               return
            if kh.email == khach_hang.email:
               print("\033[91mEmail đã tồn tại!\033[0m")
               return

        self.danh_sach_khach_hang.append(khach_hang)
        self.ghi_file()
        ghi_log("Thêm", khach_hang)
        print("\033[92m✔ Thêm khách hàng thành công.\033[0m")

    def sua_thong_tin(self, ma_khach_hang, ten_moi=None, email_moi=None, sdt_moi=None):
        kh = next((k for k in self.danh_sach_khach_hang if k.ma_khach_hang == ma_khach_hang), None)
        if kh:
            if ten_moi:   kh.ten_khach_hang = ten_moi
            if email_moi: kh.email = email_moi
            if sdt_moi: kh.so_dien_thoai = sdt_moi
            self.ghi_file()
            ghi_log('Sửa', kh)
            print("\033[92m✔ Cập nhật thành công.\033[0m")
        else:
            print("\033[91mKhông tìm thấy khách hàng.\033[0m")

    def xoa_khach_hang(self, ma_khach_hang):
        kh = next((k for k in self.danh_sach_khach_hang if k.ma_khach_hang == ma_khach_hang), None)
        if kh:
            confirm = input("\033[91mBạn có chắc chắn muốn xoá khách hàng này? (y/n): \033[0m")
            if confirm.lower() == 'y':
                self.danh_sach_khach_hang.remove(kh)
                self.ghi_file()
                ghi_log('Xóa', kh)
                print("\033[92m✔ Xóa thành công.\033[0m")
        else:
            print("\033[91mKhông tìm thấy khách hàng.\033[0m")

    def cap_nhat_mua_hang(self, ma_khach_hang, so_lan_mua, gia_tri):
        kh = next((k for k in self.danh_sach_khach_hang if k.ma_khach_hang == ma_khach_hang), None)

        if kh is None:
           print("\033[91mKhông tìm thấy khách hàng.\033[0m")
           return

        if not isinstance(kh, CasualCustomer):
           print("\033[91mKhông áp dụng cho khách thân thiết.\033[0m")
           return

        if so_lan_mua < 0 or gia_tri < 0:
           print("\033[91mGiá trị mua hàng không hợp lệ.\033[0m")
           return

        # Cập nhật số lần và giá trị
        kh.so_lan_mua_hang += so_lan_mua
        kh.tong_gia_tri_mua_hang += gia_tri

        # Kiểm tra điều kiện nâng cấp
        if kh.tong_gia_tri_mua_hang > 2000000:
           diem_tich_luy = kh.tong_gia_tri_mua_hang // 10000  # Quy đổi 10.000 VND = 1 điểm
           self.danh_sach_khach_hang.remove(kh)
           kh_moi = LoyalCustomer(kh.ma_khach_hang, kh.ten_khach_hang, kh.so_dien_thoai, kh.email)
           kh_moi.diem_tich_luy = diem_tich_luy
           self.danh_sach_khach_hang.append(kh_moi)
           print(f"\033[94mKhách hàng đã trở thành khách thân thiết! (Điểm tích lũy: {diem_tich_luy})\033[0m")
           ghi_log('Chuyển sang khách thân thiết', kh_moi)
        else:
           ghi_log('Cập nhật mua hàng', kh)

        self.ghi_file()
        print("\033[92m✔ Cập nhật mua hàng thành công.\033[0m")

    def hien_thi_danh_sach(self, key_sort=None, reverse=False, loai=None):
        """Hiển thị danh sách khách hàng với tùy chọn lọc theo loại"""
        ds_hien_thi = self.danh_sach_khach_hang
        
        # Lọc theo loại nếu được chỉ định
        if loai == 'Loyal':
            ds_hien_thi = [kh for kh in self.danh_sach_khach_hang if isinstance(kh, LoyalCustomer)]
        elif loai == 'Casual':
            ds_hien_thi = [kh for kh in self.danh_sach_khach_hang if isinstance(kh, CasualCustomer)]
        
        # Sắp xếp nếu có chỉ định
        if key_sort:
            ds_hien_thi.sort(key=lambda x: getattr(x, key_sort, ''), reverse=reverse)

        header = f"{'Mã KH':<10} | {'Tên KH':<20} | {'SĐT':<12} | {'Email':<25} | {'Số lần':<8} | {'Tổng tiền':<10} | {'Loại':<7}"
        print("\033[96m" + header + "\033[0m")
        print("-" * len(header))
        for kh in ds_hien_thi:
            self.in_thong_tin(kh)

    def in_thong_tin(self, kh):
        if isinstance(kh, CasualCustomer):
            print(f"{kh.ma_khach_hang:<10} | {kh.ten_khach_hang:<20} | {kh.so_dien_thoai:<12} | {kh.email:<25} | {kh.so_lan_mua_hang:<8} | {kh.tong_gia_tri_mua_hang:<10,.0f} | Casual")
        else:
            diem = getattr(kh, 'diem_tich_luy', 0)
            print(f"{kh.ma_khach_hang:<10} | {kh.ten_khach_hang:<20} | {kh.so_dien_thoai:<12} | {kh.email:<25} | {'-':<8} | {'-':<10} | Loyal ({diem})")

    def thong_ke(self):
        """Thống kê số lượng và doanh thu theo loại khách hàng"""
        loyal = sum(1 for kh in self.danh_sach_khach_hang if isinstance(kh, LoyalCustomer))
        casual = sum(1 for kh in self.danh_sach_khach_hang if isinstance(kh, CasualCustomer))
        doanh_thu = sum(kh.tong_gia_tri_mua_hang for kh in self.danh_sach_khach_hang if isinstance(kh, CasualCustomer))

        # Tính trung bình cho từng loại khách hàng
        casual_customers = [kh for kh in self.danh_sach_khach_hang if isinstance(kh, CasualCustomer)]
        tb_casual = sum(kh.tong_gia_tri_mua_hang for kh in casual_customers) / len(casual_customers) if casual_customers else 0

        print("\n=== THỐNG KÊ KHÁCH HÀNG ===")
        print(f"Tổng số khách hàng: {loyal + casual}")
        print(f"- Khách hàng thân thiết: {loyal}")
        print(f"- Khách hàng vãng lai: {casual}")
        print(f"Tổng doanh thu: {doanh_thu:,.0f} VND")
        print(f"Trung bình giá trị mua hàng của khách vãng lai: {tb_casual:,.0f} VND")

        with open('thongke.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Loại', 'Số lượng', 'Doanh thu', 'Trung bình'])
            writer.writerow(['Loyal', loyal, '-', '-'])
            writer.writerow(['Casual', casual, doanh_thu, f"{tb_casual:.0f}"])
            writer.writerow(['Tổng', loyal + casual, doanh_thu, '-'])

        labels = ['Loyal', 'Casual']
        values = [loyal, casual]
        plt.figure(figsize=(10, 6))
        plt.bar(labels, values, color=['green', 'blue'])
        plt.title('Thống kê số lượng khách hàng')
        plt.xlabel('Loại khách hàng')
        plt.ylabel('Số lượng')
        plt.savefig('thongke.png')
        plt.show()

    def hien_thi_top_khach_hang(self, n=3):
        """Hiển thị n khách hàng có giá trị mua hàng cao nhất"""
        # Lọc các khách hàng vãng lai
        casual_customers = [kh for kh in self.danh_sach_khach_hang if isinstance(kh, CasualCustomer)]
        # Sắp xếp theo giá trị mua hàng giảm dần
        casual_customers.sort(key=lambda kh: kh.tong_gia_tri_mua_hang, reverse=True)
        # Lấy n khách hàng đầu tiên
        top_n = casual_customers[:n]
        
        print(f"\n=== TOP {n} KHÁCH HÀNG MUA HÀNG NHIỀU NHẤT ===")
        print(f"{'Mã KH':<10} | {'Tên KH':<20} | {'Số lần':<8} | {'Tổng giá trị':<15}")
        print("-" * 60)
        for kh in top_n:
            print(f"{kh.ma_khach_hang:<10} | {kh.ten_khach_hang:<20} | {kh.so_lan_mua_hang:<8} | {kh.tong_gia_tri_mua_hang:<15,.0f}")
        
        return top_n

    def thong_ke_khach_hang_than_thiet(self):
        """Thống kê khách hàng thân thiết để tặng quà Tết"""
        # Lọc khách hàng thân thiết có điểm tích lũy > 500
        kh_tiem_nang = [kh for kh in self.danh_sach_khach_hang 
                       if isinstance(kh, LoyalCustomer) and kh.diem_tich_luy > 500]
        
        # Sắp xếp theo điểm tích lũy giảm dần (vì không có trung bình giá trị cho LoyalCustomer)
        kh_tiem_nang.sort(key=lambda kh: kh.diem_tich_luy, reverse=True)
        top_10 = kh_tiem_nang[:10]

        print("\n🎁 DANH SÁCH KHÁCH HÀNG ĐƯỢC NHẬN QUÀ TẾT 🎁")
        print(f"{'Mã KH':<10} | {'Tên KH':<20} | {'SĐT':<12} | {'Email':<25} | {'Điểm tích lũy':<15}")
        print("-" * 85)
        for kh in top_10:
            print(f"{kh.ma_khach_hang:<10} | {kh.ten_khach_hang:<20} | {kh.so_dien_thoai:<12} | {kh.email:<25} | {kh.diem_tich_luy:<15}")

        with open("khach_hang_tet.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["MaKH", "TenKH", "SDT", "Email", "DiemTichLuy"])
            for kh in top_10:
                writer.writerow([
                    kh.ma_khach_hang,
                    kh.ten_khach_hang,
                    kh.so_dien_thoai,
                    kh.email,
                    kh.diem_tich_luy
                ])
        print("✅ Đã lưu danh sách vào file: khach_hang_tet.csv")
        return top_10