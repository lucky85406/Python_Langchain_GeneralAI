from langchain_ollama import ChatOllama
import gradio as gr
from dotenv import load_dotenv
import os

# 載入環境變數（可用 OLLAMA_URL / OLLAMA_MODEL 覆蓋預設）
load_dotenv()


# 使用最原始的呼叫方式：直接以字串 prompt 送到 Ollama
model = ChatOllama(model="gemma3:270m", base_url="http://localhost:11434")


def answer(prompt: str) -> str:
    """最簡單的 wrapper：把 prompt 傳給 model.invoke，回傳文字回應。"""
    if not prompt or not prompt.strip():
        return ""
    try:
        response = model.invoke(prompt)
        # LangChain v0.2.0 之後，ChatOllama 的 invoke 回傳的是 AIMessage 物件。
        # AIMessage.content 的型別可能是 str 或 list。
        # 為了確保回傳型別是 str，我們需要處理 content 是 list 的情況。
        if hasattr(response, "content"):
            content = response.content
            if isinstance(content, list):
                return "\n".join(str(part) for part in content)
            return str(content)
        return str(response)
    except Exception as e:
        return f"呼叫 Ollama 時發生錯誤：{e}"


# 最小的 Gradio 介面：一個輸入框 + 一個文字輸出
iface = gr.Interface(
    fn=answer,
    inputs=gr.Textbox(lines=3, placeholder="在此輸入問題，按送出..."),
    outputs="text",
    title="Ollama 簡易 Gradio 範例",
    description="示範如何把原先的 Ollama 呼叫整合到 Gradio。可用 OLLAMA_URL/OLLAMA_MODEL 環境變數覆蓋預設。",
)

if __name__ == "__main__":
    # Windows default ip 127.0.0.1 / Mac 0.0.0.0
    iface.launch(server_name="127.0.0.1", server_port=7860)
    