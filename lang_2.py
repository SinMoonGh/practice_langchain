import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from dotenv import load_dotenv
import os
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# 제목
st.title("URL crawling service")

# 사이드 바에 채팅 목록 표시하기
with st.sidebar:
    click_cl = st.button(label='chat_list')
    # if click_cl:
    #     st.write(url_input)
    #     st.write(f'{question_input}')

# api key 가져오기
load_dotenv()
openai_api_key=os.getenv("NEW_API_KEY")

# docs 정보 가져오기
url_input = st.text_input(label="",
                         help="저희 서비스는 희망하시는 웹 페이지의 정보를 가져와서 해당 웹 페이지에서 제공하는 정보를 손 쉽게 제공해주는 서비스입니다.",
                         placeholder='정보를 제공 받기 희망하시는 url 주소를 적어주세요.')
question_input = st.chat_input(placeholder="무엇이든 물어보세요.")

if target_url := url_input:
    loader = WebBaseLoader(target_url)
    docs = loader.load()

    # llm 인스턴스 생성
    llm = ChatOpenAI(openai_api_key=openai_api_key)

    # embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(docs)
    vector = FAISS.from_documents(documents, embeddings)

    # 프롬프트 구성
    prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

    <context>
    {context}
    </context>

    Question: {input}""")

    # document_chain 구성
    document_chain = create_stuff_documents_chain(llm, prompt)

    # 검색기 구성
    retriever = vector.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    # 요청
    if question:=question_input:
        response = retrieval_chain.invoke({"input": question})
        answer = st.write(response["answer"])
    else:
        st.stop()


        



