import os
import unittest
from unittest.mock import MagicMock, patch
import numpy as np
import shutil
from hymn_remaker.main import process_single_midi
from hymn_remaker.src.suno_remaker import SunoRemaker

class TestMatrixPreprocessing(unittest.TestCase):
    def setUp(self):
        self.test_midi = "test_input/Emmanuel.mid"
        self.output_dir = "hymn_remaker/output/test_matrix"
        os.makedirs(self.output_dir, exist_ok=True)

        # Mock components to avoid external API calls
        self.mock_renderer = MagicMock()
        self.mock_renderer.get_midi_bpm.return_value = 120.0

        # Create a dummy base audio file to satisfy the fallback
        self.base_audio = os.path.join(self.output_dir, "Emmanuel_base.wav")
        with open(self.base_audio, "wb") as f:
            f.write(b"dummy audio data")

        # Use a REAL SunoRemaker but mock its API and browser components
        self.suno_remaker = SunoRemaker()
        self.suno_remaker.api = MagicMock()
        # Mock is_available to return True for the test
        self.suno_remaker.is_available = MagicMock(return_value=True)

        self.mock_content_gen = MagicMock()
        self.mock_content_gen.analyze_audio_for_content.return_value = {
            "metadata": {"title": "Emmanuel"},
            "lyrics": [],
            "theme": "Peaceful",
            "visual_prompt": "Landscape"
        }
        self.mock_content_gen.generate_image.return_value = "black"
        self.mock_content_gen.generate_art_prompt.return_value = "Art prompt"

        self.mock_video = MagicMock()

    def tearDown(self):
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

    @patch('hymn_remaker.src.suno_browser_automation.SunoBrowserAutomation.trigger_generation')
    @patch('hymn_remaker.src.suno_browser_automation.SunoBrowserAutomation.wait_for_completion_and_download')
    @patch('hymn_remaker.main.process_audio')
    def test_suno_matrix_preprocessing(self, mock_process_audio, mock_wait, mock_trigger):
        mock_trigger.return_value = True
        mock_wait.return_value = True

        # Run pipeline with suno_matrix=True
        process_single_midi(
            midi_path=self.test_midi,
            output_dir=self.output_dir,
            style="Deep House",
            skip_render=True, # Skip actual rendering
            skip_remake=False,
            upload=False,
            renderer=self.mock_renderer,
            remaker=MagicMock(),
            suno_remaker=self.suno_remaker,
            content_gen=self.mock_content_gen,
            video_producer=self.mock_video,
            suno_matrix=True
        )

        # Check if dry_render variants exist (created during run_experiment_matrix)
        dry_render_dir = os.path.join(self.output_dir, "dry_render")
        self.assertTrue(os.path.exists(dry_render_dir), f"Directory {dry_render_dir} should exist")

        variants = ["Emmanuel_05x.wav", "Emmanuel_1x.wav", "Emmanuel_2x.wav"]
        for v in variants:
            p = os.path.join(dry_render_dir, v)
            self.assertTrue(os.path.exists(p), f"Variant {p} should exist")

        # Verify that trigger_generation was called 10 times
        # (9 for matrix + 1 for primary remake)
        self.assertEqual(mock_trigger.call_count, 10)

if __name__ == "__main__":
    unittest.main()
