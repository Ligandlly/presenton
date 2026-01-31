from typing import Optional
from models.llm_message import LLMSystemMessage, LLMUserMessage
from services.llm_client import LLMClient
from utils.llm_client_error_handler import handle_llm_client_exceptions
from utils.llm_provider import get_model

system_prompt = """
    你是一个专业的HTML幻灯片编辑器。你的任务是根据用户提示修改幻灯片HTML内容，同时保持正确的结构、样式和功能。

    指导原则:
    1. **保留结构**: 保持整体的HTML结构，包括必要的容器、类和ID
    2. **内容更新**: 按要求修改文本、图片、列表和其他内容元素
    3. **样式一致性**: 保留现有的CSS类和样式，除非明确要求更改
    4. **响应式设计**: 确保修改在不同屏幕尺寸下都能正常工作
    5. **可访问性**: 保持正确的语义HTML和可访问性属性
    6. **清洁输出**: 只返回修改后的HTML，不添加解释，除非发生错误

    常见编辑类型:
    - 文本内容更改（标题、段落、列表）
    - 图片更新（src、alt文本、标题）
    - 布局修改（添加/删除部分）
    - 样式调整（颜色、字体、通过类进行间距调整）
    - 交互元素（按钮、链接、表单）

    错误处理:
    - 如果HTML结构无效，在进行请求的更改时修复它
    - 如果请求会破坏功能，建议采用替代方法
    - 对于不明确的提示，做出合理的假设并注明任何歧义

    输出格式:
    返回完整的修改后的HTML。如果原始HTML包含<style>或<script>标签，保留它们，除非明确要求修改。
"""


def get_user_prompt(prompt: str, html: str):
    return f"""
        请根据以下提示编辑下面的幻灯片HTML：

        **编辑请求:** {prompt}

        **当前HTML:**
        ```html
        {html}
        ```

        返回应用了你的更改后的修改HTML。
    """


async def get_edited_slide_html(prompt: str, html: str):
    model = get_model()

    client = LLMClient()
    try:
        response = await client.generate(
            model=model,
            messages=[
                LLMSystemMessage(content=system_prompt),
                LLMUserMessage(content=get_user_prompt(prompt, html)),
            ],
        )
        return extract_html_from_response(response) or html
    except Exception as e:
        raise handle_llm_client_exceptions(e)


def extract_html_from_response(response_text: str) -> Optional[str]:
    start_index = response_text.find("<")
    end_index = response_text.rfind(">")

    if start_index != -1 and end_index != -1 and end_index > start_index:
        return response_text[start_index : end_index + 1]

    return None
