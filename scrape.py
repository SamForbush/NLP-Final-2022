import sys
from pdfminer.high_level import extract_text

text = extract_text(f'pdfs/{sys.argv[1]}.pdf')
with open(f'poems/{sys.argv[1]}.csv', 'w') as fp:
    fp.write(text)

