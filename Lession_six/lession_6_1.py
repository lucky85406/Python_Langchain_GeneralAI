from langchain.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain.schema.output_parser import StrOutputParser

prompt = ChatPromptTemplate.from_template("""你是一位專業的{role}，請用{style}的風格來介紹{topic}。

要求：
1. 內容要準確且易懂
2. 長度控制在200字以內
3. 使用繁體中文回答

請開始介紹：""") #建立ChatPromptTemplate實體
model = OllamaLLM(
    model="llama3.2:latest",
    temperature=0.7,
    top_p=0.9)
output_parser = StrOutputParser()

#使用LCEL語法建立鏈

chain = prompt | model | output_parser
# 準備輸入資料
input_data = {
    "role": "AI 專家",
    "style": "簡潔明瞭",
    "topic": "人工智慧"
}

print("📝 輸入資料：")
for key, value in input_data.items():
    print(f"   {key}: {value}")

print("\n🔄 正在執行基礎鏈...")
print("=" * 50)

# 執行基礎鏈
result = chain.invoke(input_data)

print("=" * 50)
print("✅ 基礎鏈執行完成！")
print("\n📋 回應結果：")
print(result)