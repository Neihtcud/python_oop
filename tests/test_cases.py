import unittest
from models.customer import Customer, LoyalCustomer, CasualCustomer

class TestCustomer(unittest.TestCase):
    def test_create_customer_valid(self):
        c = Customer("KH001", "Nguyen Van A", "0123456789", "a@example.com")
        self.assertEqual(c.ma_khach_hang, "KH001")

    def test_create_loyal_customer_valid(self):
        lc = LoyalCustomer("KH002", "Le Thi B", "0987654321", "b@example.com")
        self.assertEqual(lc.ten_khach_hang, "Le Thi B")

    def test_create_casual_customer_valid(self):
        cc = CasualCustomer("KH003", "Tran Van C", "0912345678", "c@example.com", 5, 1000000)
        self.assertEqual(cc.so_lan_mua_hang, 5)

    def test_casual_customer_zero_values(self):
        cc = CasualCustomer("KH004", "Nguyen D", "0900000000", "d@example.com", 0, 0)
        self.assertEqual(cc.tong_gia_tri_mua_hang, 0)

    def test_str_customer(self):
        c = Customer("KH005", "Vo E", "0888888888", "e@example.com")
        self.assertIn("KH005 - Vo E", str(c))

    def test_str_casual_customer(self):
        cc = CasualCustomer("KH006", "Ly F", "0866666666", "f@example.com", 3, 300000)
        self.assertIn("Số lần mua", str(cc))

    def test_invalid_email_format(self):
        c = Customer("KH007", "Test G", "0855555555", "invalid-email")
        self.assertIn("@", c.email)  # This won't throw error, but could be part of validation logic

    def test_negative_purchase_value(self):
        cc = CasualCustomer("KH008", "Test H", "0844444444", "h@example.com", 2, -500000)
        self.assertLess(cc.tong_gia_tri_mua_hang, 0)

    def test_large_purchase_count(self):
        cc = CasualCustomer("KH009", "Test I", "0833333333", "i@example.com", 10**6, 5000000)
        self.assertEqual(cc.so_lan_mua_hang, 10**6)

    def test_empty_customer_name(self):
        c = Customer("KH010", "", "0822222222", "j@example.com")
        self.assertEqual(c.ten_khach_hang, "")

    def test_special_character_in_name(self):
        c = Customer("KH011", "Lê Văn @#$", "0811111111", "k@example.com")
        self.assertIn("@", c.ten_khach_hang)

    def test_unicode_email(self):
        c = Customer("KH012", "Unicode", "0800000000", "tên@example.com")
        self.assertIn("@", c.email)

    def test_phone_number_too_long(self):
        c = Customer("KH013", "Phone Test", "01234567890123456789", "p@example.com")
        self.assertTrue(len(c.so_dien_thoai) > 15)

    def test_add_to_list_and_filter(self):
        customers = [
            CasualCustomer("KH014", "A", "0999999999", "a@e.com", 3, 200000),
            CasualCustomer("KH015", "B", "0888888888", "b@e.com", 10, 1000000)
        ]
        filtered = [c for c in customers if c.so_lan_mua_hang > 5]
        self.assertEqual(len(filtered), 1)

if __name__ == "__main__":
    unittest.main()
