import pandas as pd

# CSV 파일 경로
file_path = 'data.csv'

# CSV 파일 읽기
df = pd.read_csv(file_path, encoding='cp949')

# 데이터프레임 내용 출력
print(dict(df.head(50)))