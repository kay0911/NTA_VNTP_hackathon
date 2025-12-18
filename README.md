# VNPT BTC 2025 – Track 2: The Builder

## Mô tả
Repository này chứa giải pháp tham gia **VNPT Blockchain & AI Hackathon 2025 – Track 2 (The Builder)**.  
Hệ thống thực hiện suy luận và trả lời câu hỏi trắc nghiệm bằng cách gọi **VNPT LLM API**, sau đó xuất kết quả theo đúng định dạng BTC yêu cầu.

---

## Pipeline Flow
- Phân loại câu hỏi thành các nhóm: **Normal, Many choices, RAG, STEM**
- Xử lý theo batch để tối ưu số lần gọi API
- Sử dụng prompt chuyên biệt cho từng loại câu hỏi

---

## Cách chạy dự án

Dự án được đóng gói sẵn dưới dạng Docker image. Bạn **không cần cài Python hay thư viện** trên máy host.

---

### 1️⃣ Tải Docker image

```bash
docker pull kay0911/nta-vnpt-hackathon-track2
```

---

### 2️⃣ Chuẩn bị dữ liệu đầu vào

* Đặt file **`private_test.json`** vào một thư mục bất kỳ trên máy
* Mở terminal (hoặc CMD / PowerShell) **tại thư mục chứa file này**

Ví dụ:

```text
/private_test.json
```

---

### 3️⃣ Chạy container (mount dữ liệu đầu vào)

#### 🔹 Linux / macOS (Terminal)

```bash
docker run -v $(pwd)/private_test.json:/code/private_test.json -v $(pwd):/output kay0911/nta-vnpt-hackathon-track2
```

#### 🔹 Windows (CMD)

```cmd
docker run -v %cd%\private_test.json:/code/private_test.json -v %cd%:/output kay0911/nta-vnpt-hackathon-track2
```

#### 🔹 Windows (PowerShell)

```powershell
docker run -v ${PWD}\private_test.json:/code/private_test.json -v ${PWD}:/output kay0911/nta-vnpt-hackathon-track2
```

---

### 4️⃣ Nhận kết quả đầu ra

Sau khi container chạy xong, trong **thư mục hiện tại trên máy** sẽ xuất hiện:

* `submission.csv`
* `submission_time.csv`

---




