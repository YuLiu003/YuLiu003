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
    # For the circle bar (donut chart)
    circle_radius = 46
    circle_circumference = 2 * 3.141592653589793 * circle_radius
    percent_solved = int(stats['solved']) / (int(stats['easy_solved']) + int(stats['medium_solved']) + int(stats['hard_solved']))
    circle_dashoffset = circle_circumference * (1 - percent_solved)

    # For horizontal bars
    max_easy = 720
    max_medium = 1522
    max_hard = 634
    bar_width = 150
    easy_width = (int(stats['easy_solved']) / max_easy) * bar_width
    medium_width = (int(stats['medium_solved']) / max_medium) * bar_width
    hard_width = (int(stats['hard_solved']) / max_hard) * bar_width

    svg_content = f"""
    <svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
        <!-- Circle bar for total solved problems -->
        <circle cx="60" cy="100" r="{circle_radius}" fill="none" stroke="#e0e0e0" stroke-width="8"></circle>
        <circle cx="60" cy="100" r="{circle_radius}" fill="none" stroke="#ff9800" stroke-width="8" stroke-dasharray="{circle_circumference}" stroke-dashoffset="{circle_dashoffset}"></circle>
        <text x="60" y="105" font-size="24" fill="#000" text-anchor="middle">{stats['solved']}</text>
        
        <!-- Horizontal bars -->
        <!-- Easy -->
        <rect x="150" y="60" width="{easy_width}" height="20" fill="#4caf50"></rect>
        <text x="155" y="75" font-size="16" fill="#ffffff">{stats['easy_solved']}/720</text>
        <!-- Medium -->
        <rect x="150" y="90" width="{medium_width}" height="20" fill="#ff9800"></rect>
        <text x="155" y="105" font-size="16" fill="#ffffff">{stats['medium_solved']}/1522</text>
        <!-- Hard -->
        <rect x="150" y="120" width="{hard_width}" height="20" fill="#e57373"></rect>
        <text x="155" y="135" font-size="16" fill="#ffffff">{stats['hard_solved']}/634</text>
    </svg>
    """
    return svg_content



if __name__ == "__main__":
    stats = get_extended_leetcode_stats('yuliu03')  # Your LeetCode username
    svg = generate_svg(stats)
    with open('stats.svg', 'w') as f:
        f.write(svg)

    # Check if the SVG file changed and if so, commit it
    os.system("git add stats.svg")
    os.system("git commit -m 'Updated LeetCode Stats'")
    os.system("git push")
