import time
from datetime import datetime

from classify import classify_dataset
from load_data import private_test_data
from chatbot import LLM_Calling, Prompt
from build import build_blocks, append_raw_text, clear_txt_file, run_sensitive_questions, parse, question_time, clear_csv, merge_time_into_answers

def main():
    # =========================
    # 1️⃣ PHÂN LOẠI (ĐÃ TỐI ƯU)
    # =========================
    sensitive_q, rag_q, stem_q, many_q, normal_q = classify_dataset(private_test_data)

    print("Sensitive:", len(sensitive_q))
    print("RAG:", len(rag_q))
    print("STEM:", len(stem_q))
    print("Many:", len(many_q))
    print("Normal:", len(normal_q))

    clear_txt_file()
    clear_csv()

    print("\n🛡️ HANDLE SENSITIVE QUESTIONS (NO LLM)")
    run_sensitive_questions(sensitive_q)

    # =========================
    # 2️⃣ CONFIG
    # =========================
    MODEL_NAME = {
        "normal": "LLM large",
        "many": "LLM large",
        "rag": "LLM large",
        "stem": "LLM small"
    }

    Temp = {
        "normal": 0.0,
        "many": 0.0,
        "rag": 0.0,
        "stem": 0.0
    }

    MAX_TOKENS_SIZE = {
        "normal": 256,
        "many": 256,
        "rag": 256,
        "stem": 8192
    }

    BATCH_SIZE = {
        "normal": 10,
        "many": 10,
        "rag": 10,
        "stem": 5
    }

    def run_blocks(data, q_type):
        if not data:
            return 0, 0.0

        blocks = build_blocks(
            data,
            block_size=BATCH_SIZE[q_type]
        )

        print(f"\n🚀 Running [{q_type.upper()}] "
            f"| Blocks: {len(blocks)} "
            f"| Batch size: {BATCH_SIZE[q_type]}")

        total_time = 0.0

        for i, block in enumerate(blocks, start=1):
            start = time.perf_counter()
        
            S_prompt, prompt = Prompt(block[0], type=q_type)
            answer = LLM_Calling(
                model=MODEL_NAME[q_type],
                tokens=MAX_TOKENS_SIZE[q_type],
                temp=Temp[q_type],
                s_prompt=S_prompt,
                prompt=prompt
            )
            append_raw_text(answer)

            elapsed = time.perf_counter() - start

            for qid in block[1]:
                question_time(qid,elapsed/len(block[1]))

            total_time += elapsed

            print(f"✅ {q_type} | Block {i}/{len(blocks)} | {elapsed:.2f}s")

        return len(blocks), total_time


    # =========================
    # 3️⃣ CHẠY THEO LOẠI
    # =========================
    print("\n🟢 START RUN")
    start_datetime = datetime.now()
    print(f"🕒 Start time : {start_datetime:%Y-%m-%d %H:%M:%S}")

    global_start = time.perf_counter()

    total_blocks = 0
    total_time = 0.0

    for dataset, q_type in [
        (normal_q, "normal"),
        (many_q, "many"),
        (rag_q, "rag"),
        (stem_q, "stem")
    ]:
        blocks, t = run_blocks(dataset, q_type)
        total_blocks += blocks
        total_time += t


    # =========================
    # 4️⃣ TỔNG KẾT
    # =========================
    elapsed = time.perf_counter() - global_start
    end_datetime = datetime.now()

    print("\n🔴 END RUN")
    print(f"🕒 End time   : {end_datetime:%Y-%m-%d %H:%M:%S}")
    print(f"⏱️ Total     : {elapsed:.2f}s")
    print(f"📦 Blocks    : {total_blocks}")

    if total_blocks:
        print(f"📊 Avg/block : {total_time / total_blocks:.2f}s")

if __name__ == "__main__":
    main()
    parse()
    merge_time_into_answers()