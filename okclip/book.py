#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import datetime

# https://github.com/juanre/dashify
import dashify

def reasonable_length(title):
    """
    >>> reasonable_length('how-children-succeed-grit-curiosity-and-the-hidden-power-of-character')
    'how-children-succeed-grit-curiosity'
    >>> reasonable_length('influence')
    'influence'
    """
    words = title.split('-')
    dont_end =['the', 'and', 'but', 'or', 'yet', 'for',
               'no', 'nor', 'not', 'so', 'a', 's']
    length = 7
    if length < len(words):
        while words[length-1] in dont_end and length > 1:
            length -= 1
    return '-'.join(words[:length])

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
    if ',' in author:
        last, first = author.split(',')
        return dashify.dash_name(last)
    else:
        return dashify.dash_name(re.split(r'[\s\.]', author)[-1])

def bibid(title, author, year):
    author = dashed_author(author)
    return (author + '-' + str(year) + '---' +
            reasonable_length(dashify.dash_name(title)))

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
