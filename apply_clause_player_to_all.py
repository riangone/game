#!/usr/bin/env python3
"""Inject ClausePlayer assets and initialization into all textbook lessons.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent

LESSONS = [
    {"file": "hanjia-jianwen.html", "slug": "hanjia"},
    {"file": "gugong.html", "slug": "gugong"},
    {"file": "yiheyuan.html", "slug": "yiheyuan"},
    {"file": "luotuo-he-yang.html", "slug": "luotuo"},
    {"file": "xiaoma-guohe.html", "slug": "xiaoma"},
    {"file": "houzi-lao-yueliang.html", "slug": "houzi"},
    {"file": "sima-guang.html", "slug": "sima"},
    {"file": "shu-xingxing.html", "slug": "xingxing"},
    {"file": "gushi-er-shou.html", "slug": "gushi"},
    {"file": "diqiu-qingjiegong.html", "slug": "diqiu"},
    {"file": "daziran-yuyan.html", "slug": "daziran"},
    {"file": "tanyue.html", "slug": "tanyue"},
]

def apply_to_file(html_name, slug):
    path = ROOT / html_name
    if not path.exists():
        print(f"File {html_name} not found, skipping.")
        return

    content = path.read_text(encoding="utf-8")

    # 1. Add CSS & JS in head if not present
    if "clause-player.js" not in content:
        if '<script src="js/voice-recorder.js"></script>' in content:
            content = content.replace(
                '<script src="js/voice-recorder.js"></script>',
                '<script src="js/voice-recorder.js"></script>\n<link rel="stylesheet" href="js/clause-player.css">\n<script src="js/clause-player.js"></script>'
            )
        elif '</head>' in content:
            content = content.replace(
                '</head>',
                '<link rel="stylesheet" href="js/clause-player.css">\n<script src="js/clause-player.js"></script>\n</head>'
            )
        print(f"  + Added clause-player tags to <head> in {html_name}")

    # 2. Add ClausePlayer.init before final </script>
    init_snippet = f"""if (typeof ClausePlayer !== 'undefined') {{
  ClausePlayer.init({{ lessonSlug: '{slug}', storyArray: STORY }});
}}
</script>"""

    if f"ClausePlayer.init({{ lessonSlug: '{slug}'" not in content and "ClausePlayer.init({" not in content:
        # Replace the last </script>
        last_script_idx = content.rfind("</script>")
        if last_script_idx != -1:
            content = content[:last_script_idx] + init_snippet + content[last_script_idx + len("</script>"):]
            print(f"  + Injected ClausePlayer.init in {html_name}")
        else:
            print(f"  ! Warning: no </script> found in {html_name}")
    else:
        print(f"  = ClausePlayer.init already present in {html_name}")

    path.write_text(content, encoding="utf-8")
    print(f"✓ Updated {html_name} successfully.")

def main():
    print("Applying ClausePlayer to all 12 Chinese lessons...")
    for item in LESSONS:
        apply_to_file(item["file"], item["slug"])
    print("\nAll lessons successfully updated!")

if __name__ == "__main__":
    main()
