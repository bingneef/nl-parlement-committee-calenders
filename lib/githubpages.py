from lib.tools import generate_safe_filename


def generate_github_page_from_committees(committees):
    with open('templates/index.md') as f:
        template = f.read()

    calendar_content = ''
    for __, committee in committees.iterrows():
        calendar_url = f"https://raw.githubusercontent.com/bingneef/rekenkamer-commissie-scraper/main/calendars/{generate_safe_filename(committee['Afkorting'])}.ics"
        committee_rows = [
            f"**{committee['NaamNL']}**\\",
            f"[{calendar_url}]({calendar_url})"
        ]
        calendar_content = calendar_content + '\n'.join(committee_rows) + '\n\n'

    github_pages_content = template.replace('[[[calendars]]]', calendar_content)

    with open('index.md', 'w') as f:
        f.write(github_pages_content)
    
    return True