import requests
from bs4 import BeautifulSoup
import os

def get_extended_leetcode_stats(username):
    url = f"https://leetcode.com/{username}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # These are placeholders, you will need to inspect the LeetCode page for exact classes or IDs
    solved = soup.find('span', class_='badge progress-bar-success').text.strip()
    total = soup.find('span', class_='badge total-solved-count').text.strip()
    contest_rating = soup.find('div', class_='css-s70srj').text.strip()
    top_percentage = soup.find('div', class_='css-aknsx9').text.strip()
    easy_solved = soup.find('span', class_='css-ea78td').text.strip()
    medium_solved = soup.find('span', class_='css-4ob7od').text.strip()
    hard_solved = soup.find('span', class_='css-sjisc5').text.strip()
    # For submissions_last_year and other stats, update selectors accordingly

    return {
        'solved': solved,
        'total': total,
        'contest_rating': contest_rating,
        'top_percentage': top_percentage,
        'easy_solved': easy_solved,
        'medium_solved': medium_solved,
        'hard_solved': hard_solved,
        # 'submissions_last_year': submissions_last_year
    }

def generate_svg(stats):
    # This is a basic placeholder. Proper SVG generation is more complex.
    svg_content = f"""
    <svg width="400" height="180">
        <!-- Add SVG elements here based on stats -->
        <text x="10" y="40">Problems Solved: {stats['solved']}/{stats['total']}</text>
        <!-- ... -->
    </svg>
    """
    return svg_content

if __name__ == "__main__":
    stats = get_extended_leetcode_stats('YuLiu003')  # Your LeetCode username
    svg = generate_svg(stats)
    with open('stats.svg', 'w') as f:
        f.write(svg)

    # Check if the SVG file changed and if so, commit it
    os.system("git add stats.svg")
    os.system("git commit -m 'Updated LeetCode Stats'")
    os.system("git push")
