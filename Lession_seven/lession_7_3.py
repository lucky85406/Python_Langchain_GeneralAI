
import os
import sys
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# 將專案根目錄添加到 Python 的模組搜尋路徑中
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from modelFun.printModel import AnsiColors, print_by_status as pm

# 定義包含文字檔案的目錄和持久化目錄
current_dir = os.path.dirname(os.path.abspath("__file__"))
books_dir = os.path.join(current_dir, "books")
db_dir = os.path.join(current_dir, "db")
persistent_directory = os.path.join(db_dir, "chroma_db_with_metadata_chinese_nb")

pm(f"書籍目錄: {books_dir}", "info")
pm(f"持久化目錄: {persistent_directory}", "info")

# 檢查 Chroma 向量存儲是否已存在
if not os.path.exists(persistent_directory):
    pm("持久化目錄不存在。正在初始化向量存儲...", "info")

    # 確保書籍目錄存在
    if not os.path.exists(books_dir):
        raise FileNotFoundError(
            f"目錄 {books_dir} 不存在。請檢查路徑。"
        )

    # 列出目錄中所有文字檔案
    book_files = [f for f in os.listdir(books_dir) if f.endswith(".txt")]

    # 從每個檔案讀取文字內容並儲存元數據
    documents = []
    for book_file in book_files:
        file_path = os.path.join(books_dir, book_file)
        loader = TextLoader(file_path, encoding="utf-8")
        book_docs = loader.load()
        for doc in book_docs:
            # 為每個文件添加元數據以指示其來源
            doc.metadata = {"source": book_file}
            documents.append(doc)

    # 將文件分割成塊
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    # 顯示分割文件的資訊
    pm("\n--- 文件塊資訊 ---", "info")
    pm(f"文件塊數量: {len(docs)}", "info")

    # 建立嵌入模型
    pm("\n--- 正在建立嵌入 ---", "info")
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-m3"
    )
    pm("\n--- 完成建立嵌入 ---", "info")

    # 建立並持久化向量存儲
    pm("\n--- 正在建立並持久化向量存儲 ---", "info")
    db = Chroma.from_documents(
        docs, embeddings, persist_directory=persistent_directory)
    pm("\n--- 完成建立並持久化向量存儲 ---", "success")

else:
    pm("向量存儲已存在。無需初始化。", "info")