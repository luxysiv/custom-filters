import os
import http.client
from urllib.parse import urlparse

FILTERS = {
    'abpvn.txt': 'https://raw.githubusercontent.com/abpvn/abpvn/master/filter/abpvn.txt',
    'easylist.txt': 'https://easylist.to/easylist/easylist.txt',
    'annoyance.txt': 'https://easylist-downloads.adblockplus.org/fanboy-annoyance.txt',
    'adguard.txt': 'https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/BaseFilter/sections/adservers.txt'
}

def download_file(url, dest):
    parsed_url = urlparse(url)
    conn = http.client.HTTPSConnection(parsed_url.netloc)
    conn.request("GET", parsed_url.path)
    response = conn.getresponse()

    if response.status != 200:
        raise Exception(f"Failed to download {url}, status code: {response.status}")
    
    with open(dest, 'wb') as file:
        file.write(response.read())

    conn.close()

def join_files(files):
    merged_lines = set()
    
    with open('my-rules.txt', 'r') as my_rules_file:
        merged_lines.update(my_rules_file.readlines())
        
    for filename in files:
        with open(filename, 'r') as file:
            for line in file:
                if not line.strip().startswith('[Adblock Plus 2.0]') and not line.strip().startswith('!'):
                    merged_lines.add(line)
    
    sorted_lines = sorted(merged_lines)
    
    with open("filters.txt", "w") as final_file:
        final_file.write("! Title: CustomList\n")
        for line in sorted_lines:
            final_file.write(line)
    

for filter, url in FILTERS.items():
    download_file(url, filter)

files = list(FILTERS.keys())
join_files(files)

for filename in files:
    os.remove(filename)

# Add, commit, and push the file (Git commands are kept the same)
os.system(f'git config --global user.email "${{GITHUB_ACTOR_ID}}+${{GITHUB_ACTOR}}@users.noreply.github.com"')
os.system(f'git config --global user.name "$(gh api /users/${{GITHUB_ACTOR}} | jq .name -r)"')
os.system('git add filters.txt || error "Failed to add the filters list to repo"')
os.system('git commit -m "Update domains list" --author=.')
os.system('git push origin main || error "Failed to push the filters list to repo"')
