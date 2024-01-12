import logging
import os
import re
import string
import sys
import warnings

from collections import namedtuple
from urllib.parse import urlparse

import pymorphy2
import requests

from bs4 import BeautifulSoup


def merge_dictionaries(directory='dicts'):
    words = set()
    for filename in os.listdir(os.path.abspath(directory)):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as fp:
            lines = [
                line.strip().replace('ё', 'е')
                for line in fp.readlines()
                if line != '\n'
            ]
            words.update(lines)
    return words


def _clean_text(content):
    text = BeautifulSoup(content, 'lxml').get_text(' ', strip=True)
    return re.sub('[' + string.punctuation + ']', ' ', text).strip()


def _clean_word(word):
    word = word.replace('«', '').replace('»', '').replace('…', '')
    word = word.replace('„', '').replace('“', '')
    return word


def split_by_words(morph, content):
    words = set()
    text = _clean_text(content)
    for word in text.split():
        cleaned_word = _clean_word(word)
        normalized_word = morph.parse(cleaned_word)[0].normal_form
        normalized_word = normalized_word.replace('ё', 'е')
        if len(normalized_word) > 2:
            words.add(normalized_word)
    return words


def parse_comments(html_page):
    comments = []
    Comment = namedtuple(
        'Comment',
        ['id', 'username', 'body']
    )

    soup = BeautifulSoup(html_page, 'lxml')

    elements = soup.find_all('div', attrs={'data-comment-body': True})

    for elem in elements:
        comment_id = elem['data-comment-body']
        body_content = elem.find('div', {'class': 'tm-comment__body-content'})
        text = body_content.get_text(separator=' ')
        user_link = elem.find('a', {'class': 'tm-user-info__username'})
        if not user_link:
            continue
        user_link = user_link['href']

        username = ''
        split_link = list(filter(None, user_link.split('/')))
        if split_link:
            username = split_link[-1]

        comments.append(
            Comment(comment_id, username, text)
        )

    return comments


def main():
    warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('pymorphy2').setLevel(logging.WARNING)
    logging.basicConfig(
        format='\u2192 %(message)s',
        level=logging.INFO,
    )

    morph = pymorphy2.MorphAnalyzer()
    checklist = merge_dictionaries()

    link = ''
    if len(sys.argv) > 1:
        link = sys.argv[1]
    else:
        return

    url = urlparse(link)
    url_path = list(filter(None, url.path.split('/')))

    if url_path[-1] != 'comments':
        link = f'{url.scheme}://{url.netloc}/{"/".join(url_path)}/comments/'

    resp = requests.get(link)

    comments = parse_comments(resp.text)

    found_comments = 0
    for comment in comments:
        words = split_by_words(morph, comment.body)
        detected_words = [word for word in words if word in checklist]

        debug_msg = ''
        if detected_words:
            debug_msg = (
                f'{link}#comment_{comment.id}\n'
                f'{comment.body}\nDetected words: {detected_words}\n{"-" * 40}'
            )
            logging.info(debug_msg)
            found_comments += 1
    logging.info(f'Found comments: {found_comments}')
    logging.info(f'Total comments: {len(comments)}')


if __name__ == '__main__':
    main()
