FROM python:3.10-slim

# SYSTEM DEPENDENCIES 
# Cài đặt Python, Pip và các gói hệ thống cần thiết 
# ------------------------------------------------------------ 
RUN apt-get update && apt-get install -y \ 
   python3 \ 
   python3-pip \ 
   git \ 
   && rm -rf /var/lib/apt/lists/* 

WORKDIR /code

COPY requirements.txt .
# INSTALL LIBRARIES 
# ------------------------------------------------------------ 
# Nâng cấp pip và cài đặt các thư viện từ requirements.txt 
RUN pip3 install --no-cache-dir --upgrade pip && \ 
   pip3 install --no-cache-dir -r requirements.txt 

COPY . .

RUN chmod +x inference.sh

ENV PYTHONUNBUFFERED=1

CMD ["bash", "inference.sh"]
