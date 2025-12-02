import streamlit as st
import pandas as pd
from datetime import datetime, date
import os

# ページ設定
st.set_page_config(
    page_title="腕立て伏せ記録アプリ",
    page_icon="💪",
    layout="wide"
)

# CSVファイルのパス
DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "pushup_records.csv")

# データディレクトリが存在しない場合は作成
os.makedirs(DATA_DIR, exist_ok=True)

# データ読み込み関数
@st.cache_data
def load_data():
    """CSVファイルからデータを読み込む"""
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            df['date'] = pd.to_datetime(df['date']).dt.date
            return df
        except Exception as e:
            st.error(f"データの読み込みに失敗しました: {e}")
            return pd.DataFrame(columns=['date', 'morning', 'afternoon', 'evening', 'total'])
    else:
        return pd.DataFrame(columns=['date', 'morning', 'afternoon', 'evening', 'total'])

# データ保存関数
def save_data(df):
    """データをCSVファイルに保存"""
    try:
        df.to_csv(CSV_FILE, index=False)
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"データの保存に失敗しました: {e}")
        return False

# データ読み込み
df = load_data()

# タイトル
st.title("💪 腕立て伏せ記録アプリ")
st.markdown("---")

# サイドバー：記録入力
with st.sidebar:
    st.header("📝 記録を入力")
    
    # 日付選択（12月1日〜31日に制限）
    today = date.today()
    current_year = today.year
    min_date = date(current_year, 12, 1)
    max_date = date(current_year, 12, 31)
    selected_date = st.date_input(
        "日付を選択",
        value=today,
        min_value=min_date,
        max_value=max_date
    )
    
    # 日付バリデーション
    if selected_date < min_date or selected_date > max_date:
        st.error("12月1日〜31日の範囲で選択してください")
        st.stop()
    
    # 既存データの確認
    existing_data = None
    existing_index = None
    if not df.empty:
        existing_rows = df[df['date'] == selected_date]
        if len(existing_rows) > 0:
            existing_index = existing_rows.index[0]
            existing_data = existing_rows.iloc[0]
    
    # 既存データがある場合は表示
    if existing_data is not None:
        st.info(f"📋 {selected_date}の既存記録: 朝{int(existing_data['morning'])}回 / 昼{int(existing_data['afternoon'])}回 / 晩{int(existing_data['evening'])}回 (合計{int(existing_data['total'])}回)")
        st.caption("⬇️ 追加する回数を入力してください（既存の値に加算されます）")
    
    # 回数入力（常に0からスタート）
    st.subheader("回数を入力")
    
    morning_count = st.number_input("朝", min_value=0, value=0, step=1)
    afternoon_count = st.number_input("昼", min_value=0, value=0, step=1)
    evening_count = st.number_input("晩", min_value=0, value=0, step=1)
    
    # 合計計算
    daily_total = morning_count + afternoon_count + evening_count
    st.metric("本日の合計", f"{daily_total}回")
    
    # 保存ボタン
    if st.button("💾 記録を保存", type="primary", use_container_width=True):
        if daily_total == 0:
            st.warning("合計が0回です。記録を保存しますか？")
        
        if existing_index is not None:
            # 既存データに加算
            new_morning = int(existing_data['morning']) + morning_count
            new_afternoon = int(existing_data['afternoon']) + afternoon_count
            new_evening = int(existing_data['evening']) + evening_count
            new_total = new_morning + new_afternoon + new_evening
            
            df.loc[existing_index, 'morning'] = new_morning
            df.loc[existing_index, 'afternoon'] = new_afternoon
            df.loc[existing_index, 'evening'] = new_evening
            df.loc[existing_index, 'total'] = new_total
            
            st.success(f"✅ {selected_date}の記録に追加しました！（朝+{morning_count}回 / 昼+{afternoon_count}回 / 晩+{evening_count}回）")
        else:
            # 新しいデータを追加
            new_row = pd.DataFrame({
                'date': [selected_date],
                'morning': [morning_count],
                'afternoon': [afternoon_count],
                'evening': [evening_count],
                'total': [daily_total]
            })
            df = pd.concat([df, new_row], ignore_index=True)
            st.success(f"✅ {selected_date}の記録を保存しました！")
        
        # 日付でソート
        df = df.sort_values('date').reset_index(drop=True)
        
        # データを保存
        if save_data(df):
            st.rerun()

# メインコンテンツ
col1, col2, col3 = st.columns(3)

# 総数表示
if not df.empty:
    total_pushups = df['total'].sum()
    col1.metric("総回数", f"{total_pushups:,}回")
    
    # 記録日数
    record_days = len(df)
    col2.metric("記録日数", f"{record_days}日")
    
    # 1日平均
    avg_daily = total_pushups / record_days if record_days > 0 else 0
    col3.metric("1日平均", f"{avg_daily:.1f}回")
else:
    col1.metric("総回数", "0回")
    col2.metric("記録日数", "0日")
    col3.metric("1日平均", "0回")

st.markdown("---")

# データ表示とグラフ
if not df.empty:
    # タブで表示を切り替え
    tab1, tab2, tab3 = st.tabs(["📊 推移グラフ", "📋 データ一覧", "📈 統計情報"])
    
    with tab1:
        st.subheader("日別の推移")
        
        # グラフ用のデータ準備
        chart_df = df.copy()
        chart_df['date'] = pd.to_datetime(chart_df['date'])
        chart_df = chart_df.sort_values('date')
        
        # 折れ線グラフ
        st.line_chart(
            chart_df.set_index('date')[['total']],
            use_container_width=True
        )
        
        # 棒グラフ（朝・昼・晩の内訳）
        st.subheader("朝・昼・晩の内訳")
        chart_data = chart_df.set_index('date')[['morning', 'afternoon', 'evening']]
        st.bar_chart(chart_data, use_container_width=True)
    
    with tab2:
        st.subheader("記録データ一覧")
        
        # データテーブル表示（編集可能）
        display_df = df.copy()
        display_df['date'] = display_df['date'].astype(str)
        display_df = display_df.rename(columns={
            'date': '日付',
            'morning': '朝',
            'afternoon': '昼',
            'evening': '晩',
            'total': '合計'
        })
        
        # 編集可能なデータエディタ
        edited_df = st.data_editor(
            display_df,
            use_container_width=True,
            hide_index=True,
            num_rows="dynamic",  # 行の追加・削除を可能にする
            column_config={
                "日付": st.column_config.DateColumn(
                    "日付",
                    format="YYYY-MM-DD",
                    required=True,
                ),
                "朝": st.column_config.NumberColumn(
                    "朝",
                    min_value=0,
                    required=True,
                ),
                "昼": st.column_config.NumberColumn(
                    "昼",
                    min_value=0,
                    required=True,
                ),
                "晩": st.column_config.NumberColumn(
                    "晩",
                    min_value=0,
                    required=True,
                ),
                "合計": st.column_config.NumberColumn(
                    "合計",
                    disabled=True,  # 合計は自動計算されるため編集不可
                ),
            }
        )
        
        # 変更を保存ボタン
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("💾 変更を保存", type="primary"):
                # カラム名を元に戻す
                edited_df = edited_df.rename(columns={
                    '日付': 'date',
                    '朝': 'morning',
                    '昼': 'afternoon',
                    '晩': 'evening',
                    '合計': 'total'
                })
                
                # 日付をdate型に変換
                edited_df['date'] = pd.to_datetime(edited_df['date']).dt.date
                
                # 合計を再計算
                edited_df['total'] = edited_df['morning'] + edited_df['afternoon'] + edited_df['evening']
                
                # データを保存
                if save_data(edited_df):
                    st.success("✅ データを保存しました！")
                    st.rerun()
        
        with col2:
            st.caption("💡 テーブル内のセルをクリックして直接編集できます。編集後は「変更を保存」ボタンをクリックしてください。")
        
        st.markdown("---")
        
        # CSVダウンロードボタン
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 CSVファイルをダウンロード",
            data=csv,
            file_name=f"pushup_records_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with tab3:
        st.subheader("統計情報")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**最高記録**")
            max_total = df['total'].max()
            max_date = df[df['total'] == max_total]['date'].values[0]
            st.metric("最高回数", f"{max_total}回", f"日付: {max_date}")
            
            st.write("**朝の最高記録**")
            max_morning = df['morning'].max()
            st.metric("最高回数", f"{max_morning}回")
            
        with col2:
            st.write("**最低記録**")
            min_total = df['total'].min()
            min_date = df[df['total'] == min_total]['date'].values[0]
            st.metric("最低回数", f"{min_total}回", f"日付: {min_date}")
            
            st.write("**晩の最高記録**")
            max_evening = df['evening'].max()
            st.metric("最高回数", f"{max_evening}回")
        
        # 週別の集計（オプション）
        st.write("**週別の合計**")
        chart_df = df.copy()
        chart_df['date'] = pd.to_datetime(chart_df['date'])
        chart_df['week'] = chart_df['date'].dt.isocalendar().week
        weekly_total = chart_df.groupby('week')['total'].sum().reset_index()
        weekly_total.columns = ['週', '合計回数']
        st.dataframe(weekly_total, use_container_width=True, hide_index=True)
        
else:
    st.info("📝 サイドバーから記録を入力してください。")
    st.markdown("""
    ### 使い方
    1. 左側のサイドバーで日付を選択
    2. 朝・昼・晩の回数を入力
    3. 「記録を保存」ボタンをクリック
    
    記録を保存すると、ここにグラフや統計情報が表示されます。
    """)

# フッター
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>💪 12月の1ヶ月間、頑張りましょう！</div>",
    unsafe_allow_html=True
)

