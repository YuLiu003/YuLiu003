import requests
from bs4 import BeautifulSoup
import os

def safe_extract(element):
    """Utility function to safely extract text data from a BeautifulSoup element."""
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
    submissions_last_year = safe_extract(soup.select_one('span.text-base.font-medium'))

    return {
        'solved': solved,
        'easy_solved': easy_solved,
        'medium_solved': medium_solved,
        'hard_solved': hard_solved,
        'submissions_last_year': submissions_last_year
    }


def generate_svg(stats):
    """Generate a custom SVG representation of the fetched LeetCode stats."""
    svg_content = f"""
    <svg width="500" height="280" xmlns="http://www.w3.org/2000/svg">
        <rect width="500" height="280" fill="#f6f8fa" />
        <text x="10" y="30" font-family="Arial" font-size="14" fill="black">LeetCode Statistics</text>
        <line x1="10" y1="40" x2="490" y2="40" stroke="black" />
        <text x="10" y="60" font-family="Arial" font-size="12" fill="black">Problems Solved: {stats['solved']}</text>
        <text x="10" y="80" font-family="Arial" font-size="12" fill="black">Easy Solved: {stats['easy_solved']}</text>
        <text x="10" y="100" font-family="Arial" font-size="12" fill="black">Medium Solved: {stats['medium_solved']}</text>
        <text x="10" y="120" font-family="Arial" font-size="12" fill="black">Hard Solved: {stats['hard_solved']}</text>
        <text x="10" y="140" font-family="Arial" font-size="12" fill="black">Submissions Last Year: {stats['submissions_last_year']}</text>
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
