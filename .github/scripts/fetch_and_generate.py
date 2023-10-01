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
    # Calculating percentages
    total_easy = 720
    total_medium = 1522
    total_hard = 634

    easy_percentage = (int(stats['easy_solved']) / total_easy) * 100
    medium_percentage = (int(stats['medium_solved']) / total_medium) * 100
    hard_percentage = (int(stats['hard_solved']) / total_hard) * 100

    svg_content = f"""
    <svg width="500" height="200" xmlns="http://www.w3.org/2000/svg" style="background-color:#222; color:white">
        <!-- Solved Circle -->
        <circle cx="100" cy="100" r="70" fill="none" stroke="#555" stroke-width="15" />
        <circle cx="100" cy="100" r="70" fill="none" stroke="#FFA500" stroke-width="15" stroke-dasharray="440" stroke-dashoffset="{440 - (440 * (int(stats['solved']) / (total_easy + total_medium + total_hard)))}" />
        <text x="100" y="105" font-size="32px" fill="white" text-anchor="middle">{stats['solved']}</text>
        <text x="100" y="130" font-size="16px" fill="#aaa" text-anchor="middle">Solved</text>
        
        <!-- Easy Bar -->
        <rect x="250" y="30" width="200" height="20" fill="#555" />
        <rect x="250" y="30" width="{2 * easy_percentage}" height="20" fill="#81c784" />
        <text x="460" y="45" font-size="14px" fill="white">Easy {stats['easy_solved']}/720 - Beats 79.6%</text>
        
        <!-- Medium Bar -->
        <rect x="250" y="80" width="200" height="20" fill="#555" />
        <rect x="250" y="80" width="{2 * medium_percentage}" height="20" fill="#ffeb3b" />
        <text x="460" y="95" font-size="14px" fill="white">Medium {stats['medium_solved']}/1522 - Beats 82.9%</text>
        
        <!-- Hard Bar -->
        <rect x="250" y="130" width="200" height="20" fill="#555" />
        <rect x="250" y="130" width="{2 * hard_percentage}" height="20" fill="#e57373" />
        <text x="460" y="145" font-size="14px" fill="white">Hard {stats['hard_solved']}/634 - Beats 85.5%</text>
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
