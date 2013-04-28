#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, codecs, sys, subprocess
import re
import datetime
import parse
from bookid import bibid

def extract_quotes(orgfile):
    return set(re.findall(r'\#\+begin_quote\n(.+?)\n\#\+end_quote',
                          codecs.open(orgfile,
                                      encoding='utf-8').read(),
                          re.DOTALL|re.IGNORECASE))


class KindleBook(object):
    def __init__(self, title, author, year,
                 book_file=None, org_path='.', text_path=''):
        self.bibid = bibid(title, author, year)
        self.title = title
        self.book_file = book_file
        self.text_path = text_path
        self.org_path = org_path

        self.txtbook_file = None
        if book_file and os.path.exists(book_file):
            self.txtbook_file = os.path.join(text_path, self.bibid + '.txt')
            if not os.path.exists(self.txtbook_file):
                try:
                    devnull = codecs.open(os.devnull, 'w', encoding='utf-8')
                    subprocess.call(['ebook-convert', book_file,
                                     self.txtbook_file],
                                    stdout=devnull, stderr=devnull)
                    print ' ->', self.txtbook_file
                except:
                    pass

        if self.txtbook_file and os.path.exists(self.txtbook_file):
            self.txtbook = codecs.open(self.txtbook_file,
                                       encoding='utf-8').read()
        else:
            self.txtbook = None
            print '** Warning: No txt book file, no links will be produced.'

    def find_clipping(self, clipping):
        """The clipping might not be identical to the text in the book.  This
        function attempts to find the closest match.  If it finds it, it
        should be usable as an org-mode link.
        """
        import difflib
        book = self.txtbook
        if book is None:
            return None
        s = difflib.SequenceMatcher(None, book, clipping, autojunk=False)
        loc = s.find_longest_match(0, len(book), 0, len(clipping))
        if loc:
            return book[loc.a : loc.a+loc.size]
        return None

    def print_clippings(self, outfile=None):
        def upcase_first(s):
            return s[0].upper() + s[1:]

        kc = parse.Clippings()

        if outfile is None:
            #outfile = self.book_name.replace(' ', '-') + '.org'
            outfile = os.path.join(self.org_path, self.bibid + '.org')

        skip = set([])
        if os.path.exists(outfile):
            skip = extract_quotes(outfile)
        else:
            with codecs.open(outfile, 'w', encoding='utf-8') as f:
                f.write(u'# -*- coding: utf-8 -*-\n')

        clippings = [(clip, meta, note)
                     for clip, meta, note in kc.list_book(self.title)
                     if not (upcase_first(clip) in skip)]
        if not clippings:
            return

        with codecs.open(outfile, 'a', encoding='utf-8') as f:
            f.write(u'\n\n* ' + kc.book_full_name(self.title) + '\n')
            f.write(u':PROPERTIES:\n:on: <%s>\n:END:\n' %
                    datetime.date.today().isoformat())
            for clip, meta, note in clippings:
                if meta.kind != 'bookmark':
                    f.write(u'** ' +
                            upcase_first(u' '.join(clip.split(' ')[:10]))
                            + '\n')
                    props = ''
                    if meta.when:
                        props = ':added: <%s>\n' % meta.when.isoformat(' ')
                    if meta.loc:
                        props += ':loc: %s\n' % str(meta.loc)
                    if meta.page:
                        props += ':page: %s\n' % str(meta.page)
                    f.write(u':PROPERTIES:\n%s:END:\n' % props)
                    if note:
                        f.write(upcase_first(note) + u'\n\n')
                    link = self.find_clipping(clip)
                    if link:
                        f.write(u'[[file:%s::%s][Read more]].\n' %
                                (self.txtbook_file, link))
                    f.write(u'\n#+begin_quote\n' + upcase_first(clip) +
                            u'\n#+end_quote\n\n')


if __name__ == '__main__':
    bdir = '/Users/juanre/Dropbox/books/'
    kb = KindleBook('Where Good Ideas Come From', 'Steven Johnson', '2000',
                    bdir +
                    'science/steven-johnson/where-good-ideas-come-from.epub')
    kb.print_clippings()
