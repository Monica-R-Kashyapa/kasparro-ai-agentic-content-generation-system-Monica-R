from typing import Any, Dict, List

from ..models import ContentBlock, GeneratedPage
from ..templates import TemplateEngine
from .base_agent import BaseAgent


class PageGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__("PageGeneratorAgent")
        self.template_engine = TemplateEngine()

    def validate_input(self, input_data: Any) -> bool:
        if not isinstance(input_data, dict):
            return False
        return all(k in input_data for k in ["product_data", "content_blocks", "page_type"])

    def validate_output(self, output_data: Any) -> bool:
        return isinstance(output_data, GeneratedPage)

    def process(self, input_data: Dict[str, Any]) -> GeneratedPage:
        if not self.validate_input(input_data):
            raise ValueError("Invalid input data format")

        content_blocks: List[ContentBlock] = input_data["content_blocks"]
        page_type: str = input_data["page_type"]
        additional_params = input_data.get("additional_params", {})

        page = self.template_engine.render_page(
            template_name=page_type,
            content_blocks=content_blocks,
            **additional_params,
        )

        if not self.validate_output(page):
            raise ValueError("Invalid page output")
        return page
