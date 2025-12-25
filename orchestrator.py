import json
from dataclasses import asdict, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List

from .agents import DataParserAgent, QuestionGeneratorAgent, PageGeneratorAgent
from .content_blocks import BenefitsBlock, UsageBlock, IngredientsBlock, SafetyBlock, ComparisonBlock
from .models import ContentBlock, GeneratedPage, ProductData, Question


def _to_jsonable(obj: Any) -> Any:
    if obj is None:
        return None
    if isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, Enum):
        return obj.value
    if is_dataclass(obj):
        return {k: _to_jsonable(v) for k, v in asdict(obj).items()}
    if isinstance(obj, dict):
        return {str(k): _to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_to_jsonable(v) for v in obj]
    return str(obj)


class ContentOrchestrator:
    def __init__(self):
        self.data_parser = DataParserAgent()
        self.question_generator = QuestionGeneratorAgent()
        self.page_generator = PageGeneratorAgent()

        self.benefits_block = BenefitsBlock()
        self.usage_block = UsageBlock()
        self.ingredients_block = IngredientsBlock()
        self.safety_block = SafetyBlock()
        self.comparison_block = ComparisonBlock()

    def get_graph(self) -> Dict[str, Any]:
        return {
            "nodes": [
                {"id": "parse", "agent": self.data_parser.name},
                {"id": "questions", "agent": self.question_generator.name},
                {"id": "blocks", "type": "content_blocks"},
                {"id": "page_faq", "agent": self.page_generator.name, "template": "faq"},
                {"id": "page_product", "agent": self.page_generator.name, "template": "product"},
                {"id": "page_comparison", "agent": self.page_generator.name, "template": "comparison"},
            ],
            "edges": [
                {"from": "parse", "to": "questions"},
                {"from": "parse", "to": "blocks"},
                {"from": "questions", "to": "page_faq"},
                {"from": "blocks", "to": "page_faq"},
                {"from": "blocks", "to": "page_product"},
                {"from": "blocks", "to": "page_comparison"},
            ],
        }

    def run_pipeline(self, raw_product_data: Dict[str, Any]) -> Dict[str, Any]:
        product_data: ProductData = self.data_parser.process(raw_product_data)
        questions: List[Question] = self.question_generator.process(product_data)

        blocks = self._generate_blocks(product_data)

        faq_page = self.page_generator.process(
            {
                "product_data": product_data,
                "content_blocks": blocks,
                "page_type": "faq",
                "additional_params": {"questions": questions, "product_data": product_data},
            }
        )

        product_page = self.page_generator.process(
            {
                "product_data": product_data,
                "content_blocks": blocks,
                "page_type": "product",
                "additional_params": {"product_data": product_data},
            }
        )

        comparison_page = self._generate_comparison_page(product_data, blocks)

        return {
            "graph": self.get_graph(),
            "artifacts": {
                "faq.json": _to_jsonable(faq_page.content),
                "product_page.json": _to_jsonable(product_page.content),
                "comparison_page.json": _to_jsonable(comparison_page.content),
                "graph.json": _to_jsonable(self.get_graph()),
            },
        }

    def _generate_blocks(self, product_data: ProductData) -> List[ContentBlock]:
        return [
            self.benefits_block.process(product_data),
            self.usage_block.process(product_data),
            self.ingredients_block.process(product_data),
            self.safety_block.process(product_data),
        ]

    def _fictional_product_b(self) -> Dict[str, Any]:
        return {
            "name": "CitraGlow Serum B",
            "concentration": "15% Vitamin C",
            "skin_types": ["Normal", "Dry"],
            "key_ingredients": ["Vitamin C", "Niacinamide"],
            "benefits": ["Brightening", "Evens skin tone"],
            "price": "₹899",
            "fictional": True,
        }

    def _generate_comparison_page(self, product_data: ProductData, base_blocks: List[ContentBlock]) -> GeneratedPage:
        product_b = self._fictional_product_b()
        comparison_block = self.comparison_block.process(product_data, comparison_product=product_b)
        blocks = list(base_blocks) + [comparison_block]

        return self.page_generator.process(
            {
                "product_data": product_data,
                "content_blocks": blocks,
                "page_type": "comparison",
                "additional_params": {"product_data": product_data},
            }
        )


def write_outputs(pipeline_result: Dict[str, Any], output_dir: str) -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    artifacts = pipeline_result.get("artifacts", {})
    for filename, content in artifacts.items():
        (out / filename).write_text(json.dumps(content, ensure_ascii=False, indent=2), encoding="utf-8")
