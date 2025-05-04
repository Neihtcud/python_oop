from managers.manage_customer import ManageCustomer
from models.customer import LoyalCustomer, CasualCustomer
from utils.helpers import clear_screen, loading, nhap_sdt, nhap_ten, kiem_tra_email, nhap_email
import re

def main():
    ql = ManageCustomer()

    while True:
        print("\033[96m╔=═════════════════════════════════════════════=╗\033[0m")
        print("\033[96m║             QUẢN LÝ KHÁCH HÀNG                ║\033[0m")
        print("\033[96m╠══════════════════════════════════════════════=╣\033[0m")
        print("\033[93m║ 1. Thêm khách hàng                            ║\033[0m")
        print("\033[93m║ 2. Sửa thông tin khách hàng                   ║\033[0m")
        print("\033[93m║ 3. Xóa khách hàng                             ║\033[0m")
        print("\033[93m║ 4. Cập nhật mua hàng                          ║\033[0m")
        print("\033[93m║ 5. Tìm kiếm                                   ║\033[0m")
        print("\033[93m║ 6. Hiển thị danh sách (có sắp xếp)            ║\033[0m")
        print("\033[93m║ 7. Thống kê và Vẽ biểu đồ                     ║\033[0m")
        print("\033[93m║ 8. Hiển thị 3 khách hàng mua hàng nhiều nhất  ║\033[0m")
        print("\033[93m║ 9. Thống kê KH thân thiết tặng quà Tết        ║\033[0m")
        print("\033[91m║ 0. Thoát                                      ║\033[0m")
        print("\033[96m╚══════════════════════════════════════════════=╝\033[0m")
        choice = input("\033[95m>> Chọn chức năng (0-9): \033[0m")

        if choice == '1':
           ma = input("Mã KH: ")
           ten = nhap_ten()
           sdt = nhap_sdt()
           email = nhap_email()

           # Hiển thị menu chọn loại khách hàng
           print("\nChọn loại khách hàng:")
           print("1. Loyal (Thân thiết)")
           print("2. Casual (Thường)")

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
              kh = LoyalCustomer(ma, ten, sdt, email)
           elif loai == 'casual':
              kh = CasualCustomer(ma, ten, sdt, email)
           else:
              print("\033[91mLỗi: Loại khách hàng không xác định.\033[0m")
              continue  # Nếu không xác định được loại, quay lại menu chính

           loading()
           ql.them_khach_hang(kh)

        elif choice == '2':
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

        elif choice == '3':
            ma = input("Nhập mã KH cần xóa: ")
            loading()
            ql.xoa_khach_hang(ma)

        elif choice == '4':
            ma = input("Nhập mã KH: ")
            # Sử dụng tim_kiem_nang_cao thay vì tim_kiem
            kh = ql.tim_kiem_nang_cao(ma_kh=ma)
            if not kh:
                print("\033[91mKhông tìm thấy khách hàng.\033[0m")
                continue
            else:
                kh = kh[0]
                # Kiểm tra loại khách hàng
                if isinstance(kh, LoyalCustomer):
                    print("\033[91mKhách hàng thân thiết không cần cập nhật mua hàng.\033[0m")
                    continue
                print(f"Khách hàng: {kh.ten_khach_hang} ({kh.ma_khach_hang})")

            try:
                so_lan_raw = input("Số lần mua: ")
                gia_tri_raw = input("Tổng giá trị đơn hàng: ")
                so_lan = int(so_lan_raw)
                gia_tri = float(gia_tri_raw)
                
                loading()
                ql.cap_nhat_mua_hang(ma, so_lan, gia_tri)
            except ValueError:
                print("\033[91mSố lần mua hoặc giá trị đơn hàng không hợp lệ.\033[0m")
                continue

        elif choice == '5':
            print("🔎 Tìm kiếm :")
            print("\nChọn loại khách hàng:")
            print("1. Loyal (Thân thiết)")
            print("2. Casual (Thường)")
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
                continue

            if ket_qua:
               print(f"\n🔍 Kết quả tìm kiếm ({len(ket_qua)} khách hàng):")
               for kh in ket_qua:
                   ql.in_thong_tin(kh)
            else:
               print("\033[91mKhông tìm thấy khách hàng.\033[0m")    

        elif choice == '6':
            # Thêm tùy chọn lọc theo loại
            print("\nChọn loại khách hàng để hiển thị:")
            print("1. Loyal (Thân thiết)")
            print("2. Casual (Thường)")
            print("3. Tất cả khách hàng")
            
            loai = None
            loai_choice = input(">> Nhập lựa chọn (1/2/3): ").strip()
            if loai_choice == '1':
                loai = 'Loyal'
            elif loai_choice == '2':
                loai = 'Casual'
                
            sort_field = input("Sắp xếp theo trường nào (ma_khach_hang/ten_khach_hang/so_dien_thoai/tong_gia_tri_mua_hang): ")
            order = input("Tăng (asc) hay giảm (desc)? ").strip().lower()
            loading()
            ql.hien_thi_danh_sach(key_sort=sort_field, reverse=(order == 'desc'), loai=loai)
        elif choice == '7':
            loading()
            ql.thong_ke()
        elif choice == '8':
            loading()
            ql.thong_ke()
            # Hiển thị top khách hàng
            top_n = input("Hiển thị top bao nhiêu khách hàng? (mặc định: 3): ")
            try:
                top_n = int(top_n) if top_n else 3
                ql.hien_thi_top_khach_hang(n=top_n)
            except ValueError:
                print("\033[91mSố lượng không hợp lệ, hiển thị mặc định top 3.\033[0m")
                ql.hien_thi_top_khach_hang()
        
        elif choice == '9':
            loading()
            ql.thong_ke_khach_hang_than_thiet()

        elif choice == '0':
            print("\033[92mCảm ơn bạn đã sử dụng chương trình. Tạm biệt!\033[0m")
            break
        else:
            print("\033[91m❌ Lựa chọn không hợp lệ. Vui lòng chọn lại!\033[0m")
        
        # Thêm tùy chọn tiếp tục hoặc quay lại menu
        if choice != '0':
            input("\nNhấn Enter để tiếp tục...")
            clear_screen()  # Làm sạch màn hình trước khi hiển thị lại menu

if __name__ == '__main__':
    main()