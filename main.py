from managers.manage_customer import ManageCustomer
from models.customer import LoyalCustomer, CasualCustomer
from utils.helpers import clear_screen, loading, nhap_sdt

def main():
    ql = ManageCustomer()

    while True:
        print("\n\033[96m╔══════════════════════════════════════════════╗\033[0m")
        print("\033[96m║             QUẢN LÝ KHÁCH HÀNG                ║\033[0m")
        print("\033[96m╠══════════════════════════════════════════════╣\033[0m")
        print("\033[93m║ 1. Thêm khách hàng                            ║\033[0m")
        print("\033[93m║ 2. Sửa thông tin khách hàng                   ║\033[0m")
        print("\033[93m║ 3. Xóa khách hàng                             ║\033[0m")
        print("\033[93m║ 4. Cập nhật mua hàng                          ║\033[0m")
        print("\033[93m║ 5. Tìm kiếm khách hàng                        ║\033[0m")
        print("\033[93m║ 6. Hiển thị danh sách (có sắp xếp)             ║\033[0m")
        print("\033[93m║ 7. Thống kê và Vẽ biểu đồ                     ║\033[0m")
        print("\033[93m║ 8. Top 3 khách hàng mua nhiều                 ║\033[0m")
        print("\033[93m║ 9. Tìm kiếm nâng cao                          ║\033[0m")
        print("\033[91m║ 0. Thoát                                       ║\033[0m")
        print("\033[96m╚══════════════════════════════════════════════╝\033[0m")
        choice = input("\033[95m>> Chọn chức năng (0-9): \033[0m")

        if choice == '1':
            ma = input("Mã KH: ")
            ten = input("Tên KH: ")
            sdt = nhap_sdt()
            while True:
               email = input("Email: ").strip()
               # Regex kiểm tra email
               if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                   break
               else:
                   print("\033[91mEmail không đúng định dạng. Vui lòng nhập lại.\033[0m")
            while True:
               loai = input("Loại (Loyal/Casual): ").strip().capitalize()
               if loai in ['Loyal', 'Casual']:
                  break
               else:
                  print("\033[91mLoại khách hàng không hợp lệ. Vui lòng nhập lại (Loyal hoặc Casual).\033[0m")

             if loai == 'Loyal':
                  kh = LoyalCustomer(ma, ten, sdt, email)
             else:
                  kh = CasualCustomer(ma, ten, sdt, email)

            loading()
            ql.them_khach_hang(kh)

        elif choice == '2':
            ma = input("Nhập mã KH cần sửa: ")
            ten_moi = input("Tên mới: ")
            email_moi = input("Email mới: ")
            loading()
            ql.sua_thong_tin(ma, ten_moi, email_moi)

        elif choice == '3':
            ma = input("Nhập mã KH cần xóa: ")
            loading()
            ql.xoa_khach_hang(ma)

        elif choice == '4':
            ma = input("Nhập mã KH: ")
            so_lan = int(input("Số lần mua: "))
            gia_tri = float(input("Tổng giá trị đơn hàng: "))
            loading()
            ql.cap_nhat_mua_hang(ma, so_lan, gia_tri)

        elif choice == '5':
            ma = input("Mã KH (bỏ qua nếu không tìm theo mã): ")
            ten = input("Tên KH (bỏ qua nếu không tìm theo tên): ")
            sdt = input("SĐT (bỏ qua nếu không tìm theo SĐT): ")
            email = input("Email (bỏ qua nếu không tìm theo Email): ")
            ket_qua = ql.tim_kiem(ma_kh=ma, ten=ten, sdt=sdt, email=email)
            loading()
            if ket_qua:
              for kh in ket_qua:
               ql.in_thong_tin(kh)
            else:
               print("\033[91mKhông tìm thấy khách hàng.\033[0m")

        elif choice == '6':
            sort_field = input("Sắp xếp theo trường nào (ma_khach_hang/ten_khach_hang/so_dien_thoai/tong_gia_tri_mua_hang): ")
            order = input("Tăng (asc) hay giảm (desc)? ").strip().lower()
            loading()
            ql.hien_thi_danh_sach(key_sort=sort_field, reverse=(order == 'desc'))

        elif choice == '7':
            loading()
            ql.thong_ke()

        elif choice == '8':
            kieu = input("Lọc theo tổng tiền hay số lần mua (gia_tri/so_lan): ").strip()
            top = ql.top_khach_hang(kieu)
            if not top:
                print("\033[91mKhông có khách hàng nào.\033[0m")
            else:    
                for kh in top:
                    ql.in_thong_tin(kh)
        elif choice == '9':
            loai = input("Loại khách hàng (Loyal/Casual/bỏ trống nếu không): ").strip().capitalize()
            ten_chua = input("Tên chứa (bỏ trống nếu không): ")
            tong_gia_min = input("Tổng giá trị tối thiểu (bỏ trống nếu không): ")
            tong_gia_min = float(tong_gia_min) if tong_gia_min else None
            tong_gia_max = input("Tổng giá trị tối đa (bỏ trống nếu không): ")
            tong_gia_max = float(tong_gia_max) if tong_gia_max else None
            so_lan_mua_min = input("Số lần mua tối thiểu (bỏ trống nếu không): ")
            so_lan_mua_min = int(so_lan_mua_min) if so_lan_mua_min else None
    
            ket_qua = ql.tim_kiem_nang_cao(loai=loai if loai else None, ten_chua=ten_chua, 
                                   tong_gia_min=tong_gia_min, tong_gia_max=tong_gia_max,
                                     so_lan_mua_min=so_lan_mua_min)
            loading()
            if ket_qua:
                 for kh in ket_qua:
                     ql.in_thong_tin(kh)
            else:
                print("\033[91mKhông tìm thấy khách hàng.\033[0m")
    

        elif choice == '0':
            print("\033[92mCảm ơn bạn đã sử dụng chương trình. Tạm biệt!\033[0m")
            break
        else:
            print("\033[91m❌ Lựa chọn không hợp lệ. Vui lòng chọn lại!\033[0m")

if __name__ == '__main__':
    main()

