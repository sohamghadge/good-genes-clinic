import urllib.request
import os

logos = {
    'vogue.png': 'https://logo.clearbit.com/vogue.com',
    'cosmo.png': 'https://logo.clearbit.com/cosmopolitan.com',
    'mirror.png': 'https://logo.clearbit.com/mumbaimirror.indiatimes.com',
    'ht.png': 'https://logo.clearbit.com/hindustantimes.com'
}

for name, url in logos.items():
    try:
        urllib.request.urlretrieve(url, f'assets/{name}')
        print(f"Downloaded {name}")
    except Exception as e:
        print(f"Failed to download {name}: {e}")

