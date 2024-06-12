---
hide:
    - feedback
---

# K-Note (mk II)
!!! Note "お知らせ"
    現在，データ消失の復旧作業中です．

!!! Note "ノートの開き方"
    PCの場合は左のサイドメニューから， その他スマートフォンなどの場合は左上からメニューを開いて章を選んでください．

## 概要
個人的な作業メモをWEBに移植したものです．  
元は他人へ見せるために作成したものではないため
説明不足の箇所もございますが，
日本語文献の少なさを受けて公開することと致しました．

???+ tip "コードの説明の見方"
    もともと個人的な軽いメモなので記法にばらつきがありますが，次の記法には注意してください:  

    1. `< >`に挟まれた部分には，
    目的に応じて値を代入してください． 
    2. `...`は省略記号です．実際には入力しないでください．  

    ### 例)
    本サイトの説明で次のように書かれていたとします．
    ```python 
    fig, ax = plt.subplots(
        figsize = (<横のサイズ　inch>,<縦のサイズ inch>),
        ...
    )
    ```
    この場合，実際には`< >`に値を入力して次のように入力してください．
    ```python 
    fig, ax = plt.subplots(
        figsize = (6,4),
    )
    ```
    またメソッドによっては複数の引数をとるわけですから，その場合は次のように他の引き数を増やしても構いません:
    ```python 
    fig, ax = plt.subplots(
        ncols = 1,
        nrows = 1,
        figsize = (6,4),
    )
    ```

## 主な変更履歴
{{ read_csv('history.csv') }}

??? success "謝辞"
    本サイトの作成にあたっては，
    <a href="https://www.mkdocs.org/">MkDocs</a>
    およびそのテーマ
    <a href="https://squidfunk.github.io/mkdocs-material/">Material for MkDocs</a>
    を使用いたしました．  
    またその際に公式ドキュメントに加えて以下のサイトを大いに参考にさせていただきました．

    - <a href="https://zenn.dev/mebiusbox/articles/81d977a72cee01#%F0%9F%93%8C-pdf-%E5%87%BA%E5%8A%9B">
    mebiusboxさん 『MkDocsによるドキュメント作成』  
    </a>

    この場を借りて感謝申し上げます．