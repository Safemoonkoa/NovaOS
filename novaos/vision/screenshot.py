import mss
import mss.tools
from PIL import Image
import easyocr
import logging
from typing import Dict, Any
import os

logger = logging.getLogger(__name__)

class VisionModule:
    def __init__(self):
        self.sct = mss.mss()
        self.reader = easyocr.Reader(['en'])
        self.screenshot_dir = os.path.expanduser("~/.novaos/screenshots")
        os.makedirs(self.screenshot_dir, exist_ok=True)
        
    def capture_screen(self) -> str:
        """Capture the current screen and save it to a file."""
        monitor = self.sct.monitors[1]
        output = os.path.join(self.screenshot_dir, "current_screen.png")
        sct_img = self.sct.grab(monitor)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        logger.info(f"Screen captured and saved to {output}")
        return output
        
    def extract_text(self, image_path: str) -> str:
        """Extract text from an image using OCR."""
        try:
            result = self.reader.readtext(image_path)
            text = " ".join([res[1] for res in result])
            return text
        except Exception as e:
            logger.error(f"OCR failed: {e}")
            return ""
            
    def analyze_screen(self) -> Dict[str, Any]:
        """Capture screen and extract text for analysis."""
        image_path = self.capture_screen()
        text = self.extract_text(image_path)
        return {
            "image_path": image_path,
            "extracted_text": text
        }
