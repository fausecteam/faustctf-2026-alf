import ctypes
import os
import logging
import base64

lib_path = os.path.join(os.path.dirname(__file__), "libparser.so")
C_library = ctypes.CDLL(lib_path)

C_library.translate.argtypes = [ctypes.c_char_p]
C_library.translate.restype = ctypes.c_char_p

def translate(text: str) -> str:
    input_bytes = base64.b64decode(text)
    input_bytes = input_bytes if input_bytes[-1] in b"!?." else input_bytes + b"."
    output_bytes = C_library.translate(input_bytes)
    
    try:
        return base64.b64encode(output_bytes).decode()
    except:
        logging.error(output_bytes)
        return "Translation failed!"

