import requests
from bs4 import BeautifulSoup
from lxml import html


class VikingsScraper:

    def __init__(self):
        self.vikings_cast_info = {}
        self.norsemen_cast_info = {}
        self.merged_cast_info = {}

    def scrape_all_data(self):
        self.scrape_vikings_cast()
        self.scrape_norsemen_cast()
        self.merged_cast_info = {
            'vikings_cast': self.vikings_cast_info,
            'norsemen_cast': self.norsemen_cast_info
        }
        return self.merged_cast_info

    def scrape_vikings_cast(self):
        base_url = 'https://www.history.com'
        url = 'https://www.history.com/shows/vikings/cast/astrid'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        cast_list = soup.find('div', class_='tile-list tile-boxed')
        cast_links_images_dict = {base_url + li.a['href']: li.find('img')['src'] for li in cast_list.ul.find_all('li')}

        for link in cast_links_images_dict.keys():
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Get character name, actor name and description from the article tag
            article = soup.find('article', class_='main-article')

            # Get character name
            character_name = article.find('header').find('h1').find('strong').text.strip()

            # Get actor name
            actor_info = article.find('header').find('h1').find('small').text.strip()
            actor_name = ' '.join(actor_info.split()[2:])  # Remove "Played by" from the actor name

            # Get character description
            character_description = article.find('p').text.strip()

            # Get actor description
            try:
                actor_description = '\n'.join([p.text.strip() for p in article.find('div', class_='page').find_all('p')])
            except:
                p_tags = article.find_all('p', recursive=False)
                actor_description = ' '.join([p.text.strip() for p in p_tags[3:]])

            self.vikings_cast_info[character_name] = {
                'Actor Name': actor_name,
                'Character Description': character_description,
                'Actor Description': actor_description,
                'Image URL': cast_links_images_dict[link],
                'TV Show': 'Vikings'
            }

    def scrape_norsemen_cast(self):
        self.scrape_norsemen_cast_wikipedia()
        self.scrape_norsemen_imdb()

    def scrape_norsemen_cast_wikipedia(self):
        url = 'https://en.wikipedia.org/wiki/Norsemen_(TV_series)'  # Replace with your actual URL
        response = requests.get(url)
        tree = html.fromstring(response.content)

        ul = tree.xpath('//*[@id="mw-content-text"]/div[1]/ul[2]')[0]
        lis = ul.findall('li')

        for li in lis:
            text = li.text_content().strip()
            actor_name, character_info = text.split(' as ', 1)
            character_name, character_description = character_info.split(', ', 1)
            self.norsemen_cast_info[character_name] = {
                'Character Description': character_description.capitalize(),
                'Actor Name': actor_name,
                'TV Show': 'Norsemen'
            }

    def scrape_norsemen_imdb(self):
        url = 'https://www.imdb.com/title/tt5905354/fullcredits?ref_=tt_cl_sm'
        base_url = 'https://www.imdb.com'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table', class_='cast_list')
        rows = table.find_all('tr')

        for row in rows[1:]:  # Skip the header row
            cols = row.find_all('td')
            if len(cols) < 4:
                continue

            # Get the URL and content from the second td tag
            try:
                actor_link = cols[1].find('a')
                actor_page_url = base_url + actor_link['href']
                actor_name = actor_link.text.strip()

                # Get the URL and content from the fourth td tag
                character_link = cols[3].find('a')
                character_page_url = base_url + character_link['href']
                character_name = character_link.text.strip()

                character_dict = {
                    'Actor Name': actor_name,
                    'TV Show': 'Norsemen'
                }

                self.norsemen_cast_info[character_name] = character_dict if \
                    character_name not in self.norsemen_cast_info.keys() \
                    else {**self.norsemen_cast_info[character_name], **character_dict}

                self.scrape_norsemen_character_page(character_page_url, character_name)
                self.scrape_norsemen_actor_page(actor_page_url, character_name)
            except:
                continue

    def scrape_norsemen_character_page(self, url, name):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        try:
            div = soup.find('div', class_='titlecharacters-image-grid media_index_thumb_list')
            image = div.find('img')
            image_url = image['src']
            self.norsemen_cast_info[name].update({'Image URL': image_url})
        except:
            pass

    def scrape_norsemen_actor_page(self, url, name):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            response = requests.get(url + 'bio/', headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            mini_bio_div = soup.find('div', attrs={'data-testid': 'sub-section-mini_bio'})
            mini_bio = mini_bio_div.text.strip()
            self.norsemen_cast_info[name].update({'Actor Description': mini_bio})
        except:
            pass
