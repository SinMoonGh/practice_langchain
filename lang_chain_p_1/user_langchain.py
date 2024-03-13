# from google.colab import userdata
# userdata.get('NEW_API_KEY')

from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

# 환경 변수를 사용하여 API 키를 불러옵니다.
openai_api_key = os.getenv('NEW_API_KEY')

llm = ChatOpenAI(openai_api_key=openai_api_key)

# from langchain_core.prompts import ChatPromptTemplate
# from langchain_openai import ChatOpenAI

# prompt = ChatPromptTemplate.from_template("tell me a joke about {foo}")
# model = ChatOpenAI(api_key=openai_api_key)
# chain = prompt | model

# # OpenAI API 키 설정
# openai.api_key = openai_api_key

# llm = ChatOpenAI()

# # GPT-3 모델을 사용하여 일자리 정보 요청 작성
# prompt = "새로운 일자리 정보를 얻고 싶습니다."

# # OpenAI API 호출
# response = llm.send(prompt)

# # 생성된 일자리 정보 출력
# job_info = response['choices'][0]['message']['content']
# print(job_info)

output = llm.invoke("2024년 청년 지원 정책에 대하여 알려줘")

prompt = ChatPromptTemplate.from_messages([
    ("system", "너는 청년을 행복하게 하기 위한 정부정책 안내 컨설턴트야"),
    ("user", "청년이 행복하기 위한 방법은 뭐야?")
])
chain = prompt | llm

# def square_numbers(numbers):
#     return [n ** 2 for n in numbers]

# def sum_numbers(numbers):
#     return sum(numbers)

# # 숫자 리스트
# numbers = [1, 2, 3, 4]

# # 파이프 연산자를 사용하여 함수 연결
# result = numbers | square_numbers | sum_numbers

# print(result)  # 출력: 30


chain.invoke({"input": "2024년 청년 지원 정책에 대해 알려줘"})

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

chain.invoke({"input": "2024년 청년 지원 정책에 대해 알려줘"})

print(chain)

# chain.invoke({"input": "2024년 청년 지원 정책에 대해 알려줘"})


loader = WebBaseLoader("https://www.moel.go.kr/policy/policyinfo/support/list4.do")

docs = loader.load()

embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

