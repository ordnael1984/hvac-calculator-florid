import json
import math
from pathlib import Path
import unittest

from legacy_estimate import EstimateInputs, calculate_preliminary


REFERENCE = json.loads((Path(__file__).parent / "reference_results.json").read_text())


class StageOneTests(unittest.TestCase):
    def test_original_results_are_preserved(self):
        for case in REFERENCE["cases"]:
            with self.subTest(case=case["name"]):
                result = calculate_preliminary(EstimateInputs(**case["inputs"]))
                for key, expected in case["expected"].items():
                    self.assertTrue(
                        math.isclose(result[key], expected, rel_tol=1e-12, abs_tol=1e-9),
                        f"{case['name']}.{key}: {result[key]} != {expected}",
                    )

    def test_areas_cannot_produce_negative_net_wall(self):
        inputs = dict(REFERENCE["cases"][0]["inputs"])
        inputs["gross_wall_area"] = 50
        self.assertEqual(calculate_preliminary(EstimateInputs(**inputs))["net_wall_area"], 0)

    def test_invalid_r_value_is_rejected(self):
        inputs = dict(REFERENCE["cases"][0]["inputs"])
        inputs["wall_r"] = 0
        with self.assertRaises(ValueError):
            calculate_preliminary(EstimateInputs(**inputs))

    def test_negative_input_is_rejected(self):
        inputs = dict(REFERENCE["cases"][0]["inputs"])
        inputs["ach"] = -1
        with self.assertRaises(ValueError):
            calculate_preliminary(EstimateInputs(**inputs))

    def test_ui_has_one_window_input_and_no_equipment_approval(self):
        from streamlit.testing.v1 import AppTest

        app = AppTest.from_file(str(Path(__file__).parent.parent / "app.py")).run()
        self.assertFalse(app.exception)
        self.assertEqual(
            sum(widget.label == "Window Area (ft²)" for widget in app.number_input), 1
        )
        self.assertTrue(any("Preliminary" in item.value for item in app.warning))
        selected = next(
            widget for widget in app.number_input
            if widget.label == "Selected System Size (tons)"
        )
        selected.set_value(1.0).run()
        self.assertFalse(app.exception)
        self.assertTrue(any("below" in item.value for item in app.warning))
        self.assertFalse(app.success)


if __name__ == "__main__":
    unittest.main()
