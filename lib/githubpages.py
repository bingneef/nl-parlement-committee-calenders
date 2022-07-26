from lib.tools import generate_safe_filename


def generate_github_page_from_commissions(commissions):
    with open('templates/index.md') as f:
        template = f.read()

    calender_content = ''
    for __, commission in commissions.iterrows():
        calender_url = f"https://raw.githubusercontent.com/bingneef/rekenkamer-commissie-scraper/main/calenders/{generate_safe_filename(commission['Afkorting'])}.ics"
        commission_rows = [
            f"**{commission['NaamNL']}**\\",
            f"[{calender_url}]({calender_url})"
        ]
        calender_content = calender_content + '\n'.join(commission_rows) + '\n\n'

    github_pages_content = template.replace('[[[calenders]]]', calender_content)

    with open('index.md', 'w') as f:
        f.write(github_pages_content)
    
    return True