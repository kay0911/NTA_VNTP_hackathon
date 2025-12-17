import csv

def load_csv(path):
    data = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            qid = row["qid"].strip()
            ans = row["answer"].strip()
            data[qid] = ans
    return data


def compare_csv(file1, file2):
    data1 = load_csv(file1)
    data2 = load_csv(file2)

    only_in_1 = sorted(set(data1.keys()) - set(data2.keys()))
    only_in_2 = sorted(set(data2.keys()) - set(data1.keys()))
    common = sorted(set(data1.keys()) & set(data2.keys()))

    diff_answers = []
    for qid in common:
        if data1[qid] != data2[qid]:
            diff_answers.append((qid, data1[qid], data2[qid]))

    print("\n===== KẾT QUẢ SO SÁNH CSV =====\n")

    print(f"🔹 Số QID chỉ có trong {file1}: {len(only_in_1)}")
    for q in only_in_1:
        print("  -", q)

    print(f"\n🔹 Số QID chỉ có trong {file2}: {len(only_in_2)}")
    for q in only_in_2:
        print("  -", q)

    print(f"\n🔹 Số QID trùng nhưng đáp án KHÁC nhau: {len(diff_answers)}")
    for qid, a1, a2 in diff_answers:
        print(f"  - {qid}: {a1} vs {a2}")

    print("\n===== HOÀN TẤT =====\n")


if __name__ == "__main__":
    file1 = "submission.csv"
    file2 = "submission1.csv"
    compare_csv(file1, file2)
