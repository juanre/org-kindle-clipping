#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, codecs, sys, subprocess
import re
import datetime
import parse
import bookid

def extract_quotes(orgfile):
    return set(re.findall(r'\#\+begin_quote\n(.+?)\n\#\+end_quote',
                          codecs.open(orgfile,
                                      encoding='utf-8').read(),
                          re.DOTALL|re.IGNORECASE))


class KindleBook(object):
    def __init__(self, book_file, org_path='.', text_path=''):
        self.meta = bookid.guess_meta(book_file)
        self.bibstr, self.bibid = bookid.bibstr(self.meta)
        self.title = self.meta['title']
        self.org_path = org_path

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

        if os.path.exists(self.txtbook_file):
            self.txtbook = codecs.open(self.txtbook_file,
                                       encoding='utf-8').read()
        else:
            self.txtbook = None
            print '** Warning: No txt book file, no links will be produced.'

    def bibstr(self):
        return self.bibstr, self.bibid

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

            f.write(u':PROPERTIES:\n:on: <%s>\n' %
                    datetime.date.today().isoformat())
            f.write(u':Custom_ID: %s\n' % self.bibid)
            f.write(u':author: %s\n' % ' and '.join(self.meta['author']))
            for k, v in self.meta.iteritems():
                if not k in ('tags', 'comments', 'author'):
                    f.write(u':%s: %s\n' % (k, v))
            f.write(u':END:\n')

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


def as_main():
    import sys
    for fname in sys.argv[1:]:
        KindleBook(fname).print_clippings()

if __name__ == '__main__':
    as_main()
