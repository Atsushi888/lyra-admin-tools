import streamlit as st
from streamlit_authenticator import Hasher

st.set_page_config(page_title="Lyra Admin Tools", layout="centered")
st.title("🔐 Lyra System – パスワードハッシュ生成ツール")

st.caption("このツールは Lyra System の管理者専用ユーティリティです。")

tab1, tab2 = st.tabs(["単発入力", "複数まとめて"])

with tab1:
    pwd = st.text_input("パスワードを入力（非表示）", type="password")
    if st.button("ハッシュ生成", key="single_btn"):
        if not pwd.strip():
            st.warning("パスワードが空です。")
        else:
            hashed = Hasher([pwd.strip()]).generate()[0]
            st.success("生成完了！")
            st.code(hashed, language="text")

with tab2:
    multi = st.text_area("複数入力（改行区切り）", height=200)
    if st.button("ハッシュ生成", key="multi_btn"):
        pwds = [line.strip() for line in multi.splitlines() if line.strip()]
        if not pwds:
            st.warning("有効なパスワードが入力されていません。")
        else:
            hashed_list = Hasher(pwds).generate()
            st.success(f"{len(hashed_list)} 件 生成しました。")
            for i, h in enumerate(hashed_list, 1):
                with st.expander(f"#{i}", expanded=False):
                    st.code(h, language="text")

st.divider()
st.caption("生成結果は secrets.toml または config.yaml の `credentials.usernames.*.password` に貼り付けてください。")
