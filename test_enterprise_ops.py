import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.enterprise_ops_tools import (
    contract_analyzer,
    inventory_forecasting_engine,
    legal_document_assistant,
    pos_intelligence_engine,
    procurement_assistant,
    supply_chain_analyzer,
)


class EnterpriseOpsTests(unittest.TestCase):
    def test_legal_procurement_and_supply_chain_render(self):
        with tempfile.TemporaryDirectory() as directory:
            ops_dir = Path(directory)
            (ops_dir / "legal_documents.json").write_text(
                json.dumps({"documents": [{"title": "MSA", "status": "draft"}]}),
                encoding="utf-8",
            )
            (ops_dir / "contracts.json").write_text(
                json.dumps({"contracts": [{"name": "Vendor A", "risk": "high", "renewal_window": "30d"}]}),
                encoding="utf-8",
            )
            (ops_dir / "procurement.json").write_text(
                json.dumps({"requests": [{"item": "Laptops", "status": "pending"}]}),
                encoding="utf-8",
            )
            (ops_dir / "supply_chain.json").write_text(
                json.dumps({"vendors": [{"name": "Supplier 1", "status": "delayed", "single_source": True}]}),
                encoding="utf-8",
            )
            with patch("tools.enterprise_ops_tools.OPS_DIR", ops_dir):
                legal = legal_document_assistant()
                contracts = contract_analyzer()
                procurement = procurement_assistant()
                supply_chain = supply_chain_analyzer()
        self.assertIn("Tracked legal documents: 1", legal)
        self.assertIn("High-risk contracts: 1", contracts)
        self.assertIn("Pending approvals: 1", procurement)
        self.assertIn("Single-source dependencies: 1", supply_chain)

    def test_inventory_pos_and_routes_cover_460_to_465(self):
        with tempfile.TemporaryDirectory() as directory:
            ops_dir = Path(directory)
            (ops_dir / "inventory.json").write_text(
                json.dumps({"items": [{"sku": "A1", "days_remaining": 7}]}),
                encoding="utf-8",
            )
            (ops_dir / "pos_sales.json").write_text(
                json.dumps({"sales": [{"revenue": 1500, "transactions": 30}]}),
                encoding="utf-8",
            )
            with patch("tools.enterprise_ops_tools.OPS_DIR", ops_dir):
                inventory = inventory_forecasting_engine()
                pos = pos_intelligence_engine()
        self.assertIn("Low-runway SKUs: 1", inventory)
        self.assertIn("Total revenue: 1500.00", pos)
        self.assertIn("Average ticket: 50.00", pos)
        for phase in range(460, 466):
            result = handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help")
            self.assertIsNotNone(result, f"missing route for {phase}")


if __name__ == "__main__":
    unittest.main()
