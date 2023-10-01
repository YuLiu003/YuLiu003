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
    solved = safe_extract(soup.select_one('div.font-medium'))
    easy_solved = safe_extract(soup.select('span.text-base.font-medium')[0])
    medium_solved = safe_extract(soup.select('span.text-base.font-medium')[1])
    hard_solved = safe_extract(soup.select('span.text-base.font-medium')[2])
    submissions_last_year = safe_extract(soup.select_one('span.font-medium:not(.text-base)'))

    return {
        'solved': solved,
        'easy_solved': easy_solved,
        'medium_solved': medium_solved,
        'hard_solved': hard_solved,
        'submissions_last_year': submissions_last_year
    }


def generate_svg(stats):
    svg_content = f"""
    <svg width="400" height="200" xmlns="http://www.w3.org/2000/svg">
        <rect width="100" height="{int(stats['easy_solved'])}" x="10" y="50" fill="#81c784" />
        <text x="10" y="40" font-size="12" fill="#000">Easy: {stats['easy_solved']}</text>
        
        <rect width="100" height="{int(stats['medium_solved'])}" x="150" y="50" fill="#ffeb3b" />
        <text x="150" y="40" font-size="12" fill="#000">Medium: {stats['medium_solved']}</text>
        
        <rect width="100" height="{int(stats['hard_solved'])}" x="290" y="50" fill="#e57373" />
        <text x="290" y="40" font-size="12" fill="#000">Hard: {stats['hard_solved']}</text>
        
        <text x="10" y="180" font-size="14" fill="#000">Submissions Last Year: {stats['submissions_last_year']}</text>
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
