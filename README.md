# LabelImg - Enhanced Edition

**Python 3.10対応版** - DICOMサポート強化とUI改善を含む画像アノテーションツール

このプロジェクトは、[tzutalin](https://github.com/tzutalin)氏の[LabelImg](https://github.com/tzutalin/labelImg)をベースに、Python 3.10サポートと強化されたDICOM機能を追加したものです。

## ✨ 新機能・改善点

### 🐍 Python 3.10 完全対応
- Python 3.10環境での完全動作保証
- すべてのPython 2構文をPython 3に移行
- 最新のライブラリとの互換性確保

### 🏥 強化されたDICOM機能
- **自動Window/Level調整**: DICOM読み込み時に最適な表示設定を自動計算
- **リアルタイムスライダー**: 画面上の直感的なスライダーでWindow/Level をリアルタイム調整
- **改善されたDICOM表示**: より正確で高速なDICOM画像処理
- **シリーズ選択**: 複数シリーズを含むDICOMフォルダから任意のシリーズを選択可能

### 🎨 UI/UX改善
- **画面上スライダー**: メニューではなく画面上に配置された使いやすいWindow/Levelコントロール
- **自動調整ボタン**: ワンクリックでWindow/Levelを最適化
- **リセット機能**: デフォルト値への簡単復帰
- **視覚的フィードバック**: 現在の設定値をリアルタイム表示

## 🔧 インストール

### 必要環境
- **Python 3.10** (3.8以上推奨)
- **PyQt5** または **PyQt4**
- **NumPy**
- **Pillow**
- **pydicom** (DICOM機能用)

### 簡単インストール (推奨)

1. **Python 3.10をインストール**
   - [Python公式サイト](https://www.python.org/downloads/)からPython 3.10以上をダウンロード・インストール

2. **リポジトリをクローン**
   ```bash
   git clone <this-repository-url>
   cd labelimg-enhanced
   ```

3. **依存関係をインストール**
   ```bash
   pip install PyQt5 numpy pillow pydicom lxml tqdm
   ```

4. **アプリケーションを起動**
   ```bash
   python labelImg.py
   ```

### Anaconda/Minicondaを使用する場合 (オプション)

Anacondaを既に使用している場合は、以下の方法も利用できます：

1. **リポジトリをクローン**
   ```bash
   git clone <this-repository-url>
   cd labelimg-enhanced
   ```

2. **Conda環境を作成・アクティベート**
   ```bash
   conda env create -f environment.yml
   conda activate label-img
   ```

3. **アプリケーションを起動**
   ```bash
   python labelImg.py
   ```

## 🚀 使用方法

### 基本的なアノテーション

1. **アプリケーションを起動**
   ```bash
   python labelImg.py
   ```

2. **保存フォルダを設定**
   - Menu/File → 'Change default saved annotation folder'

3. **画像フォルダを開く**
   - 'Open Dir' をクリックして画像フォルダを選択

4. **アノテーション開始**
   - 'Create RectBox' をクリック
   - マウスでドラッグしてバウンディングボックスを作成
   - 右クリックでボックスのコピー・移動が可能

### DICOM画像の処理

1. **DICOMフォルダを開く**
   - 'Open DICOMs' をクリック
   - DICOMファイルを含むフォルダを選択

2. **シリーズを選択**
   - 複数シリーズがある場合、選択ダイアログが表示されます

3. **Window/Level調整**
   - **自動調整**: DICOM読み込み時に自動で最適化
   - **手動調整**: 画面右上のスライダーで調整
   - **Auto ボタン**: ワンクリックで再最適化
   - **Reset ボタン**: デフォルト値に戻す

### クラス定義のカスタマイズ

`data/predefined_classes.txt` ファイルを編集して、独自のクラスを定義できます。

```text
person
car
bicycle
dog
cat
```

## ⌨️ キーボードショートカット

| キー           | 機能                           |
|----------------|--------------------------------|
| `w`            | バウンディングボックスを作成   |
| `d`            | 次の画像                       |
| `a`            | 前の画像                       |
| `Ctrl + Wheel` | ズームイン/アウト             |
| `Ctrl + S`     | 保存                           |
| `Ctrl + D`     | ラベルとボックスを複製         |
| `Del`          | 選択中のボックスを削除         |
| `Space`        | 現在の画像を検証済みにマーク   |
| `Ctrl + +`     | ズームイン                     |
| `Ctrl + -`     | ズームアウト                   |
| `↑ → ↓ ←`     | 選択中のボックスを移動         |

## 📁 対応フォーマット

### 入力画像フォーマット
- **DICOM** (.dcm, .dicom)
- **JPEG** (.jpg, .jpeg)
- **PNG** (.png)
- **BMP** (.bmp)
- **TIFF** (.tiff, .tif)

### 出力アノテーションフォーマット
- **Pascal VOC** (XML)
- **YOLO** (TXT)

## 🧪 開発・貢献

### 開発環境のセットアップ

```bash
# 開発用の依存関係をインストール
conda env create -f environment.yml
conda activate label-img

# テストの実行
python -m pytest tests/
```

### 貢献方法

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add some amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 🐛 トラブルシューティング

### よくある問題

**Q: PyQt5のインストールエラー**
```bash
# conda経由でのインストール
conda install pyqt

# または pip経由
pip install PyQt5
```

**Q: DICOMファイルが読み込めない**
```bash
# pydicomをインストール
conda install pydicom
# または
pip install pydicom
```

**Q: Python 3.10で動作しない**
- このバージョンはPython 3.10に完全対応しています
- 古いバージョンを使用している場合は、最新版に更新してください

## 📝 更新履歴

### v2.0.0 (2024年版)
- ✨ Python 3.10完全対応
- ✨ DICOM自動Window/Level調整機能
- ✨ リアルタイムスライダーウィジェット
- 🐛 すべてのPython 2構文を修正
- 🎨 UI/UXの大幅改善
- 📚 ドキュメントの全面更新

## 📄 ライセンス

MIT License - 詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 🙏 謝辞

- オリジナルの[LabelImg](https://github.com/tzutalin/labelImg) by [tzutalin](https://github.com/tzutalin)
- DICOMサポートの初期実装 by [chrischute](https://github.com/chrischute)

## 📚 引用

```bibtex
@misc{labelimg2024,
  title={LabelImg - Enhanced Edition with Python 3.10 and DICOM Support},
  year={2024},
  publisher={GitHub},
  url={<this-repository-url>}
}
```

---

💡 **ヒント**: DICOMファイルの処理で問題が発生した場合は、まず自動調整機能を試してみてください。ほとんどのケースで最適な表示設定が自動的に適用されます。
