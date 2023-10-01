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


def generate_solved_problems_svg(stats):
    # Calculate percentages
    total_easy, total_medium, total_hard = 720, 1522, 634
    solved_percentage = int(stats['solved']) / (total_easy + total_medium + total_hard)
    circumference = 2 * 3.14159 * 70  # for a circle of radius 70
    offset = circumference * (1 - solved_percentage)

    svg_content = f"""
    <svg width="100%" viewBox="0 0 500 150" xmlns="http://www.w3.org/2000/svg" style="background-color:#1E1E1E; color:white">
        <!-- Solved Circle -->
        <circle cx="80" cy="75" r="70" fill="none" stroke="#333" stroke-width="15" />
        <circle cx="80" cy="75" r="70" fill="none" stroke="#FFA500" stroke-width="15" stroke-dasharray="{circumference}" stroke-dashoffset="{offset}" />
        <text x="80" y="80" font-size="32px" fill="white" text-anchor="middle">{stats['solved']}</text>
        <text x="80" y="105" font-size="16px" fill="#aaa" text-anchor="middle">Solved</text>

        <!-- Bars: Base + Fill + Text -->
        <!-- Easy -->
        <rect x="200" y="25" width="150" height="20" fill="#555" />
        <rect x="200" y="25" width="{150 * (int(stats['easy_solved']) / total_easy)}" height="20" fill="#81c784" />
        <text x="360" y="40" font-size="14px" fill="white">Easy {stats['easy_solved']}/{total_easy}</text>

        <!-- Medium -->
        <rect x="200" y="65" width="150" height="20" fill="#555" />
        <rect x="200" y="65" width="{150 * (int(stats['medium_solved']) / total_medium)}" height="20" fill="#FFA500" />
        <text x="360" y="80" font-size="14px" fill="white">Medium {stats['medium_solved']}/{total_medium}</text>

        <!-- Hard -->
        <rect x="200" y="105" width="150" height="20" fill="#555" />
        <rect x="200" y="105" width="{150 * (int(stats['hard_solved']) / total_hard)}" height="20" fill="#e57373" />
        <text x="360" y="120" font-size="14px" fill="white">Hard {stats['hard_solved']}/{total_hard}</text>
    </svg>
    """
    return svg_content





if __name__ == "__main__":
    stats = get_extended_leetcode_stats('yuliu03')  # Your LeetCode username
    svg = generate_solved_problems_svg(stats)
    print(svg)  # Add this line to print the generated SVG
    with open('stats.svg', 'w') as f:
        f.write(svg)

    # Check if the SVG file changed and if so, commit it
    os.system("git add stats.svg")
    os.system("git commit -m 'Updated LeetCode Stats'")
    os.system("git push")
