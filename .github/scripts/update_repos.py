import re, requests, os

token = os.environ["GITHUB_TOKEN"]
user  = "Brainitech"

repos = requests.get(
    f"https://api.github.com/users/{user}/repos",
    params={"sort": "stars", "per_page": 4, "type": "owner"},
    headers={"Authorization": f"Bearer {token}"},
).json()

def card(repo):
    name = repo["name"]
    return (
        f'<a href="https://github.com/{user}/{name}">\n'
        f'  <img width="49%" src="https://github-readme-stats.vercel.app/api/pin/'
        f'?username={user}&repo={name}&theme=tokyonight&hide_border=true" />\n'
        f'</a>'
    )

block = '<div align="center">\n\n' + "\n".join(card(r) for r in repos) + '\n\n</div>'

with open("README.md", "r") as f:
    content = f.read()

updated = re.sub(
    r"<!-- PROJECTS:START -->.*?<!-- PROJECTS:END -->",
    f"<!-- PROJECTS:START -->\n{block}\n<!-- PROJECTS:END -->",
    content,
    flags=re.DOTALL,
)

with open("README.md", "w") as f:
    f.write(updated)
