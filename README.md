# curvature
2025.9.6更新

野球のボールのモーションキャプチャデータを使用し，ボールの曲率中心の変化（軌道）を計算する，Python解析サンプル

コードの説明や曲率中心については，
Qiita記事「[Numerical Recipes in Biomechanics #4 空間の曲率中心と力学](https://qiita.com/skill-vis/items/657261e08d7f8452466c)」
を参照されたい．

データの置き場所は，下記のように変更した．

curvature/

├── data/

│　　　└── ball_trajectory.csv  ← サンプルデータ

└── code/

　　　└── curvaturee.py    ← Pythonコード

codeディレクトリ下にPythonコード**curvature.py**を配置し，dataディレクトリ下にサンプルデータの**ball_trajectory.csv**を置いた．
また，この変更に応じ，Pythonコード**curvature.py**のディレクトリをos.path.dirname()で設定し，そこからdataディレクトリに移動し，サンプルデータの**ball_trajectory.csv**を読み込むように変更した．

curvature.pyは，実際に約140km/hの投球時のモーションキャプチャ（1kHz）で計測したボールの重心の位置データball_trajectory.csvを利用し，曲率計算行うコードである．

ball_trajectory.csvデータは最大外旋位（MER）からリリース後10フレーム（10ms）までの，ボールの空間軌道データを下記にアップした．おおよそXの正の方向へ飛翔する野球の投球データで，多点のマーカをボールに貼付し，モーションキャプチャ（1kHzでサンプリング）で計測したその多点位置から非線形最適化（Levenberg-Marquardt法）でボールの中心（重心相当）を計算したデータである．ball_trajectory.csvデータ自体は平滑化はしていない．

<img width="314" height="301" alt="ball_with_marker" src="https://github.com/user-attachments/assets/3d000190-86c3-43a0-8074-e02894d3f808" />


コードを実行すると，「ボールの速度のグラフ」と，「ボールと曲率中心の３D軌道のグラフ」を描画できる．

<img width="640" height="480" alt="Figure_1" src="https://github.com/user-attachments/assets/431ef70a-9b00-46f2-8235-0358837dee1c" />

<img width="1000" height="800" alt="Figure_2" src="https://github.com/user-attachments/assets/165af1ab-3d66-43e6-bd32-cb30e1480811" />


リリース前は曲率半径が大きくなるので（理論上無限大），リリースの３フレーム前まで描いている．

# 曲率とその力学に関係する式のまとめ
### 曲率
$$
\kappa = \frac{1}{R} = \frac{|\boldsymbol{a} \times \boldsymbol{v}|}{|\boldsymbol{v}|^3}
$$
### 単位主法線ベクトル
$$
\boldsymbol{n}  = \frac{\boldsymbol{v} \times (\boldsymbol{a} \times \boldsymbol{v})}{|\boldsymbol{v}| ~|\boldsymbol{a} \times \boldsymbol{v}|}
$$

### 接線方向の加速度
$$
\begin{aligned}
\boldsymbol{a}_{\parallel} &= (\boldsymbol{a}^T \boldsymbol{T})\boldsymbol{T} = \left( \boldsymbol{a}^T \frac{\boldsymbol{v}}{|\boldsymbol{v}|} \right) \frac{\boldsymbol{v}}{|\boldsymbol{v}|}
\\\\
&= \frac{d}{dt}|\boldsymbol{v}| \boldsymbol{T}
\end{aligned}
$$

### 主法線方向（半径）の加速度
$$
\begin{aligned}
\boldsymbol{a}_{\perp} &= \boldsymbol{a} - \boldsymbol{a}_{\parallel}
\\\\
&= \frac{\boldsymbol{v} \times (\boldsymbol{a} \times \boldsymbol{v})}{|\boldsymbol{v}|^2}
\end{aligned}
$$

### 曲率中心
$$
\begin{aligned}
\boldsymbol{C}(t) &= \boldsymbol{x}(t) + \frac{1}{\kappa(t)}\boldsymbol{n}(t) = \boldsymbol{x}(t) + R(t) \boldsymbol{n}(t)
\\\\
&= \boldsymbol{x}(t) + 
|\boldsymbol{v}|^2 ~\frac{\boldsymbol{v} \times (\boldsymbol{a} \times \boldsymbol{v})}{|\boldsymbol{a} \times \boldsymbol{v}|^2}
\\\\
&= \boldsymbol{x}(t) + \frac{|\boldsymbol{v}|^3}{|\boldsymbol{a} \times \boldsymbol{v}|}
\left(\frac{\boldsymbol{a} - \boldsymbol{a}_{\parallel}}{|\pmb{a} - \boldsymbol{a}_{\parallel}|} \right)= \boldsymbol{x}(t) + \frac{|\boldsymbol{v}|^3}{|\boldsymbol{a} \times \boldsymbol{v}|}
\frac{\boldsymbol{a} - (\boldsymbol{a}^T \boldsymbol{T})\boldsymbol{T}}{|\pmb{a} - (\boldsymbol{a}^T \boldsymbol{T})\boldsymbol{T}|}
\end{aligned}
$$
