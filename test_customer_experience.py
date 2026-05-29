import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.customer_experience_tools import (
    customer_sentiment_analyzer,
    e_commerce_optimization_engine,
    public_relations_assistant,
    review_monitoring_assistant,
)


class CustomerExperienceTests(unittest.TestCase):
    def test_ecommerce_sentiment_reviews_and_pr_render(self):
        with tempfile.TemporaryDirectory() as directory:
            cx_dir = Path(directory)
            (cx_dir / "ecommerce.json").write_text(
                json.dumps({"conversion_rate": 2.8, "cart_abandonment_rate": 61.2, "average_order_value": 48.5}),
                encoding="utf-8",
            )
            (cx_dir / "sentiment.json").write_text(
                json.dumps({"entries": [{"label": "positive"}, {"label": "negative"}, {"label": "neutral"}]}),
                encoding="utf-8",
            )
            (cx_dir / "reviews.json").write_text(
                json.dumps({"reviews": [{"rating": 5}, {"rating": 2}, {"rating": 4}]}),
                encoding="utf-8",
            )
            (cx_dir / "pr_campaigns.json").write_text(
                json.dumps({"campaigns": [{"name": "launch", "status": "draft"}]}),
                encoding="utf-8",
            )
            with patch("tools.customer_experience_tools.CX_DIR", cx_dir):
                ecommerce = e_commerce_optimization_engine()
                sentiment = customer_sentiment_analyzer()
                reviews = review_monitoring_assistant()
                pr = public_relations_assistant()
        self.assertIn("Conversion rate: 2.80%", ecommerce)
        self.assertIn("Positive: 1", sentiment)
        self.assertIn("Negative: 1", sentiment)
        self.assertIn("Average rating: 3.67", reviews)
        self.assertIn("Upcoming campaigns: 1", pr)

    def test_routes_cover_466_to_470(self):
        for phase in range(466, 471):
            result = handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help")
            self.assertIsNotNone(result, f"missing route for {phase}")


if __name__ == "__main__":
    unittest.main()
