from lib.tools import generate_safe_filename


def generate_github_page_from_commissions(commissions):
    with open('templates/index.md') as f:
        template = f.read()

    calender_content = ''
    for __, commission in commissions.iterrows():
        commission_rows = [
            commission['NaamNL'],
            f"https://raw.githubusercontent.com/bingneef/rekenkamer-commissie-scraper/data/calenders/{generate_safe_filename(commission['Afkorting'])}.ics"
        ]
        calender_content = calender_content + '\n'.join(commission_rows) + '\n\n'

    github_pages_content = template.replace('[[[calenders]]]', calender_content)

    with open('index.md', 'w') as f:
        f.write(github_pages_content)
    
    return True