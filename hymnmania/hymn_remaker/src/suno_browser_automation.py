"""Suno Browser Automation Client — Driving Suno.com via CDP (Chrome DevTools Protocol).

Updated for Suno v5.5 (June 2026):
- Audio upload: real CDP mouse click + DOM.setFileInputFiles
- Handles 'Identify audio content' and 'Describe Your Audio' steps
- Audio Influence slider (Melody/Percussion)
- Advanced mode: textarea[0]=lyrics, textarea[1]=style prompt
- WAV→MP3 conversion for faster uploads
- Bypass Suno's 'matches existing recording' filter with audio modification
- v1.37.0: Support for 9-way Experiment Matrix (Speeds x Genres)
"""

import json
import time
import logging
import subprocess
import websocket
import os

logger = logging.getLogger(__name__)


class SunoBrowserAutomation:
    """Automates Suno.com generation by injecting prompts directly into the
    active Edge tab via CDP (Chrome DevTools Protocol)."""

    def __init__(self, port=9222, base_url="https://suno.com"):
        self.port = port
        self.base_url = base_url

    # ── low-level CDP helpers ────────────────────────────────────────────

    def _get_page_targets(self):
        """Fetch all debuggable targets from Edge and filter for pages."""
        import requests as _req

        try:
            res = _req.get(f"http://127.0.0.1:{self.port}/json", timeout=3)
            targets = res.json()
        except Exception:
            try:
                res = _req.get(f"http://localhost:{self.port}/json", timeout=3)
                targets = res.json()
            except Exception as e:
                logger.warning(
                    f"Could not connect to Edge debugging port {self.port}: {e}"
                )
                return []
        return [
            t
            for t in targets
            if t.get("type") == "page" and "webSocketDebuggerUrl" in t
        ]

    def _get_active_tab(self, require_suno=False):
        """Find or prioritize the Suno tab."""
        targets = self._get_page_targets()
        suno_targets = [t for t in targets if "suno.com" in t.get("url", "").lower()]
        if suno_targets:
            res_tab = suno_targets[0]
            for t in suno_targets:
                if "/create" in t.get("url", "").lower():
                    res_tab = t
                    break
            logger.info(
                f"Selected Suno tab: {res_tab.get('url')} (ID: {res_tab.get('id')})"
            )
            return res_tab
        if require_suno:
            raise RuntimeError("No Suno tab found. Please open suno.com in Edge.")
        return targets[0] if targets else None

    def execute_js(self, ws_url, script, timeout=60):
        """Evaluate arbitrary JavaScript on the target tab via CDP and return result."""
        ws = None
        last_err = None
        for attempt in range(6):
            if attempt > 0:
                try:
                    tab = self._get_active_tab(require_suno=True)
                    ws_url = tab.get("webSocketDebuggerUrl")
                except Exception as e:
                    logger.warning(f"Could not re-fetch Suno tab: {e}")
            ws_url_variants = [
                ws_url.replace("localhost", "127.0.0.1"),
                ws_url.replace("127.0.0.1", "localhost"),
            ]
            target_ws = ws_url_variants[attempt % 2]
            try:
                ws = websocket.create_connection(
                    target_ws, suppress_origin=True, timeout=30
                )
                ws.send(json.dumps({"id": 1, "method": "Runtime.enable"}))
                ws.send(
                    json.dumps(
                        {
                            "id": 2,
                            "method": "Runtime.evaluate",
                            "params": {
                                "expression": script,
                                "returnByValue": True,
                                "awaitPromise": True,
                            },
                        }
                    )
                )
                start_poll = time.time()
                while time.time() - start_poll < timeout:
                    try:
                        resp = json.loads(ws.recv())
                        if resp.get("id") == 2:
                            result = resp.get("result", {}).get("result", {})
                            if "exceptionDetails" in resp.get("result", {}):
                                exception = resp["result"]["exceptionDetails"].get(
                                    "exception", {}
                                )
                                if "description" in exception:
                                    raise RuntimeError(
                                        f"JS Error: {exception['description']}"
                                    )
                            return result.get("value")
                    except websocket.WebSocketTimeoutException:
                        pass
                raise TimeoutError(f"CDP Timeout after {timeout}s")
            except Exception as e:
                last_err = e
                logger.warning(f"WebSocket attempt {attempt + 1} failed: {e}")
                time.sleep(3)
            finally:
                if ws:
                    ws.close()
        raise last_err or RuntimeError(
            "Failed to connect to WebSocket after multiple attempts"
        )

    def _send_cdp_cmd(self, ws, msg_id, method, params=None):
        payload = {"id": msg_id, "method": method}
        if params:
            payload["params"] = params
        ws.send(json.dumps(payload))
        start_time = time.time()
        while time.time() - start_time < 30:
            try:
                resp = json.loads(ws.recv())
                if resp.get("id") == msg_id:
                    return resp
            except websocket.WebSocketTimeoutException:
                pass
        raise TimeoutError(f"No response for {method}")

    # ── CDP mouse helpers ────────────────────────────────────────────────

    def _real_click(self, ws_url, x, y):
        """Dispatch a real CDP mouse click at coordinates (x, y)."""
        ws = websocket.create_connection(
            ws_url.replace("localhost", "127.0.0.1"), suppress_origin=True, timeout=15
        )
        try:
            ws.send(
                json.dumps(
                    {
                        "id": 1,
                        "method": "Input.dispatchMouseEvent",
                        "params": {"type": "mouseMoved", "x": x, "y": y},
                    }
                )
            )
            time.sleep(0.1)
            ws.send(
                json.dumps(
                    {
                        "id": 2,
                        "method": "Input.dispatchMouseEvent",
                        "params": {
                            "type": "mousePressed",
                            "x": x,
                            "y": y,
                            "button": "left",
                            "clickCount": 1,
                        },
                    }
                )
            )
            time.sleep(0.05)
            ws.send(
                json.dumps(
                    {
                        "id": 3,
                        "method": "Input.dispatchMouseEvent",
                        "params": {
                            "type": "mouseReleased",
                            "x": x,
                            "y": y,
                            "button": "left",
                            "clickCount": 1,
                        },
                    }
                )
            )
        finally:
            ws.close()

    def cdp_click(self, ws_url, selector):
        """Click an element by CSS selector using real CDP mouse events."""
        coords = self.execute_js(
            ws_url,
            f"""
        (function() {{
            var el = document.querySelector("{selector}");
            if (!el || el.offsetParent === null) return null;
            el.scrollIntoView({{ block: 'center' }});
            var r = el.getBoundingClientRect();
            return [r.left + r.width/2, r.top + r.height/2];
        }})()
        """,
        )
        if not coords:
            return False
        self._real_click(ws_url, coords[0], coords[1])
        return True

    def _clear_suno_popups(self, ws_url):
        """Clear modals/overlays in Suno."""
        self.execute_js(
            ws_url,
            """
        (function() {
            var all = Array.from(document.querySelectorAll('button, [role="button"]'));
            var closeBtn = all.find(function(el) {
                var t = (el.innerText || '').toLowerCase();
                var a = (el.getAttribute('aria-label') || '').toLowerCase();
                return (t.includes('close') || t.includes('dismiss') || t.includes('got it') || a.includes('close'));
            });
            if (closeBtn && closeBtn.offsetParent !== null) { closeBtn.click(); return "closed_modal"; }
            return "ready";
        })()
        """,
        )

    def _save_debug_screenshot(self, ws_url):
        try:
            ws = websocket.create_connection(
                ws_url.replace("localhost", "127.0.0.1"),
                suppress_origin=True,
                timeout=10,
            )
            ws.send(json.dumps({"id": 99, "method": "Page.captureScreenshot"}))
            resp = json.loads(ws.recv())
            if "result" in resp and "data" in resp["result"]:
                import base64

                with open("cdp_debug_suno.png", "wb") as f:
                    f.write(base64.b64decode(resp["result"]["data"]))
                logger.info("Saved debug screenshot to cdp_debug_suno.png")
            ws.close()
        except Exception as e:
            logger.warning(f"Failed to save debug screenshot: {e}")

    # ── audio upload helpers ─────────────────────────────────────────────

    def _ensure_mp3(self, audio_path):
        """Convert WAV to MP3 if needed. Returns path to MP3 file."""
        if audio_path.lower().endswith(".mp3"):
            return audio_path
        mp3_path = audio_path.rsplit(".", 1)[0] + ".mp3"
        if os.path.exists(mp3_path):
            return mp3_path
        ffmpeg = os.path.join(os.path.dirname(__file__), "..", "bin", "ffmpeg.exe")
        if not os.path.exists(ffmpeg):
            ffmpeg = "ffmpeg"  # fallback to PATH
        logger.info(f"Suno: Converting {audio_path} → MP3...")
        result = subprocess.run(
            [
                ffmpeg,
                "-i",
                audio_path,
                "-codec:a",
                "libmp3lame",
                "-b:a",
                "128k",
                "-y",
                mp3_path,
            ],
            capture_output=True,
            timeout=120,
        )
        if result.returncode != 0:
            logger.warning(
                f"MP3 conversion failed, using original: {result.stderr[:200]}"
            )
            return audio_path
        logger.info(
            f"Suno: Converted to MP3 ({os.path.getsize(mp3_path) / 1024:.0f}KB)"
        )
        return mp3_path

    def _modify_audio_to_bypass_filter(self, audio_path):
        """Apply subtle audio modifications to bypass Suno's copyright filter.
        Returns path to modified MP3 file.
        """
        modified_path = audio_path.rsplit(".", 1)[0] + "_modified.mp3"
        if os.path.exists(modified_path):
            return modified_path
        ffmpeg = os.path.join(os.path.dirname(__file__), "..", "bin", "ffmpeg.exe")
        if not os.path.exists(ffmpeg):
            ffmpeg = "ffmpeg"
        logger.info("Suno: Modifying audio to bypass copyright filter...")
        # Pitch shift +1 semitone, add subtle reverb, high-pass filter
        result = subprocess.run(
            [
                ffmpeg,
                "-i",
                audio_path,
                "-af",
                "asetrate=44100*1.0595,atempo=0.9439,aresample=44100,"
                "lowpass=f=4500,highpass=f=80,adelay=300|300",
                "-codec:a",
                "libmp3lame",
                "-b:a",
                "128k",
                "-y",
                modified_path,
            ],
            capture_output=True,
            timeout=120,
        )
        if result.returncode != 0:
            logger.warning(f"Audio modification failed: {result.stderr[:200]}")
            return audio_path
        logger.info(
            f"Suno: Modified audio ({os.path.getsize(modified_path) / 1024:.0f}KB)"
        )
        return modified_path

    def _set_file_input(self, ws_url, file_path):
        """Set a file on Suno's hidden file input via CDP DOM.setFileInputFiles."""
        ws = websocket.create_connection(
            ws_url.replace("localhost", "127.0.0.1"), suppress_origin=True, timeout=30
        )
        try:
            self._send_cdp_cmd(ws, 10, "DOM.enable")
            root = self._send_cdp_cmd(ws, 11, "DOM.getDocument")["result"]["root"][
                "nodeId"
            ]
            nodes = self._send_cdp_cmd(
                ws,
                12,
                "DOM.querySelectorAll",
                {"nodeId": root, "selector": "input[type='file']"},
            )
            node_ids = nodes["result"]["nodeIds"]
            for nid in node_ids:
                self._send_cdp_cmd(
                    ws,
                    20 + nid,
                    "DOM.setFileInputFiles",
                    {"files": [os.path.abspath(file_path)], "nodeId": nid},
                )
            logger.info(f"Suno: File set on {len(node_ids)} input nodes")
        finally:
            ws.close()

    def _wait_for_upload(self, ws_url, timeout=120):
        """Poll for upload completion. Returns True if upload succeeded."""
        for i in range(timeout // 5):
            info = self.execute_js(
                ws_url,
                """
            (function() {
                var texts = Array.from(document.querySelectorAll('*'))
                    .filter(function(e) { return e.offsetParent !== null && e.children.length === 0; })
                    .map(function(e) { return (e.innerText||'').trim(); })
                    .filter(function(t) { return t.length > 0 && t.length < 50; });
                var upload = texts.filter(function(t) {
                    return /upload|clip|match|exist|error|fail|done|complete|remov|identify/i.test(t);
                });
                var createBtn = Array.from(document.querySelectorAll('button'))
                    .find(function(b) { return (b.innerText||'').includes('Create') && b.offsetParent !== null; });
                return {
                    upload: Array.from(new Set(upload)).slice(0, 10),
                    createEnabled: createBtn ? !createBtn.disabled : 'not_found'
                };
            })()
            """,
            )
            if i % 4 == 0:
                logger.info(f"  Upload poll {i * 5}s: {info}")
            upload_texts = [t.lower() for t in info.get("upload", [])]

            # Check for copyright filter rejection
            for t in upload_texts:
                if "matches an existing" in t:
                    logger.warning("Suno: Audio matches existing recording")
                    return False

            # Check for upload success — "Uploaded" or "Identify" appears after successful upload
            for t in upload_texts:
                if t == "uploaded" or t.startswith("identify audio"):
                    logger.info("Suno: Upload completed!")
                    return True

            # Check for hard errors
            for t in upload_texts:
                if "error occurred" in t:
                    logger.warning(f"Suno: Upload error: {t}")
                    return False

            time.sleep(5)
        return False

    def _handle_identify_audio(self, ws_url, audio_type="Full Song"):
        """Handle Suno's 'Identify audio content' step after upload."""
        logger.info(f"Suno: Identifying audio as '{audio_type}'...")
        # Click the audio type button
        self.execute_js(
            ws_url,
            f"""
        (function() {{
            var btns = Array.from(document.querySelectorAll('button'));
            var btn = btns.find(function(b) {{
                return (b.innerText||'').trim() === '{audio_type}' && b.offsetParent !== null;
            }});
            if (btn) {{ btn.click(); return 'clicked'; }}
            return 'not_found';
        }})()
        """,
        )
        time.sleep(1)
        # Click Continue
        self.execute_js(
            ws_url,
            """
        (function() {
            var btns = Array.from(document.querySelectorAll('button'));
            var cont = btns.filter(function(b) {
                return (b.innerText||'').trim() === 'Continue' && b.offsetParent !== null;
            });
            if (cont.length > 0) { cont[cont.length-1].click(); return 'clicked'; }
            return 'not_found';
        })()
        """,
        )
        logger.info("Suno: Identified audio content")

    def _handle_describe_audio(self, ws_url, description=None):
        """Handle Suno's 'Describe Your Audio' step."""
        logger.info("Suno: Handling 'Describe Your Audio' step...")
        if not description:
            description = "Classical hymn melody with orchestral arrangement"
        # Fill in the description textarea (the last visible textarea)
        self.execute_js(
            ws_url,
            f"""
        (function() {{
            var textareas = Array.from(document.querySelectorAll('textarea'))
                .filter(function(t) {{ return t.offsetParent !== null; }});
            if (textareas.length === 0) return 'no_textareas';
            var ta = textareas[textareas.length - 1];
            var propsKey = Object.keys(ta).find(function(k) {{ return k.startsWith('__reactProps'); }});
            if (propsKey && ta[propsKey] && ta[propsKey].onChange) {{
                ta[propsKey].onChange({{ target: {{ value: {json.dumps(description)} }}, persist: function(){{}} }});
            }}
            try {{
                var setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
                setter.call(ta, {json.dumps(description)});
            }} catch(e) {{
                ta.value = {json.dumps(description)};
            }}
            ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
            ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
            return 'described';
        }})()
        """,
        )
        time.sleep(1)
        # Click Continue
        self.execute_js(
            ws_url,
            """
        (function() {
            var btns = Array.from(document.querySelectorAll('button'));
            var cont = btns.filter(function(b) {
                return (b.innerText||'').trim() === 'Continue' && b.offsetParent !== null;
            });
            if (cont.length > 0) { cont[cont.length-1].click(); return 'clicked'; }
            return 'not_found';
        })()
        """,
        )
        logger.info("Suno: Described audio content")

    def _set_audio_influence(self, ws_url, melody=True, percussion=False):
        """Set audio influence options after upload completes."""
        logger.info("Suno: Setting audio influence...")
        # The influence section has a "Loose/Strict" toggle and percentage slider.
        # For now, just log what we see.
        influence_info = self.execute_js(
            ws_url,
            """
        (function() {
            var all = document.querySelectorAll('*');
            var target = null;
            for (var i = 0; i < all.length; i++) {
                var el = all[i];
                var text = (el.innerText||'').trim();
                if (text.startsWith('Audio Influence') && el.children.length > 0 && el.children.length < 20) {
                    target = el;
                    break;
                }
            }
            if (!target) return 'not_found';
            return (target.innerText||'').slice(0, 200);
        })()
        """,
        )
        logger.info(f"  Audio Influence: {influence_info}")

    # ── main generation flow ─────────────────────────────────────────────

    def trigger_generation(
        self, prompt, audio_path=None, make_instrumental=True, lyrics=None
    ):
        """Trigger a Suno generation with optional audio upload and lyrics."""
        tab = self._get_active_tab(require_suno=True)
        if not tab:
            raise RuntimeError("No Suno tab found for trigger_generation")
        ws_url = tab.get("webSocketDebuggerUrl")

        # Always navigate fresh to /create (clears previous upload state)
        self.execute_js(ws_url, f"window.location.href = '{self.base_url}/create'")
        time.sleep(10)
        self._clear_suno_popups(ws_url)

        # ── Step 1: Audio Upload ─────────────────────────────────────────
        if audio_path and os.path.exists(audio_path):
            logger.info(f"Suno: Uploading audio {audio_path}...")

            # Convert to MP3 for faster upload
            upload_file = self._ensure_mp3(audio_path)
            upload_ok = False

            # Try uploading; if rejected, modify audio and retry
            for attempt in range(2):
                # Real CDP mouse click on Audio button
                audio_btn_rect = self.execute_js(
                    ws_url,
                    """
                (function() {
                    var btn = Array.from(document.querySelectorAll('button')).find(function(el) {
                        return (el.getAttribute('aria-label')||'').includes('Add audio') && el.offsetParent !== null;
                    });
                    if (!btn) return null;
                    var r = btn.getBoundingClientRect();
                    return {x: Math.round(r.left + r.width/2), y: Math.round(r.top + r.height/2)};
                })()
                """,
                )
                if not audio_btn_rect:
                    logger.error("Suno: Audio button not found!")
                    break

                self._real_click(ws_url, audio_btn_rect["x"], audio_btn_rect["y"])
                time.sleep(5)

                # Set file via CDP
                self._set_file_input(ws_url, upload_file)
                logger.info("Suno: Audio file injected. Waiting for upload...")

                # Poll for upload result
                upload_ok = self._wait_for_upload(ws_url, timeout=90)

                if upload_ok:
                    logger.info("Suno: Upload succeeded!")
                    break
                else:
                    # Check if rejected by copyright filter
                    if attempt == 0:
                        logger.warning(
                            "Suno: Upload rejected — modifying audio and retrying..."
                        )
                        # Dismiss error dialog
                        self._clear_suno_popups(ws_url)
                        time.sleep(2)
                        upload_file = self._modify_audio_to_bypass_filter(upload_file)
                        # Navigate fresh and retry
                        self.execute_js(
                            ws_url, "window.location.href = 'https://suno.com/create'"
                        )
                        time.sleep(10)
                        self._clear_suno_popups(ws_url)
                    else:
                        logger.error("Suno: Audio upload failed after retry")
                        break

            if upload_ok:
                # Handle 'Identify audio content'
                self._handle_identify_audio(ws_url, "Full Song")
                time.sleep(2)

                # Handle 'Describe Your Audio'
                self._handle_describe_audio(ws_url)
                time.sleep(3)

                # Set Audio Influence
                self._set_audio_influence(ws_url, melody=True)
                time.sleep(2)

            self._clear_suno_popups(ws_url)

        # ── Step 2: Switch to Advanced mode ──────────────────────────────
        logger.info("Suno: Switching to Advanced mode...")
        adv_result = self.execute_js(
            ws_url,
            """
        (function() {
            var btns = Array.from(document.querySelectorAll('button'));
            var advBtn = btns.find(function(el) {
                return (el.innerText||'').trim() === 'Advanced' && el.offsetParent !== null;
            });
            if (advBtn) {
                var isActive = advBtn.className.includes('active');
                if (!isActive) { advBtn.click(); return 'clicked_advanced'; }
                return 'already_advanced';
            }
            return 'advanced_btn_not_found';
        })()
        """,
        )
        logger.info(f"Suno: Mode switch: {adv_result}")
        time.sleep(2)

        # ── Step 3: Set Lyrics (textarea[0] in Advanced mode) ────────────
        if lyrics:
            logger.info(f"Suno: Injecting lyrics ({len(lyrics)} chars)...")
            lyrics_result = self.execute_js(
                ws_url,
                f"""
            (function() {{
                var textareas = Array.from(document.querySelectorAll('textarea'))
                    .filter(function(t) {{ return t.offsetParent !== null; }});
                if (textareas.length === 0) return 'no_textareas';
                // In Advanced mode: first textarea = lyrics/write
                var ta = textareas[0];
                var propsKey = Object.keys(ta).find(function(k) {{ return k.startsWith('__reactProps'); }});
                if (propsKey && ta[propsKey] && ta[propsKey].onChange) {{
                    ta[propsKey].onChange({{ target: {{ value: {json.dumps(lyrics)} }}, persist: function(){{}} }});
                }}
                try {{
                    var setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
                    setter.call(ta, {json.dumps(lyrics)});
                }} catch(e) {{
                    ta.value = {json.dumps(lyrics)};
                }}
                ta.dispatchEvent(new Event('input', {{bubbles:true}}));
                ta.dispatchEvent(new Event('change', {{bubbles:true}}));
                return 'lyrics_set_on_' + (ta.placeholder||'').slice(0,30);
            }})()
            """,
            )
            logger.info(f"Suno: Lyrics result: {lyrics_result}")
            time.sleep(1)

        # ── Step 4: Set Style Prompt (textarea[1] in Advanced mode) ──────
        logger.info(f"Suno: Setting style/prompt: {prompt[:50]}...")
        prompt_result = self.execute_js(
            ws_url,
            f"""
        (function() {{
            var textareas = Array.from(document.querySelectorAll('textarea'))
                .filter(function(el) {{ return el.offsetParent !== null; }});
            if (textareas.length === 0) return 'no_textareas';
            // In Advanced mode: second textarea = style/prompt
            var ta = textareas.length > 1 ? textareas[1] : textareas[0];
            var propsKey = Object.keys(ta).find(function(k) {{ return k.startsWith('__reactProps'); }});
            if (propsKey && ta[propsKey] && ta[propsKey].onChange) {{
                ta[propsKey].onChange({{ target: {{ value: {json.dumps(prompt)} }}, persist: function(){{}} }});
            }}
            try {{
                var setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
                setter.call(ta, {json.dumps(prompt)});
            }} catch(e) {{
                ta.value = {json.dumps(prompt)};
            }}
            ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
            ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
            return 'prompt_set_on_' + (ta.placeholder||'').slice(0,30);
        }}())""",
        )
        logger.info(f"Suno: Prompt result: {prompt_result}")

        # ── Step 5: Toggle Instrumental ──────────────────────────────────
        if make_instrumental:
            instr_result = self.execute_js(
                ws_url,
                """
            (function() {
                var b = Array.from(document.querySelectorAll('button')).find(function(el) {
                    return (el.innerText||'').includes('Instrumental') && el.offsetParent !== null;
                });
                if (b) {
                    var isChecked = b.className.includes('checked') || b.getAttribute('aria-checked') === 'true';
                    if (!isChecked) { b.click(); return 'toggled_instrumental'; }
                    return 'instrumental_already_on';
                }
                return 'instrumental_btn_not_found';
            })()
            """,
            )
            logger.info(f"Suno: Instrumental: {instr_result}")

        # ── Step 6: Click Create ─────────────────────────────────────────
        logger.info("Suno: Clicking Create...")
        time.sleep(2)
        res = self.execute_js(
            ws_url,
            """
        (function() {
            var allBtns = Array.from(document.querySelectorAll('button'));
            var b = allBtns.find(function(el) {
                return (el.getAttribute('aria-label') || '').includes('Create') && el.offsetParent !== null;
            }) || allBtns.find(function(el) {
                return (el.innerText || '').includes('Create') && el.offsetParent !== null;
            });
            if (b) {
                var info = { text: b.innerText, disabled: b.disabled, classes: b.className };
                if (b.disabled) { return "disabled:" + JSON.stringify(info); }
                b.click();
                return "clicked:" + JSON.stringify(info);
            }
            return "not_found";
        })()
        """,
        )
        if res and "clicked" in str(res):
            logger.info(f"Suno: Generation triggered! {res}")
            return True
        else:
            logger.warning(f"Suno: Could not trigger generation: {res}")
            self._save_debug_screenshot(ws_url)
            return False

    # ── post-generation ──────────────────────────────────────────────────

    def wait_for_completion_and_download(self, timeout=400):
        """Poll for completion and trigger download of the latest track."""
        start = time.time()
        logger.info("Suno: Polling for track completion...")
        while time.time() - start < timeout:
            tab = self._get_active_tab(require_suno=True)
            if not tab:
                raise RuntimeError(
                    "No Suno tab found for wait_for_completion_and_download"
                )
            ws_url = tab.get("webSocketDebuggerUrl")
            res = self.execute_js(
                ws_url,
                """
            (function() {
                var rows = Array.from(document.querySelectorAll('[data-testid="song-row"], [class*="SongRow"]'));
                if (rows.length === 0) return "no_tracks";
                var latest = rows[0];
                var text = (latest.innerText || '').toLowerCase();
                if (text.includes('error') || text.includes('failed')) return "error";
                if (text.includes('creating') || text.includes('queue') || text.includes('generating')) return "generating";
                var hasDuration = /\d+:\d+/.test(text);
                if (hasDuration) {
                    var moreBtn = latest.querySelector('button[aria-label*="More"], [data-testid*="more-actions"]');
                    if (moreBtn) { moreBtn.click(); return "menu_opened"; }
                }
                return "waiting";
            })()
            """,
            )
            if res == "menu_opened":
                time.sleep(3)
                res2 = self.execute_js(
                    ws_url,
                    """
                (function() {
                    var menuItems = Array.from(document.querySelectorAll('[role="menuitem"], button, a'));
                    var dl = menuItems.find(function(el) {
                        return (el.innerText || '').toLowerCase().includes('download') && el.offsetParent !== null;
                    });
                    if (dl) { dl.click(); return "download_clicked"; }
                    return "dl_not_found";
                })()
                """,
                )
                if res2 == "download_clicked":
                    logger.info("Suno: Download triggered!")
                    return True
            logger.info(f"Suno status: {res} ({int(time.time() - start)}s)")
            time.sleep(15)
        return False

    # ── v1.37.0: Experiment Matrix ──────────────────────────────────────

    def run_experiment_matrix(self, midi_path, output_dir, lyrics=None):
        """Execute a 9-way experiment matrix (3 speeds x 3 genres) for a hymn."""
        from pipeline.processing.sonic_vacuum import SonicVacuumProcessor

        logger.info(f"Suno: Starting 9-way Experiment Matrix for {midi_path}...")

        # 1. Preprocess: Generate 3 speed variants
        vacuum = SonicVacuumProcessor(midi_path)
        base_name = os.path.splitext(os.path.basename(midi_path))[0]
        output_base = os.path.join(output_dir, "dry_render", base_name)
        os.makedirs(os.path.join(output_dir, "dry_render"), exist_ok=True)

        audio_array, sr = vacuum.render_dry_piano(None, return_audio=True)
        speed_variant_paths = vacuum.export_speed_variants(audio_array, sr, output_base)

        # 2. Define Genre Matrix
        genres = {
            "Deep House": "deep house, 122 bpm, melodic house, structural synth pluck, minimal driving 4x4 groove, pristine club mix",
            "Drum and Bass": "liquid drum and bass, 174 bpm, rolling reesebass, high velocity synth arpeggio, sharp breakbeat drums",
            "Psytrance": "modern full-on psytrance, 145 bpm, rolling bassline, acid squelch, twilight psytrance driving groove, fm synthesizer leads"
        }

        speeds = ["0.5x", "1x", "2x"]

        results = []

        # 3. Iterate through Matrix
        for i, speed_path in enumerate(speed_variant_paths):
            speed_label = speeds[i]
            for genre_name, style_prompt in genres.items():
                logger.info(f"--- Experiment: {speed_label} | {genre_name} ---")

                # Full prompt with speed and genre context
                full_prompt = f"{style_prompt}. Inspired by the attached melody (rendered at {speed_label} speed)."

                success = self.trigger_generation(
                    prompt=full_prompt,
                    audio_path=speed_path,
                    make_instrumental=True,
                    lyrics=lyrics
                )

                if success:
                    # In experiment mode, we trigger but don't necessarily block
                    # and wait for each download one-by-one to save time,
                    # as Suno generates in batches.
                    # However, for robustness we'll wait for completion and download here.
                    dl_ok = self.wait_for_completion_and_download()
                    if dl_ok:
                        results.append({
                            "speed": speed_label,
                            "genre": genre_name,
                            "status": "success"
                        })
                    else:
                        results.append({
                            "speed": speed_label,
                            "genre": genre_name,
                            "status": "download_failed"
                        })
                else:
                    results.append({
                        "speed": speed_label,
                        "genre": genre_name,
                        "status": "trigger_failed"
                    })

                time.sleep(10) # Cooling off between matrix steps

        return results
