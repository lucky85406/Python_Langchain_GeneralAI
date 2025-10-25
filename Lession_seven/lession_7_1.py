import os
import sys
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import chromadb

# 將專案根目錄添加到 Python 的模組搜尋路徑中
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from modelFun.printModel import print_by_status as pm

current_file = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_file, "books", "智慧型手機使用手冊.txt")
persistent_directory = os.path.join(current_file, "db", "chroma_db_v3")
collection_name = "smartphone_manual"

try:
    # 準備 embedding model 和 chroma client
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
    client = chromadb.PersistentClient(path=persistent_directory)

    if not os.path.exists(persistent_directory):
        pm("向量資料庫不存在，開始進行初始化...", "info")
        if not os.path.exists(file_path):
            raise FileExistsError(f"檔案：{file_path}不存在，請檢查路徑")
        loader = TextLoader(file_path=file_path, encoding="utf-8")
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=200)
        docs = text_splitter.split_documents(documents)
        db = Chroma.from_documents(
            docs, 
            embedding=embeddings, 
            client=client, 
            collection_name=collection_name
        )
        pm("向量資料庫初始化完成", "success")
    else:
        pm("向量資料庫已存在，直接載入", "info")
        db = Chroma(
            persist_directory=persistent_directory,
            embedding_function=embeddings,
            client=client,
            collection_name=collection_name,
        )

except Exception as e:
    pm(f"{e}", "error")
    sys.exit(1)  # 發生錯誤時，終止程式

query = "我想了解藍牙配置?"

retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})

relevant_docs = retriever.invoke(query)
for doc in relevant_docs:
    pm(doc.page_content, "info")
    pm("=" * 60, "success")
