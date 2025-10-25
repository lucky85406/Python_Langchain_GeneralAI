# 定義 ANSI 顏色代碼 (使用 256 色碼以呈現更柔和的色調)
class AnsiColors:
    # 格式: \033[38;5;{色碼}m
    RED = '\033[38;5;203m'      # 柔和的紅色 (for error)
    GREEN = '\033[38;5;114m'    # 柔和的綠色 (for success)
    YELLOW = '\033[38;5;228m'   # 柔和的黃色 (for warning)
    CYAN = '\033[38;5;81m'      # 柔和的青色 (for info)
    MAGENTA = '\033[38;5;171m'  # 柔和的洋紅色 (for debug)
    DARK_GREEN = '\033[38;5;28m' # 深綠色 (for input prompts)
    RESET = '\033[0m'           # 重設所有屬性

def print_by_status(text: str, status: str):
    """
    根據指定的狀態打印帶有顏色的文字。

    Args:
        text (str): 要打印的文字。
        status (str): 狀態字串 (e.g., 'success', 'error', 'warning', 'info')。
    """
    # 建立狀態與顏色的對應關係
    status_color_map = {
        'success': AnsiColors.GREEN,
        'error': AnsiColors.RED,
        'warning': AnsiColors.YELLOW,
        'info': AnsiColors.CYAN,
        'debug': AnsiColors.MAGENTA,
    }

    # 根據 status 取得對應的顏色代碼
    # 如果找不到指定的 status，就使用預設的重設代碼 (終端機預設顏色)
    color_code = status_color_map.get(status.lower(), AnsiColors.RESET)
    
    # 組合字串並打印
    print(f"{color_code}{text}{AnsiColors.RESET}")

# --- 使用範例 ---
if __name__ == "__main__":
    print("--- 以下是新的 print_by_status 函式範例 ---")
    print_by_status("操作成功！", "success")
    print_by_status("發生嚴重錯誤，請檢查日誌。", "error")
    print_by_status("警告：磁碟空間即將用盡。", "warning")
    print_by_status("提示：系統將在 5 分鐘後重啟。", "info")
    print_by_status("偵錯訊息：變數 x 的值為 42。", "debug")
    print_by_status("這是一個未定義狀態的訊息。", "unknown_status")
    print("所有訊息打印完畢。")
