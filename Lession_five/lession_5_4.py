from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
import gradio as gr

model_name = "llama3.2:latest"
model = OllamaLLM(model=model_name)

print("=== Ollama 模型設定完成 ===")
print(f"使用模型：{model_name}")
print(f"使用類型：{type(model)}")


# 建立多變數的翻譯模板
complex_template = """
你是一位專業的{target_language}翻譯家，專精於{domain}領域。
請將以下{source_language}文本翻譯成{target_language}，並確保：
1. 保持原文的語氣和風格
2. 使用專業術語
3. 符合{target_language}的語言習慣
4. 無需加入其他資訊

{source_language}文本：{text}
{target_language}翻譯：
"""

# 建立 ChatPromptTemplate
chat_prompt_template = ChatPromptTemplate.from_template(complex_template)

def translate_text(source_language, target_language, domain, text):
    """使用 Gradio 輸入的參數進行翻譯"""
    if not all([source_language, target_language, domain, text.strip()]):
        return "錯誤：所有欄位都必須填寫！"
    
    # 使用多個變數格式化 Prompt
    formatted_prompt = chat_prompt_template.format(
        source_language=source_language,
        target_language=target_language, 
        domain=domain,
        text=text
    )
    
    print("=== 正在處理請求 ===")
    print(formatted_prompt)
    print(f"{'=' * 50}")
    
    try:
        res = model.invoke(formatted_prompt)
        print(f"模型回應：{res}")
        return res
    except Exception as e:
        error_msg = f"呼叫模型時發生錯誤: {e}"
        print(error_msg)
        return error_msg

# 建立 Gradio 介面
iface = gr.Interface(
    fn=translate_text,
    inputs=[
        gr.Dropdown(["英文", "繁體中文", "日文"], label="來源語言", value="英文"),
        gr.Dropdown(["繁體中文", "英文", "日文"], label="目標語言", value="繁體中文"),
        gr.Dropdown(["商業", "科技", "生活", "學術"], label="專業領域", value="商業"),
        gr.Textbox(lines=5, label="要翻譯的文本", placeholder="請在此輸入要翻譯的內容...")
    ],
    outputs=gr.Textbox(label="翻譯結果"),
    title="專業領域翻譯器",
    description="這是一個使用 LangChain 和 Ollama (Llama 3.2) 打造的專業翻譯工具。請選擇語言、專業領域，並輸入您想翻譯的文本。",
    examples=[
        ["英文", "繁體中文", "商業", "The quarterly revenue increased by 15% compared to last year."],
        ["英文", "繁體中文", "科技", "The new algorithm improves data processing efficiency by optimizing memory allocation."],
        ["繁體中文", "英文", "生活", "今天天氣真好，我們去公園散步吧！"]
    ]
)

if __name__ == "__main__":
    print("🚀 啟動 Gradio 專業翻譯器介面...")
    iface.launch()