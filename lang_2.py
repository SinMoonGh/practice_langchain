from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
import streamlit as st
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

# 환경 변수를 사용하여 API 키를 불러옵니다.
openai_api_key = os.getenv('NEW_API_KEY')

llm = ChatOpenAI(openai_api_key=openai_api_key)

st.header("크롤링 봇")
st.info("국민취업지원제도에 관련된 서비스를 제공합니다. 무엇이든 물어보세요.")
st.error("교육 커리큘럼 내용이 적용되어 있습니다.")

loader = WebBaseLoader("https://namu.wiki/w/%ED%8F%AC%EC%BC%93%EB%AA%AC%20%EB%8F%84%EA%B0%90")

docs = loader.load()

embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = FAISS.from_documents(documents, embeddings)

prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

document_chain = create_stuff_documents_chain(llm, prompt)

document_chain.invoke({
    "input": "피카츄의 속성을 알려줘",
    "context": [Document(page_content="""전국: 0001
성도: 231
호연: 203RSE
센트럴칼로스: 080
가라르: 068갑옷섬
팔데아: 164블루베리""")]
})

retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

response = retrieval_chain.invoke({"input": "국민취업지원제도가 뭐야"})
print(response["answer"])