#!/usr/bin/python

import time, os
from datetime import datetime
import pyperclip

"""
save_clipboard_to_file.py
Run it in your terminal or as a background process. It appends new clipboard items to daily file.
Usage:
 python save_clipboard_to_file.py
"""

out = os.path.expanduser('~/clipboard_history')
os.makedirs(out, exist_ok=True)
last = None
while True:
    try:
        txt = pyperclip.paste()
    except Exception:
        txt = ''
    if txt and txt != last:
        last = txt
        fn = os.path.join(out, datetime.now().strftime('%Y-%m-%d') + '.txt')
        with open(fn, 'a', encoding='utf-8') as f:
            f.write(f"\n\n[{datetime.now().isoformat()}]\n{txt}\n")
        print("Saved to", fn)
    time.sleep(1.5)
