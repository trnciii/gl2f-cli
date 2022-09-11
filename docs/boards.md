# リストの作り方

サブコマンド `cat, ls, open` は、対象となるリストや表示の整形を指示する必要があります（[コマンドの説明](./commands.md)）。
リストの指定はページの種類（ブログ、ニュース、ラジオ等）と、さらに必要なグループまたはメンバーを与えて行います、。
またメインコマンドとして `gl2b / gl2n / gl2r` を使うとページの種類を省略することができます。

Girls2 のブログを開く
```sh
gl2b open girls2
# or
gl2f open blogs girls2
```

杉浦優來のラジオを開く
```sh
gl2r open yura
# or
gl2f open radio yura
```

GL2 family のニュースを開く
```sh
gl2n open family
# or
gl2f open news family
```


## 引数

ページの種類によって、指定できるメンバー名などは変わります。

### `blogs` 日記

日記のリスト ( https://girls2-fc.jp/page/blogs 等 ) を取得します。
指定できるのはグループ名 `girls2, loveky2, lucky2`, メンバーの下の名前のアルファベット小文字 `yuzuha, momoka, misaki, ...`, また当日の更新を取得する `today` です。
メインコマンドを `gl2b` とすると `blogs` を省略できます。

今日投稿されたブログを全て開く
```sh
gl2b open -a today
# or
gl2f open -a blogs today
```

### `news` ニュース

ニュースのリスト ( https://girls2-fc.jp/page/familyNews 等 ) を取得します。
指定できるのはグループ名 `girls2, loveky2, lucky2` と、Girls2 + Lucky2 の `family` です。
メインコマンドを `gl2n` とすると `news` を省略できます。

GL2 family のニュース本文を表示する。
```sh
gl2n cat family
# or
gl2f cat news family
```

### `radio` ラジオ

ラジオのリスト ( https://girls2-fc.jp/page/lucky2radio 等 ) を取得します。
指定できるのはグループ名 `girls2, loveky2, lucky2`, メンバーの下の名前のアルファベット小文字 `yuzuha, momoka, misaki, ...` です。
メインコマンドを `gl2r` とすると `radio` を省略できます。

比嘉優和のラジオをブラウザで開く
```sh
gl2r open yuwa
# or
gl2f open radio yuwa
```

### `gtube` Gtube

Gtube ( https://girls2-fc.jp/page/gtube ) を取得します。
メインコマンドを `gl2t` とすると `gtube` を省略できます。

Gtube をブラウザで開く
```sh
gl2t open
# or
gl2f open gtube
```


### `shangrila` Girls2 Live Tour 2022 Shangri-la Photo Gallery

Shangri-la のフォトギャラリー ( https://girls2-fc.jp/page/ShangrilaPG ) を取得します。
`pg` を省略できるメインコマンドはありません。

Shangri-la Photo Gallery の画像をダウンロードする
```sh
gl2f dl shangrila
```

> **Note**
> 特設ページをどうまとめるかまだ迷っていて、今後変更があるかもしれません。


## オプション

リストを作るために共通して以下のオプションがあります。

* `-n, --number` 読み込み数の指定。1~99 の範囲です。
* `-p, --page` ページの指定。
* `--group` グループの指定。ブログで、莉愛と優來のときに `--group lovley2` とすることで lovely2 時代の記事を取りに行きます。
* `--order <オプション>` ソートの指定。 公開日 `reservedAt` と記事タイトル `name` のどちらかについて、昇順 `asc`と降順 `desc` を指定します。デフォルトは `reservedAt:desc` で、更新日の新しいものから並べます。

山口莉愛 の lovely2 の頃のブログを開く
```sh
gl2b open rina --group lovely2
# or
gl2f open blogs rina --group lovely2
```

lovely2 のブログを20件一覧表示する
```sh
gl2b ls lovely2 -n 20
# or
gl2f ls blogs lovely2 -n 20
```

Lucky2 のニュースの最新6番目から10番目を一覧表示する (1ページあたり5件の2ページ目)
```sh
gl2n ls lucky2 -n 5 -p 2
# or
gl2f ls news lucky2 -n 5 -p 2
```

原田都愛のブログをタイトル降順で30件を一覧表示する
```sh
gl2b ls toa --order name:desc -n 30
# or
gl2f ls blogs toa --order name:desc -n 30
```


また、表示方法を制御するために以下のオプションがあります。

* `-f, --format` リストのフォーマット指定。以下の要素を `:` で区切って与えます。デフォルトは `author:title:url` です。
	* `author` 著者名
	* `title` 記事タイトル
	* `url` URL
	* `date-p` 記事が公開された日時
	* `date-c` 記事がアップロードされた日時
	* `index` リスト上での番号を振ります
	* `br` 改行。
* `-d, --date` フォーマット指定を指定して記事の公開日時を左側に表示します。デフォルトは月/日(`%m/%d`)。書式については[こちら](https://docs.python.org/ja/3/library/datetime.html#strftime-strptime-behavior)
* `--break-urls` URLを改行して表示します。 `-f` で `url -> br:url` と置き換えることと同じです。
* `--enum` リストに番号を振ります。 `-f` に `index` を含めることと同じです。


Girls2 のニュースを公開日の早いものから10件一覧表示する。公開年月日も表示する
```sh
gl2n ls girls2 --order reservedAt:asc  -d '%Y/%m/%d'
# or
gl2f ls news girls2 --order reservedAt:asc -d '%Y/%m/%d'
```

lovely2 スタッフのブログを、投稿日と公開日とともに一覧表示する。日時は秒まで表示する。
```sh
gl2b ls lovely2staff -f author:date-p:date-c:title:url -d '%m/%d %H:%M:%S'
# or
gl2f ls blogs lovely2staff -f author:date-p:date-c:title:url -d '%m/%d %H:%M:%S'
```