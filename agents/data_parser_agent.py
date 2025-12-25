from typing import Any, Dict, List

from ..models import ProductData
from .base_agent import BaseAgent


class DataParserAgent(BaseAgent):
    def __init__(self):
        super().__init__("DataParserAgent")

    def validate_input(self, input_data: Any) -> bool:
        return isinstance(input_data, dict)

    def validate_output(self, output_data: Any) -> bool:
        return isinstance(output_data, ProductData)

    def process(self, input_data: Dict[str, Any]) -> ProductData:
        if not self.validate_input(input_data):
            raise ValueError("Invalid input data format")

        def _split_list(value: Any) -> List[str]:
            if value is None:
                return []
            if isinstance(value, list):
                return [str(v).strip() for v in value if str(v).strip()]
            return [v.strip() for v in str(value).split(",") if v.strip()]

        product = ProductData(
            name=str(input_data.get("Product Name", "")),
            concentration=str(input_data.get("Concentration", "")),
            skin_types=_split_list(input_data.get("Skin Type", "")),
            key_ingredients=_split_list(input_data.get("Key Ingredients", "")),
            benefits=_split_list(input_data.get("Benefits", "")),
            usage_instructions=str(input_data.get("How to Use", "")),
            side_effects=str(input_data.get("Side Effects", "")),
            price=str(input_data.get("Price", "")),
        )

        if not self.validate_output(product):
            raise ValueError("Failed to parse product data")

        self.state["product_data"] = product
        return product
