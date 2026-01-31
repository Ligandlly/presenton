from datetime import datetime
from typing import Optional
from models.llm_message import LLMSystemMessage, LLMUserMessage
from models.presentation_layout import SlideLayoutModel
from models.presentation_outline_model import SlideOutlineModel
from services.llm_client import LLMClient
from utils.llm_client_error_handler import handle_llm_client_exceptions
from utils.llm_provider import get_model
from utils.schema_utils import add_field_in_schema, remove_fields_from_schema


def get_system_prompt(
    tone: Optional[str] = None,
    verbosity: Optional[str] = None,
    instructions: Optional[str] = None,
):
    return f"""
        根据提供的大纲生成结构化的幻灯片内容，遵循以下步骤和注意事项并提供结构化输出。

        必须以简体中文输出所有内容。

        {"# 用户指令:" if instructions else ""}
        {instructions or ""}

        {"# 语气:" if tone else ""}
        {tone or ""}

        {"# 详细程度:" if verbosity else ""}
        {verbosity or ""}

        # 步骤
        1. 分析大纲内容。
        2. 根据大纲生成结构化的幻灯片。
        3. 生成简洁明了的演讲者备注。

        # 注意事项
        - 幻灯片正文不应使用"本幻灯片"、"本演示文稿"等词语。
        - 重新措辞使幻灯片内容自然流畅。
        - 只使用markdown来突出重要内容。
        - 确保遵循语言规范。
        - 演讲者备注应为纯文本，而非markdown格式。
        - 严格遵守幻灯片各属性的最大和最小字符限制。
        - 绝对不要超过最大字符限制。控制你的叙述以确保不超过最大字符限制。
        - 项目数量不应超过幻灯片schema中指定的最大项目数。如果需要放置多个要点，请合并它们以符合最大项目数限制。
        - 根据给定的语气生成内容。
        - 严格控制生成内容的字数。超过最大字符数会导致设计溢出。因此，请提前分析，永远不要生成超过允许字符数的内容。
        - 不要在内容中添加表情符号。
        - 指标应使用缩写形式，使用尽可能少的字符。不要为指标添加一长串文字。
        - 关于详细程度:
            - 如果详细程度为'简洁'，则生成的内容应为最大字符限制的1/3或更少。不要担心遗漏内容或上下文。
            - 如果详细程度为'标准'，则生成的内容应为最大字符限制的2/3。
            - 如果详细程度为'内容丰富'，则生成的内容应为最大字符限制的3/4或更高。确保不要超过最大字符限制。

        用户指令、语气和详细程度应始终被遵循，并优先于其他指令（最大/最小字符限制、幻灯片schema和项目数量除外）。

        - 以JSON格式输出，**不要包含<parameters>标签**。

        # 图片和图标输出格式
        image: {{
            __image_prompt__: string,
        }}
        icon: {{
            __icon_query__: string,
        }}

    """


def get_user_prompt(outline: str, language: str):
    return f"""
        ## 当前日期和时间
        {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

        ## 图标查询和图片提示词语言
        中文

        ## 幻灯片内容语言
        {language}

        ## 幻灯片大纲
        {outline}
    """


def get_messages(
    outline: str,
    language: str,
    tone: Optional[str] = None,
    verbosity: Optional[str] = None,
    instructions: Optional[str] = None,
):

    return [
        LLMSystemMessage(
            content=get_system_prompt(tone, verbosity, instructions),
        ),
        LLMUserMessage(
            content=get_user_prompt(outline, language),
        ),
    ]


async def get_slide_content_from_type_and_outline(
    slide_layout: SlideLayoutModel,
    outline: SlideOutlineModel,
    language: str,
    tone: Optional[str] = None,
    verbosity: Optional[str] = None,
    instructions: Optional[str] = None,
):
    client = LLMClient()
    model = get_model()

    response_schema = remove_fields_from_schema(
        slide_layout.json_schema, ["__image_url__", "__icon_url__"]
    )
    response_schema = add_field_in_schema(
        response_schema,
        {
            "__speaker_note__": {
                "type": "string",
                "minLength": 100,
                "maxLength": 250,
                "description": "Speaker note for the slide",
            }
        },
        True,
    )

    try:
        response = await client.generate_structured(
            model=model,
            messages=get_messages(
                outline.content,
                language,
                tone,
                verbosity,
                instructions,
            ),
            response_format=response_schema,
            strict=False,
        )
        return response

    except Exception as e:
        raise handle_llm_client_exceptions(e)
