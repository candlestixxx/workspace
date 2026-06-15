"""Psy-Mono Bridge: Reverse Engineering Suno/Udio Audio back to Ableton MIDI/Projects.

This module implements the 'Reverse Engineering' pipeline:
1. Stem Separation (Demucs)
2. Audio-to-MIDI (Basic-Pitch)
3. Programmatic Ableton Assembly (AbletonOSC / pylive)
"""

import os
import subprocess
import logging
import time
from pathlib import Path

logger = logging.getLogger(__name__)

class PsyMonoBridge:
    def __init__(self, ableton_host="127.0.0.1", ableton_port=11000):
        self.ableton_host = ableton_host
        self.ableton_port = ableton_port

    def separate_stems(self, audio_path, output_dir):
        """Step 1: Isolate stems using Demucs."""
        logger.info(f"Bridge: Separating stems for {audio_path}...")
        os.makedirs(output_dir, exist_ok=True)

        # We use the subprocess to call demucs
        # --two-stems=vocals is often useful to just get vocals vs everything else
        # but here we might want all 4 (drums, bass, other, vocals)
        cmd = [
            "python", "-m", "demucs.separate",
            "--out", output_dir,
            audio_path
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info("Bridge: Stem separation complete.")
            # Demucs creates a folder named after the model (e.g. htdemucs)
            # and then a folder named after the file.
            return os.path.join(output_dir, "htdemucs", Path(audio_path).stem)
        except Exception as e:
            logger.error(f"Bridge: Demucs failed: {e}")
            return None

    def audio_to_midi(self, audio_path, output_midi_path):
        """Step 2: Convert an instrumental stem to MIDI using basic-pitch."""
        logger.info(f"Bridge: Converting {audio_path} to MIDI...")

        cmd = [
            "basic-pitch",
            os.path.dirname(output_midi_path),
            audio_path
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            # basic-pitch usually outputs [input_name]_basic_pitch.mid
            generated_mid = audio_path.rsplit(".", 1)[0] + "_basic_pitch.mid"
            if os.path.exists(generated_mid):
                import shutil
                shutil.move(generated_mid, output_midi_path)
                logger.info(f"Bridge: MIDI generated at {output_midi_path}")
                return output_midi_path
        except Exception as e:
            logger.error(f"Bridge: Audio-to-MIDI failed: {e}")
            return None

    def assemble_pro_song(self, midi_map, vocal_path, target_bpm=124):
        """Step 3: Connect to Ableton Live and inject MIDI/Audio."""
        try:
            from live.set import Set
            logger.info("Bridge: Connecting to Ableton Live via AbletonOSC...")

            # This requires Ableton Live to be running with AbletonOSC extension
            live_set = Set(scan=True)
            live_set.tempo = target_bpm

            # Map MIDI files to tracks
            # midi_map is a dict: {track_index: midi_path}
            for track_idx, midi_path in midi_map.items():
                if track_idx < len(live_set.tracks):
                    track = live_set.tracks[track_idx]
                    logger.info(f"Bridge: Injecting MIDI into Track {track_idx} ({track.name})")
                    # Simplified: create a clip and assume the user has a way to load MIDI data
                    # In a real setup, we'd use pylive or OSC to send Note messages
                    # or load the MIDI file into a clip slot.
                    track.create_clip(slot_index=0, length_in_beats=32)
                    # Note: Loading literal .mid files via OSC is DAW-dependent.

            # Handle Vocals
            if vocal_path and os.path.exists(vocal_path):
                # In a real script, we'd use an OSC command to 'load_sample' if supported
                logger.info(f"Bridge: Vocals ready for manual import or automated load: {vocal_path}")

            logger.info("Bridge: Ableton assembly commands sent.")
            return True
        except ImportError:
            logger.error("Bridge: 'pylive' not installed. Cannot control Ableton.")
            return False
        except Exception as e:
            logger.error(f"Bridge: Ableton assembly failed: {e}")
            return False

    def run_full_reversal(self, suno_audio_path, output_dir):
        """Execute the entire reversal pipeline."""
        # 1. Separate
        stem_dir = self.separate_stems(suno_audio_path, os.path.join(output_dir, "stems"))
        if not stem_dir: return False

        # Expected stems: drums.wav, bass.wav, other.wav, vocals.wav
        bass_wav = os.path.join(stem_dir, "bass.wav")
        other_wav = os.path.join(stem_dir, "other.wav")
        vocal_wav = os.path.join(stem_dir, "vocals.wav")

        # 2. Extract MIDI
        midi_map = {}
        if os.path.exists(bass_wav):
            bass_mid = os.path.join(output_dir, "extracted_bass.mid")
            if self.audio_to_midi(bass_wav, bass_mid):
                midi_map[1] = bass_mid # Assume Track 2 is Bass

        if os.path.exists(other_wav):
            lead_mid = os.path.join(output_dir, "extracted_lead.mid")
            if self.audio_to_midi(other_wav, lead_mid):
                midi_map[2] = lead_mid # Assume Track 3 is Leads

        # 3. Assemble
        return self.assemble_pro_song(midi_map, vocal_wav)
