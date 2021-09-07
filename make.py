from os import listdir

# Functions: HTML Template
def get_head(dir, lang, style):
        return f'''
        <html dir="{dir}" lang="{lang}">
        <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width">
        <style>{style}</style>
        </head><body>
        <h1>سەرچاوەکانی دەیتا(Data)ی زمانی کوردی</h1>
        '''

def get_style():
        return '''
        @font-face {
        font-family:'nesx';
        font-display:swap;
        src:url("//allekok.github.io/src/frontend/style/DroidNaskh-Regular.woff2") format("woff2")
        }
        body {
        max-width:1000px;
        margin:0 auto;
        font-family:'nesx';
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
        font-size:1.3em
        }
        .entry a:hover {
        opacity:.6
        }
        .entry {
        padding:1em;
        color:#333
        }
        .entry:nth-child(odd) {
        background:#EFEFEF;
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
        small {
        font-family:monospace;
        font-size:.6em;
        font-weight:bold;
        padding-left:.5em;
        }
        li {
        word-wrap:break-word;
        }
        '''

def get_script():
        return ''

def get_foot(script):
        return f'<script>{script}</script></body></html>'

# Functions: Parser
def lines(text):
        return text.strip().split('\n')

def pair(line):
        return [x.strip() for x in line.split(':', 1)]

def parse(text):
        return [pair(x) for x in lines(text)]

def k(pair):
        return pair[0]

def v(pair):
        return pair[1]

def assoc(lst, key):
        for x in lst:
                if key == k(x):
                        return x

# Functions: Misc.
def kurdish_numbers(str):
        eng = ['1','2','3','4','5','6','7','8','9','0']
        ckb = ['١','٢','٣','٤','٥','٦','٧','٨','٩','٠']
        for i in range(len(eng)):
                str = str.replace(eng[i], ckb[i])
        return str

# Constants
LIST_DIR = 'LIST'

LANG = 'ckb'
DIR = 'rtl'
STYLE = get_style()
SCRIPT = get_script()
HEAD = get_head(DIR, LANG, STYLE)
FOOT = get_foot(SCRIPT)

# Body
body = ''
i = 0
filelist = listdir(LIST_DIR)
filelist.sort(reverse=True, key=lambda x:int(x))
for fname in filelist:
        fpath = f'{LIST_DIR}/{fname}'
        with open(fpath, 'r') as f:
                text = f.read()
                lst = parse(text)
                name = assoc(lst, 'ناو')
                href = assoc(lst, 'نیشانی')
                link = ''

                if name and href:
                        link = f'''
                        <a href="{fpath}"><small>[TXT]</small></a>
                        {kurdish_numbers(fname)}. <a href="{v(href)}"
                        >{v(name)}</a>
                        '''
                        
                body += f'''
                <div class="entry">
                <p>{link}</p>
                <ul class="ff">
                '''
                
                for p in lst:
                        key = k(p)
                        if key == 'ناو' or key == 'نیشانی':
                                continue
                        body += f'<li>{key}: {v(p)}</li>'

                body += '</ul></div>'
                
                # foot
                html = HEAD + body + FOOT
                html = html.replace('\n','').replace('        ','')
                with open('index.html', 'w') as f:
                        f.write(html)
                        
# done
print('done')
