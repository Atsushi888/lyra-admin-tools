import streamlit as st

# まずはHasherを試す。使えなければNoneにしてフォールバック。
try:
    from streamlit_authenticator import Hasher  # 0.3系想定API
except Exception:
    Hasher = None

import bcrypt


def hash_passwords(passwords: list[str]) -> list[str]:
    """
    可能なら streamlit-authenticator の Hasher を使い、
    失敗したら bcrypt 直叩きにフォールバックする安全版。
    """
    # Hasherが生きていればまず試す
    if Hasher is not None:
        try:
            return Hasher(passwords).generate()
        except Exception:
            pass

    # フォールバック: bcryptで生成（utf-8文字列にデコードして返す）
    out = []
    for p in passwords:
        p = (p or "").strip()
        if not p:
            raise ValueError("空のパスワードが含まれています。")
        out.append(bcrypt.hashpw(p.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"))
    return out


st.set_page_config(page_title="Lyra Admin Tools", layout="centered")
st.title("🔐 Lyra System – パスワードハッシュ生成ツール")
st.caption("このツールは Lyra System の管理者専用ユーティリティです。")

tab1, tab2 = st.tabs(["単発入力", "複数まとめて"])

with tab1:
    pwd = st.text_input("パスワードを入力（非表示）", type="password")
    if st.button("ハッシュ生成", key="single_btn"):
        try:
            if not (pwd or "").strip():
                st.warning("パスワードが空です。")
            else:
                hashed = hash_passwords([pwd.strip()])[0]
                st.success("生成完了！")
                st.code(hashed, language="text")
        except Exception as e:
            st.error(f"エラー: {e!s}")

with tab2:
    multi = st.text_area("複数入力（改行区切り）", height=200,
                         placeholder="一行にひとつずつパスワードを入力")
    if st.button("ハッシュ生成", key="multi_btn"):
        try:
            pwds = [line.strip() for line in (multi or "").splitlines() if line.strip()]
            if not pwds:
                st.warning("有効なパスワードが入力されていません。")
            else:
                hashed_list = hash_passwords(pwds)
                st.success(f"{len(hashed_list)} 件 生成しました。")
                for i, h in enumerate(hashed_list, 1):
                    with st.expander(f"#{i}", expanded=False):
                        st.code(h, language="text")
        except Exception as e:
            st.error(f"エラー: {e!s}")

st.divider()
st.caption("生成結果は `secrets.toml` もしくは `config.yaml` の "
           "`credentials.usernames.<id>.password` に貼り付けてください。")
