# Caro_AI
The Caro AI game with a strong heuristic AI built on minimax and alpha-beta pruning. The codebase has grown from a compact student project into a version with deeper search, optional native acceleration, benchmark tooling, and configurable difficulty.
# Tính năng nổi bật
Không yêu cầu thư viện ngoài: Toàn bộ logic và giao diện được xây dựng bằng Python thuần và thư viện chuẩn `tkinter`. Không cần cài đặt môi trường phức tạp.
Giao diện trực quan (GUI):Bàn cờ trực quan, cho phép người chơi tương tác trực tiếp bằng chuột.
Tùy chỉnh thuật toán:Cho phép chuyển đổi linh hoạt giữa Minimax thuần và Alpha-Beta theo thời gian thực để so sánh tốc độ.
Tùy chỉnh độ khó:Thay đổi độ sâu tìm kiếm (Depth 1, 2, 3) để điều chỉnh độ thông minh của AI.
# Hướng dẫn cài đặt và Chạy chương trình
Dự án được thiết kế để có thể chạy "ngay lập tức" (plug-and-play) trên mọi hệ điều hành (Windows, macOS, Linux) miễn là máy tính của bạn đã cài đặt Python.
## 1. Yêu cầu hệ thống
Đã cài đặt **Python 3.8** trở lên. (Tải tại: [python.org](https://www.python.org/))
## 2. Cài đặt dự án:Tải mã nguồn
Mở Terminal tại thư mục bạn muốn lưu dự án và gõ lệnh:
### Bước 1: Tải toàn bộ mã nguồn từ GitHub của bạn về máy
git clone https://github.com/manhngoc2682005-jpg/23021316_23021370.git
### Bước 2: Di chuyển con trỏ Terminal vào bên trong thư mục dự án vừa tải về
cd 23021316_23021370
### Bước 3: Khởi chạy file game (Nơi chứa giao diện Tkinter)
python src/main.py
