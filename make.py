from os import listdir
# Constants
LIST_DIR = 'LIST'
SITE_DIR = 'site'
foot = '</body></html>'
style = """body {
    max-width:1000px;
    margin:0 auto;
    font-size:17px;
    line-height:2;
}
h1 {
    font-weight:normal;
    margin:0;
    padding:0 .5em;
}
.entry a {
    color:#06F;
    text-decoration:none;
    font-size:1.6em;
}
.entry a:hover {
    text-decoration:underline;
}
.entry {
    padding:.5em;
    color:#333;
}
.entry p {
    margin:0
}
"""

# Functions
def list_strip (lst):
    return [x.strip() for x in lst]
def lines (text):
    return text.strip().split('\n')
def pair (line):
    return list_strip(line.split(':', 1))
def parse (text):
    return [pair(x) for x in lines(text)]
def k(pair): return pair[0]
def v(pair): return pair[1]
def assoc (lst, key):
    for x in lst:
        if key == k(x): return x
def kurdish_numbers (str):
    eng = ['1','2','3','4','5','6','7','8','9','0']
    ckb = ['١','٢','٣','٤','٥','٦','٧','٨','٩','٠']
    for i in range(len(eng)):
        str = str.replace(eng[i], ckb[i])
    return str

# Run
for lang in listdir(LIST_DIR):
    if lang.endswith('ar'): dir = 'rtl'
    else: dir = 'ltr'
    lng = lang[0:lang.find('.')]
    head = '<html dir="' + dir  + '" lang="' + lng + \
        '"><head><meta charset="utf-8">' + \
        '<meta name="viewport" content="width=device-width, initial-scale=1">' + \
        '<style>' + style + '</style></head><body>' + \
        '<h1>سەرچاوەکانی دەیتا(Data)ی زمانی کوردی</h1>'
    body = ''
    lang_path = LIST_DIR + '/' + lang
    i = 0
    filelist = listdir(lang_path)
    filelist.sort(reverse=True, key=lambda x:int(x))
    for fname in filelist:
        i += 1
        with open(lang_path + '/' + fname, 'r') as f:
            text = f.read()
        lst = parse(text)
        name = assoc(lst, 'ناو')
        href = assoc(lst, 'نیشانی')
        link = ''
        if name and href:
            link = '<p>' + kurdish_numbers(str(i)) + \
                '. <a href="' + v(href) + '">' + v(name) + '</a></p>'
        body += '<div class="entry">' + link
        for p in lst:
            if k(p) == 'ناو': continue
            if k(p) == 'نیشانی': continue
            body += '<p>' + k(p) + ': ' + v(p) + '</p>'
        body += '</div>'
    with open(SITE_DIR + '/list.' + lang + '.html', 'w') as f:
        f.write(head+body+foot)
    print(lang, 'done')
