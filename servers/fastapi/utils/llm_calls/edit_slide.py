from datetime import datetime
from typing import Optional
from models.llm_message import LLMSystemMessage, LLMUserMessage
from models.presentation_layout import SlideLayoutModel
from models.sql.slide import SlideModel
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
    根据提供的提示编辑幻灯片数据和演讲者备注，遵循以下步骤和注意事项并提供结构化输出。

    必须以简体中文输出所有内容。

    {"# 用户指令:" if instructions else ""}
    {instructions or ""}

    {"# 语气:" if tone else ""}
    {tone or ""}

    {"# 详细程度:" if verbosity else ""}
    {verbosity or ""}

    # 注意事项
    - 根据**输入**中提到的语言输出内容。
    - 目标是根据提供的提示更改幻灯片数据。
    - 如果提示中没有要求，不要更改**图片提示词**和**图标查询**。
    - 如果提示中要求生成或更改，则生成**图片提示词**和**图标查询**。
    - 确保遵循语言规范。
    - 演讲者备注应为纯文本，而非markdown格式。
    - 演讲者备注应该简单、清晰、简洁、切中要点。

    **请仔细阅读所有注意事项和步骤，确保遵循，包括提到的约束条件**
    """


def get_user_prompt(prompt: str, slide_data: dict, language: str):
    return f"""
        ## 图标查询和图片提示词语言
        中文

        ## 当前日期和时间
        {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

        ## 幻灯片内容语言
        {language}

        ## 提示
        {prompt}

        ## 幻灯片数据
        {slide_data}
    """


def get_messages(
    prompt: str,
    slide_data: dict,
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
            content=get_user_prompt(prompt, slide_data, language),
        ),
    ]


async def get_edited_slide_content(
    prompt: str,
    slide: SlideModel,
    language: str,
    slide_layout: SlideLayoutModel,
    tone: Optional[str] = None,
    verbosity: Optional[str] = None,
    instructions: Optional[str] = None,
):
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

    client = LLMClient()
    try:
        response = await client.generate_structured(
            model=model,
            messages=get_messages(
                prompt, slide.content, language, tone, verbosity, instructions
            ),
            response_format=response_schema,
            strict=False,
        )
        return response

    except Exception as e:
        raise handle_llm_client_exceptions(e)
