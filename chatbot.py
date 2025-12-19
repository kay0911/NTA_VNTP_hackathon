from config import config
import requests

def Prompt(content,type="normal"):
    add_ct = ""
    add_sys = ""
    add_ans = "<ANSWER>test_0001,A</ANSWER>\n<ANSWER>test_0002,B</ANSWER>\n<ANSWER>test_0003,C</ANSWER>"
    if type == "rag":
        add_sys = ". Dựa trên Thông tin đã cho."
        add_ct = f"""
- Chỉ được sử dụng thông tin trong "Đoạn thông tin:".
- Không được sử dụng kiến thức ngoài ngữ cảnh.
- Không được bịa, không suy luận vượt quá dữ liệu.
- Không suy luận từng bước ra ngoài.
        """

    if type == "stem":
        add_sys = "chuyên trả lời các câu hỏi STEM (Toán, Lý, Hóa, Kinh tế, Tài chính, Định lượng)."
        add_ct = f"""
- Chỉ sử dụng dữ liệu trong câu hỏi và đáp án.
- Hãy đọc kỹ số liệu, ký hiệu, đơn vị và công thức.
- Thực hiện đầy đủ suy luận và tính toán trong nội bộ hoặc phần giải thích.
- Sau khi có kết quả, hãy so sánh với TẤT CẢ các đáp án.
- Nếu các đáp án gần giống nhau, hãy kiểm tra lại một lần nữa.
- Giải thích ngắn gọn phải nằm giữa hai thẻ <EXPLAIN>...</EXPLAIN>
- Dòng trả lời BẮT BUỘC là dòng duy nhất nằm sau thẻ </EXPLAIN>
        """
        add_ans = f"""
<EXPLAIN>...</EXPLAIN>
<ANSWER>test_0001,A</ANSWER>
<EXPLAIN>...</EXPLAIN>
<ANSWER>test_0002,B</ANSWER>
<EXPLAIN>...</EXPLAIN>
<ANSWER>test_0003,C</ANSWER>
        """
    if type == "many":
        add_ct = f"""
- Lưu ý số lượng đáp án có thể nhiều hơn 4, hãy chọn phương án phù hợp nhất trong tất cả các đáp án.
- Lưu ý những câu hỏi phủ định thường chứa từ "không" nên đọc kỹ.
- Không giải thích.
"""
    if type == "normal":
        add_sys = ". Am hiểu về pháp luật Việt Nam."
        add_ct = f"""
- - Không suy luận từng bước ra ngoài.
- Lưu ý những câu hỏi phủ định thường chứa từ "không" nên đọc kỹ.
- Không giải thích.
"""
    system_prompt = f"""
Bạn là một hệ thống trả lời câu hỏi trắc nghiệm. {add_sys}

Quy tắc nghiêm ngặt:
- Mỗi câu hỏi là ĐỘC LẬP, nhăn cách nhau các dấu "-------------------".
- Hãy trả lời tất cả những câu hỏi.
{add_ct}
- qid và Đáp_án phải nằm giữa hai thẻ <ANSWER>qid,Đáp_án</ANSWER>
- TUYỆT ĐỐI KHÔNG lặp lại cùng một câu hỏi.
- Nếu không chắc chắn, chọn đáp án gần đúng nhất và tiếp tục.

Ví dụ:
{add_ans}
    """
    prompt = f"""
Câu hỏi và các đáp án:
{content}

    """
    return system_prompt, prompt

def extract_llm_content(response):
    try:
        data = response.json()
    except Exception:
        return None, "Invalid JSON response"

    # ✅ Case 1: trả lời thành công
    if "choices" in data and len(data["choices"]) > 0:
        return data["choices"][0]["message"]["content"], None

    # ❌ Case 2: API trả lỗi
    if "error" in data:
        return None, data["error"].get("message", "Unknown error")

    # ❌ Case 3: format lạ
    return None, "Unexpected response format"


def LLM_Calling(model="LLM small",temp=0.0,p=1.0,k=20,tokens = 512,prompt="",s_prompt=""):
    model_cfg = config.get_by_api_name(model)
    headers = { 
        'Authorization': model_cfg.authorization,
        'Token-id': model_cfg.tokenId,
        'Token-key': model_cfg.tokenKey,
        'Content-Type': 'application/json',
    }

    md = ""
    link = "https://api.idg.vnpt.vn/data-service/v1/chat/completions/"
    
    if model == "LLM small":
        md = "vnptai_hackathon_small"
        link_endpoint = link + "vnptai-hackathon-small"
    else: 
        md = "vnptai_hackathon_large"
        link_endpoint = link + "vnptai-hackathon-large"


    json_data = { 
        'model': md, 
        'messages': [ 
            {
                'role': 'system', 
                'content': s_prompt, 
            },
            { 
                'role': 'user', 
                'content': prompt, 
            }, 
        ], 
        'temperature': temp, 
        'top_p': p, 
        'top_k': k, 
        'n': 1, 
        'max_completion_tokens': tokens,
    }
    try:
        response = requests.post(
            link_endpoint,
            headers=headers,
            json=json_data,
            timeout=60
        )
    except requests.exceptions.Timeout:
        return "[TIMEOUT] LLM request timed out", False
    except requests.exceptions.ConnectionError as e:
        return f"[CONNECTION_ERROR] {e}", False
    except Exception as e:
        return f"[REQUEST_ERROR] {e}", False

    answer, message = extract_llm_content(response)

    if answer is not None:
        return answer, True
    else:
        return message, False

