
# coding: utf-8

# In[1]:

#20 Wikipedia記事のJSONファイルを読み込み，「イギリス」に関する記事本文を表示せよ．問題21-29では，ここで抽出した記事本文に対して実行せよ．
import gzip
import json

with gzip.open("jawiki-country.json.gz", "rt") as fi:
    for line in fi:
        data_json = json.loads(line)
        if data_json["title"] == "イギリス":
            print(data_json["text"])
#loads関数：JSON文字列からPythonオブジェクトに変換する
#with ファイル読み込み as 変数:~~~~


# In[31]:

#21 記事中でカテゴリ名を宣言している行を抽出せよ．
import re
fname = 'jawiki-country.json.gz'

def extract_UK():
    with gzip.open(fname, 'rt') as fi:
        for line in fi:
            data_json = json.loads(line)
            if data_json['title'] == 'イギリス':
                return data_json['text']

# 正規表現のコンパイル
pattern = re.compile(r"^(.*\[\[Category:.*\]\].*)$", re.MULTILINE)
#\で特殊文字[]をエスケープする
#「.*」=任意の一文字＋繰り返し
#^先頭$末尾
#MULTILINE=通常 ^ は文字列の先頭にマッチし、 $ は文字列の末尾と文字列の末尾に改行(があれば)その直前にマッチします。
#このフラグが指定されると、 ^ は文字列の先頭と文字列の中の改行に続く各行の先頭にマッチします。
#同様に $ 特殊文字は文字列の末尾と各行の末尾(各改行の直前)のどちらにもマッチします

#findall(pattern, string)=正規表現にマッチする部分文字列を全て探しだしリストとして返します。
result = pattern.findall(extract_UK())

for line in result:
    print(line)


# In[35]:

#22 記事のカテゴリ名を（行単位ではなく名前で）抽出せよ．

pattern = re.compile(r"^.*\[\[Category:(.*?)(?:\]\]|\|).*$", re.MULTILINE)
#キャプチャー対象のみを()でくくる
#非貪欲マッチ(.*?)=できるだけ少ない#文字数のマッチ
#イギリス|*,英連邦王国|*,島国|くれいとふりてんに対処するために、キャプチャー対象外(?:...)、']]'または'|'

result = pattern.findall(extract_UK())

for line in result:
    print(line)


# In[56]:

#23 記事中に含まれるセクション名とそのレベル（例えば"== セクション名 =="なら1）を表示せよ．

pattern = re.compile(r"^(={2,})\s*(.+?)\s*(={2,}).*", re.MULTILINE)
#\s=任意の空白文字とマッチ
#(={2,}),=が２つ以上

result = pattern.findall(extract_UK())

for line in result:
    level = len(line[0]) - 1
    print("セクション名:",line[1],"レベル:",level)


# In[58]:

#24 記事から参照されているメディアファイルをすべて抜き出せ．
pattern = re.compile(r"(?:File|ファイル):(.+?)\|", re.MULTILINE)
#(?:...)=キャプチャしない、File or ファイル

result = pattern.findall(extract_UK())

for line in result:
    print(line)


# In[69]:

#25 記事中に含まれる「基礎情報」テンプレートのフィールド名と値を抽出し，辞書オブジェクトとして格納せよ

pattern = re.compile(r"^\{\{基礎情報.*?$(.*?)^\}\}$", re.MULTILINE+re.DOTALL)
#re.DOTALL=特殊文字 '.' を、改行を含むどんな文字にもマッチさせます
#re.compileは2objectsのみ故、+で接続

contents = pattern.findall(extract_UK())
#"|略名 = イギリス"から、フィールド名と値を抽出
pattern2 = re.compile(r"^\|(.+?)\s*=\s*(.+?)(?:(?=\n\|)| (?=\n$))", re.MULTILINE+re.DOTALL)
#(?=\n\|)=改行+'|'の手前（肯定の先読み）
#| (?=\n$)=または、改行+終端の手前（肯定の先読み）
#普通に\n\|と書いてしまうとフィールド名の行頭の|を消費してしまうため、次の検索でそのフィールドがヒットせず、フィールドの抽出が1行置きになってしまいます。

fields = pattern2.findall(contents[0])

result = {}
for field in fields:
    result[field[0]] = field[1]
result


# In[76]:

#26 25の処理時に，テンプレートの値からMediaWikiの強調マークアップ（弱い強調，強調，強い強調のすべて）を除去してテキストに変換せよ

pattern = re.compile(r"^\{\{基礎情報.*?$(.*?)^\}\}$", re.MULTILINE+re.DOTALL)

contents = pattern.findall(extract_UK())

pattern2 = re.compile(r"^\|(.+?)\s*=\s*(.+?)(?:(?=\n\|)| (?=\n$))", re.MULTILINE+re.DOTALL)

fields = pattern2.findall(contents[0])

patern3 = re.compile(r"\'{2,5}", re.MULTILINE+re.DOTALL)

result = {}
for field in fields:
    result[field[0]] = patern3.sub("",field[1])
result
#patern.sub("代替ワード",対象)


# In[91]:

#27 26の処理に加えて，テンプレートの値からMediaWikiの内部リンクマークアップを除去し，テキストに変換せよ

def remove_markup(target):

    # 強調マークアップの除去
    pattern = re.compile(r"(?:\'{2,5})(.*?)(?:\1)", re.MULTILINE)
    target = pattern.sub(r'\1', target)
    #r'\2,group2に置き換える

    # 内部リンクの除去
    pattern = re.compile(r"\[\[(?:[^|]*?\|)?([^|]*?)\]\]", re.MULTILINE)
    target = pattern.sub(r'\1', target)

    return target
    #[]=集合、[^a]はaを除くあらゆる文字にマッチ

pattern = re.compile(r"^\{\{基礎情報.*?$(.*?)^\}\}$", re.MULTILINE+re.DOTALL)

contents = pattern.findall(extract_UK())

pattern2 = re.compile(r"^\|(.+?)\s*=\s*(.+?)(?:(?=\n\|)| (?=\n$))", re.MULTILINE+re.DOTALL)

fields = pattern2.findall(contents[0])

result = {}
for field in fields:
    result[field[0]] = remove_markup(field[1])
result


# In[94]:

#28 27の処理に加えて，テンプレートの値からMediaWikiマークアップを可能な限り除去し，国の基本情報を整形せよ．

def remove_markup(target):

    # 強調マークアップの除去
    pattern = re.compile(r"(?:\'{2,5})(.*?)(?:\1)", re.MULTILINE)
    target = pattern.sub(r'\1', target)

    # 内部リンクの除去
    pattern = re.compile(r"\[\[(?:[^|]*?\|)?([^|]*?)\]\]", re.MULTILINE)
    target = pattern.sub(r'\1', target)

    # Template:Langの除去        {{lang|言語タグ|文字列}}
    pattern = re.compile(r"\{\{lang(?:[^|]*?\|)*?([^|]*?)\}\}", re.MULTILINE )
    target = pattern.sub(r'\1', target)

    # 外部リンクの除去  [http://xxxx] 、[http://xxx xxx]
    pattern = re.compile(r"\[http:\/\/(?:[^\s]*?\s)?([^]]*?)\]",re.MULTILINE )
    target = pattern.sub(r'\1', target)

    # <br>、<ref>の除去
    pattern = re.compile(r"<\/?[br|ref][^>]*?>", re.MULTILINE)
    target = pattern.sub('', target)

    return target

pattern = re.compile(r"^\{\{基礎情報.*?$(.*?)^\}\}$", re.MULTILINE+re.DOTALL)

contents = pattern.findall(extract_UK())

pattern2 = re.compile(r"^\|(.+?)\s*=\s*(.+?)(?:(?=\n\|)| (?=\n$))", re.MULTILINE+re.DOTALL)

fields = pattern2.findall(contents[0])

result = {}
for field in fields:
    result[field[0]] = remove_markup(field[1])
result


# In[98]:

#29 テンプレートの内容を利用し，国旗画像のURLを取得せよ
import urllib.parse, urllib.request

# 国旗画像の値を取得
fname_flag = result['国旗画像']

# リクエスト生成
url = 'https://www.mediawiki.org/w/api.php?'     + 'action=query'     + '&titles=File:' + urllib.parse.quote(fname_flag)     + '&format=json'     + '&prop=imageinfo'     + '&iiprop=url'

# MediaWikiのサービスへリクエスト送信
request = urllib.request.Request(url,
    headers={'User-Agent': 'TanakamaruNatsurou'})
connection = urllib.request.urlopen(request)

# jsonとして受信
data = json.loads(connection.read().decode())

# URL取り出し
url = data['query']['pages'].popitem()[1]['imageinfo'][0]['url']
print(url)


# In[ ]:



