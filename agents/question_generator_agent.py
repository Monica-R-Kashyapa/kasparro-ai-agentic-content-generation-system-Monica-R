from typing import Any, Dict, List

from ..models import ProductData, Question, QuestionCategory
from .base_agent import BaseAgent


class QuestionGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__("QuestionGeneratorAgent")
        self.question_templates = self._initialize_templates()

    def validate_input(self, input_data: Any) -> bool:
        return isinstance(input_data, ProductData)

    def validate_output(self, output_data: Any) -> bool:
        return isinstance(output_data, list) and all(isinstance(q, Question) for q in output_data)

    def _initialize_templates(self) -> Dict[QuestionCategory, List[str]]:
        return {
            QuestionCategory.INFORMATIONAL: [
                "What is {product_name}?",
                "What concentration does {product_name} contain?",
                "What are the key ingredients in {product_name}?",
                "What skin types is {product_name} suitable for?",
            ],
            QuestionCategory.SAFETY: [
                "Are there any side effects of using {product_name}?",
                "Is {product_name} safe for sensitive skin?",
                "Can {product_name} cause skin irritation?",
                "What precautions should I take when using {product_name}?",
            ],
            QuestionCategory.USAGE: [
                "How do I use {product_name}?",
                "When should I apply {product_name}?",
                "How many drops of {product_name} should I use?",
                "Can I use {product_name} with other skincare products?",
            ],
            QuestionCategory.PURCHASE: [
                "How much does {product_name} cost?",
                "Where can I buy {product_name}?",
                "Is {product_name} worth the price?",
                "What size is {product_name} available in?",
            ],
            QuestionCategory.COMPARISON: [
                "How does {product_name} compare to other vitamin C serums?",
                "Is {product_name} better than other vitamin C serums?",
                "What makes {product_name} different from competitors?",
                "Should I choose {product_name} or other vitamin C serums?",
            ],
        }

    def process(self, input_data: ProductData) -> List[Question]:
        if not self.validate_input(input_data):
            raise ValueError("Invalid input data format")

        questions: List[Question] = []
        for category, templates in self.question_templates.items():
            for template in templates:
                text = template.replace("{product_name}", input_data.name)
                q = Question(text=text, category=category, answer_template="")
                questions.append(q)

        # Ensure 15+ (this set is 20 by default)
        self.state["generated_questions"] = questions
        if not self.validate_output(questions):
            raise ValueError("Invalid question output")
        return questions
