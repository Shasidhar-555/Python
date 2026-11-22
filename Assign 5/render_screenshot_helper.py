"""
High-Resolution Color Terminal Screenshot Generator
File: render_screenshot_helper.py
Course: CSA08 - Python Programming (Assignment 5)
Student: V. Karthik Harish (Reg No: 192511328)

Renders text logs into authentic, high-resolution color terminal screenshots
with rich syntax highlighting (Electric Cyan prompt, Emerald Green pass,
Coral Red error, Golden Amber warning, and macOS/Linux traffic light buttons).
"""

import os
from PIL import Image, ImageDraw, ImageFont


def read_text_file(filepath):
    for enc in ['utf-8', 'utf-16', 'utf-16-le', 'cp1252', 'latin-1']:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                return f.readlines()
        except (UnicodeDecodeError, UnicodeError):
            continue
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        return f.readlines()


def render_terminal_screenshot(text_source, output_png_path, title="PowerShell - Python Execution", prompt_cmd="python script.py", max_lines=46):
    if isinstance(text_source, str) and os.path.exists(text_source):
        lines = read_text_file(text_source)
    elif isinstance(text_source, list):
        lines = text_source
    else:
        lines = [str(text_source)]

    font_path = "C:/Windows/Fonts/consola.ttf"
    if not os.path.exists(font_path):
        font_path = "C:/Windows/Fonts/arial.ttf"
        if not os.path.exists(font_path):
            font_path = None

    font_size = 14
    try:
        font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()
        bold_font = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", font_size)
    except:
        font = ImageFont.load_default()
        bold_font = font

    display_lines = []
    display_lines.append(f"PS C:\\Users\\karthik harish\\CSA08-192511328-Assignment5> {prompt_cmd}")
    for raw_l in lines[:max_lines]:
        clean_l = raw_l.rstrip("\r\n")
        display_lines.append(clean_l)

    line_height = 21
    top_bar_height = 38
    padding_x = 22
    padding_bottom = 22

    max_len = max((len(l) for l in display_lines), default=80)
    img_width = max(1000, max_len * 9 + padding_x * 2)
    img_height = top_bar_height + (len(display_lines) * line_height) + padding_bottom

    # Canvas Background: Modern Dark Slate (#0d1117)
    img = Image.new("RGB", (img_width, img_height), color="#0d1117")
    draw = ImageDraw.Draw(img)

    # Window Header Bar (#161b22)
    draw.rectangle([0, 0, img_width, top_bar_height], fill="#161b22")
    draw.line([0, top_bar_height, img_width, top_bar_height], fill="#30363d", width=1)

    # Traffic Light Buttons
    draw.ellipse([16, 12, 28, 24], fill="#ff5f56", outline="#e0443e")  # Red
    draw.ellipse([36, 12, 48, 24], fill="#ffbd2e", outline="#dea123")  # Yellow
    draw.ellipse([56, 12, 68, 24], fill="#27c93f", outline="#1aab29")  # Green

    # Window Title
    draw.text((88, 10), title, fill="#c9d1d9", font=font)

    # Render Terminal Lines
    y = top_bar_height + 12
    for idx, line in enumerate(display_lines):
        line_str = line.strip()
        use_font = font

        if idx == 0:
            color = "#58a6ff"  # Prompt in Cyan
            use_font = bold_font
        elif line_str.startswith("==="):
            color = "#79c0ff"  # Sky blue headers
            use_font = bold_font
        elif line_str.startswith("---"):
            color = "#8b949e"  # Subtle rule
        elif any(k in line for k in ["[✓]", "PASSED", "Success", "SUCCESS", "100% PASS", "agree", "positive"]):
            color = "#3fb950"  # Vivid Emerald Green
        elif any(k in line for k in ["REJECTED", "FAILED", "Error", "ERROR", "Exception", "negative", "injection"]):
            color = "#f85149"  # Vivid Coral Red
        elif any(k in line for k in ["WARN", "Warning", "neutral", "Adversarial", "Fahrenheit"]):
            color = "#e3b341"  # Golden Amber
        elif any(k in line for k in ["STAGE", "TASK", "Task A", "Task B", "Part A", "Part B"]):
            color = "#d2a8ff"  # Soft Lavender
            use_font = bold_font
        elif any(k in line for k in ["Speedup", "Benchmark", "Throughput", "Latency", "Time", "ms", "queries/sec"]):
            color = "#ffa657"  # Warm Tangerine
        elif line_str.startswith("[") and "]" in line_str:
            color = "#56d364"  # Light Mint Green tags
        elif "•" in line or line_str.startswith("TS-") or line_str.startswith("Rule"):
            color = "#58a6ff"  # Bullets / Rules in Blue
        elif ":" in line and len(line.split(":")[0]) < 25:
            color = "#e6edf3"  # Key-value in crisp gray
        else:
            color = "#c9d1d9"  # Console text

        draw.text((padding_x, y), line, fill=color, font=use_font)
        y += line_height

    img.save(output_png_path, "PNG")
    print(f"Rendered color terminal screenshot to {output_png_path}")
