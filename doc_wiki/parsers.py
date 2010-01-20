import re

from markdown import Markdown, TextPreprocessor
from smartypants import smartyPants

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, TextLexer


class CodeBlockPreprocessor(TextPreprocessor):
    """
        The Pygments Markdown Preprocessor
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        This fragment is a Markdown_ preprocessor that renders source code
        to HTML via Pygments.  To use it, invoke Markdown like so::

            from markdown import Markdown

            md = Markdown()
            md.textPreprocessors.insert(0, CodeBlockPreprocessor())
            html = md.convert(someText)

        markdown is then a callable that can be passed to the context of
        a template and used in that template, for example.

        This uses CSS classes by default, so use
        ``pygmentize -S <some style> -f html > pygments.css``
        to create a stylesheet to be added to the website.

        You can then highlight source code in your markdown markup::

            @@ lexer
            some code
            @@ end

        .. _Markdown: http://www.freewisdom.org/projects/python-markdown/

        :copyright: 2007 by Jochen Kupperschmidt.
        :license: BSD, see LICENSE for more details.
    """
    pattern = re.compile(r'@@ (.+?)\n(.+?)\n@@ end', re.S)
    
    formatter = HtmlFormatter(noclasses=False)
    
    def run(self, lines):
        def repl(m):
            try:
                lexer = get_lexer_by_name(m.group(1))
            except ValueError, instance:
                lexer = TextLexer()
            
            code = highlight(m.group(2), lexer, self.formatter)
            code = code.replace('\n\n', '\n&nbsp;\n').replace('\n', '<br />')
            
            return '\n\n<div class="code">%s</div>\n\n' % code
        
        return self.pattern.sub(repl, lines)


class SmartyPantsPreprocessor(TextPreprocessor):
    """
    A Markdown preprocessor that implements SmartyPants for converting plain 
    ASCII punctuation characters into typographically correct versions
    """
    pattern = re.compile(r'(.+?)(@@.+?@@ end|$)', re.S)
    
    def run(self, lines):
        def repl(m):
            return smartyPants(m.group(1)) + m.group(2)
        
        return self.pattern.sub(repl, lines)


def parse_markdown(value):
    """
    Parses a value into markdown syntax, using the pygments preprocessor and smartypants
    """
    md = Markdown()
    
    md.textPreprocessors.insert(0, SmartyPantsPreprocessor())
    md.textPreprocessors.insert(1, CodeBlockPreprocessor())
    
    return md.convert(value)
