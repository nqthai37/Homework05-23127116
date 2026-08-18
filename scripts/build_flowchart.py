#!/usr/bin/env python3
"""Build the continuous-performance flowchart used by the HW05 report."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "assets" / "continuous-performance-flow.png"
FONT_DIR = Path(r"C:\Windows\Fonts")


def font(name: str, size: int):
    return ImageFont.truetype(str(FONT_DIR / name), size)


REGULAR = font("arial.ttf", 25)
BOLD = font("arialbd.ttf", 27)
SMALL = font("arial.ttf", 21)


def centered_text(draw, box, text, text_font=REGULAR, fill="#17365D"):
    left, top, right, bottom = box
    lines = text.split("\n")
    sizes = [draw.textbbox((0, 0), line, font=text_font) for line in lines]
    widths = [item[2] - item[0] for item in sizes]
    heights = [item[3] - item[1] for item in sizes]
    gap = 7
    y = top + (bottom - top - sum(heights) - gap * (len(lines) - 1)) / 2
    for line, width, height in zip(lines, widths, heights):
        draw.text((left + (right - left - width) / 2, y), line, font=text_font, fill=fill)
        y += height + gap


def rounded(draw, box, text, fill="#EAF2F8", outline="#2F5597"):
    draw.rounded_rectangle(box, radius=22, fill=fill, outline=outline, width=4)
    centered_text(draw, box, text)


def diamond(draw, center, width, height, text):
    x, y = center
    points = [(x, y - height / 2), (x + width / 2, y), (x, y + height / 2), (x - width / 2, y)]
    draw.polygon(points, fill="#FFF2CC", outline="#BF9000", width=4)
    centered_text(
        draw,
        (x - width / 2 + 45, y - height / 2 + 28, x + width / 2 - 45, y + height / 2 - 28),
        text,
        SMALL,
        "#5B4500",
    )


def arrow(draw, start, end, label=None, label_offset=(0, 0)):
    draw.line([start, end], fill="#44546A", width=5)
    x2, y2 = end
    x1, y1 = start
    if abs(x2 - x1) >= abs(y2 - y1):
        direction = 1 if x2 > x1 else -1
        head = [(x2, y2), (x2 - 18 * direction, y2 - 10), (x2 - 18 * direction, y2 + 10)]
    else:
        direction = 1 if y2 > y1 else -1
        head = [(x2, y2), (x2 - 10, y2 - 18 * direction), (x2 + 10, y2 - 18 * direction)]
    draw.polygon(head, fill="#44546A")
    if label:
        midpoint = ((x1 + x2) / 2 + label_offset[0], (y1 + y2) / 2 + label_offset[1])
        draw.text(midpoint, label, font=BOLD, fill="#44546A", anchor="mm")


def main():
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    canvas = Image.new("RGB", (1800, 1060), "white")
    draw = ImageDraw.Draw(canvas)
    title_font = font("arialbd.ttf", 38)
    title = "Continuous Performance Testing Flow"
    title_box = draw.textbbox((0, 0), title, font=title_font)
    draw.text(((1800 - (title_box[2] - title_box[0])) / 2, 28), title, font=title_font, fill="#17365D")

    rounded(draw, (60, 130, 330, 260), "Commit /\npull request")
    rounded(draw, (420, 130, 740, 260), "Classify\nchanged files")
    diamond(draw, (970, 195), 340, 210, "Performance-\nsensitive?")
    rounded(draw, (1260, 130, 1710, 260), "Deploy isolated SUT\nwith fixed data")
    rounded(draw, (1260, 380, 1710, 510), "Run short\nperformance smoke")
    diamond(draw, (970, 445), 340, 210, "Assertion or\nerror gate failed?")
    rounded(draw, (420, 380, 740, 510), "Compare endpoint p95\nwith baseline")
    diamond(draw, (200, 445), 320, 210, "Relative and absolute\ngates exceeded?")
    rounded(draw, (430, 295, 735, 350), "Skip; record reason", fill="#F2F2F2", outline="#7F7F7F")
    rounded(draw, (790, 585, 1150, 645), "Fail; retain artifacts", fill="#FCE4D6", outline="#C65911")
    rounded(draw, (60, 700, 380, 840), "Pass and publish\ntrend", fill="#E2F0D9", outline="#548235")
    rounded(draw, (500, 700, 820, 840), "Repeat test twice\n(three runs total)")
    diamond(draw, (1070, 770), 360, 220, "Reproduced\nin 2 of 3?")
    rounded(draw, (1360, 680, 1740, 810), "Block change or\nrequire approval", fill="#FCE4D6", outline="#C65911")
    rounded(draw, (1360, 870, 1740, 1000), "Flaky warning; retain\nartifacts", fill="#FFF2CC", outline="#BF9000")

    arrow(draw, (330, 195), (420, 195))
    arrow(draw, (740, 195), (800, 195))
    arrow(draw, (1140, 195), (1260, 195), "Yes", (0, -18))
    arrow(draw, (900, 260), (735, 322), "No", (0, -18))
    arrow(draw, (1485, 260), (1485, 380))
    arrow(draw, (1260, 445), (1140, 445))
    arrow(draw, (800, 445), (740, 445), "No", (0, -18))
    arrow(draw, (420, 445), (360, 445))
    arrow(draw, (970, 550), (970, 585), "Yes", (50, 0))
    arrow(draw, (200, 550), (200, 700), "No", (0, -18))
    arrow(draw, (360, 500), (660, 700), "Yes", (0, -18))
    arrow(draw, (820, 770), (890, 770))
    arrow(draw, (1250, 770), (1360, 745), "Yes", (0, -18))
    arrow(draw, (1070, 880), (1360, 935), "No", (0, -18))

    draw.text(
        (60, 1015),
        "PR: changed-file filter + smoke | Nightly: Load/Stress/Spike | Weekly: Endurance",
        font=SMALL,
        fill="#666666",
    )
    canvas.save(TARGET, optimize=True)
    print(TARGET)


if __name__ == "__main__":
    main()
