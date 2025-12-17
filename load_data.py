import json
from typing import List
import os
from dataclasses import dataclass
from typing import Dict

@dataclass
class QAItem_val:
    qid: str
    question: str
    choices: Dict[str, str]   # A/B/C/D...
    answer: str               # ví dụ: "C"

@dataclass
class QAItem_test:
    qid: str
    question: str
    choices: Dict[str, str]   # A/B/C/D...

def label_choices(choices: list[str]) -> dict[str, str]:
    return {
        chr(ord('A') + i): choice
        for i, choice in enumerate(choices)
    }

def format_choices(choices: dict) -> str:
    return "\n".join(
        f"{k}. {v}" for k, v in choices.items()
    )


def load_val_data(json_path: str) -> List[QAItem_val]:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    qa_items = []
    for item in data:
        labeled_choices = label_choices(item["choices"])
        formated_choices = format_choices(labeled_choices)
        qa_items.append(
            QAItem_val(
                qid=item["qid"],
                question=item["question"],
                choices=formated_choices,
                answer=item["answer"] 
            )
        )

    return qa_items

def load_test_data(json_path: str) -> List[QAItem_test]:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    qa_items = []
    for item in data:
        labeled_choices = label_choices(item["choices"])
        formated_choices = format_choices(labeled_choices)
        qa_items.append(
            QAItem_test(
                qid=item["qid"],
                question=item["question"],
                choices=formated_choices
            )
        )

    return qa_items
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VAL_PATH = os.path.join(BASE_DIR, "data/val.json")
TEST_PATH = os.path.join(BASE_DIR, "data/test.json")

val_data = load_val_data(VAL_PATH)
test_data = load_test_data(TEST_PATH)

private_test_PATH = os.path.join(BASE_DIR, "private_test.json")
private_test_data = load_test_data(private_test_PATH)