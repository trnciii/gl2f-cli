# 全てのコマンド

全てのコマンドを説明するページです。
多くのコマンドは記事のリストを作り、それらに対して操作を行います。
リストする対象の指定や表示の整形は共通の引数で行うので、 [リストの作り方](./boards.md) に書きます。
必要に応じてそちらも参照してください。

リストを引数とするコマンドは、記事の種類によって短縮ができます。
`gl2f <subcommand> <blogs/news/radio>` がそれぞれ `gl2b <subcommand> / gl2n <subcommand> / gl2r <subcommand>` と同等です。


## `gl2f auth` 認証関係

### `gl2f auth login`

Chrome が開ける環境では、このコマンドで開いたブラウザでログインすることで、日記の本文や画像のダウンロードができるようになります。

### `gl2f auth remove`

PCに保存されている認証情報を削除します。



## `gl2f cat` ターミナルで本文を読む

引数に記事のリストを与えます。
チェックボックスが現れるので、記事を選択して本文をターミナル上に出力します。
リストの与え方の詳細は [リストの作り方](./boards.md) を読んでください。

[GL2 family ニュース](https://girls2-fc.jp/page/familyNews) のリストを使う
```sh
gl2f cat news family
# or
gl2n cat family
```

オプションは以下のものがあります。

* `-a, --all` チェックボックスを使った選択を行わず、リストされた全ての記事本文を出力します。
* `--option { full, compact, compressed }` 本文の改行をどれくらい詰めるかを決めます。 `full` は全ての改行を維持します。 `compact` は空行をなくします（デフォルト）。 `compressed` は全く改行しません。

GL2 family のニュース本文を、すべての改行を維持して表示する。
```sh
gl2n cat --option full family
# or
gl2f cat --option full news family
```


## `gl2f dl` 記事に含まれる画像や動画をダウンロードする

引数に記事のリストを与えます。
チェックボックスが現れるので、記事を選択してダウンロードします。
ダウンロード先は `~/gl2f/media` です。
リストの与え方の詳細は [リストの作り方](./boards.md) を読んでください。

> **Note**
> 現在、すべてのファイルが同じ保存されるようになっています。
> 正直使いにくいと思うので今後何かしら修正するつもりです。
> その際フォルダ構成が非互換になることを予想しています。


## `gl2f ls` 記事の情報をリストする

記事のリストを整形して表示します。
集める記事や整形のオプションは [リストの作り方](./boards.md) に従います。

小田柚葉のブログを表示する。urlは改行する。
```sh
gl2r ls yuzuha --break-urls
# or
gl2f ls radio yuzuha --break-urls
```

lovely2 スタッフのブログ20件を投稿日と公開日（秒まで）表示する。
```sh
gl2b ls lovely2staff -f author:date-p:date-c:title:url -d '%m/%d %H:%M:%S'
# or
gl2f ls blogs lovely2staff -f author:date-p:date-c:title:url -d '%m/%d %H:%M:%S'
```



## `gl2f open` 記事をブラウザで開く

引数に記事のリストを与えます。
チェックボックスが現れるので、記事を選択してページをブラウザで開きます。
リストの与え方の詳細は [リストの作り方](./boards.md) を読んでください。

鶴屋美咲のラジオを開く
```sh
gl2f open radio misaki
# or
gl2r open misaki
```

オプションは以下のものがあります。

* `-a, --all` チェックボックスを使った選択を行わず、リストされた全ての記事本文を出力します。

今日投稿されたブログを全て開く
```sh
gl2b open -a today
# or
gl2f open -a blogs today
```
