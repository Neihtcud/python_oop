from managers.manage_customer import ManageCustomer
from models.customer import LoyalCustomer, CasualCustomer



def run_tests():
    ql = ManageCustomer()

    print("\n========== TEST: Thêm khách hàng ==========")
    for i in range(1, 11):
        ma = f"KH{i:02d}"
        ten = f"Customer {i}"
        sdt = f"09{i:08d}"
        email = f"customer{i}@mail.com"
        kh = CasualCustomer(ma, ten, sdt, email)
        ql.them_khach_hang(kh)

    print("\n========== TEST: Sửa thông tin khách hàng ==========")
    ql.sua_thong_tin("KH01", "Khach Hang 1 Update", "update1@mail.com")
    ql.sua_thong_tin("KH02", "Khach Hang 2 Update", "update2@mail.com")

    print("\n========== TEST: Xóa khách hàng ==========")
    ql.xoa_khach_hang("KH03")
    ql.xoa_khach_hang("KH04")

    print("\n========== TEST: Cập nhật mua hàng ==========")
    ql.cap_nhat_mua_hang("KH05", 5, 500000)
    ql.cap_nhat_mua_hang("KH06", 10, 2500000)  # Khách này sẽ lên Loyal

    print("\n========== TEST: Tìm kiếm khách hàng ==========")
    ket_qua = ql.tim_kiem(ma_kh="KH01")
    if ket_qua:
        print(f"Tìm thấy: {ket_qua[0].ten_khach_hang}")
    else:
        print("Không tìm thấy KH01")

    print("\n========== TEST: Thống kê khách hàng ==========")
    ql.thong_ke()

if __name__ == "__main__":
    run_tests()
