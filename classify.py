import re

MATH_SYMBOLS = r"[%^$]"

# Đáp án thuần số
NUMBER_PATTERN = r"^\s*\d+(\.\d+)?\s*$"

# Đơn vị đo lường thông dụng
UNITS = [
    r"kg", r"g", r"mg", r"km", r"m", r"cm", r"mm",
    r"l", r"ml", r"kWh", r"m/s", r"m2", r"m3",
    r"%", r"°c", r"độ c"
]

# Đơn vị vật lý
PHYSICS_UNITS = [
    r"ω", r"ohm", r"Ω",
    r"ev", r"mev", r"kev",
    r"j", r"n", r"w", r"v", r"a",
    r"hz", r"ghz", r"pa"
]

# Đơn vị tiền tệ nâng cao
CURRENCY_UNITS = [
    # Việt Nam
    r"vnd", r"vnđ", r"đồng", r"dong", r"đ", r"d", r"₫", r"nghìn", r"ngàn",
    r"triệu", r"tỷ", r"tỉ",

    # Quốc tế
    r"usd", r"eur", r"gbp", r"jpy", r"cny", r"krw", r"sgd", r"aud", r"cad",
    r"chf", r"hkd", r"thb", r"inr", r"dollar", r"cent", r"đô la",

    # Viết tắt tiền tệ kiểu mạng
    r"\d+k", r"\d+m", r"\d+b"
]

# Regex số + đơn vị (đo lường + vật lý + tiền tệ)
ALL_UNITS_REGEX = r"\b(\d+(\.\d+)?\s*(" + "|".join(UNITS + PHYSICS_UNITS + CURRENCY_UNITS) + r"))\b"



def parse_choices(choices_str):
    """Tách A., B., C. thành list"""
    lines = [l.strip() for l in choices_str.split("\n") if l.strip()]
    return lines

SENSITIVE_KEYWORDS = [
    "chống lại đường lối",
    "chống phá ", "trì hoãn", "làm giả ",
    "xúc phạm", "đình chỉ",
    "biểu tình bất hợp pháp", "tài liệu mật",
    "lôi kéo", "hối lộ", "tham nhũng",
    "thông tin sai lệch", "vi phạm pháp luật",
    "để phá hoại", "bôi nhọ", "chế ngạo", "trái quy định"
]
def safe_answer_from_choices(qid: str, choices: str) -> str | None:
    """
    Trả về chuỗi 'qid,ANS' nếu tìm thấy đáp án an toàn
    Ngược lại trả về None
    """
    for line in choices.split("\n"):
        text = line.lower()
        if (
            "tôi không thể" in text
            or "không biết" in text
            or "từ chối" in text
        ):
            ans = line.split(".", 1)[0].strip()  # A / B / C / D
            return f"<ANSWER>{qid},{ans}</ANSWER>"

    return None

def is_sensitive_question(question: str, choices: list[str]) -> bool:
    text = question.lower() + " " + " ".join(c.lower() for c in choices)
    return any(k in text for k in SENSITIVE_KEYWORDS)


def is_stem_question(question: str, choices: list[str]) -> bool:
    """Nhận diện câu hỏi STEM dựa trên ký hiệu toán học, số, hoặc đơn vị đo/vật lý."""

    text = question.lower() + " " + " ".join(c.lower() for c in choices)

    # 1. Chứa ký hiệu toán học
    if re.search(MATH_SYMBOLS, text):
        return True

    # 2. Đáp án là số thuần
    for c in choices:
        if re.match(NUMBER_PATTERN, c.strip()):
            return True
        # trường hợp dạng: "tăng 5%", "giảm 10%"
        if "tăng" in c.lower() or "giảm" in c.lower():
            if "%" in c.lower():
                return True

    # 3. Số + đơn vị vật lý hoặc đo lường
    if re.search(ALL_UNITS_REGEX, text):
        return True

    return False


def is_rag_question(question):
    return question.strip().lower().startswith("đoạn thông tin:")


def is_many_choice(choices):
    return len(choices) > 4


def classify_dataset(dataset):
    sensitive_q = []
    stem_q = []
    rag_q = []
    many_q = []
    normal_q = []

    for item in dataset:
        q = item.question
        c = parse_choices(item.choices)
        if is_rag_question(q):
            rag_q.append(item)
        elif is_sensitive_question(q,c):
            sensitive_q.append(item)
        elif is_stem_question(q, c):
            stem_q.append(item)
        elif is_many_choice(c):
            many_q.append(item)
        else:
            normal_q.append(item)

    return sensitive_q, rag_q, stem_q, many_q, normal_q



