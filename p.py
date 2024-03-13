from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI


# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

# 환경 변수를 사용하여 API 키를 불러옵니다.
openai_api_key = os.getenv('NEW_API_KEY')

model = ChatOpenAI(api_key=openai_api_key)
