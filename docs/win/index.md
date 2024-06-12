# WINシステム（地震学）の使い方
!!! Note "ノートの開き方"
    PCの場合は左のサイドメニューから， その他スマートフォンなどの場合は左上からメニューを開いて章を選んでください．

## 内容
東京大学地震研究所によるWINシステムについて． インストール方法やフォーマットの概要など．

## WINシステムとは
日本で標準的に使われている地震波形データのフォーマット，およびそれを処理するプログラム群です． 地震波形を読み取るためのGUIソフトウェアや，それを補助するためのプログラムから成ります．

フリーソフトなので無料でインストールできます．

日本の地震波形データは， ほとんどが 
<a href="https://wwweic.eri.u-tokyo.ac.jp/WIN/man.ja/winformat.html">WINフォーマット</a>
や
<a href="https://www.hinet.bosai.go.jp/faq/?LANG=ja#Q09">WIN32フォーマット</a>
（<a href="https://www.bosai.go.jp/">NIED</a>
による拡張版）で管理されているので知っておくと良いでしょう．

震源決定の論文でたまに見られる，Hirata, Matsu’uraの手法による震源決定プログラム<a href="https://wwweic.eri.u-tokyo.ac.jp/WIN/man.ja/hypomh.html">hypomh</a>もWINに付随しています．

## 動作環境
対応しているのはUnixのみです．

しかし最近はWindowsでも
<a href="https://learn.microsoft.com/ja-jp/windows/wsl/install">WSL(Windows Subsystem for Linux)</a>を使用して気軽に利用できます． 
ただし一度設定を終えれば快適に利用できますが，WSLでのGUIの設定は少し大変です．

またソフト自体がかなり古いので，Unix環境でしか動作せず，GUIの操作性にもやや癖があります．


## WINのつまづきポイント
フォーマットが複雑です． 処理に必要なデータが複数ファイルに分かれていることや，FORTRAN用の固定長ファイルの書式が独特である点など．

なおこれについては，波形処理の際に<a href="https://ds.iris.edu/ds/support/faq/17/sac-file-format/">SACフォーマット</a>に変換するとPythonなどでの取り扱いが便利です．
公式でWIN→SAC変換用の<a href="https://wwweic.eri.u-tokyo.ac.jp/WIN/man.ja/wintosac.html">wintosac</a>やwin2sacというコマンドが配布されています （ここでも2種類あるのがまたややこしい）．

さらに，公式マニュアルがかなり古いままで見にくかったり，使い方についての説明が不明瞭なところが多いです．  
それゆえ実際には大学での指導教員や先輩学生から使い方を伝授されなければ中々使いこなせない状況にあるように感じます．

そしてWINについて調べたい人に対して，そもそもの文献の少なさに加えて「WIN」という名前が追い打ちをかけます．  
検索してもWindowsの情報ばかりがでてきてしまうからです．

上記のような点が，初心者が導入や使用をする上でのハードルを上げているように感じます．

!!! success "参考サイト"
    -  WINシステムHP  
    [(https://wwweic.eri.u-tokyo.ac.jp/WIN/](https://wwweic.eri.u-tokyo.ac.jp/WIN/) 
    - WIN公式ドキュメンテーション  
    [https://wwweic.eri.u-tokyo.ac.jp/WIN/man.ja/](https://wwweic.eri.u-tokyo.ac.jp/WIN/man.ja/)
    - HYPOMHの手法についての論文  
    Hirata, N., and M. Matsu’ura (1987). Maximum-likelihood estimation of hypocenter with origin time eliminated using nonlinear inversion technique, Physics of the Earth and Planetary Interiors 47, 50–61, doi: 
    [10.1016/0031-9201%2887%2990066-5](https://doi.org/10.1016/0031-9201%2887%2990066-5).
    - SACフォーマットについて (英語)  
    [https://ds.iris.edu/ds/support/faq/17/sac-file-format/](https://ds.iris.edu/ds/support/faq/17/sac-file-format/)

    
