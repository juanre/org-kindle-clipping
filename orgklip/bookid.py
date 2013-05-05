#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import subprocess

# https://github.com/juanre/dashify
import dashify

def ensure_comma(author):
    if not u',' in author:
        author = author.split(' ')
        if len(author) > 1:
            return author[-1] + u', ' + u' '.join(author[:-1])
        else:
            return u'' + author[0]
    return author

def parse_author(info):
    """Try to preserve information on what's the last name:
 http://tex.stackexchange.com/questions/557/how-should-i-type-author-names-in-a-bib-file

    >>> parse_author('Stuckey, Maggie & McGee, Rose Marie Nichols [Stuckey, Maggie]')
    [u'Stuckey, Maggie', u'McGee, Rose Marie Nichols']
    >>> parse_author('Cialdini, Robert B. [Cialdini, Robert B.]')
    [u'Cialdini, Robert B.']
    >>> parse_author('Robert B. Cialdini')
    [u'Cialdini, Robert B.']
    >>> parse_author(u'Cialdini')
    [u'Cialdini']
    """
    info = re.sub(u'\[.+\]', u'', info)
    if u'&' in info:
        out = [s.strip() for s in info.split(u'&')]
    elif u' and ' in info:
        out = [s.strip() for s in info.split(u' and ')]
    else:
        out = [info.strip()]
    return [ensure_comma(a) for a in out]

def guess_meta(book):
    """Tries to figure out the metadata of the book (title, author and
    publishing year) using the ebook-meta command line tool from
    calibre.  Install calibre from http://calibre-ebook.com/, then
    Preferences -> Miscelaneous -> Install command line tools.  It
    requires dateutil-parser.
    """
    import dateutil.parser
    meta = {}
    for line in [re.split(r'\s+:\s+', l) for l in
                 subprocess.check_output(['ebook-meta', book]).splitlines()]:
        if len(line) != 2:
            continue
        what, info = line[0].lower(), line[1]
        if 'author' in what:
            meta['author'] = parse_author(info.decode('utf8'))
        if 'language' in what:
            meta['language'] = info.decode('utf8')
        elif 'identifier' in what:
            identified = False
            for identifier in [ii.strip() for ii in info.split(',')]:
                if ':' in identifier:
                    idtype, idcontent = identifier.split(':')
                    meta[idtype] = idcontent
                    identified = True
            if not identified:
                meta['identifier'] = info
        elif 'published' in what:
            published = dateutil.parser.parse(info)
            meta['date'] = published
        else:
            meta[what] = u'' + info.decode('utf8')
    return meta

def reasonable_length(title):
    """
    >>> reasonable_length('how-children-succeed-grit-curiosity-and-the-hidden-power-of-character')
    'how-children-succeed-grit-curiosity'
    >>> reasonable_length('influence')
    'influence'
    """
    words = title.split('-')
    dont_end =['the', 'and', 'but', 'or', 'yet', 'for', 'with',
               'no', 'nor', 'not', 'so', 'a', 's', 'that']
    length = 7
    if length < len(words):
        while words[length-1] in dont_end and length > 1:
            length -= 1
    return '-'.join(words[:length])

def dashed_title(title):
    """
    >>> dashed_title(u'This Very Long and Unwieldy Title That Never Ends')
    u'this-very-long-and-unwieldy-title'
    >>> dashed_title(u'This Title: With a Subtitle')
    u'this-title'
    >>> dashed_title('this title (with paren)')
    u'this-title'
    """
    title = title.split(u':')[0]
    title = re.sub(u'\(.*\)', '', title).strip()
    return reasonable_length(dashify.dash_name(title))

def dashed_author(author):
    """
    >>> dashed_author('Cialdini, Robert B.')
    'cialdini'
    >>> dashed_author('Robert B. Cialdini')
    'cialdini'
    >>> dashed_author('Robert B.Cialdini')
    'cialdini'
    >>> dashed_author('Cialdini')
    'cialdini'
    """
    if not isinstance(author, basestring):
        author = author[0]
    if ',' in author:
        last, first = author.split(',')
        return dashify.dash_name(last)
    else:
        return dashify.dash_name(re.split(r'[\s\.]', author)[-1])

def bibid(title, author, year=''):
    author = dashed_author(author)
    if author:
        author = author + '-'
    if year:
        year = str(year) + '-'
    title = dashed_title(title)
    if year or author:
        title = '--' + title
    return (author + year + title)

def bibstr(meta):
    if 'year' in meta:
        year = meta['year']
    elif 'date' in meta:
        year = meta['date'].year
    else:
        year = ''
    bid = bibid(meta['title'], meta['author'], year)
    bib = [bid,
           'title = {%s}' % meta['title'],
           'author = {%s}' % ' and '.join(meta['author']),
           'year = {%s}' % str(year)]
    for field in ['isbn', 'publisher', 'url']:
        if field in meta:
            bib.append('%s = {%s}' % (field, meta[field]))
    return "@book {%s\n}" % ',\n  '.join(bib), bid

def _test():
    import doctest
    doctest.testmod()

def as_main():
    import sys
    if len(sys.argv) > 1:
        for book in sys.argv[1:]:
            print bibstr(guess_meta(book))[0]
    else:
        _test()

if __name__ == '__main__':
    as_main()
