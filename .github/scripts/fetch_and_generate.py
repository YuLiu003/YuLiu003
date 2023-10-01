import requests
from bs4 import BeautifulSoup
import os

def safe_extract(element):
    if isinstance(element, str):
        return element.strip()
    return element.text.strip() if element else "N/A"



def get_extended_leetcode_stats(yuliu03):
    url = f"https://leetcode.com/{yuliu03}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Using more generic selectors
    solved = safe_extract(soup.select_one('div.absolute div div.text-label-1.font-medium').text)
    easy_solved = safe_extract(soup.select('span.text-base.font-medium')[0])
    medium_solved = safe_extract(soup.select('span.text-base.font-medium')[1])
    hard_solved = safe_extract(soup.select('span.text-base.font-medium')[2])
    submissions_last_year = safe_extract(soup.select_one('span.font-medium:not(.text-base)'))

    if not solved.isdigit():
        raise ValueError(f"Unexpected value for 'solved': {solved}")
    if not easy_solved.isdigit():
        raise ValueError(f"Unexpected value for 'easy_solved': {easy_solved}")
    if not medium_solved.isdigit():
        raise ValueError(f"Unexpected value for 'medium_solved': {medium_solved}")
    if not hard_solved.isdigit():
        raise ValueError(f"Unexpected value for 'hard_solved': {hard_solved}")

        

    return {
        'solved': solved,
        'easy_solved': easy_solved,
        'medium_solved': medium_solved,
        'hard_solved': hard_solved,
        'submissions_last_year': submissions_last_year
    }


def generate_svg(stats):
    # Circle (Donut chart) properties
    cx, cy, r = 60, 60, 45
    circumference = 2 * 3.14159 * r
    total_easy = 720
    total_medium = 1522
    total_hard = 634
    solved_percentage = int(stats['solved']) / (total_easy + total_medium + total_hard)
    offset = circumference * (1 - solved_percentage)

    # Bar properties
    bar_width, bar_height = 120, 14

    svg_content = f"""
    <svg width="380" height="140" xmlns="http://www.w3.org/2000/svg" style="background-color:#222; color:white; font-family:Arial, sans-serif">
        <!-- Solved Circle -->
        <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#555" stroke-width="10" />
        <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#FFA500" stroke-width="10" stroke-dasharray="{circumference}" stroke-dashoffset="{offset}" />
        <text x="{cx}" y="{cy + 5}" font-size="24px" fill="white" text-anchor="middle">{stats['solved']}</text>
        <text x="{cx}" y="{cy + 25}" font-size="12px" fill="#aaa" text-anchor="middle">Solved</text>

        <!-- Bars: Base + Fill + Text -->
        <!-- Easy -->
        <rect x="140" y="30" width="{bar_width}" height="{bar_height}" fill="#555" />
        <rect x="140" y="30" width="{bar_width * (int(stats['easy_solved']) / total_easy)}" height="{bar_height}" fill="#81c784" />
        <text x="270" y="41" font-size="12px" fill="white">Easy {stats['easy_solved']}/720</text>

        <!-- Medium -->
        <rect x="140" y="60" width="{bar_width}" height="{bar_height}" fill="#555" />
        <rect x="140" y="60" width="{bar_width * (int(stats['medium_solved']) / total_medium)}" height="{bar_height}" fill="#FFA500" />
        <text x="270" y="71" font-size="12px" fill="white">Medium {stats['medium_solved']}/1522</text>

        <!-- Hard -->
        <rect x="140" y="90" width="{bar_width}" height="{bar_height}" fill="#555" />
        <rect x="140" y="90" width="{bar_width * (int(stats['hard_solved']) / total_hard)}" height="{bar_height}" fill="#e57373" />
        <text x="270" y="101" font-size="12px" fill="white">Hard {stats['hard_solved']}/634</text>
    </svg>
    """
    return svg_content








if __name__ == "__main__":
    stats = get_extended_leetcode_stats('yuliu03')  # Your LeetCode username
    svg = generate_svg(stats)
    print(svg)  # Add this line to print the generated SVG
    with open('stats.svg', 'w') as f:
        f.write(svg)

    # Check if the SVG file changed and if so, commit it
    os.system("git add stats.svg")
    os.system("git commit -m 'Updated LeetCode Stats'")
    os.system("git push")
