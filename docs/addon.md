# アドオンを追加する

gl2f はpython パッケージとして配布されたアドオンを追加し、新しいコマンドを登録することができます。
インストールされたアドオンの名前をconfig の addons リストに追加することでコマンドが使用可能になります。

`~/gl2f/config.json` の設定例
```json
{
  "addons": [
    "gl2f_share"
  ]
}
```

Config のaddons の項目は `gl2f config edit`, `addons` コマンドを使用して編集することもできます。


## アドオンを作成する

アドオンはpython パッケージとして提供され、gl2f がコマンドを解決するのに使用する [argparse](https://docs.python.org/3/library/argparse.html) のサブパーサを編集することで新しいコマンドを登録します。
アドオンはコマンドを一つ登録するモジュールのリスト `registrars` を提供し、各モジュールはパーサーを編集するために必要な関数を実装する必要があります。

次のパッケージは新しく二つのコマンド `gl2f lovegenic`, `gl2f local shakeshakeshake` を追加するアドオン gl2f-intro` の例です。

[`gl2f-intro` 名前空間]
```python
class LoveGenic:
	@staticmethod
	def add_to():
		# コマンドの登録先 'gl2f' とコマンド名 'lovegenic' を返します。
		return 'gl2f', 'lovegenic'

	@staticmethod
	def add_args(parser):
		# argparse.ArgumentParser オブジェクトを編集します。
		# サブコマンドとして実行される関数を登録するために、handler アトリビュートを追加します。
		parser.set_defaults(handler = lambda _:print(f'Yeah, yeah, yeah, yeah, yeah, yeah'))


class ShakeShakeShake:
	@staticmethod
	def add_to():
		# コマンドの登録先 'gl2f local' とコマンド名 'shakeshakeshake' を返します。
		return 'gl2f.local', 'shakeshakeshake'

	@staticmethod
	def add_args(parser):
		# argparse.ArgumentParser オブジェクトを編集します。
		# サブコマンドとして実行される関数を登録するために、handler アトリビュートを追加します。
		parser.set_defaults(handler = lambda _:print(f'Shake-shake-shake (Come on)'))


registrars = [LoveGenic, ShakeShakeShake] # 各コマンドの登録関数リスト
```

`~/gl2f/config.json` に `gl2f-intro` アドオンを追加します。
```json
{
  "addons": [
    "gl2f_intro"
  ]
}
```

登録したコマンドが使用できるようになります。
```
$ gl2f lovegenic
Yeah, yeah, yeah, yeah, yeah, yeah
$ gl2f local shakeshakeshake
Shake-shake-shake (Come on)
```
