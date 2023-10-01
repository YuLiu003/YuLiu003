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
    cx, cy, r = 90, 90, 60
    circumference = 2 * 3.14159 * r
    total_easy = 720
    total_medium = 1522
    total_hard = 634
    solved_percentage = int(stats['solved']) / (total_easy + total_medium + total_hard)
    offset = circumference * (1 - solved_percentage)

    # Bar properties
    bar_width, bar_height = 220, 20

    svg_content = f"""
    <svg width="600" height="200" xmlns="http://www.w3.org/2000/svg" style="background-color:#222; color:white; font-family:Arial, sans-serif">
        <!-- Solved Circle -->
        <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#555" stroke-width="16" />
        <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#orangeGradient)" stroke-width="16" stroke-dasharray="{circumference}" stroke-dashoffset="{offset}" />
        <text x="{cx}" y="{cy + 10}" font-size="32px" fill="white" text-anchor="middle">{stats['solved']}</text>
        <text x="{cx}" y="{cy + 40}" font-size="16px" fill="#aaa" text-anchor="middle">Solved</text>

        <!-- Gradient for circle -->
        <defs>
            <linearGradient id="orangeGradient">
                <stop offset="10%" stop-color="#FFA500" />
                <stop offset="90%" stop-color="#FF4500" />
            </linearGradient>
        </defs>

        <!-- Bars: Base + Fill + Text -->
        <!-- Easy -->
        <rect x="200" y="35" width="{bar_width}" height="{bar_height}" fill="#555" />
        <rect x="200" y="35" width="{bar_width * (int(stats['easy_solved']) / total_easy)}" height="{bar_height}" fill="#81c784" />
        <text x="430" y="50" font-size="14px" fill="white">Easy {stats['easy_solved']}/720 - Beats 79.6%</text>

        <!-- Medium -->
        <rect x="200" y="80" width="{bar_width}" height="{bar_height}" fill="#555" />
        <rect x="200" y="80" width="{bar_width * (int(stats['medium_solved']) / total_medium)}" height="{bar_height}" fill="#FFA500" />
        <text x="430" y="95" font-size="14px" fill="white">Medium {stats['medium_solved']}/1522 - Beats 82.9%</text>

        <!-- Hard -->
        <rect x="200" y="125" width="{bar_width}" height="{bar_height}" fill="#555" />
        <rect x="200" y="125" width="{bar_width * (int(stats['hard_solved']) / total_hard)}" height="{bar_height}" fill="#e57373" />
        <text x="430" y="140" font-size="14px" fill="white">Hard {stats['hard_solved']}/634 - Beats 85.5%</text>
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
