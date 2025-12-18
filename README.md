# VNPT BTC 2025 – Track 2: The Builder

## Mô tả
Repository này chứa giải pháp tham gia **VNPT Blockchain & AI Hackathon 2025 – Track 2 (The Builder)**.  
Hệ thống thực hiện suy luận và trả lời câu hỏi trắc nghiệm bằng cách gọi **VNPT LLM API**, sau đó xuất kết quả theo đúng định dạng BTC yêu cầu.

---

## Pipeline Flow
- Phân loại câu hỏi thành các nhóm: **Sensitive,Normal, Many choices, RAG, STEM**.
- Xử lý theo các gói câu hỏi thay vì chỉ 1 câu mỗi để tối ưu số lần gọi API, thời gian trả lời.
- Sử dụng prompt chuyên biệt cho từng loại câu hỏi(cân đối giữa độ chính xác và thơi gian.
- Sơ đồ Pipeline.
```mermaid

flowchart LR
    A[Bộ câu hỏi] -->|Input| B[Phần Classify]

    B -->|Base rule| C1[sensitive_q]
    B -->|Base rule| C2[rag_q]
    B -->|Base rule| C3[stem_q]
    B -->|Base rule| C4[many_q]
    B -->|Base rule| C5[normal_q]

    C1 -->|Answer rule| F[ANSWER]
    C2 --> D[Phần Build]
    C3 --> D
    C4 --> D
    C5 --> D

    D -->|Chia gói rag_q 10 câu| E1[Prompt riêng cho RAG]
    D -->|Chia gói stem_q 5 câu| E2[Prompt riêng cho STEM]
    D -->|Chia gói many_q 10 câu| E3[Prompt riêng cho MANY]
    D -->|Chia gói normal_q 10 câu| E4[Prompt riêng cho NORMAL]

    E1 --> F[ANSWER]
    E2 --> F
    E3 --> F
    E4 --> F

    F -->|Output| G1[submission.csv]
	F -->|Log time| G2[submission_time.csv]
```

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




