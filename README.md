# curvature
野球のボールのモーションキャプチャデータを使用したPython解析サンプル

curvature.pyは，実際に約140km/hの投球時のモーションキャプチャ（1kHz）で計測したボールの重心の位置データを利用し，曲率計算を計算するコードである．データは最大外旋位（MER）からリリース後10フレーム（10ms）までの，ボールの空間軌道データを下記にアップした．おおよそ$X$の正の方向へ飛翔する投球データである．

コードを実行すると，「ボールの速度のグラフ」と，「ボールと曲率中心の３D軌道のグラフ」を描画できる．ただし，データ（ball_trajectory.csv）をダウンロードしていただき，ご自身の環境にあわせてデータ保存場所のディレクトリを，コードのdata_dir=の後に入力していただく必要がある．

<img width="640" height="480" alt="Figure_1" src="https://github.com/user-attachments/assets/431ef70a-9b00-46f2-8235-0358837dee1c" />

<img width="1000" height="800" alt="Figure_2" src="https://github.com/user-attachments/assets/eb79680f-7018-4deb-8f87-b614c9e5ec44" />
