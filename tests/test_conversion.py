import unittest

from authlab.convert import convert_rules


class ConversionTests(unittest.TestCase):
    def test_every_detection_produces_reviewable_spl(self) -> None:
        results = convert_rules("splunk")
        self.assertEqual(len(results), 5)
        self.assertTrue(all(result["ok"] for result in results), results)
        self.assertEqual(
            sum(result["mode"] == "compatibility" for result in results),
            2,
        )


if __name__ == "__main__":
    unittest.main()
