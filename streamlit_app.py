import streamlit as st
import pandas as pd
import sqlite3

# === Настройки страницы ===
st.set_page_config(page_title="AI-Ticket Manager", layout="wide")

st.title("📬 AI Система Тикетов für IT Support")
st.markdown("Просмотр и управление тикетами из электронной почты.")

# === Загрузка базы данных ===
DB_PATH = "tickets.db"

@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM requests ORDER BY datetime DESC", conn)
    conn.close()
    return df

df = load_data()

# === Фильтры ===
with st.sidebar:
    st.header("🔎 Фильтры")
    status_filter = st.multiselect("Статус", options=df["status"].unique(), default=list(df["status"].unique()))
    category_filter = st.multiselect("Категория", options=df["category"].unique(), default=list(df["category"].unique()))
    priority_filter = st.multiselect("Приоритет", options=df["priority"].unique(), default=list(df["priority"].unique()))
    client_filter = st.multiselect("Клиент", options=df["client"].unique(), default=list(df["client"].unique()))

# === Применение фильтров ===
filtered_df = df[
    (df["status"].isin(status_filter)) &
    (df["category"].isin(category_filter)) &
    (df["priority"].isin(priority_filter)) &
    (df["client"].isin(client_filter))
]

st.success(f"Найдено {len(filtered_df)} тикетов")

# === Таблица ===
st.dataframe(filtered_df, use_container_width=True)

# === Экспорт ===
st.download_button("💾 Скачать как CSV", filtered_df.to_csv(index=False), file_name="filtered_tickets.csv", mime="text/csv")