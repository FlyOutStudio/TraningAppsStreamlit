# 💪 腕立て伏せ記録アプリ

Streamlitで動作する簡易的な筋トレ記録アプリです。腕立て伏せの回数を朝・昼・晩の3回記録し、総数と推移を可視化します。

## 機能

- 📝 **記録入力**: 日付を選択して、朝・昼・晩の回数を入力
- 📊 **データ可視化**: 日別の推移グラフと内訳グラフを表示
- 📈 **統計情報**: 総回数、記録日数、1日平均、最高/最低記録を表示
- 💾 **データ保存**: CSVファイルに自動保存（同じ日付の場合は更新）
- 📥 **データエクスポート**: CSVファイルをダウンロード可能

## 使い方

### ローカルで実行

1. リポジトリをクローン
```bash
git clone <your-repository-url>
cd TraningAppsStreamlit
```

2. 依存関係をインストール
```bash
pip install -r requirements.txt
```

3. アプリを起動
```bash
streamlit run app.py
```

4. ブラウザで `http://localhost:8501` にアクセス

### Streamlit Cloudにデプロイ

1. GitHubにリポジトリをプッシュ
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repository-url>
git push -u origin main
```

2. [Streamlit Cloud](https://streamlit.io/cloud)にアクセス

3. "New app"をクリック

4. GitHubリポジトリを選択

5. ブランチとメインファイル（`app.py`）を指定

6. "Deploy"をクリック

デプロイが完了すると、PWAとしてスマートフォンからもアクセス可能になります。

## データ形式

データは `data/pushup_records.csv` に保存されます。

```csv
date,morning,afternoon,evening,total
2024-12-01,10,15,20,45
2024-12-02,12,18,22,52
```

## 注意事項

- 記録期間は12月1日〜31日に制限されています
- 同じ日付の記録を保存すると、既存のデータが更新されます
- データファイルはStreamlit Cloudの永続ストレージに保存されます

## 技術スタック

- Python 3.8+
- Streamlit
- Pandas

## ライセンス

MIT License

