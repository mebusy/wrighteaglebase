import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
content = path.read_text()

pattern = re.compile(
    r"^([ \t]*)g_str\s*\.\s*reserve\s*\(\s*8192\s*\*\s*4\s*\)\s*;", re.MULTILINE
)

if pattern.search(content):
    content = pattern.sub(r"\1// g_str.reserve(8192 * 4);", content, count=1)
    path.write_text(content)
    print("已成功注释 g_str.reserve()")
elif re.search(r"^[ \t]*//.*g_str\s*\.\s*reserve\s*\(", content, re.MULTILINE):
    print("g_str.reserve() 已经注释，无需修改")
else:
    print("错误：没有找到目标语句")
    print("请检查实际内容：")
    for i, line in enumerate(content.splitlines(), 1):
        if "g_str" in line and "reserve" in line:
            print(f"{i}: {line}")
    sys.exit(1)
