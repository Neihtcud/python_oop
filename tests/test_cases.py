import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock, call
from datetime import datetime

from models.customer import Customer, LoyalCustomer, CasualCustomer
from manage.manage_customer import ManageCustomer
from utils.helpers import nhap_sdt, nhap_email, nhap_ten, loading
from utils.logger import ghi_log

class TestCustomerModels(unittest.TestCase):
    def setUp(self):
        self.customer = Customer("KH001", "Nguyen Van A", "0987654321", "a@example.com")
        self.loyal = LoyalCustomer("KH002", "Nguyen Van B", "0987654322", "b@example.com", 100)
        self.casual = CasualCustomer("KH003", "Nguyen Van C", "0987654323", "c@example.com", 3, 3000000)

    def test_customer_initialization(self):
        self.assertEqual(self.customer.ma_khach_hang, "KH001")
        self.assertEqual(self.customer.ten_khach_hang, "Nguyen Van A")
        self.assertEqual(self.customer.so_dien_thoai, "0987654321")
        self.assertEqual(self.customer.email, "a@example.com")

    def test_loyal_customer_initialization(self):
        self.assertEqual(self.loyal.diem_tich_luy, 100)
        self.assertIsInstance(self.loyal, Customer)

    def test_casual_customer_initialization(self):
        self.assertEqual(self.casual.so_lan_mua_hang, 3)
        self.assertEqual(self.casual.tong_gia_tri_mua_hang, 3000000)

    def test_casual_customer_average_purchase(self):
        self.assertEqual(self.casual.tinh_trung_binh_gia_tri(), 1000000)

    def test_loyal_customer_str_representation(self):
        self.assertIn("Điểm tích lũy: 100", str(self.loyal))

    def test_casual_customer_str_representation(self):
        self.assertIn("Số lần mua: 3", str(self.casual))
        self.assertIn("Tổng giá trị: 3,000,000", str(self.casual))

    def test_loyal_customer_from_dict(self):
        data = {
            "Loai": "Loyal", "MaKH": "KH004", "TenKH": "Nguyen Van D",
            "SDT": "0987654324", "Email": "d@example.com",
            "DiemTichLuy": "200", "TongGiaTri": "5000000"
        }
        customer = LoyalCustomer.from_dict(data)
        self.assertEqual(customer.diem_tich_luy, 200)
        self.assertEqual(customer.tong_gia_tri_mua_hang, 5000000)

    def test_casual_customer_from_dict(self):
        data = {
            "Loai": "Casual", "MaKH": "KH005", "TenKH": "Nguyen Van E",
            "SDT": "0987654325", "Email": "e@example.com",
            "SoLanMua": "5", "TongGiaTri": "7000000"
        }
        customer = CasualCustomer.from_dict(data)
        self.assertEqual(customer.so_lan_mua_hang, 5)
        self.assertEqual(customer.tong_gia_tri_mua_hang, 7000000)

class TestManageCustomer(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        self.temp_file.close()
        self.manager = ManageCustomer(self.temp_file.name)

    def tearDown(self):
        os.unlink(self.temp_file.name)

    def test_add_loyal_customer(self):
        loyal = LoyalCustomer("KH001", "Nguyen Van A", "0987654321", "a@example.com", 100)
        self.assertTrue(self.manager.them_khach_hang(loyal))
        self.assertEqual(len(self.manager.danh_sach_khach_hang), 1)

    def test_add_casual_customer(self):
        casual = CasualCustomer("KH001", "Nguyen Van A", "0987654321", "a@example.com", 5, 5000000)
        self.assertTrue(self.manager.them_khach_hang(casual))
        self.assertEqual(len(self.manager.danh_sach_khach_hang), 1)

    def test_add_duplicate_customer_id(self):
        loyal1 = LoyalCustomer("KH001", "Nguyen Van A", "0987654321", "a@example.com", 100)
        loyal2 = LoyalCustomer("KH001", "Nguyen Van B", "0987654322", "b@example.com", 50)
        self.manager.them_khach_hang(loyal1)
        self.assertFalse(self.manager.them_khach_hang(loyal2))

    def test_add_customer_with_invalid_phone(self):
        loyal = LoyalCustomer("KH001", "Nguyen Van A", "12345", "a@example.com", 100)
        self.assertFalse(self.manager.them_khach_hang(loyal))

    def test_update_customer_info(self):
        loyal = LoyalCustomer("KH001", "Nguyen Van A", "0987654321", "a@example.com", 100)
        self.manager.them_khach_hang(loyal)
        self.assertTrue(self.manager.sua_thong_tin("KH001", ten_moi="Nguyen Van B"))
        self.assertEqual(self.manager.danh_sach_khach_hang[0].ten_khach_hang, "Nguyen Van B")

    def test_delete_customer(self):
        loyal = LoyalCustomer("KH001", "Nguyen Van A", "0987654321", "a@example.com", 100)
        self.manager.them_khach_hang(loyal)
        with patch('builtins.input', return_value='y'):
            self.assertTrue(self.manager.xoa_khach_hang("KH001"))
        self.assertEqual(len(self.manager.danh_sach_khach_hang), 0)

    def test_delete_customer_cancel(self):
        loyal = LoyalCustomer("KH001", "Nguyen Van A", "0987654321", "a@example.com", 100)
        self.manager.them_khach_hang(loyal)
        with patch('builtins.input', return_value='n'):
            self.assertFalse(self.manager.xoa_khach_hang("KH001"))
        self.assertEqual(len(self.manager.danh_sach_khach_hang), 1)

    def test_update_purchase_for_loyal_customer(self):
        loyal = LoyalCustomer("KH001", "Nguyen Van A", "0987654321", "a@example.com", 100)
        self.manager.them_khach_hang(loyal)
        self.assertTrue(self.manager.cap_nhat_mua_hang("KH001", 1, 150000))
        self.assertEqual(self.manager.danh_sach_khach_hang[0].diem_tich_luy, 115)

    def test_promote_casual_to_loyal(self):
        casual = CasualCustomer("KH001", "Nguyen Van A", "0987654321", "a@example.com", 3, 1900000)
        self.manager.them_khach_hang(casual)
        self.assertTrue(self.manager.cap_nhat_mua_hang("KH001", 0, 200000))
        self.assertIsInstance(self.manager.danh_sach_khach_hang[0], LoyalCustomer)

    def test_search_customer_by_id(self):
        loyal = LoyalCustomer("KH001", "Nguyen Van A", "0987654321", "a@example.com", 100)
        self.manager.them_khach_hang(loyal)
        result = self.manager.tim_kiem(ma_kh="KH001")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].ma_khach_hang, "KH001")

    def test_search_customer_by_name(self):
        loyal = LoyalCustomer("KH001", "Nguyen Van A", "0987654321", "a@example.com", 100)
        self.manager.them_khach_hang(loyal)
        result = self.manager.tim_kiem(ten_chua="Van A")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].ten_khach_hang, "Nguyen Van A")

    def test_search_customer_by_phone(self):
        loyal = LoyalCustomer("KH001", "Nguyen Van A", "0987654321", "a@example.com", 100)
        self.manager.them_khach_hang(loyal)
        result = self.manager.tim_kiem(sdt_chua="0987654321")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].so_dien_thoai, "0987654321")

    def test_search_customer_by_type(self):
        loyal = LoyalCustomer("KH001", "Nguyen Van A", "0987654321", "a@example.com", 100)
        casual = CasualCustomer("KH002", "Nguyen Van B", "0987654322", "b@example.com", 3, 3000000)
        self.manager.them_khach_hang(loyal)
        self.manager.them_khach_hang(casual)
        
        loyal_results = self.manager.tim_kiem(loai="Loyal")
        self.assertEqual(len(loyal_results), 1)
        self.assertIsInstance(loyal_results[0], LoyalCustomer)
        
        casual_results = self.manager.tim_kiem(loai="Casual")
        self.assertEqual(len(casual_results), 1)
        self.assertIsInstance(casual_results[0], CasualCustomer)

    def test_read_write_csv(self):
        loyal = LoyalCustomer("KH001", "Nguyen Van A", "0987654321", "a@example.com", 100)
        self.manager.them_khach_hang(loyal)
        self.assertTrue(self.manager.ghi_file())
        
        new_manager = ManageCustomer(self.temp_file.name)
        self.assertEqual(len(new_manager.danh_sach_khach_hang), 1)
        self.assertEqual(new_manager.danh_sach_khach_hang[0].ma_khach_hang, "KH001")

    def test_backup_file(self):
        loyal = LoyalCustomer("KH001", "Nguyen Van A", "0987654321", "a@example.com", 100)
        self.manager.them_khach_hang(loyal)
        self.assertTrue(self.manager.backup_file())

    def test_thong_ke(self):
        loyal = LoyalCustomer("KH001", "Nguyen Van A", "0987654321", "a@example.com", 100)
        casual = CasualCustomer("KH002", "Nguyen Van B", "0987654322", "b@example.com", 3, 3000000)
        self.manager.them_khach_hang(loyal)
        self.manager.them_khach_hang(casual)
        
        with patch('manage.manage_customer.plt.show') as mock_show:
            self.manager.thong_ke()
            self.assertEqual(mock_show.call_count, 2)

    def test_hien_thi_top_khach_hang(self):
        casual1 = CasualCustomer("KH001", "Nguyen Van A", "0987654321", "a@example.com", 3, 5000000)
        casual2 = CasualCustomer("KH002", "Nguyen Van B", "0987654322", "b@example.com", 2, 3000000)
        self.manager.them_khach_hang(casual1)
        self.manager.them_khach_hang(casual2)
        
        top = self.manager.hien_thi_top_khach_hang(n=1)
        self.assertEqual(len(top), 1)
        self.assertEqual(top[0].ma_khach_hang, "KH001")

    def test_thong_ke_khach_hang_than_thiet(self):
        loyal1 = LoyalCustomer("KH001", "Nguyen Van A", "0987654321", "a@example.com", 600)
        loyal2 = LoyalCustomer("KH002", "Nguyen Van B", "0987654322", "b@example.com", 400)
        self.manager.them_khach_hang(loyal1)
        self.manager.them_khach_hang(loyal2)
        
        result = self.manager.thong_ke_khach_hang_than_thiet()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].ma_khach_hang, "KH001")

class TestHelpers(unittest.TestCase):
    @patch('builtins.input', return_value="0987654321")
    def test_nhap_sdt_valid(self, mock_input):
        self.assertEqual(nhap_sdt(), "0987654321")

    @patch('builtins.input', side_effect=["12345", "0987654321"])
    def test_nhap_sdt_invalid_then_valid(self, mock_input):
        with patch('builtins.print') as mock_print:
            result = nhap_sdt()
            self.assertTrue(mock_print.called)
            self.assertEqual(result, "0987654321")

    @patch('builtins.input', return_value="test@example.com")
    def test_nhap_email_valid(self, mock_input):
        self.assertEqual(nhap_email(), "test@example.com")

    @patch('builtins.input', side_effect=["test@", "test@example.com"])
    def test_nhap_email_invalid_then_valid(self, mock_input):
        with patch('builtins.print') as mock_print:
            result = nhap_email()
            self.assertTrue(mock_print.called)
            self.assertEqual(result, "test@example.com")

    @patch('builtins.input', return_value="Nguyen Van A")
    def test_nhap_ten_valid(self, mock_input):
        self.assertEqual(nhap_ten(), "Nguyen Van A")

    @patch('builtins.input', side_effect=["Nguyen123", "Nguyen Van A"])
    def test_nhap_ten_invalid_then_valid(self, mock_input):
        with patch('builtins.print') as mock_print:
            result = nhap_ten()
            self.assertTrue(mock_print.called)
            self.assertEqual(result, "Nguyen Van A")

    def test_loading(self):
        with patch('time.sleep'), patch('builtins.print') as mock_print:
            loading("Đang tải")
            self.assertTrue(mock_print.called)
            mock_print.assert_has_calls([
                call("Đang tải", end=""),
                call(".", end="", flush=True),
                call(".", end="", flush=True),
                call(".", end="", flush=True),
                call()
            ])

class TestLogger(unittest.TestCase):
    def setUp(self):
        self.temp_log = tempfile.NamedTemporaryFile(delete=False)
        self.temp_log.close()
        self.customer = LoyalCustomer("KH001", "Nguyen Van A", "0987654321", "a@example.com", 100)

    def tearDown(self):
        os.unlink(self.temp_log.name)

    @patch('utils.logger.datetime')
    def test_ghi_log(self, mock_datetime):
        mock_datetime.now.return_value.strftime.return_value = "2023-01-01 00:00:00"
        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            ghi_log("Test", self.customer)
            mock_file.assert_called_once()
            handle = mock_file()
            handle.write.assert_called_once_with(
                "[2023-01-01 00:00:00] Test khách hàng: KH001 - Nguyen Van A - Loyal\n"
            )

    def test_ghi_log_to_file(self):
        customer = CasualCustomer("KH002", "Nguyen Van B", "0987654322", "b@example.com", 3, 3000000)
        ghi_log("Test file", customer, log_file=self.temp_log.name)
        
        with open(self.temp_log.name, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("KH002", content)
            self.assertIn("Nguyen Van B", content)
            self.assertIn("Casual", content)

class TestMainFunctions(unittest.TestCase):
    @patch('main.ManageCustomer')
    @patch('builtins.input', return_value="0")
    def test_main_menu_exit(self, mock_input, mock_manager):
        from main import main
        main()
        mock_manager.assert_called_once()

    @patch('main.ManageCustomer')
    @patch('builtins.input', side_effect=["1", "0", "0"])  # Chọn menu quản lý rồi thoát
    def test_main_menu_management(self, mock_input, mock_manager):
        from main import main
        mock_instance = mock_manager.return_value
        main()
        self.assertTrue(mock_instance.them_khach_hang.called or 
                      mock_instance.sua_thong_tin.called or 
                      mock_instance.xoa_khach_hang.called)

    @patch('main.ManageCustomer')
    @patch('builtins.input', side_effect=["2", "1", "KH001", "0", "0"])  # Tìm kiếm rồi thoát
    def test_search_customer_flow(self, mock_input, mock_manager):
        from main import main
        mock_instance = mock_manager.return_value
        mock_instance.tim_kiem.return_value = [
            LoyalCustomer("KH001", "Nguyen Van A", "0987654321", "a@example.com", 100)
        ]
        
        with patch('builtins.print') as mock_print:
            main()
            self.assertTrue(mock_print.called)
            output = "\n".join([args[0] for args, _ in mock_print.call_args_list])
            self.assertIn("KH001", output)

    @patch('main.ManageCustomer')
    @patch('builtins.input', side_effect=["3", "0"])  # Hiển thị DS rồi thoát
    def test_display_customer_list(self, mock_input, mock_manager):
        from main import main
        mock_instance = mock_manager.return_value
        mock_instance.danh_sach_khach_hang = [
            LoyalCustomer("KH001", "Nguyen Van A", "0987654321", "a@example.com", 100)
        ]
        
        with patch('builtins.print') as mock_print:
            main()
            self.assertTrue(mock_print.called)
            output = "\n".join([args[0] for args, _ in mock_print.call_args_list])
            self.assertIn("KH001", output)

if __name__ == '__main__':
    unittest.main()