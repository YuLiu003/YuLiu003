import requests
from bs4 import BeautifulSoup
import os

def get_leetcode_stats(yuliu03):
    url = f"https://leetcode.com/{yuliu03}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Parsing might change depending on the exact structure of the LeetCode profile page
    solved = soup.find('span', class_='badge progress-bar-success').text.strip()
    total = soup.find('span', class_='badge total-solved-count').text.strip()

    return {
        "solved": solved,
        "total": total
    }

def update_readme(stats):
    with open('README.md', 'r') as file:
        content = file.read()

        content = content.replace('[solved]', stats['solved'])
        content = content.replace('[total]', stats['total'])

    with open('README.md', 'w') as file:
        file.write(content)

    os.system("git add README.md")
    os.system("git commit -m 'Updated LeetCode Stats'")
    os.system("git push")

if __name__ == "__main__":
    username = "yuliu03"
    stats = get_leetcode_stats(username)
    update_readme(stats)
