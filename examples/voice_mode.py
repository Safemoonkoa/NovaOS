"""
NovaOS Example: Voice Mode
--------------------------
Demonstrates hands-free voice control using the global hotkey listener.
Press Ctrl+Alt+N to start speaking.
"""

import time
from novaos.core.agent import NovaAgent
from novaos.voice.stt import SpeechToText
from novaos.voice.tts import TextToSpeech
from novaos.voice.hotkey import HotkeyListener

agent = NovaAgent()
stt = SpeechToText()
tts = TextToSpeech()

def on_hotkey():
    print("[NovaOS] Listening... (5 seconds)")
    text = stt.transcribe_microphone(duration=5.0)
    if text:
        print(f"[You] {text}")
        response = agent.process_command(text)
        print(f"[NovaOS] {response}")
        tts.speak(response)
    else:
        print("[NovaOS] Could not understand audio.")

listener = HotkeyListener(callback=on_hotkey)
listener.start()

print("[NovaOS] Voice mode active. Press Ctrl+Alt+N to speak. Ctrl+C to exit.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    listener.stop()
    print("[NovaOS] Voice mode stopped.")
