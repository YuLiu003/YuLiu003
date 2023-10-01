import requests
from bs4 import BeautifulSoup
import os

def safe_extract(element):
    """Utility function to safely extract text data from a BeautifulSoup element."""
    return element.text.strip() if element else "N/A"

def get_extended_leetcode_stats(yuliu03):
    """Fetch and extract the specified stats from a LeetCode user profile."""
    url = f"https://leetcode.com/{yuliu03}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    solved = safe_extract(soup.find('span', class_='badge progress-bar-success'))
    total = safe_extract(soup.find('span', class_='badge total-solved-count'))
    contest_rating = safe_extract(soup.find('div', class_='css-s70srj'))
    top_percentage = safe_extract(soup.find('div', class_='css-aknsx9'))
    easy_solved = safe_extract(soup.find('span', class_='css-ea78td'))
    medium_solved = safe_extract(soup.find('span', class_='css-4ob7od'))
    hard_solved = safe_extract(soup.find('span', class_='css-sjisc5'))
    
    return {
        'solved': solved,
        'total': total,
        'contest_rating': contest_rating,
        'top_percentage': top_percentage,
        'easy_solved': easy_solved,
        'medium_solved': medium_solved,
        'hard_solved': hard_solved
    }

def generate_svg(stats):
    """Generate a custom SVG representation of the fetched LeetCode stats."""
    svg_content = f"""
    <svg width="500" height="280" xmlns="http://www.w3.org/2000/svg">
        <rect width="500" height="280" fill="#f6f8fa" />
        <text x="10" y="30" font-family="Arial" font-size="14" fill="black">LeetCode Statistics</text>
        <line x1="10" y1="40" x2="490" y2="40" stroke="black" />
        <text x="10" y="60" font-family="Arial" font-size="12" fill="black">Problems Solved: {stats['solved']}/{stats['total']}</text>
        <text x="10" y="80" font-family="Arial" font-size="12" fill="black">Contest Rating: {stats['contest_rating']}</text>
        <text x="10" y="100" font-family="Arial" font-size="12" fill="black">Top Percentage: {stats['top_percentage']}</text>
        <text x="10" y="120" font-family="Arial" font-size="12" fill="black">Easy Solved: {stats['easy_solved']}</text>
        <text x="10" y="140" font-family="Arial" font-size="12" fill="black">Medium Solved: {stats['medium_solved']}</text>
        <text x="10" y="160" font-family="Arial" font-size="12" fill="black">Hard Solved: {stats['hard_solved']}</text>
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
