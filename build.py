import re
import csv
import os
import pandas as pd
from classify import safe_answer_from_choices
def format_one_question(item) -> str:
    content = f"""
QID: {item.qid}
Câu hỏi:
{item.question}

Lựa chọn:
{item.choices}
    """
    return content

def build_blocks(items, block_size=20):
    blocks = []
    
    for i in range(0, len(items), block_size):
        chunk = items[i:i + block_size]
        qid_list = []
        block = "\n" + "-" * 40 + "\n"
        for item in chunk:
            qid_list.append(item.qid)
            block += format_one_question(item)
            block += "\n" + "-" * 40 + "\n"

        blocks.append([block,qid_list])

    return blocks

def append_raw_text(text, path="answers_raw.txt"):
    with open(path, "a", encoding="utf-8") as f:
        f.write(text.strip())
        f.write("\n\n")   # cách block

def clear_txt_file(path="answers_raw.txt"):
    """Xóa toàn bộ nội dung file txt (giữ lại file trống)"""
    with open(path, "w", encoding="utf-8"):
        pass

def run_sensitive_questions(data, output_file="answers_raw.txt"):
    """
    Xử lý các câu hỏi nhạy cảm bằng rule-based,
    KHÔNG gọi LLM, ghi kết quả qid,ans vào file.
    """
    if not data:
        print("⚠️ No sensitive questions.")
        return 0

    count = 0

    with open(output_file, "a", encoding="utf-8") as f:
        for item in data:
            # ưu tiên đáp án an toàn
            ans = safe_answer_from_choices(item.qid, item.choices)

            if ans is None:
                # fallback cứng nếu không có đáp án an toàn
                ans = f"{item.qid},B"

            f.write(ans + "\n")
            count += 1

    print(f"🛡️ Sensitive handled: {count}")
    return count

def question_time(qid, time_value, output_file="answers_time.csv"):
    file_exists = os.path.exists(output_file)
    need_header = True

    if file_exists:
        # file tồn tại nhưng rỗng
        if os.path.getsize(output_file) > 0:
            need_header = False

    with open(output_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if need_header:
            writer.writerow(["qid", "time"])

        writer.writerow([qid, round(time_value, 4)])

def clear_csv(file_path="answers_time.csv"):
    with open(file_path, "w", newline="", encoding="utf-8"):
        pass


def sort_csv_by_qid(input_file, output_file=None):
    if output_file is None:
        output_file = input_file

    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames

    def qid_key(row):
        m = re.search(r"\d+", row["qid"])
        return int(m.group()) if m else float("inf")

    rows.sort(key=qid_key)

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def merge_time_into_answers(
    file_answer="submission.csv",
    file_time="answers_time.csv",
    output_file="submission_time.csv",
    default_time=0.01
):
    df_ans = pd.read_csv(file_answer)
    df_time = pd.read_csv(file_time)

    # merge theo qid (LEFT JOIN)
    df_merged = df_ans.merge(df_time, on="qid", how="left")

    # điền time mặc định nếu thiếu
    df_merged["time"] = df_merged["time"].fillna(default_time)

    df_merged.to_csv(output_file, index=False)


ANSWER_PATTERN = re.compile(
    r"<ANSWER>\s*([\w\d_]+)\s*,\s*([A-Z])\s*</ANSWER>",
    re.IGNORECASE
)

def parse(new_file ="submission.csv"):
    rows = []
    with open("answers_raw.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            m = ANSWER_PATTERN.match(line)
            if m:
                rows.append((m.group(1), m.group(2).upper()))

    # ✅ SẮP XẾP THEO SỐ TĂNG DẦN
    rows.sort(key=lambda x: int(x[0].split("_")[1]))

    with open(new_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["qid", "answer"])
        writer.writerows(rows)