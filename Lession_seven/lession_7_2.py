import os
import sys
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda,RunnablePassthrough
from langchain_ollama import ChatOllama
import chromadb

# 將專案根目錄添加到 Python 的模組搜尋路徑中
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from modelFun.printModel import AnsiColors, print_by_status as pm

current_file = os.path.dirname(os.path.abspath(__file__))
persistent_directory = os.path.join(current_file, "db", "chroma_db_v3")

template = """你是一個智慧型手機的客服助手。請根據以下參考資料回答使用者的問題。

參考資料：
{context}

使用者問題：{question}

請用繁體中文回答，並且：
1. 只根據參考資料回答，不要編造內容
2. 如果參考資料中沒有答案，請誠實說「我在資料中找不到相關資訊」
3. 回答要清楚、具體、有條理

回答："""

# 準備 llma model
prompt = ChatPromptTemplate.from_template(template)
llm = ChatOllama(
    model="llama3.2:latest"
)

# 準備 embedding model 和 chroma client
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
client = chromadb.PersistentClient(path=persistent_directory)
db = Chroma(
    client=client,
    embedding_function=embeddings,
    collection_name="smartphone_manual",
)
retriever = db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k": 5,"score_threshold":0.5})
def retriever_docs(question):
    relevant_docs = retriever.invoke(query)
    context = "\n".join(doc.page_content for doc in relevant_docs)
    return {"context":context,"question":question}

def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

rag_chain = (
    RunnableLambda(retriever_docs)
    | prompt
    | llm
    | StrOutputParser()
)

rag_chain_2 = (
    {
        "question":RunnablePassthrough(),
        "context": retriever | format_docs 
    }
    | prompt
    | llm
    | StrOutputParser()
)
while True:
    prompt_text = f"{AnsiColors.DARK_GREEN}請輸入您想查詢的問題（輸入 'exit' 離開）：{AnsiColors.RESET}"
    query = input(prompt_text)
    if query.lower() == 'exit':
        break
    result = rag_chain_2.invoke(query)
    pm("result：","warning")
    pm(result, "info")

