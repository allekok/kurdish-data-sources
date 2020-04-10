from os import listdir
# Functions
def get_head (dir, lang, style):
    HEAD = f'''<html dir="{dir}" lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>{style}</style>
</head><body>
<h1>سەرچاوەکانی دەیتا(Data)ی زمانی کوردی</h1>'''
    return HEAD.replace('\n','')
def get_style ():
    STYLE = '''
body {
max-width:1000px;
margin:0 auto;
font-size:17px;
line-height:2;
padding:2em 0
}
h1 {
font-weight:normal;
margin:0;
padding:0 .5em 1em
}
.entry a {
color:#333;
text-decoration:none;
font-size:1.2em
}
.entry a:hover {
opacity:.6
}
.entry {
padding:.3em .5em;
color:#333
}
.entry p {
margin:0
}
.ffbtn {
background:none;
border:0;
outline:0;
padding:1em 1em;
color:#333;
letter-spacing:2px
}
.ffbtn:hover {
opacity:.6
}
'''
    return STYLE.replace('\n','')
def get_script ():
    SCRIPT = '''
document.querySelectorAll(".ffbtn").forEach(function (o) {
o.addEventListener("click", function () {
const ff = o.parentNode.parentNode.querySelector(".ff");
ff.style.display = ff.style.display == "none" ? "" : "none";
});
});
'''
    return SCRIPT.replace('\n','')
def get_foot (script):
    return f'<script>{script}</script></body></html>'
def lines (text):
    return text.strip().split('\n')
def pair (line):
    return [x.strip() for x in line.split(':', 1)]
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

# Constants
LIST_DIR = 'LIST'
SITE_DIR = 'site'
FOOT = get_foot(get_script())
STYLE = get_style()

# Run
for lang in listdir(LIST_DIR):
    if lang.endswith('ar'): dir = 'rtl'
    else: dir = 'ltr'
    lng = lang[0:lang.find('.')]
    HEAD = get_head(dir,lng,STYLE)
    body = ''
    lang_path = f'{LIST_DIR}/{lang}'
    i = 0
    filelist = listdir(lang_path)
    filelist.sort(reverse=True, key=lambda x:int(x))
    for fname in filelist:
        i += 1
        with open(f'{lang_path}/{fname}', 'r') as f:
            text = f.read()
        lst = parse(text)
        name = assoc(lst, 'ناو')
        href = assoc(lst, 'نیشانی')
        link = ''
        if name and href:
            link = f'{kurdish_numbers(str(i))}. <a href="{v(href)}">{v(name)}</a>'
        body += f'''<div class="entry">
<p>{link}<button type="button" class="ffbtn">&bull;&bull;&bull;</button></p>
<div class="ff" style="display:none">'''
        for p in lst:
            key = k(p)
            if key == 'ناو' or key == 'نیشانی': continue
            body += f'<p>{key}: {v(p)}</p>'
        body += '</div></div>'
        body = body.replace('\n', '')
    with open(f'{SITE_DIR}/list.{lang}.html', 'w') as f:
        f.write(HEAD+body+FOOT)
    print(lang, 'done')
