class Customer:
    def __init__(self, ma_khach_hang, ten_khach_hang, so_dien_thoai, email):
        self.ma_khach_hang = ma_khach_hang
        self.ten_khach_hang = ten_khach_hang
        self.so_dien_thoai = so_dien_thoai
        self.email = email
    
    def __str__(self):
        return f"{self.ma_khach_hang} - {self.ten_khach_hang}"
    
class LoyalCustomer(Customer):
    def __init__(self, ma_khach_hang, ten_khach_hang, so_dien_thoai, email, diem_tich_luy=0, tong_gia_tri_mua_hang=0, so_lan_mua_hang=0):
        super().__init__(ma_khach_hang, ten_khach_hang, so_dien_thoai, email)
        self.diem_tich_luy = int(diem_tich_luy) if isinstance(diem_tich_luy, str) else diem_tich_luy
        self.tong_gia_tri_mua_hang = float(tong_gia_tri_mua_hang) if isinstance(tong_gia_tri_mua_hang, str) else tong_gia_tri_mua_hang
        self.so_lan_mua_hang = int(so_lan_mua_hang) if isinstance(so_lan_mua_hang, str) else so_lan_mua_hang
    
    def __str__(self):
        return f"{super().__str__()} | Điểm tích lũy: {self.diem_tich_luy} | Số lần mua: {self.so_lan_mua_hang} | Tổng giá trị: {self.tong_gia_tri_mua_hang:,.0f}"
    
    def to_dict(self):
        return {
            "Loai": "Loyal",
            "MaKH": self.ma_khach_hang,
            "TenKH": self.ten_khach_hang,
            "SDT": self.so_dien_thoai,
            "Email": self.email,
            "SoLanMua": self.so_lan_mua_hang,
            "TongGiaTri": self.tong_gia_tri_mua_hang,
            "DiemTichLuy": self.diem_tich_luy
        }
    
    @classmethod
    def from_dict(cls, row):
        diem_tich_luy = int(row.get("DiemTichLuy", 0)) if row.get("DiemTichLuy") else 0
        tong_gia_tri = float(row.get("TongGiaTri", 0)) if row.get("TongGiaTri") else 0
        so_lan_mua = int(row.get("SoLanMua", 0)) if row.get("SoLanMua") else 0
        
        return cls(
            ma_khach_hang=row["MaKH"],
            ten_khach_hang=row["TenKH"],
            so_dien_thoai=row["SDT"],
            email=row["Email"],
            diem_tich_luy=diem_tich_luy,
            tong_gia_tri_mua_hang=tong_gia_tri,
            so_lan_mua_hang=so_lan_mua
        )
    
    # Thêm phương thức để chuyển đổi từ CasualCustomer
    @classmethod
    def from_casual_customer(cls, casual_customer, diem_tich_luy=0):
        return cls(
            ma_khach_hang=casual_customer.ma_khach_hang,
            ten_khach_hang=casual_customer.ten_khach_hang,
            so_dien_thoai=casual_customer.so_dien_thoai,
            email=casual_customer.email,
            diem_tich_luy=diem_tich_luy,
            tong_gia_tri_mua_hang=casual_customer.tong_gia_tri_mua_hang,
            so_lan_mua_hang=casual_customer.so_lan_mua_hang
        )

class CasualCustomer(Customer):
    def __init__(self, ma_khach_hang, ten_khach_hang, so_dien_thoai, email, so_lan_mua_hang=0, tong_gia_tri_mua_hang=0):
        super().__init__(ma_khach_hang, ten_khach_hang, so_dien_thoai, email)
        self.so_lan_mua_hang = int(so_lan_mua_hang) if isinstance(so_lan_mua_hang, str) else so_lan_mua_hang
        self.tong_gia_tri_mua_hang = float(tong_gia_tri_mua_hang) if isinstance(tong_gia_tri_mua_hang, str) else tong_gia_tri_mua_hang
    
    def tinh_trung_binh_gia_tri(self):
        if self.so_lan_mua_hang == 0:
            return 0
        return self.tong_gia_tri_mua_hang / self.so_lan_mua_hang
    
    def __str__(self):
        return f"{super().__str__()} | Số lần mua: {self.so_lan_mua_hang}, Tổng giá trị: {self.tong_gia_tri_mua_hang:,.0f}"
    
    def to_dict(self):
        return {
            "Loai": "Casual",
            "MaKH": self.ma_khach_hang,
            "TenKH": self.ten_khach_hang,
            "SDT": self.so_dien_thoai,
            "Email": self.email,
            "SoLanMua": self.so_lan_mua_hang,
            "TongGiaTri": self.tong_gia_tri_mua_hang,
            "DiemTichLuy": ""
        }
    
    @classmethod
    def from_dict(cls, row):
        so_lan_mua = int(row.get("SoLanMua", 0)) if row.get("SoLanMua") else 0
        tong_gia_tri = float(row.get("TongGiaTri", 0)) if row.get("TongGiaTri") else 0
        
        return cls(
            ma_khach_hang=row["MaKH"],
            ten_khach_hang=row["TenKH"],
            so_dien_thoai=row["SDT"],
            email=row["Email"],
            so_lan_mua_hang=so_lan_mua,
            tong_gia_tri_mua_hang=tong_gia_tri
        )