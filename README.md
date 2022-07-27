# GL2F-cli

GL2 family ファンクラブサイトをターミナルから閲覧する非公式アプリです。
ブラウザで開くとき以上のやりとりをしていないので大丈夫と思っていますが、このアプリは利用規約に触れる行為を目的とはしていませんので、問題があるかもしれない部分を見つけたら教えてくださると助かります。


## 機能

* ブログ・ラジオ・ニュースのリストを表示する
	* グループごと、メンバーごとの出力
	* 引数による出力フォーマットの指定
	* ラジオの特別編やニュースの分類はまだ


## 必要なもの

* 以下の機能に対応したターミナル
	* 全角文字・絵文字の表示（なかなか完全には難しいようです）
	* 256 color
	* url を開いてくれるものが便利です
* python3 & pip
	* request （インストールすれば同時に入ります）


## インストール

pip でこのリポジトリから直接インストール

```sh
pip install git+https://github.com/trnciii/gl2f-cli
```

## 使い方

`gl2f <サブコマンド>` もしくは `gl2f-<サブコマンド>` という形で利用します。
サブコマンドは `blogs, radio, news` があり、それぞれブログ（ https://api.fensi.plus/v1/sites/girls2-fc/texts/271474317252887717/contents 等）、ラジオ ( https://api.fensi.plus/v1/sites/girls2-fc/texts/lucky2Radio/contents 等)、 ニュース ( https://api.fensi.plus/v1/sites/girls2-fc/news/familyNews/contents 等) の最新情報をリストします。
直後にある引数とオプションの説明に加えて、コマンドの例を末尾にたくさん載せますので参考にしてください。


## サブコマンドの引数

サブコマンドに続けて、グループや個人名を引数で指定します。

```sh
gl2f blogs girls2 # Girls2 のブログ
gl2f radio yura # 杉浦優來 のラジオ
gl2f news family # GL2 family 両方のニュース。 https://girls2-fc.jp/page/familyNews
```

引数はグループ名もしくはメンバーの下の名前を、アルファベット小文字で書きます。
また、`blogs` では lovely2 スタッフを表す `lovely2staff` と今日の投稿を取得する `today` が使えます。
`news` ではGL2 family 両方のニュースを取得するために `family` が使えます。


### オプション

* `-n, --number` 読み込み数の指定。1~99 の範囲です。
* `-p, --page` ページの指定。
* `--group` グループの指定。ブログで、莉愛と優來のときに `--group lovley2` とすることで lovely2 時代の記事を取りに行きます。
* `-f, --format` リストのフォーマット指定。以下の要素をパイプで区切って与えます。デフォルトは `author|title|url` です。
	* `author` 著者名
	* `title` 記事タイトル
	* `url` URL
	* `date-p` 記事が公開された日時
	* `date-c` 記事がアップロードされた日時
	* `index` リスト上での番号を振ります
	* `\n` 改行。
* `-df, --date-format` 日時のフォーマット指定。デフォルトは月/日(`%m/%d`)。書式については[こちら](https://docs.python.org/ja/3/library/datetime.html#strftime-strptime-behavior)
* `--preview <オプション>` 記事本文を表示します。会員限定コンテンツは認証が必要なので、ニュースだけ見れる状態かと思います。オプションは `full, compact, compressed` がありいずれも全文を表示しますが、後のものほど改行等が短縮され短く表示されます。オプションを入力しなければ `compact` となります。
* `--break-urls` URLを改行して表示します。 `-f` で `url -> \n|url` と置き換えることと同じです。
* `--enum` リストに番号を振ります。 `-f` に `index` を含めることと同じです。
* `-d, --date` リストの左側に公開日時を表示します。 `-f` に `date-p` を含めることと同じです。


## 開発予定

[issues](https://github.com/trnciii/gl2f-cli/issues) を見てください。
また希望があれば追加してください。

機能で分類するため、以下のタグを用意しています。

* listing


## コマンドの例

### 対象の指定

Girls2 のブログを表示する
```sh
gl2f blogs girls2
```

小田柚葉のブログを表示する
```sh
gi2f blogs yuzuha
```

今日投稿されたブログを表示する（`today` は `blogs` でのみ使えます）
```sh
gl2f blogs today
```

山口莉愛 の lovely2 の頃のブログを表示する。
```sh
gl2f blogs rina --group lovely2
```

Lucky2 のラジオを表示する
```sh
gl2f radio lucky2
```

森朱里 のラジオを表示する
```sh
gl2f radio akari
```

Girls2 のニュースを表示する
```sh
gl2f news girls2
```

Girls2, Lucky2 両方のニュースを表示する（`family` の指定は `news` でのみ使えます）
```sh
gl2f news family
```

lovely2 のブログを20件表示する
```sh
gl2f blogs lovely2 -n 20
```

Lucky2 のニュースの最新6番目から10番目を表示する (1ページあたり5件の2ページ目)
```sh
gl2f news lucky2 -n 5 -p 2
```


### 表示方法の指定

Girls2 のニュースを本文とともに表示する。本文は連続した改行を省略する。
```sh
gl2f news girls2 --preview
# もしくは
gl2f news girls2 --preview compact
```

Lucky2 のニュース99件を、改行の全くない本文とともに表示する。
```sh
gl2f news lucky2 -n 99 --preview compressed
```

GL2 family のニュース最新5件を、すべての改行を維持して表示する。
```sh
gl2f news family -n 5 --preview full
```

原田都愛のブログを、左端に番号を振って表示する
```sh
gl2f blogs toa --enum
# もしくは
gl2f blogs toa -f 'index|author|title|url'
```

鶴屋美咲のラジオを公開日とともに表示する
```sh
gl2f radio misaki -d
# もしくは
gl2f radio misaki -f'date-p|author|title|url'
```

永山椿のブログを url は改行して表示する
```sh
gl2f blogs tsubaki --break-urls
# もしくは
gl2f blogs tsubaki -f'author|title|\n|url'
```

lovely2 スタッフのブログを、投稿日と公開日とともに表示する。日時は秒まで表示する。
```sh
gl2f blogs lovely2staff -f'author|date-p|date-c|title|url' -df '%m/%d %H:%M:%S'
```
