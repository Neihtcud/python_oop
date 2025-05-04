import unittest
import os
import sys
import tempfile
import shutil
import csv

# Thêm thư mục gốc vào đường dẫn để import các module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.customer import Customer, LoyalCustomer, CasualCustomer  
from managers.manage_customer import ManageCustomer
from utils.helpers import kiem_tra_email

class TestCustomer(unittest.TestCase):
    def setUp(self):
        """
        Thiết lập trước mỗi test case
        """
        # Tạo file tạm để test
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, "test_khachhang.csv")
        
        # Tạo đối tượng quản lý với file tạm
        self.manager = ManageCustomer(self.filename)
        
        # Tạo các đối tượng khách hàng mẫu
        self.loyal_customer = LoyalCustomer("L001", "Nguyễn Văn A", "0912345678", "a@example.com", 500)
        self.casual_customer = CasualCustomer("C001", "Trần Thị B", "0987654321", "b@example.com", 5, 1500000)
        
    def tearDown(self):
        """
        Dọn dẹp sau mỗi test case
        """
        # Xóa thư mục tạm sau khi test
        shutil.rmtree(self.temp_dir)

    def test_customer_creation(self):
        """
        Test case 1: Kiểm tra khởi tạo đối tượng Customer
        """
        customer = Customer("001", "Test Name", "0123456789", "test@example.com")
        self.assertEqual(customer.ma_khach_hang, "001")
        self.assertEqual(customer.ten_khach_hang, "Test Name")
        self.assertEqual(customer.so_dien_thoai, "0123456789")
        self.assertEqual(customer.email, "test@example.com")

    def test_loyal_customer_creation(self):
        """
        Test case 2: Kiểm tra khởi tạo đối tượng LoyalCustomer
        """
        self.assertEqual(self.loyal_customer.ma_khach_hang, "L001")
        self.assertEqual(self.loyal_customer.ten_khach_hang, "Nguyễn Văn A")
        self.assertEqual(self.loyal_customer.diem_tich_luy, 500)

    def test_casual_customer_creation(self):
        """
        Test case 3: Kiểm tra khởi tạo đối tượng CasualCustomer
        """
        self.assertEqual(self.casual_customer.ma_khach_hang, "C001")
        self.assertEqual(self.casual_customer.tong_gia_tri_mua_hang, 1500000)
        self.assertEqual(self.casual_customer.so_lan_mua_hang, 5)

    def test_tinh_trung_binh_gia_tri(self):
        """
        Test case 4: Kiểm tra phương thức tính trung bình giá trị đơn hàng
        """
        # 1500000 / 5 = 300000
        self.assertEqual(self.casual_customer.tinh_trung_binh_gia_tri(), 300000)
        
        # Trường hợp so_lan_mua_hang = 0
        customer = CasualCustomer("C002", "Test", "0123456789", "test@example.com", 0, 0)
        self.assertEqual(customer.tinh_trung_binh_gia_tri(), 0)

    def test_them_khach_hang(self):
        """
        Test case 5: Kiểm tra thêm khách hàng
        """
        # Thêm khách hàng vào manager
        self.manager.them_khach_hang(self.loyal_customer)
        self.assertEqual(len(self.manager.danh_sach_khach_hang), 1)
        
        # Kiểm tra khách hàng đã được thêm đúng
        added_customer = self.manager.danh_sach_khach_hang[0]
        self.assertEqual(added_customer.ma_khach_hang, "L001")
        self.assertEqual(added_customer.ten_khach_hang, "Nguyễn Văn A")

    def test_them_khach_hang_trung_ma(self):
        """
        Test case 6: Kiểm tra không cho phép thêm khách hàng trùng mã
        """
        # Thêm khách hàng lần đầu
        self.manager.them_khach_hang(self.loyal_customer)
        self.assertEqual(len(self.manager.danh_sach_khach_hang), 1)
        
        # Thêm khách hàng với mã trùng
        duplicate = LoyalCustomer("L001", "Tên Khác", "0123456789", "other@example.com")
        self.manager.them_khach_hang(duplicate)
        # Số lượng khách hàng không tăng
        self.assertEqual(len(self.manager.danh_sach_khach_hang), 1)

    def test_them_khach_hang_trung_sdt(self):
        """
        Test case 7: Kiểm tra không cho phép thêm khách hàng trùng số điện thoại
        """
        # Thêm khách hàng lần đầu
        self.manager.them_khach_hang(self.loyal_customer)
        self.assertEqual(len(self.manager.danh_sach_khach_hang), 1)
        
        # Thêm khách hàng với số điện thoại trùng
        duplicate = LoyalCustomer("L002", "Tên Khác", "0912345678", "other@example.com")
        self.manager.them_khach_hang(duplicate)
        # Số lượng khách hàng không tăng
        self.assertEqual(len(self.manager.danh_sach_khach_hang), 1)

    def test_them_khach_hang_trung_email(self):
        """
        Test case 8: Kiểm tra không cho phép thêm khách hàng trùng email
        """
        # Thêm khách hàng lần đầu
        self.manager.them_khach_hang(self.loyal_customer)
        self.assertEqual(len(self.manager.danh_sach_khach_hang), 1)
        
        # Thêm khách hàng với email trùng
        duplicate = LoyalCustomer("L002", "Tên Khác", "0123456789", "a@example.com")
        self.manager.them_khach_hang(duplicate)
        # Số lượng khách hàng không tăng
        self.assertEqual(len(self.manager.danh_sach_khach_hang), 1)

    def test_sua_thong_tin(self):
        """
        Test case 9: Kiểm tra sửa thông tin khách hàng
        """
        # Thêm khách hàng
        self.manager.them_khach_hang(self.loyal_customer)
        
        # Sửa thông tin
        self.manager.sua_thong_tin(
            "L001", 
            ten_moi="Nguyễn Văn A Mới", 
            email_moi="new_a@example.com", 
            sdt_moi="0912345679"
        )
        
        # Kiểm tra thông tin sau khi sửa
        updated = self.manager.tim_kiem_nang_cao(ma_kh="L001")[0]
        self.assertEqual(updated.ten_khach_hang, "Nguyễn Văn A Mới")
        self.assertEqual(updated.email, "new_a@example.com")
        self.assertEqual(updated.so_dien_thoai, "0912345679")

    def test_xoa_khach_hang(self):
        """
        Test case 10: Kiểm tra xóa khách hàng
        """
        # Thêm khách hàng
        self.manager.them_khach_hang(self.loyal_customer)
        self.manager.them_khach_hang(self.casual_customer)
        self.assertEqual(len(self.manager.danh_sach_khach_hang), 2)
        
        # Xóa khách hàng (giả lập người dùng xác nhận bằng input 'y')
        with unittest.mock.patch('builtins.input', return_value='y'):
            self.manager.xoa_khach_hang("L001")
        
        # Kiểm tra sau khi xóa
        self.assertEqual(len(self.manager.danh_sach_khach_hang), 1)
        self.assertEqual(self.manager.danh_sach_khach_hang[0].ma_khach_hang, "C001")

    def test_cap_nhat_mua_hang(self):
        """
        Test case 11: Kiểm tra cập nhật thông tin mua hàng
        """
        # Thêm khách hàng casual
        self.manager.them_khach_hang(self.casual_customer)
        
        # Cập nhật mua hàng
        self.manager.cap_nhat_mua_hang("C001", 3, 500000)
        
        # Kiểm tra sau khi cập nhật
        updated = self.manager.tim_kiem_nang_cao(ma_kh="C001")[0]
        self.assertEqual(updated.so_lan_mua_hang, 8)  # Ban đầu 5, thêm 3
        self.assertEqual(updated.tong_gia_tri_mua_hang, 2000000)  # Ban đầu 1500000, thêm 500000

    def test_cap_nhat_mua_hang_nang_cap_thanh_loyal(self):
        """
        Test case 12: Kiểm tra nâng cấp khách hàng thành thân thiết
        """
        # Thêm khách hàng casual
        self.manager.them_khach_hang(self.casual_customer)
        
        # Cập nhật mua hàng đủ điều kiện nâng cấp (> 2 triệu)
        self.manager.cap_nhat_mua_hang("C001", 3, 600000)  # Tổng: 1500000 + 600000 = 2100000
        
        # Kiểm tra sau khi cập nhật
        # Không tìm thấy casual customer nữa
        casual_results = self.manager.tim_kiem_nang_cao(ma_kh="C001", loai="Casual")
        self.assertEqual(len(casual_results), 0)
        
        # Tìm thấy loyal customer mới
        loyal_results = self.manager.tim_kiem_nang_cao(ma_kh="C001", loai="Loyal")
        self.assertEqual(len(loyal_results), 1)
        
        # Kiểm tra điểm tích lũy (2100000 / 10000 = 210 điểm)
        self.assertEqual(loyal_results[0].diem_tich_luy, 210)

    def test_tim_kiem_nang_cao_theo_loai(self):
        """
        Test case 13: Kiểm tra tìm kiếm nâng cao theo loại khách hàng
        """
        # Thêm cả hai loại khách hàng
        self.manager.them_khach_hang(self.loyal_customer)
        self.manager.them_khach_hang(self.casual_customer)
        
        # Tìm kiếm loyal customers
        loyal_results = self.manager.tim_kiem_nang_cao(loai="Loyal")
        self.assertEqual(len(loyal_results), 1)
        self.assertEqual(loyal_results[0].ma_khach_hang, "L001")
        
        # Tìm kiếm casual customers
        casual_results = self.manager.tim_kiem_nang_cao(loai="Casual")
        self.assertEqual(len(casual_results), 1)
        self.assertEqual(casual_results[0].ma_khach_hang, "C001")

    def test_tim_kiem_nang_cao_theo_ten(self):
        """
        Test case 14: Kiểm tra tìm kiếm nâng cao theo tên
        """
        # Thêm khách hàng
        self.manager.them_khach_hang(self.loyal_customer)
        self.manager.them_khach_hang(self.casual_customer)
        self.manager.them_khach_hang(
            LoyalCustomer("L002", "Nguyễn Văn C", "0912345670", "c@example.com")
        )
        
        # Tìm kiếm theo tên chứa "Nguyễn"
        results = self.manager.tim_kiem_nang_cao(ten_chua="Nguyễn")
        self.assertEqual(len(results), 2)
        self.assertIn("L001", [kh.ma_khach_hang for kh in results])
        self.assertIn("L002", [kh.ma_khach_hang for kh in results])

    def test_tim_kiem_nang_cao_theo_sdt(self):
        """
        Test case 15: Kiểm tra tìm kiếm nâng cao theo số điện thoại
        """
        # Thêm khách hàng
        self.manager.them_khach_hang(self.loyal_customer)
        self.manager.them_khach_hang(self.casual_customer)
        
        # Tìm kiếm theo số điện thoại chứa "0912"
        results = self.manager.tim_kiem_nang_cao(sdt_chua="0912")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].ma_khach_hang, "L001")

    def test_tim_kiem_nang_cao_theo_email(self):
        """
        Test case 16: Kiểm tra tìm kiếm nâng cao theo email
        """
        # Thêm khách hàng
        self.manager.them_khach_hang(self.loyal_customer)
        self.manager.them_khach_hang(self.casual_customer)
        
        # Tìm kiếm theo email chứa "example.com"
        results = self.manager.tim_kiem_nang_cao(email_chua="example.com")
        self.assertEqual(len(results), 2)
        
        # Tìm kiếm theo email chứa "a@"
        results = self.manager.tim_kiem_nang_cao(email_chua="a@")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].ma_khach_hang, "L001")

    def test_tim_kiem_nang_cao_theo_tong_gia_tri(self):
        """
        Test case 17: Kiểm tra tìm kiếm nâng cao theo tổng giá trị mua hàng
        """
        # Thêm khách hàng casual
        self.manager.them_khach_hang(self.casual_customer)  # 1.5 triệu
        self.manager.them_khach_hang(
            CasualCustomer("C002", "Lê Thị D", "0912345677", "d@example.com", 2, 800000)
        )
        
        # Tìm kiếm theo tổng giá trị tối thiểu 1 triệu
        results = self.manager.tim_kiem_nang_cao(tong_gia_min=1000000)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].ma_khach_hang, "C001")
        
        # Tìm kiếm theo tổng giá trị tối đa 1 triệu
        results = self.manager.tim_kiem_nang_cao(tong_gia_max=1000000)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].ma_khach_hang, "C002")

    def test_tim_kiem_nang_cao_theo_so_lan_mua(self):
        """
        Test case 18: Kiểm tra tìm kiếm nâng cao theo số lần mua hàng
        """
        # Thêm khách hàng casual
        self.manager.them_khach_hang(self.casual_customer)  # 5 lần
        self.manager.them_khach_hang(
            CasualCustomer("C002", "Lê Thị D", "0912345677", "d@example.com", 2, 800000)
        )
        
        # Tìm kiếm theo số lần mua tối thiểu 3
        results = self.manager.tim_kiem_nang_cao(so_lan_mua_min=3)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].ma_khach_hang, "C001")

    def test_tim_kiem_nang_cao_ket_hop(self):
        """
        Test case 19: Kiểm tra tìm kiếm nâng cao kết hợp nhiều điều kiện
        """
        # Thêm nhiều khách hàng
        self.manager.them_khach_hang(self.loyal_customer)
        self.manager.them_khach_hang(self.casual_customer)
        self.manager.them_khach_hang(
            CasualCustomer("C002", "Nguyễn Thị D", "0912345677", "d@example.com", 2, 800000)
        )
        
        # Tìm kiếm kết hợp: loại Casual + tên có "Nguyễn"
        results = self.manager.tim_kiem_nang_cao(loai="Casual", ten_chua="Nguyễn")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].ma_khach_hang, "C002")

    def test_hien_thi_top_khach_hang(self):
        """
        Test case 20: Kiểm tra hiển thị top khách hàng
        """
        # Thêm nhiều khách hàng casual với giá trị khác nhau
        self.manager.them_khach_hang(
            CasualCustomer("C001", "A", "0912345671", "a@test.com", 1, 1000000)
        )
        self.manager.them_khach_hang(
            CasualCustomer("C002", "B", "0912345672", "b@test.com", 1, 3000000)
        )
        self.manager.them_khach_hang(
            CasualCustomer("C003", "C", "0912345673", "c@test.com", 1, 2000000)
        )
        self.manager.them_khach_hang(
            CasualCustomer("C004", "D", "0912345674", "d@test.com", 1, 500000)
        )
        
        # Lấy top 2 khách hàng
        top_khs = self.manager.hien_thi_top_khach_hang(n=2)
        self.assertEqual(len(top_khs), 2)
        self.assertEqual(top_khs[0].ma_khach_hang, "C002")  # 3 triệu
        self.assertEqual(top_khs[1].ma_khach_hang, "C003")  # 2 triệu

    def test_thong_ke_khach_hang_than_thiet(self):
        """
        Test case 21: Kiểm tra thống kê khách hàng thân thiết để tặng quà
        """
        # Thêm nhiều khách hàng loyal với điểm tích lũy khác nhau
        self.manager.them_khach_hang(
            LoyalCustomer("L001", "A", "0912345671", "a@test.com", 600)
        )
        self.manager.them_khach_hang(
            LoyalCustomer("L002", "B", "0912345672", "b@test.com", 400)
        )
        self.manager.them_khach_hang(
            LoyalCustomer("L003", "C", "0912345673", "c@test.com", 700)
        )
        
        # Thực hiện thống kê (chỉ lấy những khách có điểm > 500)
        kh_qua = self.manager.thong_ke_khach_hang_than_thiet()
        self.assertEqual(len(kh_qua), 2)
        self.assertIn("L001", [kh.ma_khach_hang for kh in kh_qua])
        self.assertIn("L003", [kh.ma_khach_hang for kh in kh_qua])
        
        # Kiểm tra sắp xếp theo điểm tích lũy giảm dần
        self.assertEqual(kh_qua[0].ma_khach_hang, "L003")  # 700 điểm
        self.assertEqual(kh_qua[1].ma_khach_hang, "L001")  # 600 điểm

    def test_to_dict_loyal_customer(self):
        """
        Test case 22: Kiểm tra phương thức to_dict của LoyalCustomer
        """
        loyal_dict = self.loyal_customer.to_dict()
        self.assertEqual(loyal_dict["Loai"], "Loyal")
        self.assertEqual(loyal_dict["MaKH"], "L001")
        self.assertEqual(loyal_dict["TenKH"], "Nguyễn Văn A")
        self.assertEqual(loyal_dict["DiemTichLuy"], 500)
        self.assertEqual(loyal_dict["SoLanMua"], "")  # Không áp dụng

    def test_to_dict_casual_customer(self):
        """
        Test case 23: Kiểm tra phương thức to_dict của CasualCustomer
        """
        casual_dict = self.casual_customer.to_dict()
        self.assertEqual(casual_dict["Loai"], "Casual")
        self.assertEqual(casual_dict["MaKH"], "C001")
        self.assertEqual(casual_dict["TenKH"], "Trần Thị B")
        self.assertEqual(casual_dict["SoLanMua"], 5)
        self.assertEqual(casual_dict["TongGiaTri"], 1500000)
        self.assertEqual(casual_dict["DiemTichLuy"], "")  # Không áp dụng

    def test_from_dict_loyal_customer(self):
        """
        Test case 24: Kiểm tra phương thức from_dict của LoyalCustomer
        """
        data = {
            "Loai": "Loyal",
            "MaKH": "L001",
            "TenKH": "Nguyễn Văn A",
            "SDT": "0912345678",
            "Email": "a@example.com",
            "DiemTichLuy": "500",
            "SoLanMua": "",
            "TongGiaTri": ""
        }
        
        loyal = LoyalCustomer.from_dict(data)
        self.assertEqual(loyal.ma_khach_hang, "L001")
        self.assertEqual(loyal.ten_khach_hang, "Nguyễn Văn A")
        self.assertEqual(loyal.diem_tich_luy, 500)

    def test_from_dict_casual_customer(self):
        """
        Test case 25: Kiểm tra phương thức from_dict của CasualCustomer
        """
        data = {
            "Loai": "Casual",
            "MaKH": "C001",
            "TenKH": "Trần Thị B",
            "SDT": "0987654321",
            "Email": "b@example.com",
            "DiemTichLuy": "",
            "SoLanMua": "5",
            "TongGiaTri": "1500000"
        }
        
        casual = CasualCustomer.from_dict(data)
        self.assertEqual(casual.ma_khach_hang, "C001")
        self.assertEqual(casual.ten_khach_hang, "Trần Thị B")
        self.assertEqual(casual.so_lan_mua_hang, 5)
        self.assertEqual(casual.tong_gia_tri_mua_hang, 1500000)

    def test_luu_va_doc_file(self):
        """
        Test case 26: Kiểm tra lưu và đọc file CSV
        """
        # Thêm khách hàng
        self.manager.them_khach_hang(self.loyal_customer)
        self.manager.them_khach_hang(self.casual_customer)
        
        # Lưu vào file
        self.manager.luu_file()
        
        # Tạo manager mới để đọc file
        new_manager = ManageCustomer(self.filename)
        new_manager.doc_file()
        
        # Kiểm tra đã đọc đúng số lượng
        self.assertEqual(len(new_manager.danh_sach_khach_hang), 2)
        
        # Kiểm tra thông tin khách hàng
        loyal = new_manager.tim_kiem_nang_cao(ma_kh="L001")[0]
        casual = new_manager.tim_kiem_nang_cao(ma_kh="C001")[0]
        
        self.assertEqual(loyal.ma_khach_hang, "L001")
        self.assertEqual(loyal.ten_khach_hang, "Nguyễn Văn A")
        self.assertEqual(loyal.diem_tich_luy, 500)
        
        self.assertEqual(casual.ma_khach_hang, "C001")
        self.assertEqual(casual.ten_khach_hang, "Trần Thị B")
        self.assertEqual(casual.so_lan_mua_hang, 5)
        self.assertEqual(casual.tong_gia_tri_mua_hang, 1500000)

    def test_cap_nhat_diem_tich_luy(self):
        """
        Test case 27: Kiểm tra cập nhật điểm tích lũy
        """
        # Thêm khách hàng thân thiết
        self.manager.them_khach_hang(self.loyal_customer)
        
        # Cập nhật điểm tích lũy
        self.manager.cap_nhat_diem_tich_luy("L001", 200)
        
        # Kiểm tra sau khi cập nhật
        updated = self.manager.tim_kiem_nang_cao(ma_kh="L001")[0]
        self.assertEqual(updated.diem_tich_luy, 700)  # 500 + 200

    def test_giam_diem_tich_luy(self):
        """
        Test case 28: Kiểm tra giảm điểm tích lũy khi đổi quà
        """
        # Thêm khách hàng thân thiết
        self.manager.them_khach_hang(self.loyal_customer)  # 500 điểm
        
        # Giảm điểm khi đổi quà
        result = self.manager.doi_qua("L001", 300)
        
        # Kiểm tra kết quả
        self.assertTrue(result)
        
        # Kiểm tra điểm sau khi đổi
        updated = self.manager.tim_kiem_nang_cao(ma_kh="L001")[0]
        self.assertEqual(updated.diem_tich_luy, 200)  # 500 - 300
        
    def test_doi_qua_khong_du_diem(self):
        """
        Test case 29: Kiểm tra trường hợp đổi quà nhưng không đủ điểm
        """
        # Thêm khách hàng thân thiết
        self.manager.them_khach_hang(self.loyal_customer)  # 500 điểm
        
        # Thử đổi quà với điểm nhiều hơn hiện có
        result = self.manager.doi_qua("L001", 600)
        
        # Kiểm tra kết quả
        self.assertFalse(result)
        
        # Kiểm tra điểm không thay đổi
        updated = self.manager.tim_kiem_nang_cao(ma_kh="L001")[0]
        self.assertEqual(updated.diem_tich_luy, 500)  # Vẫn giữ nguyên

    def test_tinh_tong_gia_tri(self):
        """
        Test case 30: Kiểm tra tính tổng giá trị mua hàng của tất cả khách hàng
        """
        # Thêm các khách hàng casual
        self.manager.them_khach_hang(
            CasualCustomer("C001", "A", "0912345671", "a@test.com", 1, 1000000)
        )
        self.manager.them_khach_hang(
            CasualCustomer("C002", "B", "0912345672", "b@test.com", 1, 3000000)
        )
        
        # Thêm khách hàng loyal (đã được nâng cấp từ casual)
        self.manager.them_khach_hang(
            LoyalCustomer("L001", "C", "0912345673", "c@test.com", 250)  # tương đương 2.5tr đã mua
        )
        
        # Tính tổng giá trị
        tong_gia_tri = self.manager.tinh_tong_gia_tri_mua_hang()
        
        # Kiểm tra kết quả: 1tr + 3tr + 2.5tr = 6.5tr
        self.assertEqual(tong_gia_tri, 6500000)
        
        # Kiểm tra trường hợp không có khách hàng
        manager_moi = ManageCustomer(self.filename)  # manager mới chưa có dữ liệu
        self.assertEqual(manager_moi.tinh_tong_gia_tri_mua_hang(), 0)