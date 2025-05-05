from managers.manage_customer import ManageCustomer
from models.customer import LoyalCustomer, CasualCustomer
from utils.helpers import clear_screen, loading, nhap_sdt, nhap_ten, kiem_tra_email, nhap_email
import re

def main():
    """Hàm chính điều khiển luồng chương trình"""
    ql = ManageCustomer()

    while True:
        # Menu chính cải tiến với màu sắc và định dạng
        print("\033[96m╔═════════════════════════════════════════════════╗\033[0m")
        print("\033[96m║            HỆ THỐNG QUẢN LÝ KHÁCH HÀNG          ║\033[0m")
        print("\033[96m╠═════════════════════════════════════════════════╣\033[0m")
        print("\033[93m║ 1. Thêm mới / Sửa thông tin / Xóa khách hàng    ║\033[0m")
        print("\033[93m║ 2. Tìm kiếm khách hàng                          ║\033[0m")
        print("\033[93m║ 3. Hiển thị danh sách khách hàng                ║\033[0m")
        print("\033[93m║ 4. Tính tổng doanh thu                          ║\033[0m")
        print("\033[93m║ 5. Hiển thị top 3 khách hàng mua nhiều nhất     ║\033[0m")
        print("\033[93m║ 6. Thống kê KH thân thiết để tặng quà Tết       ║\033[0m")
        print("\033[91m║ 0. Thoát chương trình                           ║\033[0m")
        print("\033[96m╚═════════════════════════════════════════════════╝\033[0m")
        choice = input("\033[95m>> Chọn chức năng (0-6): \033[0m")

        if choice == '1':
            # Menu quản lý thêm/sửa/xóa
            sub_menu_quan_ly()
        elif choice == '2':
            # Tìm kiếm khách hàng
            tim_kiem_khach_hang(ql)
        elif choice == '3':
            # Hiển thị danh sách khách hàng
            hien_thi_danh_sach(ql)
        elif choice == '4':
            # Tính tổng doanh thu
            loading()
            ql.thong_ke()
        elif choice == '5':
            # Hiển thị top khách hàng mua nhiều nhất
            loading()
            ql.hien_thi_top_khach_hang(n=3)
        elif choice == '6':
            # Thống kê khách hàng thân thiết để tặng quà Tết
            loading()
            ql.thong_ke_khach_hang_than_thiet()
        elif choice == '0':
            print("\033[92mCảm ơn bạn đã sử dụng chương trình. Tạm biệt!\033[0m")
            break
        else:
            print("\033[91m❌ Lựa chọn không hợp lệ. Vui lòng chọn lại!\033[0m")
        
        # Dừng màn hình để người dùng xem kết quả
        if choice != '0':
            input("\nNhấn Enter để tiếp tục...")
            clear_screen()

def sub_menu_quan_ly():
    """Menu con cho chức năng quản lý khách hàng"""
    ql = ManageCustomer()
    while True:
        print("\033[96m╔═════════════════════════════════════════════════╗\033[0m")
        print("\033[96m║                QUẢN LÝ KHÁCH HÀNG               ║\033[0m")
        print("\033[96m╠═════════════════════════════════════════════════╣\033[0m")
        print("\033[93m║ 1. Thêm khách hàng mới                          ║\033[0m")
        print("\033[93m║ 2. Sửa thông tin khách hàng                     ║\033[0m")
        print("\033[93m║ 3. Xóa khách hàng                               ║\033[0m")
        print("\033[93m║ 4. Cập nhật mua hàng cho khách                  ║\033[0m")
        print("\033[91m║ 0. Quay lại menu chính                          ║\033[0m")
        print("\033[96m╚═════════════════════════════════════════════════╝\033[0m")
        choice = input("\033[95m>> Chọn chức năng (0-4): \033[0m")

        if choice == '1':
            them_khach_hang(ql)
        elif choice == '2':
            sua_thong_tin_khach_hang(ql)
        elif choice == '3':
            xoa_khach_hang(ql)
        elif choice == '4':
            cap_nhat_mua_hang(ql)
        elif choice == '0':
            clear_screen()
            return
        else:
            print("\033[91m❌ Lựa chọn không hợp lệ. Vui lòng chọn lại!\033[0m")
        
        if choice != '0':
            input("\nNhấn Enter để tiếp tục...")
            clear_screen()

def them_khach_hang(ql):
    """Chức năng thêm khách hàng mới"""
    print("\n=== THÊM KHÁCH HÀNG MỚI ===")
    
    ma = input("Mã KH: ")
    ten = nhap_ten()
    sdt = nhap_sdt()
    email = nhap_email()

    # Hiển thị menu chọn loại khách hàng
    print("\nChọn loại khách hàng:")
    print("1. Loyal (Thân thiết)")
    print("2. Casual (Vãng lai)")

    loai = None  # Khởi tạo loại trước vòng lặp
    while True:
        loai_choice = input(">> Nhập lựa chọn (1 hoặc 2): ").strip()
        if loai_choice == '1':
            loai = 'loyal'
            break
        elif loai_choice == '2':
            loai = 'casual'
            break
        else:
            print("\033[91mLựa chọn không hợp lệ. Vui lòng chọn 1 hoặc 2.\033[0m")

    # Tạo khách hàng tương ứng
    if loai == 'loyal':
        diem = input("Điểm tích lũy: ")
        try:
            diem = int(diem) if diem else 0
            kh = LoyalCustomer(ma, ten, sdt, email, diem)
        except ValueError:
            print("\033[91mĐiểm tích lũy phải là số nguyên.\033[0m")
            return
    elif loai == 'casual':
        so_lan = input("Số lần mua hàng: ")
        tong_gia_tri = input("Tổng giá trị mua hàng: ")
        try:
            so_lan = int(so_lan) if so_lan else 0
            tong_gia_tri = float(tong_gia_tri) if tong_gia_tri else 0
            kh = CasualCustomer(ma, ten, sdt, email, so_lan, tong_gia_tri)
        except ValueError:
            print("\033[91mSố lần mua hàng và tổng giá trị phải là số.\033[0m")
            return
    else:
        print("\033[91mLỗi: Loại khách hàng không xác định.\033[0m")
        return

    loading()
    ql.them_khach_hang(kh)

def sua_thong_tin_khach_hang(ql):
    """Chức năng sửa thông tin khách hàng"""
    print("\n=== SỬA THÔNG TIN KHÁCH HÀNG ===")
    ma = input("Nhập mã KH cần sửa: ")
    # Sử dụng tim_kiem_nang_cao thay vì tim_kiem
    kh = ql.tim_kiem_nang_cao(ma_kh=ma)
    if not kh:
        print("\033[91mKhông tìm thấy khách hàng.\033[0m")
    else: 
        kh = kh[0]
        print(f"\nHiện tại: Tên: {kh.ten_khach_hang}, Email: {kh.email}, SĐT: {kh.so_dien_thoai}")
        if input("Bạn có muốn sửa tên không? (y/n): ").strip().lower() == 'y':
            ten_moi = nhap_ten()
        else:
            ten_moi = kh.ten_khach_hang 
        if input("Bạn có muốn sửa email không? (y/n): ").strip().lower() == 'y':
            email_moi = nhap_email()
        else:
            email_moi = kh.email       
        if input("Bạn có muốn sửa số điện thoại không? (y/n): ").strip().lower() == 'y':
            sdt_moi = nhap_sdt()                
        else:
            sdt_moi = kh.so_dien_thoai    
        loading()
        ql.sua_thong_tin(ma, ten_moi, email_moi, sdt_moi)

def xoa_khach_hang(ql):
    """Chức năng xóa khách hàng"""
    print("\n=== XÓA KHÁCH HÀNG ===")
    ma = input("Nhập mã KH cần xóa: ")
    loading()
    ql.xoa_khach_hang(ma)

def cap_nhat_mua_hang(ql):
    """Chức năng cập nhật mua hàng cho khách hàng"""
    print("\n=== CẬP NHẬT MUA HÀNG ===")
    ma = input("Nhập mã KH: ")
    # Sử dụng tim_kiem_nang_cao thay vì tim_kiem
    kh = ql.tim_kiem_nang_cao(ma_kh=ma)
    if not kh:
        print("\033[91mKhông tìm thấy khách hàng.\033[0m")
        return
    else:
        kh = kh[0]
        print(f"Khách hàng: {kh.ten_khach_hang} ({kh.ma_khach_hang})")
        
        # Hiển thị thông tin khách hàng theo loại
        if isinstance(kh, LoyalCustomer):
            print(f"Loại: Khách hàng thân thiết (Loyal)")
            print(f"Điểm tích lũy hiện tại: {kh.diem_tich_luy}")
        else:
            print(f"Loại: Khách hàng vãng lai (Casual)")
            print(f"Số lần mua hàng: {kh.so_lan_mua_hang}")
            print(f"Tổng giá trị mua hàng: {kh.tong_gia_tri_mua_hang:,.0f} VND")

    try:
        # Đối với khách hàng thân thiết, số lần mua không được sử dụng
        if isinstance(kh, LoyalCustomer):
            so_lan = 0
            gia_tri_raw = input("Tổng giá trị đơn hàng: ")
            gia_tri = float(gia_tri_raw)
            print(f"Quy đổi: {int(gia_tri // 10000)} điểm tích lũy (10.000 VND = 1 điểm)")
        else:
            so_lan_raw = input("Số lần mua: ")
            gia_tri_raw = input("Tổng giá trị đơn hàng: ")
            so_lan = int(so_lan_raw)
            gia_tri = float(gia_tri_raw)
        
        loading()
        ql.cap_nhat_mua_hang(ma, so_lan, gia_tri)
    except ValueError:
        print("\033[91mSố lần mua hoặc giá trị đơn hàng không hợp lệ.\033[0m")
def tim_kiem_khach_hang(ql):
    """Chức năng tìm kiếm khách hàng"""
    print("\n=== TÌM KIẾM KHÁCH HÀNG ===")
    print("Chọn loại tìm kiếm:")
    print("1. Tìm theo mã khách hàng")
    print("2. Tìm theo tên")
    print("3. Tìm kiếm nâng cao")
    
    option = input(">> Chọn tùy chọn (1-3): ")
    
    if option == '1':
        ma_kh = input("Nhập mã khách hàng: ")
        loading()
        ket_qua = ql.tim_kiem_nang_cao(ma_kh=ma_kh)
    elif option == '2':
        ten = input("Nhập tên khách hàng (hoặc một phần tên): ")
        loading()
        ket_qua = ql.tim_kiem_nang_cao(ten_chua=ten)
    elif option == '3':
        # Tìm kiếm nâng cao với nhiều điều kiện
        print("\nChọn loại khách hàng:")
        print("1. Loyal (Thân thiết)")
        print("2. Casual (Vãng lai)")
        print("3. Bỏ qua lọc theo loại")

        loai = None  # Khởi tạo loại mặc định
        while True:
            loai_input = input(">> Nhập lựa chọn (1/2/3): ").strip()
            if loai_input == '1':
              loai = "Loyal"
              break
            elif loai_input == '2':
              loai = "Casual"
              break
            elif loai_input == '3' or loai_input == '':
              loai = None
              break
            else:
              print("\033[91mLựa chọn không hợp lệ. Vui lòng chọn 1, 2 hoặc 3.\033[0m")

        ten_chua = input("Tên chứa (bỏ trống nếu không): ")
        email_chua = input("Email chứa (bỏ trống nếu không): ")
        ma_kh = input("Mã KH (bỏ trống nếu không): ")
        sdt_chua = input("SĐT chứa (bỏ trống nếu không): ")
        
        try:
            tong_gia_min = input("Tổng giá trị tối thiểu (bỏ trống nếu không): ")
            tong_gia_min = float(tong_gia_min) if tong_gia_min else None
            
            tong_gia_max = input("Tổng giá trị tối đa (bỏ trống nếu không): ")
            tong_gia_max = float(tong_gia_max) if tong_gia_max else None
            
            so_lan_mua_min = input("Số lần mua tối thiểu (bỏ trống nếu không): ")
            so_lan_mua_min = int(so_lan_mua_min) if so_lan_mua_min else None
            
            loading()
            ket_qua = ql.tim_kiem_nang_cao(
                loai=loai,
                ten_chua=ten_chua,
                email_chua=email_chua,
                ma_kh=ma_kh,
                sdt_chua=sdt_chua,
                tong_gia_min=tong_gia_min,
                tong_gia_max=tong_gia_max,
                so_lan_mua_min=so_lan_mua_min
            )
        except ValueError:
            print("\033[91mGiá trị số không hợp lệ.\033[0m")
            return
    else:
        print("\033[91mLựa chọn không hợp lệ!\033[0m")
        return
        
    # Hiển thị kết quả tìm kiếm
    if ket_qua:
        print(f"\n🔍 Kết quả tìm kiếm ({len(ket_qua)} khách hàng):")
        for kh in ket_qua:
            ql.in_thong_tin(kh)
    else:
        print("\033[91mKhông tìm thấy khách hàng.\033[0m")

def hien_thi_danh_sach(ql):
    """Chức năng hiển thị danh sách khách hàng"""
    print("\n=== HIỂN THỊ DANH SÁCH KHÁCH HÀNG ===")
    # Thêm tùy chọn lọc theo loại
    print("\nChọn loại khách hàng để hiển thị:")
    print("1. Loyal (Thân thiết)")
    print("2. Casual (Vãng lai)")
    print("3. Tất cả khách hàng")
    
    loai = None
    loai_choice = input(">> Nhập lựa chọn (1/2/3): ").strip()
    if loai_choice == '1':
        loai = 'Loyal'
    elif loai_choice == '2':
        loai = 'Casual'
        
    # Tùy chọn sắp xếp
    print("\nSắp xếp theo:")
    print("1. Mã khách hàng")
    print("2. Tên khách hàng")
    print("3. Số điện thoại")
    print("4. Tổng giá trị mua hàng (chỉ áp dụng cho khách vãng lai)")
    
    sort_field_map = {
        '1': 'ma_khach_hang',
        '2': 'ten_khach_hang',
        '3': 'so_dien_thoai',
        '4': 'tong_gia_tri_mua_hang'
    }
    
    sort_choice = input(">> Chọn trường sắp xếp (1-4): ")
    if sort_choice in sort_field_map:
        sort_field = sort_field_map[sort_choice]
    else:
        print("\033[93mLựa chọn không hợp lệ, sắp xếp theo mã khách hàng.\033[0m")
        sort_field = 'ma_khach_hang'
    
    # Thứ tự sắp xếp
    order = input("Sắp xếp tăng dần (asc) hay giảm dần (desc)? ").strip().lower()
    
    loading()
    ql.hien_thi_danh_sach(key_sort=sort_field, reverse=(order == 'desc'), loai=loai)

if __name__ == '__main__':
    main()