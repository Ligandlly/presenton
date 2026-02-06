from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
    PowerpointFormatOption,
    WordFormatOption,
)
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat


class DoclingService:
    def __init__(self):
        import os

        # 检查是否有预下载的模型（在Docker镜像中）
        model_path = "/app/docling/models"
        if os.path.exists(model_path) and os.listdir(model_path):
            os.environ["HUGGINGFACE_HUB_CACHE"] = model_path
            print(f"Using pre-downloaded docling models from {model_path}")

        self.pipeline_options = PdfPipelineOptions()
        self.pipeline_options.do_ocr = True
        self.pipeline_options.artifacts_path = "/app/docling/models"

        self.converter = DocumentConverter(
            allowed_formats=[InputFormat.PPTX, InputFormat.PDF, InputFormat.DOCX],
            format_options={
                InputFormat.DOCX: WordFormatOption(
                    pipeline_options=self.pipeline_options,
                ),
                InputFormat.PPTX: PowerpointFormatOption(
                    pipeline_options=self.pipeline_options,
                ),
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=self.pipeline_options,
                ),
            },
        )

    def parse_to_markdown(self, file_path: str) -> str:
        result = self.converter.convert(file_path)
        return result.document.export_to_markdown()
