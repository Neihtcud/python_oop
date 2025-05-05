import csv
import os
import shutil
import datetime
import matplotlib.pyplot as plt
from models.customer import LoyalCustomer, CasualCustomer
from utils.logger import ghi_log
from utils.helpers import read_customers_from_csv, write_customers_to_csv
    # ... Các phương thức khác của lớp ...

class ManageCustomer:
    def __init__(self, filename='khachhang.csv'):
        self.danh_sach_khach_hang = []
        self.filename = filename
        self.doc_file()

    def backup_file(self):
        """Tạo bản sao lưu cho file dữ liệu"""
        if os.path.exists(self.filename):
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{self.filename}.backup_{timestamp}"
            try:
                shutil.copy(self.filename, backup_filename)
                print(f"\033[92mĐã tạo bản sao lưu: {backup_filename}\033[0m")
                return True
            except Exception as e:
                print(f"\033[91mLỗi sao lưu file: {e}\033[0m")
                return False
        return False

    def doc_file(self):
        """Đọc dữ liệu khách hàng từ file CSV"""
        if not os.path.exists(self.filename):
            # Tạo file mới nếu chưa tồn tại
            try:
                with open(self.filename, 'w', newline='', encoding='utf-8') as f:
                    fieldnames = ['Loai', 'MaKH', 'TenKH', 'SDT', 'Email', 'SoLanMua', 'TongGiaTri', 'DiemTichLuy']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                print(f"\033[92mĐã tạo file dữ liệu mới: {self.filename}\033[0m")
            except Exception as e:
                print(f"\033[91mLỗi tạo file mới: {e}\033[0m")
            return
        
        try:
            with open(self.filename, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        if row['Loai'] == 'Loyal':
                            kh = LoyalCustomer.from_dict(row)
                        else:
                            kh = CasualCustomer.from_dict(row)
                        self.danh_sach_khach_hang.append(kh)
                    except Exception as e:
                        print(f"\033[91mLỗi đọc dòng dữ liệu: {e}\033[0m")
                        continue
            print(f"\033[92mĐã đọc {len(self.danh_sach_khach_hang)} khách hàng từ file\033[0m")
        except Exception as e:
            print(f"\033[91mLỗi đọc file: {e}\033[0m")
            # Tạo bản sao lưu của file lỗi và tạo file mới
            if os.path.exists(self.filename):
                corrupt_file = f"{self.filename}.corrupt_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
                try:
                    shutil.copy(self.filename, corrupt_file)
                    print(f"\033[93mĐã lưu file lỗi tại: {corrupt_file}\033[0m")
                    # Tạo file mới
                    with open(self.filename, 'w', newline='', encoding='utf-8') as f:
                        fieldnames = ['Loai', 'MaKH', 'TenKH', 'SDT', 'Email', 'SoLanMua', 'TongGiaTri', 'DiemTichLuy']
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                    print(f"\033[92mĐã tạo file dữ liệu mới: {self.filename}\033[0m")
                except Exception as e2:
                    print(f"\033[91mKhông thể khôi phục file lỗi: {e2}\033[0m")

    def ghi_file(self):
        """Ghi danh sách khách hàng vào file CSV"""
        if not self.backup_file():
            confirm = input("\033[93mKhông thể sao lưu file. Bạn có muốn tiếp tục lưu? (y/n): \033[0m")
            if confirm.lower() != 'y':
                print("\033[93mĐã hủy thao tác lưu file.\033[0m")
                return False
                
        try:
            with open(self.filename, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['Loai', 'MaKH', 'TenKH', 'SDT', 'Email', 'SoLanMua', 'TongGiaTri', 'DiemTichLuy']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for kh in self.danh_sach_khach_hang:
                    writer.writerow(kh.to_dict())
            print("\033[92mLưu file thành công\033[0m")
            return True
        except Exception as e:
            print(f"\033[91mLỗi ghi file: {e}\033[0m")
            return False


    def la_ma_kh_hop_le(self, ma_kh):
        """Kiểm tra mã khách hàng có hợp lệ không"""
        if not ma_kh or not isinstance(ma_kh, str) or len(ma_kh) < 3:
            return False
        return True
        
    def la_sdt_hop_le(self, sdt):
        """Kiểm tra số điện thoại có hợp lệ không"""
        if not sdt or not isinstance(sdt, str):
            return False
        # Chỉ chấp nhận số điện thoại có 10 hoặc 11 chữ số
        return sdt.isdigit() and (len(sdt) == 10 or len(sdt) == 11)
        
    def la_email_hop_le(self, email):
        """Kiểm tra email có hợp lệ không"""
        if not email:  # Email có thể để trống
            return True
        if not isinstance(email, str):
            return False
        # Kiểm tra email có đúng định dạng không (kiểm tra đơn giản)
        return '@' in email and '.' in email.split('@')[-1]

    def tim_kiem(self, loai=None, ten_chua=None, tong_gia_min=None, tong_gia_max=None, 
                          so_lan_mua_min=None, ma_kh=None, sdt_chua=None, email_chua=None, 
                          diem_tich_luy_min=None):
        """Hàm tìm kiếm nâng cao với nhiều tiêu chí
        
        Args:
            loai (str): 'Loyal' hoặc 'Casual'
            ten_chua (str): Chuỗi có trong tên khách hàng
            tong_gia_min (float): Giá trị mua hàng tối thiểu
            tong_gia_max (float): Giá trị mua hàng tối đa
            so_lan_mua_min (int): Số lần mua hàng tối thiểu
            ma_kh (str): Mã khách hàng cần tìm
            sdt_chua (str): Chuỗi có trong số điện thoại
            email_chua (str): Chuỗi có trong email
            diem_tich_luy_min (int): Điểm tích lũy tối thiểu
            
        Returns:
            list: Danh sách khách hàng phù hợp với điều kiện
        """
        ket_qua = []
        for kh in self.danh_sach_khach_hang:
            # Kiểm tra loại khách hàng
            if loai and not ((loai == 'Loyal' and isinstance(kh, LoyalCustomer)) or (loai == 'Casual' and isinstance(kh, CasualCustomer))):
                continue
                
            # Kiểm tra thông tin cơ bản
            if ten_chua and ten_chua.lower() not in kh.ten_khach_hang.lower():
                continue
            if ma_kh and kh.ma_khach_hang != ma_kh:
                continue
            if sdt_chua and sdt_chua not in kh.so_dien_thoai:
                continue
            if email_chua and (not kh.email or email_chua.lower() not in kh.email.lower()):
                continue
            
            # Kiểm tra thông tin đặc biệt cho cả hai loại khách hàng
            if tong_gia_min is not None:
                if isinstance(kh, CasualCustomer) and kh.tong_gia_tri_mua_hang < tong_gia_min:
                    continue
                if isinstance(kh, LoyalCustomer) and kh.tong_gia_tri_mua_hang < tong_gia_min:
                    continue
                    
            if tong_gia_max is not None:
                if isinstance(kh, CasualCustomer) and kh.tong_gia_tri_mua_hang > tong_gia_max:
                    continue
                if isinstance(kh, LoyalCustomer) and kh.tong_gia_tri_mua_hang > tong_gia_max:
                    continue
                    
            if so_lan_mua_min is not None:
                if isinstance(kh, CasualCustomer) and kh.so_lan_mua_hang < so_lan_mua_min:
                    continue
                if isinstance(kh, LoyalCustomer) and kh.so_lan_mua_hang < so_lan_mua_min:
                    continue
            
            # Kiểm tra điểm tích lũy cho khách hàng thân thiết
            if isinstance(kh, LoyalCustomer) and diem_tich_luy_min is not None and kh.diem_tich_luy < diem_tich_luy_min:
                continue
                
            ket_qua.append(kh)
        return ket_qua

    def them_khach_hang(self, khach_hang):
        """Thêm khách hàng mới vào hệ thống
        
        Args:
            khach_hang: Đối tượng LoyalCustomer hoặc CasualCustomer
            
        Returns:
            bool: True nếu thêm thành công, False nếu thất bại
        """
        # Kiểm tra thông tin bắt buộc
        if not self.la_ma_kh_hop_le(khach_hang.ma_khach_hang):
            print("\033[91mMã khách hàng không hợp lệ!\033[0m")
            return False
            
        if not self.la_sdt_hop_le(khach_hang.so_dien_thoai):
            print("\033[91mSố điện thoại không hợp lệ!\033[0m")
            return False
            
        if not self.la_email_hop_le(khach_hang.email):
            print("\033[91mEmail không hợp lệ!\033[0m")
            return False

        # Kiểm tra trùng lặp
        for kh in self.danh_sach_khach_hang:
            if kh.ma_khach_hang == khach_hang.ma_khach_hang:
               print("\033[91mMã khách hàng đã tồn tại!\033[0m")
               return False
            if kh.so_dien_thoai == khach_hang.so_dien_thoai:
               print("\033[91mSố điện thoại đã tồn tại!\033[0m")
               return False
            if kh.email and kh.email == khach_hang.email and khach_hang.email:
               print("\033[91mEmail đã tồn tại!\033[0m")
               return False

        # Đảm bảo thiết lập giá trị mặc định cho số lần mua và tổng giá trị
        if isinstance(khach_hang, LoyalCustomer):
            if not hasattr(khach_hang, 'so_lan_mua_hang') or khach_hang.so_lan_mua_hang is None:
                khach_hang.so_lan_mua_hang = 0
            if not hasattr(khach_hang, 'tong_gia_tri_mua_hang') or khach_hang.tong_gia_tri_mua_hang is None:
                khach_hang.tong_gia_tri_mua_hang = 0

        self.danh_sach_khach_hang.append(khach_hang)
        self.ghi_file()
        ghi_log("Thêm", khach_hang)
        print("\033[92m✔ Thêm khách hàng thành công.\033[0m")
        return True

    def sua_thong_tin(self, ma_khach_hang, ten_moi=None, email_moi=None, sdt_moi=None):
        """Sửa thông tin khách hàng
        
        Args:
            ma_khach_hang (str): Mã khách hàng cần sửa
            ten_moi (str, optional): Tên mới của khách hàng
            email_moi (str, optional): Email mới của khách hàng
            sdt_moi (str, optional): Số điện thoại mới của khách hàng
            
        Returns:
            bool: True nếu sửa thành công, False nếu thất bại
        """
        # Kiểm tra mã khách hàng
        if not self.la_ma_kh_hop_le(ma_khach_hang):
            print("\033[91mMã khách hàng không hợp lệ!\033[0m")
            return False
            
        # Kiểm tra số điện thoại mới
        if sdt_moi and not self.la_sdt_hop_le(sdt_moi):
            print("\033[91mSố điện thoại mới không hợp lệ!\033[0m")
            return False
            
        # Kiểm tra email mới
        if email_moi and not self.la_email_hop_le(email_moi):
            print("\033[91mEmail mới không hợp lệ!\033[0m")
            return False
        
        kh = next((k for k in self.danh_sach_khach_hang if k.ma_khach_hang == ma_khach_hang), None)
        if kh:
            # Kiểm tra trùng lặp số điện thoại và email
            if sdt_moi and sdt_moi != kh.so_dien_thoai:
                if any(k.so_dien_thoai == sdt_moi for k in self.danh_sach_khach_hang if k.ma_khach_hang != ma_khach_hang):
                    print("\033[91mSố điện thoại đã tồn tại!\033[0m")
                    return False
                    
            if email_moi and email_moi != kh.email:
                if any(k.email == email_moi for k in self.danh_sach_khach_hang if k.ma_khach_hang != ma_khach_hang and k.email):
                    print("\033[91mEmail đã tồn tại!\033[0m")
                    return False
            
            # Cập nhật thông tin
            if ten_moi:   kh.ten_khach_hang = ten_moi
            if email_moi: kh.email = email_moi
            if sdt_moi:   kh.so_dien_thoai = sdt_moi
            
            self.ghi_file()
            ghi_log('Sửa', kh)
            print("\033[92m✔ Cập nhật thành công.\033[0m")
            return True
        else:
            print("\033[91mKhông tìm thấy khách hàng.\033[0m")
            return False

    def xoa_khach_hang(self, ma_khach_hang):
        """Xoá khách hàng khỏi hệ thống
        
        Args:
            ma_khach_hang (str): Mã khách hàng cần xoá
            
        Returns:
            bool: True nếu xoá thành công, False nếu thất bại
        """
        # Kiểm tra mã khách hàng
        if not self.la_ma_kh_hop_le(ma_khach_hang):
            print("\033[91mMã khách hàng không hợp lệ!\033[0m")
            return False
            
        kh = next((k for k in self.danh_sach_khach_hang if k.ma_khach_hang == ma_khach_hang), None)
        if kh:
            confirm = input("\033[91mBạn có chắc chắn muốn xoá khách hàng này? (y/n): \033[0m")
            if confirm.lower() == 'y':
                self.danh_sach_khach_hang.remove(kh)
                self.ghi_file()
                ghi_log('Xóa', kh)
                print("\033[92m✔ Xóa thành công.\033[0m")
                return True
            else:
                print("\033[93mĐã hủy xóa khách hàng.\033[0m")
                return False
        else:
            print("\033[91mKhông tìm thấy khách hàng.\033[0m")
            return False

    def cap_nhat_mua_hang(self, ma_khach_hang, so_lan_mua, gia_tri):
        """Cập nhật thông tin mua hàng cho cả khách hàng thân thiết và vãng lai
        
        Args:
            ma_khach_hang (str): Mã khách hàng
            so_lan_mua (int): Số lần mua hàng cần cập nhật
            gia_tri (float): Giá trị mua hàng cần cập nhật
            
        Returns:
            bool: True nếu cập nhật thành công, False nếu thất bại
        """
        # Kiểm tra mã khách hàng
        if not self.la_ma_kh_hop_le(ma_khach_hang):
            print("\033[91mMã khách hàng không hợp lệ!\033[0m")
            return False
            
        # Kiểm tra giá trị đầu vào
        try:
            so_lan_mua = int(so_lan_mua)
            gia_tri = float(gia_tri)
        except ValueError:
            print("\033[91mSố lần mua hoặc giá trị không hợp lệ!\033[0m")
            return False
            
        if so_lan_mua < 0 or gia_tri < 0:
            print("\033[91mGiá trị mua hàng không hợp lệ.\033[0m")
            return False

        kh = next((k for k in self.danh_sach_khach_hang if k.ma_khach_hang == ma_khach_hang), None)

        if kh is None:
           print("\033[91mKhông tìm thấy khách hàng.\033[0m")
           return False

        # Xử lý khách hàng thân thiết
        if isinstance(kh, LoyalCustomer):
            # Đảm bảo khách hàng thân thiết có thuộc tính theo dõi số lần mua và tổng giá trị
            if not hasattr(kh, 'so_lan_mua_hang'):
                kh.so_lan_mua_hang = 0
            if not hasattr(kh, 'tong_gia_tri_mua_hang'):
                kh.tong_gia_tri_mua_hang = 0
                
            # Cập nhật số lần mua và tổng giá trị
            kh.so_lan_mua_hang += so_lan_mua
            kh.tong_gia_tri_mua_hang += gia_tri
            
            # Quy đổi điểm tích lũy: 10.000 VND = 1 điểm
            diem_moi = int(gia_tri // 10000)
            kh.diem_tich_luy += diem_moi
            
            print(f"\033[94m✨ Cập nhật thành công:\033[0m")
            print(f"\033[94m💰 +{diem_moi} điểm tích lũy (tổng: {kh.diem_tich_luy} điểm)\033[0m")
            print(f"\033[94m📊 Số lần mua hàng: {kh.so_lan_mua_hang} lần\033[0m")
            print(f"\033[94m💵 Tổng giá trị mua hàng: {kh.tong_gia_tri_mua_hang:,.0f} VND\033[0m")
            
            ghi_log('Cập nhật mua hàng và điểm tích lũy', kh)
            self.ghi_file()
            return True

        # Xử lý khách hàng vãng lai
        # Cập nhật số lần và giá trị
        kh.so_lan_mua_hang += so_lan_mua
        kh.tong_gia_tri_mua_hang += gia_tri

        # Kiểm tra điều kiện nâng cấp: tổng giá trị > 2.000.000 VND và số lần mua ≥ 3
        if kh.tong_gia_tri_mua_hang > 2000000 and kh.so_lan_mua_hang >= 3:
           # Quy đổi điểm tích lũy theo tỷ lệ 10.000 VND = 1 điểm
           diem_tich_luy = int(kh.tong_gia_tri_mua_hang // 10000)
           
           # Xóa khách hàng vãng lai
           self.danh_sach_khach_hang.remove(kh)
           
           # Tạo khách hàng thân thiết mới với cùng thông tin cơ bản
           kh_moi = LoyalCustomer(kh.ma_khach_hang, kh.ten_khach_hang, kh.so_dien_thoai, kh.email, diem_tich_luy)
           
           # Thêm thông tin về số lần mua và tổng giá trị mua hàng
           kh_moi.so_lan_mua_hang = kh.so_lan_mua_hang
           kh_moi.tong_gia_tri_mua_hang = kh.tong_gia_tri_mua_hang
           
           self.danh_sach_khach_hang.append(kh_moi)
           
           print(f"\033[94m✨ Khách hàng đã được nâng cấp thành khách hàng thân thiết!\033[0m")
           print(f"\033[94m🎁 Điểm tích lũy khởi đầu: {diem_tich_luy} điểm\033[0m")
           ghi_log('Chuyển sang khách thân thiết', kh_moi)
        else:
           # Chưa đủ điều kiện nâng cấp
           print(f"\033[93mĐiều kiện nâng cấp: Tổng giá trị > 2.000.000 VND và số lần mua ≥ 3\033[0m")
           if kh.tong_gia_tri_mua_hang <= 2000000:
               print(f"\033[93mKhách hàng cần mua thêm {2000000 - kh.tong_gia_tri_mua_hang:,.0f} VND để đủ điều kiện.\033[0m")
           if kh.so_lan_mua_hang < 3:
               print(f"\033[93mKhách hàng cần mua thêm {3 - kh.so_lan_mua_hang} lần để đủ điều kiện.\033[0m")
           ghi_log('Cập nhật mua hàng', kh)

        self.ghi_file()
        print("\033[92m✔ Cập nhật mua hàng thành công.\033[0m")
        return True

    def cap_nhat_diem_tich_luy(self, ma_khach_hang, diem_moi):
        """Cập nhật trực tiếp điểm tích lũy cho khách hàng thân thiết
        
        Args:
            ma_khach_hang (str): Mã khách hàng
            diem_moi (int): Điểm tích lũy mới
            
        Returns:
            bool: True nếu cập nhật thành công, False nếu thất bại
        """
        # Kiểm tra mã khách hàng
        if not self.la_ma_kh_hop_le(ma_khach_hang):
            print("\033[91mMã khách hàng không hợp lệ!\033[0m")
            return False
            
        kh = next((k for k in self.danh_sach_khach_hang if k.ma_khach_hang == ma_khach_hang), None)
        
        if kh is None:
            print("\033[91mKhông tìm thấy khách hàng.\033[0m")
            return False
            
        if not isinstance(kh, LoyalCustomer):
            print("\033[91mKhông áp dụng cho khách vãng lai.\033[0m")
            return False
            
        try:
            diem_moi = int(diem_moi)
            if diem_moi < 0:
                print("\033[91mĐiểm tích lũy không thể là số âm.\033[0m")
                return False
                
            kh.diem_tich_luy = diem_moi
            self.ghi_file()
            ghi_log('Cập nhật điểm tích lũy', kh)
            print(f"\033[92m✔ Cập nhật điểm tích lũy thành công: {diem_moi} điểm\033[0m")
            return True
        except ValueError:
            print("\033[91mĐiểm tích lũy phải là số nguyên.\033[0m")
            return False

    
    def cap_nhat_diem_tich_luy(self, ma_khach_hang, diem_moi):
        """Cập nhật trực tiếp điểm tích lũy cho khách hàng thân thiết
        
        Args:
            ma_khach_hang (str): Mã khách hàng
            diem_moi (int): Điểm tích lũy mới
            
        Returns:
            bool: True nếu cập nhật thành công, False nếu thất bại
        """
        # Kiểm tra mã khách hàng
        if not self.la_ma_kh_hop_le(ma_khach_hang):
            print("\033[91mMã khách hàng không hợp lệ!\033[0m")
            return False
            
        kh = next((k for k in self.danh_sach_khach_hang if k.ma_khach_hang == ma_khach_hang), None)
        
        if kh is None:
            print("\033[91mKhông tìm thấy khách hàng.\033[0m")
            return False
            
        if not isinstance(kh, LoyalCustomer):
            print("\033[91mKhông áp dụng cho khách vãng lai.\033[0m")
            return False
            
        try:
            diem_moi = int(diem_moi)
            if diem_moi < 0:
                print("\033[91mĐiểm tích lũy không thể là số âm.\033[0m")
                return False
                
            kh.diem_tich_luy = diem_moi
            self.ghi_file()
            ghi_log('Cập nhật điểm tích lũy', kh)
            print(f"\033[92m✔ Cập nhật điểm tích lũy thành công: {diem_moi} điểm\033[0m")
            return True
        except ValueError:
            print("\033[91mĐiểm tích lũy phải là số nguyên.\033[0m")
            return False

    def them_diem_tich_luy(self, ma_khach_hang, diem_them):
        """Thêm điểm tích lũy cho khách hàng thân thiết
        
        Args:
            ma_khach_hang (str): Mã khách hàng
            diem_them (int): Số điểm thêm vào
            
        Returns:
            bool: True nếu thêm điểm thành công, False nếu thất bại
        """
        # Kiểm tra mã khách hàng
        if not self.la_ma_kh_hop_le(ma_khach_hang):
            print("\033[91mMã khách hàng không hợp lệ!\033[0m")
            return False
            
        kh = next((k for k in self.danh_sach_khach_hang if k.ma_khach_hang == ma_khach_hang), None)
        
        if kh is None:
            print("\033[91mKhông tìm thấy khách hàng.\033[0m")
            return False
            
        if not isinstance(kh, LoyalCustomer):
            print("\033[91mKhông áp dụng cho khách vãng lai.\033[0m")
            return False
            
        try:
            
            diem_them = int(diem_them)
            kh.diem_tich_luy += diem_them
            
            # Đảm bảo điểm tích lũy không âm
            if kh.diem_tich_luy < 0:
                kh.diem_tich_luy = 0
                print("\033[93mCảnh báo: Điểm tích lũy đã giảm xuống 0.\033[0m")
                
            self.ghi_file()
            ghi_log(f'{"Thêm" if diem_them > 0 else "Trừ"} điểm tích lũy', kh)
            print(f"\033[92m✔ {diem_them:+d} điểm tích lũy. Tổng điểm hiện tại: {kh.diem_tich_luy}\033[0m")
        except ValueError:
            print("\033[91mĐiểm tích lũy phải là số nguyên.\033[0m")
            
    def giam_diem_tich_luy(self, ma_khach_hang, diem_giam):
        """Giảm điểm tích lũy cho khách hàng thân thiết (wrapper cho them_diem_tich_luy)"""
        try:
            diem_giam = int(diem_giam)
            if diem_giam < 0:
                print("\033[91mVui lòng nhập số dương để giảm điểm.\033[0m")
                return
            self.them_diem_tich_luy(ma_khach_hang, -diem_giam)
        except ValueError:
            print("\033[91mĐiểm giảm phải là số nguyên.\033[0m")

    def hien_thi_danh_sach(self, key_sort=None, reverse=False, loai=None):
        
        """Hiển thị danh sách khách hàng với tùy chọn lọc theo loại
    
        Args:
            key_sort (str): Trường để sắp xếp
            reverse (bool): True để sắp xếp giảm dần, False để sắp xếp tăng dần
            loai (str): 'Loyal' cho khách hàng thân thiết, 'Casual' cho khách hàng vãng lai, None cho tất cả
        """
        ds_hien_thi = self.danh_sach_khach_hang.copy()
    
        # Lọc theo loại nếu được chỉ định
        if loai == 'Loyal':
            ds_hien_thi = [kh for kh in ds_hien_thi if isinstance(kh, LoyalCustomer)]
        elif loai == 'Casual':
            ds_hien_thi = [kh for kh in ds_hien_thi if isinstance(kh, CasualCustomer)]
    
        # Kiểm tra xem danh sách có rỗng không
        if not ds_hien_thi:
            print("\033[93mKhông có khách hàng nào phù hợp với điều kiện.\033[0m")
            return
    
        # Sắp xếp dữ liệu
        if key_sort:
            if key_sort == 'diem_tich_luy' and loai != 'Casual':
                # Chỉ áp dụng sắp xếp theo điểm tích lũy cho khách hàng thân thiết
                # hoặc cho danh sách tổng hợp (sắp xếp khách thân thiết trước)
                ds_loyal = [kh for kh in ds_hien_thi if isinstance(kh, LoyalCustomer)]
                ds_casual = [kh for kh in ds_hien_thi if isinstance(kh, CasualCustomer)]
                ds_loyal.sort(key=lambda x: x.diem_tich_luy, reverse=reverse)
                ds_hien_thi = ds_loyal + ds_casual if not reverse else ds_loyal + ds_casual
            elif key_sort == 'tong_gia_tri_mua_hang' and loai != 'Loyal':
                # Chỉ áp dụng sắp xếp theo tổng giá trị cho khách hàng vãng lai
                # hoặc cho danh sách tổng hợp (sắp xếp khách vãng lai trước)
                ds_loyal = [kh for kh in ds_hien_thi if isinstance(kh, LoyalCustomer)]
                ds_casual = [kh for kh in ds_hien_thi if isinstance(kh, CasualCustomer)]
                ds_casual.sort(key=lambda x: x.tong_gia_tri_mua_hang, reverse=reverse)
                ds_hien_thi = ds_casual + ds_loyal if not reverse else ds_casual + ds_loyal
            else:
                # Sắp xếp theo các trường thông thường (chung cho cả hai loại)
                try:
                   ds_hien_thi.sort(key=lambda x: getattr(x, key_sort, ''), reverse=reverse)
                except AttributeError:
                   print(f"\033[93mCảnh báo: Trường '{key_sort}' không tồn tại ở một số khách hàng. Sắp xếp có thể không chính xác.\033[0m")

            # Hiển thị tiêu đề
            loai_title = "THÂN THIẾT" if loai == 'Loyal' else "VÃNG LAI" if loai == 'Casual' else "TẤT CẢ"
            print(f"\n📋 DANH SÁCH KHÁCH HÀNG {loai_title}")
    
            # Tiêu đề cột tùy theo loại khách hàng
            if loai == 'Loyal':
               header = f"{'Mã KH':<10} | {'Tên KH':<20} | {'SĐT':<12} | {'Email':<25} | {'Điểm tích lũy':<15}"
               print("\033[96m" + header + "\033[0m")
               print("-" * len(header))
        
               for kh in ds_hien_thi:
                  print(f"{kh.ma_khach_hang:<10} | {kh.ten_khach_hang:<20} | {kh.so_dien_thoai:<12} | {kh.email:<25} | {kh.diem_tich_luy:<15}")
    
            elif loai == 'Casual':
               header = f"{'Mã KH':<10} | {'Tên KH':<20} | {'SĐT':<12} | {'Email':<25} | {'Số lần mua':<12} | {'Tổng giá trị':<15}"
               print("\033[96m" + header + "\033[0m")
               print("-" * len(header))
        
               for kh in ds_hien_thi:
                 print(f"{kh.ma_khach_hang:<10} | {kh.ten_khach_hang:<20} | {kh.so_dien_thoai:<12} | {kh.email:<25} | {kh.so_lan_mua_hang:<12} | {kh.tong_gia_tri_mua_hang:15,.0f}")
    
            else:
               # Hiển thị danh sách kết hợp
               header = f"{'Mã KH':<10} | {'Tên KH':<20} | {'SĐT':<12} | {'Email':<25} | {'Loại KH':<10} | {'Chi tiết':<20}"
               print("\033[96m" + header + "\033[0m")
               print("-" * len(header))
        
               for kh in ds_hien_thi:
                    if isinstance(kh, LoyalCustomer):
                      chi_tiet = f"Điểm TL: {kh.diem_tich_luy}"
                      loai_kh = "Thân thiết"
                    else:
                      chi_tiet = f"SL: {kh.so_lan_mua_hang}, GT: {kh.tong_gia_tri_mua_hang:,.0f}"
                      loai_kh = "Vãng lai"
            
                    print(f"{kh.ma_khach_hang:<10} | {kh.ten_khach_hang:<20} | {kh.so_dien_thoai:<12} | {kh.email:<25} | {loai_kh:<10} | {chi_tiet:<20}")
    
            print(f"\nTổng số: {len(ds_hien_thi)} khách hàng")
    def in_thong_tin(self, kh):
        """Hiển thị thông tin của một khách hàng
    
        Args:
           kh: Đối tượng khách hàng (LoyalCustomer hoặc CasualCustomer)
        """
        if isinstance(kh, CasualCustomer):
           print(f"{kh.ma_khach_hang:<10} | {kh.ten_khach_hang:<20} | {kh.so_dien_thoai:<12} | {kh.email:<25} | Vãng lai | SL: {kh.so_lan_mua_hang}, GT: {kh.tong_gia_tri_mua_hang:,.0f} VND")
        else:
           print(f"{kh.ma_khach_hang:<10} | {kh.ten_khach_hang:<20} | {kh.so_dien_thoai:<12} | {kh.email:<25} | Thân thiết | Điểm TL: {kh.diem_tich_luy}")        
    def thong_ke(self):
        """Thống kê số lượng và doanh thu theo loại khách hàng"""
        # Đếm số lượng khách hàng theo loại
        loyal_customers = [kh for kh in self.danh_sach_khach_hang if isinstance(kh, LoyalCustomer)]
        casual_customers = [kh for kh in self.danh_sach_khach_hang if isinstance(kh, CasualCustomer)]
        loyal = len(loyal_customers)
        casual = len(casual_customers)
        
        # Tính tổng doanh thu và trung bình
        doanh_thu = sum(kh.tong_gia_tri_mua_hang for kh in casual_customers)
        tb_casual = doanh_thu / casual if casual else 0
        
        # Tính trung bình điểm tích lũy cho khách thân thiết
        tb_diem = sum(kh.diem_tich_luy for kh in loyal_customers) / loyal if loyal else 0

        print("\n=== THỐNG KÊ KHÁCH HÀNG ===")
        print(f"Tổng số khách hàng: {loyal + casual}")
        print(f"- Khách hàng thân thiết: {loyal}")
        print(f"- Khách hàng vãng lai: {casual}")
        print(f"Tổng doanh thu: {doanh_thu:,.0f} VND")
        print(f"Trung bình giá trị mua hàng của khách vãng lai: {tb_casual:,.0f} VND")
        print(f"Trung bình điểm tích lũy của khách thân thiết: {tb_diem:,.0f} điểm")

        # Lưu thống kê ra file CSV
        with open('thongke.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Loại', 'Số lượng', 'Doanh thu', 'Trung bình'])
            writer.writerow(['Loyal', loyal, '-', f"{tb_diem:.0f} điểm"])
            writer.writerow(['Casual', casual, doanh_thu, f"{tb_casual:.0f} VND"])
            writer.writerow(['Tổng', loyal + casual, doanh_thu, '-'])
        print("✅ Đã lưu thống kê vào file: thongke.csv")

        # Vẽ biểu đồ phân bố khách hàng
        labels = ['Khách thân thiết', 'Khách vãng lai']
        values = [loyal, casual]
        plt.figure(figsize=(10, 6))
        plt.bar(labels, values, color=['green', 'blue'])
        plt.title('Thống kê số lượng khách hàng')
        plt.xlabel('Loại khách hàng')
        plt.ylabel('Số lượng')
        plt.savefig('thongke_soluong.png')
        
        # Vẽ biểu đồ doanh thu nếu có khách hàng vãng lai
        if casual > 0:
            # Tính doanh thu trung bình theo từng khách hàng vãng lai
            ten_khach_hang = [kh.ten_khach_hang for kh in casual_customers]
            doanh_thu_values = [kh.tong_gia_tri_mua_hang for kh in casual_customers]
            
            plt.figure(figsize=(12, 6))
            plt.bar(ten_khach_hang, doanh_thu_values, color='orange')
            plt.title('Doanh thu theo khách hàng vãng lai')
            plt.xlabel('Khách hàng')
            plt.ylabel('Doanh thu (VND)')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig('thongke_doanhthu.png')
        
        plt.show()

    def hien_thi_top_khach_hang(self, n=3):
        """Hiển thị n khách hàng có giá trị mua hàng cao nhất"""
        # Lọc các khách hàng vãng lai
        casual_customers = [kh for kh in self.danh_sach_khach_hang if isinstance(kh, CasualCustomer)]
        
        if not casual_customers:
            print("\033[93mKhông có khách hàng vãng lai nào để hiển thị.\033[0m")
            return []
            
        # Sắp xếp theo giá trị mua hàng giảm dần
        casual_customers.sort(key=lambda kh: kh.tong_gia_tri_mua_hang, reverse=True)
        
        # Lấy n khách hàng đầu tiên
        top_n = casual_customers[:n]
        
        print(f"\n=== TOP {n} KHÁCH HÀNG MUA HÀNG NHIỀU NHẤT ===")
        if not top_n:
            print("\033[93mKhông có đủ khách hàng để hiển thị.\033[0m")
            return []
            
        print(f"{'Mã KH':<10} | {'Tên KH':<20} | {'Số lần':<8} | {'Tổng giá trị':<15}")
        print("-" * 60)
        for i, kh in enumerate(top_n, 1):
            print(f"{i}. {kh.ma_khach_hang:<8} | {kh.ten_khach_hang:<20} | {kh.so_lan_mua_hang:<8} | {kh.tong_gia_tri_mua_hang:<15,.0f}")
        
        return top_n

    def thong_ke_khach_hang_than_thiet(self):
        """Thống kê khách hàng thân thiết để tặng quà Tết"""
        # Lọc khách hàng thân thiết có điểm tích lũy > 500
        kh_tiem_nang = [kh for kh in self.danh_sach_khach_hang 
                       if isinstance(kh, LoyalCustomer) and kh.diem_tich_luy > 500]
        
        if not kh_tiem_nang:
            print("\033[93mKhông có khách hàng thân thiết nào có đủ điểm (>500) để nhận quà Tết.\033[0m")
            return []
            
        # Sắp xếp theo điểm tích lũy giảm dần
        kh_tiem_nang.sort(key=lambda kh: kh.diem_tich_luy, reverse=True)
        
        # Giới hạn top 10 khách hàng
        top_10 = kh_tiem_nang[:10]

        print("\n🎁 DANH SÁCH KHÁCH HÀNG ĐƯỢC NHẬN QUÀ TẾT 🎁")
        print(f"{'Mã KH':<10} | {'Tên KH':<20} | {'SĐT':<12} | {'Email':<25} | {'Điểm tích lũy':<15}")
        print("-" * 85)
        
        for i, kh in enumerate(top_10, 1):
            print(f"{i}. {kh.ma_khach_hang:<8} | {kh.ten_khach_hang:<20} | {kh.so_dien_thoai:<12} | {kh.email:<25} | {kh.diem_tich_luy:<15}")

        # Lưu danh sách ra file CSV
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