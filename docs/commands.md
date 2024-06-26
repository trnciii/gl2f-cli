# 全てのコマンド

全てのコマンドを説明するページです。
多くのコマンドは記事のリストを作り、それらに対して操作を行います。
リストする対象の指定や表示の整形は共通の引数で行うので、 [リストの作り方](./boards.md) に書きます。
必要に応じてそちらも参照してください。


## `gl2f auth` 認証関係

### `gl2f auth login`

email アドレスとパスワードを入力して認証をとります。

オプション
* `-u --email` アカウントのemailアドレス
* `-p --password` アカウントのパスワード

### `gl2f auth remove`

PCに保存されている認証情報を削除します。

### `gl2f auth set-token`

認証情報を直接入力します。

### `gl2f auth update`

認証情報を更新します。


## `gl2f cat` ターミナルで本文を読む

引数に記事のリストまたは一つのURLを与えます。
チェックボックスが現れるので、記事を選択して本文をターミナル上に出力します。
また可能な環境であれば sixel で画像も表示します。
リストの与え方の詳細は [リストの作り方](./boards.md) を読んでください。

[GL2 family ニュース](https://girls2-fc.jp/page/familyNews) のリストを使う
```sh
gl2f cat news/family
```

オプションは以下のものがあります。

* `-a, --all` チェックボックスを使った選択を行わず、リストされた全ての記事本文を出力します。
* `--style { full, compact, compressed }` 本文の改行をどれくらい詰めるかを決めます。 `full` は全ての改行を維持し、可能であれば画像も表示します。 `compact` （デフォルト）は空行をなくし、可能であれば画像を表示します。 `compressed` は全く改行せず、画像も表示しません。
* `--no-image` このフラグを立てると、どのスタイルにおいても画像を表示しないようになります。

GL2 family のニュース本文を、まったく改行せずに表示する。
```sh
gl2f cat --style compressed news/family
```

特定のURLを開く
```sh
gl2f cat https://girls2-fc.jp/page/lucky2blogs/748008846546437131
```


## `gl2f completion` Bash 補完を生成する

bash-completion 用の簡単なスクリプトを用意しています。
インストール後、 `gl2f completion` で生成されるので、シェルの起動時などに読み込むとコマンドやページ名に補完が効くようになります。

```sh
eval "$(gl2f completion)"
```

もしくはbash-completion の読み込み先 (`/share/bash-completion/completions` とか `/etc/bash_completion.d`　とか?) にファイルとして保存します。

```sh
gl2f completion > path/to/bash_completions/gl2f.bash
```


## `gl2f dl` 記事に含まれる画像や動画をダウンロードする

引数に記事のリストまたは一つのURLを与えます。
チェックボックスが現れるので、記事を選択してダウンロードします。
ダウンロード先は `~/gl2f/contents/<content id>` です。
ID が数字ばかりで分かりにくいので、ダウンロードしたファイルを読むための機能を追加するつもりです。
リストの与え方の詳細は [リストの作り方](./boards.md) を読んでください。

> **Note**
> 以前はダウンロード先が `~/gl2f/media/` でした。
> その頃にダウンロードしたファイルは今のシステムに影響しませんが、互換性もありません。

オプションは以下のものがあります。

* `-a, --all` チェックボックスを使った選択を行わず、リストされた全ての記事をダウンロードします。
* `--steam` 動画の場合にファイルそのものをダウンロードせず、ストリーム再生用のファイルをダウンロードします。視聴に時間制限があります。
* `--skip` 動画ファイルはダウンロードしません。
* `-F, --force` デフォルトでは既に存在するファイルを改めてダウンロードしませんが、これを有効にすると新しくダウンロードしたファイルで上書き保存します。
* `-o` 出力先を指定します。


## `gl2f local` ローカルファイルを操作する

ダウンロードしたデータなどを操作するコマンドです。

* `gl2f local clear-cache` 画像等のキャッシュを削除します。
* `gl2f local dir` ファイルなどが保存されているディレクトリを返します。これは `~/gl2f` の絶対パスです。
* `gl2f local index` ダウンロードしたファイルを閲覧するWeb UI を構築・更新します。
* `gl2f local install` Web UI をインストールします。
* `gl2f local ls` ダウンロードしたファイルを全てリストします。[リストの整形](./boards.md#リストの整形) に従って表示方法を変えることができます。
* `gl2f local stat` ダウンロードしたファイルの数とサイズを表示します。
* `gl2f local open` Web UI をブラウザで開きます。

### Web UI

ダウンロードしたファイルはもともとのIDで保存/管理しています。
しかしこれは閲覧しにくいため、見やすいweb形式のファイルを構築することができます。

利用のためにはまず `gl2f local install` でファイルをインストールしてください。
以降は `gl2f local open` コマンドか、ブラウザで `~/gl2f/site/index.html` を直接開くことでダウンロードした記事の一覧を見ることができます。



## `gl2f ls` 記事の情報をリストする

記事のリストを整形して表示します。
集める記事や整形のオプションは [リストの作り方](./boards.md) に従います。

小田柚葉のブログを表示する。urlは改行する。
```sh
gl2f ls radio/yuzuha --break-urls
```

lovely2 スタッフのブログ20件を投稿日と公開日（秒まで）表示する。
```sh
gl2f ls blogs/lovely2staff -f author:date-p:date-c:title:url -d '%m/%d %H:%M:%S'
```



## `gl2f open` 記事をブラウザで開く

引数に記事のリストを与えます。
チェックボックスが現れるので、記事を選択してページをブラウザで開きます。
リストの与え方の詳細は [リストの作り方](./boards.md) を読んでください。

鶴屋美咲のラジオを開く
```sh
gl2f open radio/misaki
```

オプションは以下のものがあります。

* `-a, --all` チェックボックスを使った選択を行わず、リストされた全ての記事本文を出力します。

今日投稿されたブログを全て開く
```sh
gl2f open -a blogs/today
```


## `gl2f pages` ページ定義を編集する

リストとして取得可能なページを追加したり、`today` で巡回するページの追加や削除をおこないます。
ページ定義の変更後はコマンド補完を改めて設定してください。

### 用語
|用語|意味|例|
||||
| key | コマンドに与えるページ名 | blogs/girls2, gtube, news/lucky2 |
| page id | url 上の page 以下の文字列 | blogs, gtube, lucky2news |



### `gl2f pages add-definition <page id>` 取得可能なページを追加する
Page id を与えて gl2f がページを取得可能にします。

オプション
* `--key <key>` コマンドの引数として使うページ名前を指定します。
* `--activate` ページを `today` の巡回対象に設定します。

ttps://girls2-fc.jp/page/Lucky2FanMeeting2024PG を `fm/lucky2-2024` として追加する。
```sh
gl2f pages add-definition Lucky2FanMeeting2024PG --key fm/lucky2-2024
# key の名前で使用可能になった
gl2f ls fm/lucky2 -f title
【東京公演】07組の突撃Vlog!⑦
【東京公演】りなゆら本番前リポーター🤍💜③
【東京公演】07組の突撃Vlog!⑥
【東京公演】07組の突撃Vlog!⑤
【東京公演】07組の突撃Vlog!④
【東京公演】集合写真📸
【東京公演】つばききのCloset
【東京公演】Lucky²の座席占い
【東京公演】07組の突撃Vlog!③
【東京公演】07組の突撃Vlog!②
```

### `gl2f pages remove-definition <key>` ページ定義を削除する
key が指すページ定義を削除します。


### `gl2f pages add-to-today <key>`
`key` のページを `today` の巡回対象に追加します。

### `gl2f pages remove-from-today <key>`
`key` のページを `today` の巡回対象から外します。


### `gl2f pages show-today`
`today` の巡回対象として設定されているページを表示します。

### `gl2f pages filter-page-data`
リスト可能なページ定義を取得し、フィルタして出力します。


オプション
* `-f, --filter` フィルタを追加します。複数指定した場合はすべての条件を満たすものが出力されます。デフォルトは `list-board not-existing` です。
* `--dump` 取得したページ定義全体を指定したパスに保存します。
* `--load` ページ定義をダウンロードするかわりに、指定したファイルから読み込みます。
* `--no-filter` フィルタを適用せず、全てのページ定義を出力します。
* `--raw` 結果のデータ構造をそのまま出力します。

使用できるフィルタ
* `list-board` リスト可能なものをフィルタします。
* `existing` ローカルの定義に存在するもののみ表示します。
* `not-existing` ローカルの定義に存在しないもののみ表示します。
* `board-id:<id>` id を `:` 区切りで直接指定します。


## `gl2f search` 記事の内容を検索する

引数に記事のリストと1つ以上のキーワードをスペース区切りで与えます。
取得した記事のタイトルと本文の中をキーワードで検索し、結果を表示します。
リストの与え方の詳細は [リストの作り方](./boards.md) を読んでください。

佐藤栞奈の直近99件のブログから"金魚", "弟"を含むものを検索する
```sh
gl2f search blogs/kanna -n99 金魚 弟
```
