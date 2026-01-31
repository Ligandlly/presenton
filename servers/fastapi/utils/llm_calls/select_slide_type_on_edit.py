from models.llm_message import LLMSystemMessage, LLMUserMessage
from models.presentation_layout import PresentationLayoutModel, SlideLayoutModel
from models.slide_layout_index import SlideLayoutIndex
from models.sql.slide import SlideModel
from services.llm_client import LLMClient
from utils.llm_client_error_handler import handle_llm_client_exceptions
from utils.llm_provider import get_model


def get_messages(
    prompt: str,
    slide_data: dict,
    layout: PresentationLayoutModel,
    current_slide_layout: int,
):
    return [
        LLMSystemMessage(
            content=f"""
                根据提供的用户提示和当前幻灯片数据选择幻灯片布局索引。
                {layout.to_string()}

                # 注意事项
                - 不要选择与当前不同的幻灯片布局，除非用户提示绝对必要。
                - 如果用户提示不清晰，选择与幻灯片数据最相关的布局。
                - 如果用户提示不清晰，选择与幻灯片数据最相关的布局。
                **请仔细阅读所有注意事项和步骤，确保遵循，包括提到的约束条件**
            """,
        ),
        LLMUserMessage(
            content=f"""
                - 用户提示: {prompt}
                - 当前幻灯片数据: {slide_data}
                - 当前幻灯片布局: {current_slide_layout}
            """,
        ),
    ]


async def get_slide_layout_from_prompt(
    prompt: str,
    layout: PresentationLayoutModel,
    slide: SlideModel,
) -> SlideLayoutModel:

    client = LLMClient()
    model = get_model()

    slide_layout_index = layout.get_slide_layout_index(slide.layout)

    try:
        response = await client.generate_structured(
            model=model,
            messages=get_messages(
                prompt,
                slide.content,
                layout,
                slide_layout_index,
            ),
            response_format=SlideLayoutIndex.model_json_schema(),
            strict=True,
        )
        index = SlideLayoutIndex(**response).index
        return layout.slides[index]

    except Exception as e:
        raise handle_llm_client_exceptions(e)
