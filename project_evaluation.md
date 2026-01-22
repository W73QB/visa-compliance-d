# Báo cáo Đánh giá Dự án: VisaFact Compliance Checker

## 1. Tổng quan Dự án
**VisaFact** là một nền tảng kiểm tra tính tuân thủ bảo hiểm cho thị thực (visa), tập trung vào "bằng chứng" (evidence-based). Hệ thống so sánh các yêu cầu của thị thực (VisaFacts) với các thông số của sản phẩm bảo hiểm (ProductFacts) để đưa ra kết quả tuân thủ.

*   **Mục tiêu chính**: Cung cấp kết quả kiểm tra tuân thủ dựa trên nguồn dữ liệu chính thống. Nguyên tắc cốt lõi: "No source = UNKNOWN" (Không có nguồn = Không xác định).
*   **Loại hình**: Static Web Application (Ứng dụng web tĩnh) với logic xử lý dữ liệu được thực hiện trước (pre-computed).

## 2. Kiến trúc Hệ thống

Dự án áp dụng kiến trúc **Static Site Generator (SSG) với Data Pipeline**:

1.  **Dữ liệu nguồn (Data Layer)**:
    *   Lưu trữ dưới dạng JSON trong thư mục `data/` (`visas`, `products`, `mappings`).
    *   Được kiểm soát chặt chẽ bởi JSON Schema (`schemas/`), đảm bảo tính nhất quán dữ liệu.

2.  **Xử lý Logic (Build-time Logic)**:
    *   Sử dụng Python (`tools/`) để đóng vai trò "Engine".
    *   Script `build_mappings.py` thực hiện so khớp giữa yêu cầu visa và sản phẩm bảo hiểm *tại thời điểm build*, thay vì runtime.
    *   Kết quả so khớp được lưu thành các file JSON tĩnh.

3.  **Giao diện (Presentation Layer)**:
    *   Sử dụng **Hugo** để tạo cấu trúc trang web và blog.
    *   Sử dụng **Vanilla JavaScript** và **Tailwind CSS** cho ứng dụng kiểm tra (`Checker UI`) tại `ui/index.html`.
    *   Trình duyệt chỉ việc tải JSON đã tính toán sẵn (`ui_index.json`) để hiển thị, giúp tốc độ cực nhanh và bảo mật cao.

## 3. Phân tích Chi tiết Mã nguồn

### 3.1. Backend / Data Processing (`tools/`)
*   **Điểm mạnh**:
    *   Mã nguồn Python rõ ràng, dễ đọc. Sử dụng `pathlib` hiện đại.
    *   Logic kiểm tra (`evaluate` function trong `build_mappings.py`) rất chi tiết, bao quát nhiều trường hợp cụ thể (deductible, co-payment, authorized in Spain...).
    *   Có các script kiểm tra (sanity check) như `validate.py` và `smoke.py` giúp phát hiện lỗi sớm.
*   **Điểm cần lưu ý**:
    *   Hàm `evaluate` trong `build_mappings.py` chứa nhiều logic `if/else` cứng (hardcoded). Khi số lượng quy tắc tăng lên, file này sẽ rất khó bảo trì.
    *   **Khuyến nghị**: Nên tách các quy tắc (rules) thành các class hoặc module riêng (Strategy Pattern) hoặc cấu hình hóa chúng thay vì viết cứng trong code.

### 3.2. Frontend (`ui/`)
*   **Điểm mạnh**:
    *   Giao diện người dùng (UI) được chăm chút kỹ lưỡng với các hiệu ứng động (animations), trạng thái rõ ràng (Loading, Empty, Result).
    *   Không sử dụng Framework nặng (React/Vue) giúp giảm tải cho trình duyệt và đơn giản hóa việc triển khai.
    *   Accessibility (A11y) tốt: Hỗ trợ phím điều hướng, dark mode.
*   **Điểm cần lưu ý**:
    *   Sử dụng Tailwind CSS qua CDN (`<script src="https://cdn.tailwindcss.com...">`). Điều này không tối ưu cho Production vì trình duyệt phải tải và parse toàn bộ thư viện Tailwind mỗi lần load, và có thể gây hiện tượng "Flash of Unstyled Content".
    *   Toàn bộ logic JS nằm chung trong một file HTML lớn (~1000 dòng).
    *   **Khuyến nghị**:
        *   Thiết lập quy trình build CSS cho Tailwind để tạo ra file CSS tĩnh nhỏ gọn.
        *   Tách code JS ra thành các file module (.js) riêng biệt nếu logic phát triển thêm.

### 3.3. Dữ liệu (`data/` & `schemas/`)
*   Việc sử dụng JSON Schema là một điểm cộng lớn, giúp đảm bảo dữ liệu đầu vào luôn đúng cấu trúc trước khi code xử lý chạy.
*   Cấu trúc dữ liệu tách biệt rõ ràng giữa `visas` (yêu cầu) và `products` (khả năng đáp ứng), giúp hệ thống linh hoạt khi thêm mới một trong hai.

## 4. Đánh giá Tổng thể

### Ưu điểm
*   **Hiệu năng cao**: Do là web tĩnh hoàn toàn.
*   **Chi phí vận hành thấp**: Không cần server backend, database động.
*   **Độ tin cậy cao**: Dữ liệu được validate kỹ càng, logic được kiểm thử trước khi deploy.
*   **UX tốt**: Giao diện chuyên nghiệp, phản hồi nhanh.

### Nhược điểm / Rủi ro
*   **Khả năng mở rộng logic**: Logic so khớp (`build_mappings.py`) đang viết theo kiểu thủ tục (procedural), sẽ khó mở rộng nếu quy tắc nghiệp vụ trở nên phức tạp hơn.
*   **Quy trình phát triển Frontend**: Thiếu build tool chuẩn cho CSS/JS (đang dùng CDN và inline code), làm giảm khả năng quản lý code frontend về lâu dài.

## 5. Kết luận
Dự án **Visa Compliance Database** được xây dựng với tư duy kỹ thuật tốt, lựa chọn công nghệ phù hợp với bài toán "Compliance Checker" (cần độ chính xác và minh bạch cao). Kiến trúc Static Site + Build-time Logic là lựa chọn xuất sắc cho loại hình ứng dụng này.

Để dự án phát triển bền vững hơn, nên tập trung vào việc:
1.  Refactor `build_mappings.py` để tách logic nghiệp vụ.
2.  Thiết lập quy trình build assets (CSS/JS) chuẩn chỉnh hơn.
