# GL2F-cli

GL2 family ファンクラブサイトをターミナルから閲覧する非公式アプリです。
公式サイトではメンバーごとのリストが用意されていなかったり複数の記事を開くのが大変だったり使いづらかったので作りました。
ブラウザで開くとき以上のやりとりをしていないので大丈夫と思っていますが、このアプリは利用規約に触れる行為を目的とはしていませんので、問題があるかもしれない部分を見つけたら教えてくださると助かります。

![](docs/demo.gif)


## 機能

* ブログ・ラジオ・ニュースのリストを表示する
	* グループごと、メンバーごとの出力
	* 引数による出力フォーマットの指定


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


## ログイン

Chrome がインストールされている環境では、次のコマンドを使うことでブラウザを使ってログインすることができます。
ログイン後は日記の本文や画像のダウンロードができるようになります。

```
gl2f auth login
```


## 使い方

とりあえず[#コマンドの例](#コマンドの例)を実行してみると良いと思います。

**記事をリストする** ためには、 `gl2f <サブコマンド>` またはその短縮コマンドを使います。
サブコマンドには以下のものがあり、取得するページの最新情報をリストします。

| コマンド | 短縮 | 取得するページ |
|:-:|:-:|:-|
| `gl2f blogs` | `gl2b` | ブログ （ https://girls2-fc.jp/page/blogs 等） |
| `gl2f radio` | `gl2r` | ラジオ ( https://girls2-fc.jp/page/lucky2radio 等) |
| `gl2f news` | `gl2n` | ニュース ( https://girls2-fc.jp/page/familyNews 等) |


`gl2f open <blogs...>` 等とすることで、リストした記事を**ブラウザで開く**ことができます。
チェックボックスが出ますので、スペースキーで選択しEnterで確定してください。


### サブコマンドの引数

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
* `--order <オプション>` ソートの指定。 公開日 `reservedAt` と記事タイトル `name` のどちらかについて、昇順 `asc`と降順 `desc` を指定します。デフォルトは `reservedAt:desc` で、更新日の新しいものから並べます。
* `-f, --format` リストのフォーマット指定。以下の要素を `:` で区切って与えます。デフォルトは `author:title:url` です。
	* `author` 著者名
	* `title` 記事タイトル
	* `url` URL
	* `date-p` 記事が公開された日時
	* `date-c` 記事がアップロードされた日時
	* `index` リスト上での番号を振ります
	* `br` 改行。
* `-df, --date-format` 日時のフォーマット指定。デフォルトは月/日(`%m/%d`)。書式については[こちら](https://docs.python.org/ja/3/library/datetime.html#strftime-strptime-behavior)
* `--break-urls` URLを改行して表示します。 `-f` で `url -> br:url` と置き換えることと同じです。
* `--enum` リストに番号を振ります。 `-f` に `index` を含めることと同じです。
* `-d, --date` リストの左側に公開日時を表示します。 `-f` に `date-p` を含めることと同じです。
* `--preview <オプション>` 記事本文を表示します。会員限定コンテンツはログインが必要です。オプションは `full, compact, compressed` がありいずれも全文を表示しますが、後のものほど改行等が短縮され短く表示されます。オプションを入力しなければ `compact` となります。
* `--dl-media <オプション>` 記事中の画像や動画を保存します（アクセスできる場合のみ）。オプションは主に動画のために用意しました。何も指定しない場合にはファイルをそのままダウンロードします。`stream` を指定すると、動画をストリーム視聴するためのファイルが保存され、待ち時間が減ります。`skip` でメディアを実際にはダウンロードしなくなります。


## 開発予定

[issues](https://github.com/trnciii/gl2f-cli/issues) を見てください。
また希望があれば追加してください。
分類のため、以下のタグを用意しています。

* listing リストする情報や整理について
* appearance リストや記事の表示・整形について

twitter [@trnciii](https://twitter.com/trnciii) [@trncix](https://twitter.com/trncix) でも報告等を受け付けます。


## コマンドの例

### 対象を指定する

Girls2 のブログを表示する
```sh
gl2f ls blogs girls2
```

渡辺未優のブログを表示する
```sh
gl2f ls blogs miyu
```

今日投稿されたブログを表示する（`today` は `blogs` でのみ使えます）
```sh
gl2f ls blogs today
```

山口莉愛 の lovely2 の頃のブログを表示する。
```sh
gl2f ls blogs rina --group lovely2
```

Lucky2 のラジオを表示する
```sh
gl2f ls radio lucky2
```

杉浦優來のラジオを表示する
```sh
gl2f ls radio yura
```

Girls2 のニュースを表示する
```sh
gl2f ls news girls2
```

Girls2, Lucky2 両方のニュースを表示する（`family` は `news` でのみ指定できます）
```sh
gl2f ls news family
```

lovely2 のブログを20件表示する
```sh
gl2f ls blogs lovely2 -n 20
```

Lucky2 のニュースの最新6番目から10番目を表示する (1ページあたり5件の2ページ目)
```sh
gl2f ls news lucky2 -n 5 -p 2
```

lovely2 のニュースを公開日の早いものから10件表示する（コメント部分を書くと公開年月日も表示する）
```sh
gl2f ls news lovely2 --order reservedAt:asc # --date --date-format '%Y/%m/%d'
```

原田都愛のブログをタイトル降順で30件表示する
```sh
gl2f ls blogs toa --order name:desc -n 30
```
```sh
原田都愛　 🦆🦆🦆🦆🦆🦆🦆🦆🦆🦆🦆🦆🦆🦆🦆 https://girls2-fc.jp/page/blogs/305718498280080541
原田都愛　 🥳🥳🥳🥳🥳 https://girls2-fc.jp/page/blogs/296237525440136273
原田都愛　 🥲😄 https://girls2-fc.jp/page/blogs/571710357186282433
原田都愛　 🥲 https://girls2-fc.jp/page/blogs/567537622214247465
原田都愛　 🥦 https://girls2-fc.jp/page/blogs/505608708496032705
原田都愛　 🤪🤪🤪🤪🤪🤪🤪 https://girls2-fc.jp/page/blogs/526227849607119675
原田都愛　 🤔🤔🤔🤔🤔🤔 https://girls2-fc.jp/page/blogs/304428618660971677
原田都愛　 🟦 https://girls2-fc.jp/page/blogs/531432161908097851
原田都愛　 🟦 https://girls2-fc.jp/page/blogs/590320261769724865
原田都愛　 🟥 https://girls2-fc.jp/page/blogs/661038676481934273
原田都愛　 🟡 https://girls2-fc.jp/page/blogs/671935404454183776
原田都愛　 🙏🙏🙏🙏 https://girls2-fc.jp/page/blogs/474485847387800617
原田都愛　 😭😭😭🙏😭😭🙏 https://girls2-fc.jp/page/blogs/415343499320230849
原田都愛　 😭😭😭😭😭😊😊😊😊😊😊 https://girls2-fc.jp/page/blogs/407733763091465324
原田都愛　 😢😢😢😢😭😭 https://girls2-fc.jp/page/blogs/479292590374519849
原田都愛　 😛😁😏☺️😋🤨😙😛😏😊😗😉 https://girls2-fc.jp/page/blogs/317133005120341149
原田都愛　 😑😑😑😑 https://girls2-fc.jp/page/blogs/470792896459572161
原田都愛　 😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊 https://girls2-fc.jp/page/blogs/434610414874002273
原田都愛　 😊😊😊 https://girls2-fc.jp/page/blogs/646890072674665409
原田都愛　 😊 https://girls2-fc.jp/page/blogs/594672645702681403
原田都愛　 😊 https://girls2-fc.jp/page/blogs/632701706739647529
原田都愛　 😊 https://girls2-fc.jp/page/blogs/556652576032949289
原田都愛　 😆😆😆😆😆 https://girls2-fc.jp/page/blogs/302787299039511387
原田都愛　 😆 https://girls2-fc.jp/page/blogs/576240964746609467
原田都愛　 😄 https://girls2-fc.jp/page/blogs/586028060705293353
原田都愛　 😁😁 https://girls2-fc.jp/page/blogs/653436213872558907
原田都愛　 😁 https://girls2-fc.jp/page/blogs/605703447957734337
原田都愛　 😁 https://girls2-fc.jp/page/blogs/588185500834071593
原田都愛　 😁 https://girls2-fc.jp/page/blogs/597980766613275585
原田都愛　 😁 https://girls2-fc.jp/page/blogs/593649955202139073
```


### 表示方法を指定する

Girls2 のニュース本文を表示する。
```sh
gl2f cat news girls2
```

GL2 family のニュースを、すべての改行を維持して表示する。
```sh
gl2f cat --opetion full news family
```

森朱里のブログを、左端に番号を振って表示する
```sh
gl2f ls blogs akari --enum
# もしくは
gl2f ls blogs akari -f index:author:title:url
```

鶴屋美咲のラジオを公開日とともに表示する
```sh
gl2f ls radio misaki -d
# もしくは
gl2f ls radio misaki -f date-p:author:title:url
```

永山椿のブログを url を改行して表示する
```sh
gl2f ls blogs tsubaki --break-urls
# もしくは
gl2f ls blogs tsubaki -f author:title:br:url
```

lovely2 スタッフのブログを、投稿日と公開日とともに表示する。日時は秒まで表示する。
```sh
gl2f ls blogs lovely2staff -f author:date-p:date-c:title:url -d '%m/%d %H:%M:%S'
```
