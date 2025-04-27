class Customer:
    def __init__(self, ma_khach_hang, ten_khach_hang, so_dien_thoai, email):
        self.ma_khach_hang = ma_khach_hang
        self.ten_khach_hang = ten_khach_hang
        self.so_dien_thoai = so_dien_thoai
        self.email = email
    def __str__(self):
        return f"{self.ma_khach_hang} - {self.ten_khach_hang}"
    

class LoyalCustomer(Customer):
    def __init__(self, ma_khach_hang, ten_khach_hang, so_dien_thoai, email):
        super().__init__(ma_khach_hang, ten_khach_hang, so_dien_thoai, email)

class CasualCustomer(Customer):
    def __init__(self, ma_khach_hang, ten_khach_hang, so_dien_thoai, email, so_lan_mua_hang=0, tong_gia_tri_mua_hang=0):
        super().__init__(ma_khach_hang, ten_khach_hang, so_dien_thoai, email)
        self.so_lan_mua_hang = so_lan_mua_hang
        self.tong_gia_tri_mua_hang = tong_gia_tri_mua_hang

    def __str__(self):
        return f"{super().__str__()} | Số lần mua: {self.so_lan_mua_hang}, Tổng giá trị: {self.tong_gia_tri_mua_hang}"    
