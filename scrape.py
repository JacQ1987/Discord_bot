import re
from pprint import pprint

from bs4 import BeautifulSoup
from requests_html import HTMLSession

import config


def google_scraper(url):
    session = HTMLSession()
    r = session.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    # print(soup)
    return soup


def google_output(url, x, y):
    try:
        # MATH ------
        if y == config.math_class:
            item = google_scraper(url).find(x, config.math_class)
            answer = item.text
            return answer

        # IMDB code generator ------
        if y == config.movie_class:
            item = google_scraper(url).find(x, config.movie_class)
            regex = 'href="(.+?)"><br/><h3'
            link = re.search(regex, str(item)).group(1)
            regex_link = 'tt(\d+)/'
            title_code = re.search(regex_link, link).group(1)
            return title_code

        # CONVERTER ------
        if y == config.convert_id:
            item = google_scraper(url).find(x, config.convert_id).find('input', config.convert_input)
            item_unit = google_scraper(url).find(x, config.convert_id).find('option', config.convert_option)
            regex = 'value="(.+)"/'
            ans = re.search(regex, str(item)).group(1)
            ans_symbol = item_unit.text
            return f'{ans} {ans_symbol.lower()}'

        # TIME ------
        if y == config.time_class:
            item = google_scraper(url).find(x, config.time_class)
            answer = item.text
            return answer

        # TRANSLATE ------
        if y == config.translate_class:
            items = google_scraper(url).find('div', {'class': 'OPPzxe'})
            pprint(items)
            if items:
                print('in items')
                ans = str()
                t = 0
                for i in items:
                    t += 1
                    ans = ans + f'{t}. {i.text}\n'
                return ans
            if not items:
                # print('in not items')
                item = google_scraper(url).find('span', {'class': 'Q4iAWc'})
                print(item)
                regex = '(.+)\s\s\s\s\s\s(Verified)'
                ans = re.search(regex, str(item.text)).group(1)
                return ans
            else:
                return f'Not able to translate that.'

        # Google Search
        if y == config.google_search_class:
            items = google_scraper(url).find_all('div', config.google_search_class['search'])

            title_response = list()
            link_response = list()

            for i in items:
                regex = 'href="(.+?)"><br/><h3'
                try:
                    link = re.search(regex, str(i)).group(1)
                    title = i.find('h3').text
                    title_response.append(title)
                    link_response.append(link)
                except Exception as e:
                    print(e)
            return title_response, link_response

        # Question
        if y == config.google_ans_class_1:
            try:
                items = google_scraper(url).find('div', config.google_ans_class_1)
                if not items:
                    items = google_scraper(url).find('div', config.google_ans_class_2)
                if not items:
                    items = google_scraper(url).find('div', config.google_population_class)

                if items:
                    answer = items.text
                    link = ""
                    return answer, link
                else:
                    pass
            except Exception as e:
                print(e)
            try:
                items = google_scraper(url).find_all('div', {'class': 'yuRUbf'})
                regex = 'href="(.+?)"'
                if items:
                    try:
                        link = re.search(regex, str(items[0])).group(1)
                        title = items[0].find('h3').text
                        return link, title
                    except Exception as e:
                        print(e)
                else:
                    pass
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)
