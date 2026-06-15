import os
import unittest
import numpy as np
from pipeline.processing.sonic_vacuum import SonicVacuumProcessor

class TestSonicVacuum(unittest.TestCase):
    def setUp(self):
        self.test_midi = "test_input/Emmanuel.mid"
        self.output_dir = "hymn_remaker/output/test_vacuum"
        os.makedirs(self.output_dir, exist_ok=True)

    def test_speed_variants(self):
        processor = SonicVacuumProcessor(self.test_midi)
        audio, sr = processor.render_dry_piano(None, return_audio=True)
        self.assertIsNotNone(audio)

        output_base = os.path.join(self.output_dir, "emmanuel")
        variant_paths = processor.export_speed_variants(audio, sr, output_base)

        self.assertEqual(len(variant_paths), 3)
        for p in variant_paths:
            self.assertTrue(os.path.exists(p))
            self.assertTrue(p.endswith(".wav"))

if __name__ == "__main__":
    unittest.main()
