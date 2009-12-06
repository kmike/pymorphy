#-----------------------------------------------------------------------------
# Copyright (c) 2006-2009  Gerard Flanagan
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be included
#    in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#-----------------------------------------------------------------------------


import sys
import os
import re
import codecs
from sgmllib import SGMLParser
from StringIO import StringIO
from textwrap import TextWrapper

CODEBLOCK = '.. sourcecode:: python'
BLOCKTAGS = ['div', 'blockquote']
IGNORETAGS = ['title', 'style', 'script']
UNDERLINES = list('=-~`+;')

# Fredrik Lundh, http://effbot.org/zone/re-sub.html
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3].lower() == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            import htmlentitydefs
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

class LineBuffer(object):

    def __init__(self):
        self._lines = []
        self._wrapper = TextWrapper()

    def __len__(self):
        return len(self._lines)

    def __getitem__(self, i):
        return self._lines[i]

    def __setitem__(self, i, value):
        self._lines[i] = value

    def clear(self):
        self._lines[:] = []

    def read(self):
        return '\n'.join(self._lines)

    def write(self, s):
        #normalise whitespace
        s = ' '.join(s.split())
        self._lines.extend(self._wrapper.wrap(s))

    def rawwrite(self, s):
        self._lines.extend(s.splitlines())

    def indent(self, numspaces=4, start=0):
        linebuf = self._lines
        n = len(linebuf)
        if n > start:
            indent = ' ' * numspaces
            for i in range(start, n):
                linebuf[i] = indent + linebuf[i]

    def lstrip(self):
        linebuf = self._lines
        for i in range(len(linebuf)):
            linebuf[i] = linebuf[i].lstrip()

class Parser(SGMLParser):

    def __init__(self, writer=sys.stdout):
        SGMLParser.__init__(self)
        self.writer = writer
        self.stringbuffer = StringIO()
        self.linebuffer = LineBuffer()
        self.verbatim = False
        self.lists = []
        self.ignoredata = False
        self.inblock = 0
        self.nobreak = False
        self.link = None

    def close(self):
        self.writeline()
        SGMLParser.close(self)

    def flush(self):
        if self.linebuffer:
            if self.inblock > 1:
                indent = 4 * (self.inblock - 1)
                self.linebuffer.indent(indent)
            self.writer.write(unescape(self.linebuffer.read()))
            self.linebuffer.clear()

    def flush_stringbuffer(self):
        sbuf = self.stringbuffer.getvalue()
        if not sbuf:
            return
        elif self.linebuffer:
            self.linebuffer[-1] += sbuf
        else:
            self.linebuffer.write(sbuf)
        self.clear_stringbuffer()

    def clear_stringbuffer(self):
        #self.stringbuffer.reset()
        self.stringbuffer.seek(0)
        self.stringbuffer.truncate()

    def data(self, text):
        self.stringbuffer.write(text)

    def pending(self):
        return self.stringbuffer.tell() or self.linebuffer

    def write(self, text=''):
        self.flush_stringbuffer()
        self.flush()
        self.writer.write(unescape(text))

    def writeline(self, text=''):
        self.write(text + '\n')

    def writestartblock(self, text=''):
        if self.pending():
            self.writeline()
        self.writeline()
        self.writeline(text)

    def writeendblock(self, text=''):
        self.writeline(text)
        self.writeline()

    def writeblock(self, text=''):
        self.writestartblock(text)
        self.writeline()

    def handle_data(self, data):
        if self.ignoredata:
            return
        elif self.verbatim:
            self.data(data)
        else:
            self.data(' '.join(data.splitlines()))

    def unknown_starttag(self, tag, attrs):
        if tag in IGNORETAGS:
            self.ignoredata = True
        elif len(tag) == 2 and tag[0] == 'h':
            self.writestartblock()
        elif tag == 'br':
            if self.verbatim:
                self.data('\n')
            elif not self.inblock:
                self.writeline()
            else:
                self.data(' ')
        elif not self.verbatim:
            self.data(' ')

    def unknown_endtag(self, tag):
        self.ignoredata = False
        if len(tag) == 2 and tag[0] == 'h':
            self.flush_stringbuffer()
            if self.linebuffer:
                linebuf = self.linebuffer
                linebuf[-1] = linebuf[-1].strip()
                char = UNDERLINES[int(tag[1])-1]
                linebuf.write(char * len(linebuf[-1]))
                self.writeline()
        #elif tag in BLOCKTAGS and self.pending():
        #    if self.lists:
        #        self.end_li()
        #    else:
        #        self.writeline()
        elif not self.verbatim:
            self.data(' ')

    def start_a(self, attrs):
        href = dict(attrs).get('href', None)
        if not href or href.startswith('#'):
            return
        self.data('`')
        self.link = href

    def end_a(self):
        if self.link:
            self.data(' <%s>`__' % self.link)
            self.link = None

    def start_pre(self, attrs):
        if self.lists:
            self.end_li()
            self.writeline()
        #self.inblock += 1
        self.verbatim = True
        self.writeblock(CODEBLOCK)

    def end_pre(self):
        sbuf = self.stringbuffer.getvalue()
        if sbuf:
            self.linebuffer.rawwrite(sbuf)
            self.linebuffer.indent(4)
        self.clear_stringbuffer()
        self.writeendblock()
        #self.inblock -= 1
        self.verbatim = False

    def start_ul(self, attrs):
        if self.lists:
            self.end_li()
            self.writeline()
        else:
            self.writeline()
        self.lists.append('+ ')
        self.inblock += 1

    def end_ul(self):
        self.end_li()
        self.lists.pop()
        self.inblock -= 1
        if self.inblock:
            self.writeline()
        else:
            self.writeendblock()

    def start_ol(self, attrs):
        if self.lists:
            self.end_li()
            self.writeline()
        else:
            self.writeline()
        self.lists.append('#. ')
        self.inblock += 1

    def end_ol(self):
        self.end_li()
        self.lists.pop()
        self.inblock -= 1
        if self.inblock:
            self.writeline()
        else:
            self.writeendblock()

    def start_p(self, attrs):
        if self.verbatim:
            self.writeline()
        elif not self.inblock:
            self.writeline()

    def end_p(self):
        if self.inblock:
        #self.flush_stringbuffer()
            if self.verbatim:
                self.writeline()
            else:
                return
        else:
            self.linebuffer.lstrip()
            self.writeline()

    def start_li(self, attrs):
        self.writeline()
        self.data(self.lists[-1])

    def end_li(self):
        self.flush_stringbuffer()
        linebuf = self.linebuffer
        if linebuf and linebuf[0] and linebuf[0].lstrip()[:2] in ['+ ', '#.']:
            start=1
        else:
            # the start of the <li> has already been written, perhaps because
            # there was a <pre> block
            start = 0
        self.linebuffer.indent(len(self.lists[-1]), start=start)
        self.write()

    def start_dl(self, attrs):
        self.writeline()
        self.inblock += 1
        self.nobreak = True

    def end_dl(self):
        self.nobreak = False
        self.writeline()
        self.inblock -= 1

    def start_dt(self, attrs):
        self.data(':')

    def end_dt(self):
        self.data(':')

    def start_dd(self, attrs):
        self.data(' ')

    def end_dd(self):
        self.flush_stringbuffer()
        self.linebuffer.indent(2, start=1)
        self.writeline()

    def start_em(self, attrs):
        self.data(' *')

    def end_em(self):
        self.data('*')

    def start_b(self, attrs):
        self.data(' **')

    def end_b(self):
        self.data('**')

    def start_code(self, attrs):
        self.data(' `')

    def end_code(self):
        self.data('`')

    def start_span(self, attrs):
        pass

    def end_span(self):
        pass

    def start_body(self, attrs):
        pass

    def end_body(self):
        self.end_p()
try:
    from BeautifulSoup import BeautifulSoup, NavigableString

    # don't seem to need this anymore - issue fixed in latest BeautifulSoup presumably
    class ShlurpUpYourShloup(BeautifulSoup):
        '''preserve whitespace in <pre>'''
        def endData(self, containerClass=NavigableString):
            if self.currentData:
                currentData = ''.join(self.currentData)
                if not currentData.strip():
                    if '\n' in currentData:
                        currentData = '\n'
                    else:
                        # just changed the following line
                        # original: currentData = ' '
                        currentData = u' ' * len(currentData)
                self.currentData = []
                if self.parseOnlyThese and len(self.tagStack) <= 1 and \
                    (not self.parseOnlyThese.text or \
                        not self.parseOnlyThese.search(currentData)):
                    return
                o = containerClass(currentData)
                o.setup(self.currentTag, self.previous)
                if self.previous:
                    self.previous.next = o
                self.previous = o
                self.currentTag.contents.append(o)

except ImportError:
    def ShlurpUpYourShloup(text, *args, **kw):
        return text

    BeautifulSoup = ShlurpUpYourSoup

def readsoup(fileobj, convert='html', encoding='utf8'):
    if hasattr(fileobj, 'read'):
        text = fileobj.read()
    else:
        text = open(fileobj, 'rb').read()
    #for br in ['<br>', '<br/>', '<br />']:
    #    text = text.replace(br, '\n')
    #    text = text.replace(br.upper(), '\n')
    return str(BeautifulSoup(text, convertEntities=convert,
                                            fromEncoding=encoding))

def html2rest(html, writer=sys.stdout):
    parser = Parser(writer)
    parser.feed(html)
    parser.close()

if __name__ == '__main__':
    # Eg.
    # python html2rest.py http://sphinx.pocoo.org/intro.html > intro.rst
    fileobj = None
    if sys.argv[1:]:
        arg = sys.argv[1]
        if arg.startswith('http://'):
            import urllib
            fileobj = urllib.urlopen(arg)
        else:
            fileobj = codecs.open(arg, 'rb', 'utf8')
    else:
        fileobj = sys.stdin
    if fileobj is not None:
        try:
            html2rest(fileobj.read())#readsoup(fileobj))
        finally:
            fileobj.close()


