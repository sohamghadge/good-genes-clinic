import urllib.request
import os

headers = {'User-Agent': 'Mozilla/5.0'}

logos = {
    'vogue.svg': 'https://upload.wikimedia.org/wikipedia/commons/e/ea/Vogue_logo.svg',
    'cosmo.svg': 'https://upload.wikimedia.org/wikipedia/commons/e/e0/Cosmopolitan_logo.svg',
    'mirror.png': 'https://upload.wikimedia.org/wikipedia/en/2/23/Mumbai_Mirror_logo.png',
    'ht.svg': 'https://upload.wikimedia.org/wikipedia/commons/2/22/Hindustan_Times_logo.svg'
}

for name, url in logos.items():
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response, open(f'assets/{name}', 'wb') as out_file:
            out_file.write(response.read())
        print(f"Downloaded {name}")
    except Exception as e:
        print(f"Failed to download {name}: {e}")

