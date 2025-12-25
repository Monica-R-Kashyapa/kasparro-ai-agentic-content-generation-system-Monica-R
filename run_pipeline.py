from pathlib import Path

from .orchestrator import ContentOrchestrator, write_outputs


def main() -> None:
    product_data = {
        "Product Name": "GlowBoost Vitamin C Serum",
        "Concentration": "10% Vitamin C",
        "Skin Type": "Oily, Combination",
        "Key Ingredients": "Vitamin C, Hyaluronic Acid",
        "Benefits": "Brightening, Fades dark spots",
        "How to Use": "Apply 2–3 drops in the morning before sunscreen",
        "Side Effects": "Mild tingling for sensitive skin",
        "Price": "₹699",
    }

    orchestrator = ContentOrchestrator()
    result = orchestrator.run_pipeline(product_data)

    output_dir = Path(__file__).parent / "outputs"
    write_outputs(result, str(output_dir))


if __name__ == "__main__":
    main()
