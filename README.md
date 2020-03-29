# Takaoka fonts

Takaoka フォントは、IPA フォントの派生としてコミュニティによりメンテナンスされている
[Takao フォント](https://launchpad.net/takao-fonts)に対し次の変更を加え、主に PDF
出力時の埋め込みフォントとしての利用を想定し MS ゴシック、MS 明朝との相互運用性を高めた
ものです。

- 等幅ゴシック体にある 0 の斜線を削除
- ベースラインを MS ゴシック、MS 明朝と概ね同じ位置になるよう補正
- 低解像度用のヒントを削除

命名の由来は、Takao フォントが IPA フォントのオリジナル・デザイナーである故・林隆男氏
から取られていることから「隆男フォントか？」→「たかお（フォント）か」→「Takaoka」と
しました。

# Build

[fonttools](https://github.com/fonttools/fonttools) をインストールし、ビルドスクリプト
を動かすと、Takao フォントを取得して dest 以下に修正後のフォントファイルを出力します。

```python
pip install -r requirements.txt
python ./build.py
```

# Development

fonttools をライブラリとして使う方法についてはほとんどドキュメントがありませんが、
[ttlib の APIドキュメント](https://rsms.me/fonttools-docs/ttLib/index.html) から
ソースコードが辿って読むのが一番簡単です。

低解像度用のヒントについては、
- 置き換えた 0 のフォントのヒントを生成する方法がわからなかった
- 最近のディスプレイは十分高解像度であり MacOS ではもはやヒントを無視する
- PDF の埋め込み用途である
ことから一律削除しましたが、生成方法がわかれば対応するかもしれません。

# License

ビルドスクリプト自体は、[MIT License](LICENSE) で配布します。
生成されたフォントファイルは、[IPAフォントライセンスv1.0](IPA_Font_License_Agreement_v1.0.txt) に従ってください。
