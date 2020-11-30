from bs4 import BeautifulSoup
import wget
import os
import re
import cloudscraper
import shutil
from tqdm import tqdm

# link = 'https://readcomiconline.to/Comic/Monstress'
link = input('Enter the link in the commented format..')
scraper = cloudscraper.CloudScraper()
soup = BeautifulSoup(scraper.get(link).content, 'html.parser')
table = soup.find_all('table', attrs={'class': 'listing'})
try:
    master_title = soup.find_all('div', attrs={'class': 'heading'})[0].text
except IndexError:
    master_title = soup.find_all('a', attrs={'class': 'bigChar'})[0].text
os.mkdir(master_title)
print(f"Title is {master_title}")

for row1 in table:
    print(f"Found {len(row1.find_all('a'))} Links")
    for row in row1.find_all('a'):
        link = 'https://readcomiconline.to' + row['href'] + '&quality=hq&readType=1'
        soup1 = BeautifulSoup(scraper.get(link).content, 'html.parser')
        title = soup1.title.text
        title = title.replace('\n', ' ')
        title = title.replace('\t', '')
        title = re.sub('\s\s+', ' ', title).split('- Read')[0][1:-1]
        title = title.replace('#', 'No.')
        links = re.findall('https://2.bp.blogspot.com/.+=s0', str(soup1))
        os.mkdir(f'{master_title}/{title}/')
        bar = tqdm(total=len(links))
        for pic_link in links:
            wget.download(pic_link, out=f'{master_title}/{title}/')
            bar.update(1)
            bar.set_postfix_str(title)
        bar.close()
        shutil.make_archive(f'{master_title}/{title}', 'zip', f'{master_title}/{title}')
        shutil.rmtree(f'{master_title}/{title}')
        os.rename(f'{master_title}/{title}.zip', f'{master_title}/{title}.cbr')
