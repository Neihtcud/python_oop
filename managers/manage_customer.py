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

    def doc_file(self):
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['Loai'] == 'Loyal':
                       kh = LoyalCustomer(row['MaKH'], row['TenKH'], row['SDT'], row['Email'])
                    else:
                       so_lan_mua = int(row['SoLanMua']) if row['SoLanMua'] else 0
                       tong_gia_tri = float(row['TongGiaTri']) if row['TongGiaTri'] else 0
                       kh = CasualCustomer(row['MaKH'], row['TenKH'], row['SDT'], row['Email'], so_lan_mua, tong_gia_tri)
                    self.danh_sach_khach_hang.append(kh)
        except Exception as e:
              print(f"\033[91mLỗi đọc file: {e}\033[0m")         


    def backup_file(self):
        if os.path.exists(self.filename):
           timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
           backup_filename = f"backup_{timestamp}_{self.filename}"
           shutil.copy(self.filename, backup_filename)


    def ghi_file(self):
        self.backup_file()
        with open(self.filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['Loai', 'MaKH', 'TenKH', 'SDT', 'Email', 'SoLanMua', 'TongGiaTri']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for kh in self.danh_sach_khach_hang:
                if isinstance(kh, LoyalCustomer):
                    writer.writerow({'Loai': 'Loyal', 'MaKH': kh.ma_khach_hang, 'TenKH': kh.ten_khach_hang,
                                     'SDT': kh.so_dien_thoai, 'Email': kh.email})
                else:
                    writer.writerow({'Loai': 'Casual', 'MaKH': kh.ma_khach_hang, 'TenKH': kh.ten_khach_hang,
                                     'SDT': kh.so_dien_thoai, 'Email': kh.email,
                                     'SoLanMua': kh.so_lan_mua_hang, 'TongGiaTri': kh.tong_gia_tri_mua_hang})

    def tim_kiem(self, ma_kh=None, ten=None, sdt=None, email=None):
        ket_qua = []
        for kh in self.danh_sach_khach_hang:
            if (not ma_kh or ma_kh.lower() in kh.ma_khach_hang.lower()) and \
               (not ten or ten.lower() in kh.ten_khach_hang.lower()) and \
               (not sdt or sdt in kh.so_dien_thoai) and \
               (not email or email.lower() in kh.email.lower()):
                ket_qua.append(kh)
        return ket_qua
    def tim_kiem_nang_cao(self, loai=None, ten_chua=None, tong_gia_min=None, tong_gia_max=None, so_lan_mua_min=None):
        ket_qua = []
        for kh in self.danh_sach_khach_hang:
            if loai and not ((loai == 'Loyal' and isinstance(kh, LoyalCustomer)) or (loai == 'Casual' and isinstance(kh, CasualCustomer))):
                continue
            if ten_chua and ten_chua.lower() not in kh.ten_khach_hang.lower():
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
        if isinstance(kh, CasualCustomer):
            if kh is None:
               print("\033[91mKhông tìm thấy khách hàng.\033[0m")
               return

            if so_lan_mua < 0 or gia_tri < 0:
                print("\033[91mGiá trị mua hàng không hợp lệ.\033[0m")
                return

            kh.so_lan_mua_hang += so_lan_mua
            kh.tong_gia_tri_mua_hang += gia_tri

            if kh.tong_gia_tri_mua_hang > 2000000:
                self.danh_sach_khach_hang.remove(kh)
                kh_moi = LoyalCustomer(kh.ma_khach_hang, kh.ten_khach_hang, kh.so_dien_thoai, kh.email)
                self.danh_sach_khach_hang.append(kh_moi)
                print("\033[94mKhách hàng đã trở thành khách thân thiết!\033[0m")

            self.ghi_file()
            ghi_log('Cập nhật mua hàng', kh)
            print("\033[92m✔ Cập nhật mua hàng thành công.\033[0m")
        else:
            print("\033[91mKhông áp dụng cho khách thân thiết.\033[0m")

    def hien_thi_danh_sach(self, key_sort=None, reverse=False):
        if key_sort:
            self.danh_sach_khach_hang.sort(key=lambda x: getattr(x, key_sort, ''), reverse=reverse)

        header = f"{'Mã KH':<10} | {'Tên KH':<20} | {'SĐT':<12} | {'Email':<25} | {'Số lần':<8} | {'Tổng tiền':<10} | {'Loại':<7}"
        print("\033[96m" + header + "\033[0m")
        print("-" * len(header))
        for kh in self.danh_sach_khach_hang:
            self.in_thong_tin(kh)
    

    def in_thong_tin(self, kh):
        if isinstance(kh, CasualCustomer):
            print(f"{kh.ma_khach_hang:<10} | {kh.ten_khach_hang:<20} | {kh.so_dien_thoai:<12} | {kh.email:<25} | {kh.so_lan_mua_hang:<8} | {kh.tong_gia_tri_mua_hang:<10,.0f} | Casual")
        else:
            print(f"{kh.ma_khach_hang:<10} | {kh.ten_khach_hang:<20} | {kh.so_dien_thoai:<12} | {kh.email:<25} | {'-':<8} | {'-':<10} | Loyal")

    def thong_ke(self):
        loyal = sum(1 for kh in self.danh_sach_khach_hang if isinstance(kh, LoyalCustomer))
        casual = sum(1 for kh in self.danh_sach_khach_hang if isinstance(kh, CasualCustomer))
        doanh_thu = sum(kh.tong_gia_tri_mua_hang for kh in self.danh_sach_khach_hang if isinstance(kh, CasualCustomer))

        with open('thongke.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Loại', 'Số lượng', 'Doanh thu'])
            writer.writerow(['Loyal', loyal, '-'])
            writer.writerow(['Casual', casual, doanh_thu])

        labels = ['Loyal', 'Casual']
        values = [loyal, casual]
        plt.bar(labels, values, color=['green', 'blue'])
        plt.title('Thống kê số lượng khách hàng')
        plt.xlabel('Loại khách hàng')
        plt.ylabel('Số lượng')
        plt.show()

    def top_khach_hang(self, kieu='gia_tri'):
        casuals = [kh for kh in self.danh_sach_khach_hang if isinstance(kh, CasualCustomer)]
        if kieu == 'gia_tri':
            casuals.sort(key=lambda x: x.tong_gia_tri_mua_hang, reverse=True)
        else:
            casuals.sort(key=lambda x: x.so_lan_mua_hang, reverse=True)
        return casuals[:3]


