import os
import sys
from PIL import Image, ImageDraw, ImageFont

def read_text_file(filepath):
    for enc in ['utf-8', 'utf-16', 'utf-16-le', 'cp1252', 'latin-1']:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                return f.readlines()
        except UnicodeDecodeError:
            continue
    with open(filepath, 'r', errors='replace') as f:
        return f.readlines()

def render_terminal_screenshot(text_lines, output_png_path, title="PowerShell - python task", prompt_cmd="python task.py", max_lines=42):
    """
    Renders text lines into an authentic, crisp terminal screenshot PNG.
    """
    font_path = "C:/Windows/Fonts/consola.ttf"
    if not os.path.exists(font_path):
        font_path = "arial.ttf"
    
    font_size = 14
    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()

    # Pre-process lines
    display_lines = []
    display_lines.append(f"PS C:\\Users\\karthik harish\\CSA08-192511328-Assignment3> {prompt_cmd}")
    for l in text_lines[:max_lines]:
        display_lines.append(l.rstrip())
    
    line_height = 20
    top_bar_height = 36
    padding_x = 20
    padding_bottom = 20
    
    max_len = max((len(l) for l in display_lines), default=80)
    img_width = max(980, max_len * 9 + padding_x * 2)
    img_height = top_bar_height + (len(display_lines) * line_height) + padding_bottom
    
    # Background
    img = Image.new("RGB", (img_width, img_height), color="#0d1117")
    draw = ImageDraw.Draw(img)
    
    # Window Header Bar
    draw.rectangle([0, 0, img_width, top_bar_height], fill="#161b22")
    draw.line([0, top_bar_height, img_width, top_bar_height], fill="#30363d", width=1)
    
    # Window control circles (macOS / Modern style)
    draw.ellipse([15, 12, 27, 24], fill="#ff5f56")  # Close
    draw.ellipse([35, 12, 47, 24], fill="#ffbd2e")  # Minimize
    draw.ellipse([55, 12, 67, 24], fill="#27c93f")  # Maximize
    
    # Window Title
    title_font = font
    draw.text((85, 10), title, fill="#8b949e", font=title_font)
    
    # Terminal Lines
    y = top_bar_height + 12
    for idx, line in enumerate(display_lines):
        if idx == 0:
            color = "#58a6ff"  # Prompt line in light blue
        elif line.startswith("="):
            color = "#79c0ff"
        elif line.startswith("[✓]") or "True" in line:
            color = "#7ee787"
        elif line.startswith("[") and "]" in line:
            color = "#f2cc60"
        elif line.startswith("•"):
            color = "#e6edf3"
        elif line.startswith("---") or line.startswith("Reading") or "Key" in line:
            color = "#d2a8ff"
        elif "Speedup" in line or "Matches" in line or "Memory" in line:
            color = "#ffa657"
        else:
            color = "#c9d1d9"
            
        draw.text((padding_x, y), line, fill=color, font=font)
        y += line_height
        
    img.save(output_png_path, "PNG")
    print(f"Rendered terminal screenshot to {output_png_path}")

if __name__ == "__main__":
    lines = read_text_file(r"C:\Users\karthik harish\.gemini\antigravity\scratch\CSA08-192511328-Assignment3\Q1_Rainfall_Analysis\output.txt")
    render_terminal_screenshot(
        lines,
        r"C:\Users\karthik harish\.gemini\antigravity\scratch\CSA08-192511328-Assignment3\Q1_Rainfall_Analysis\output_screenshot.png",
        title="Windows PowerShell - python Q1_Rainfall_Analysis/q1_rainfall.py",
        prompt_cmd="python Q1_Rainfall_Analysis/q1_rainfall.py",
        max_lines=48
    )
