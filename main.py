import streamlit as st
import pandas as pd

st.set_page_config(page_title="紙タオル ランニングコスト比較", layout="centered")

st.title("🧻 紙タオル ランニングコスト比較アプリ（製品選択版）")

st.markdown("""
このアプリでは、新エルナと比較対象製品を選択して、使用枚数と価格から
1人あたりのコストおよび月間コストを比較できます。

※ 製品ごとのパック枚数・入数も反映しています
""")

# 製品情報（辞書）
products = {
    "旧エルナ（エシュット）": {
        "daily_usage": 8.25,
        "pack_size": 200,
        "default_price_per_pack": 72,
        "packs_per_case": 35
    },
    "26gパルプ品": {
        "daily_usage": 12.53,
        "pack_size": 200,
        "default_price_per_pack": 62,
        "packs_per_case": 40
    },
    "新エルナ": {
        "daily_usage": 6.71,
        "pack_size": 200,
        "default_price_per_pack": 79,
        "packs_per_case": 35
    }
}

with st.sidebar:
    st.header("📋 比較製品を選択")
    target_product = st.selectbox("比較対象製品を選んでください", ["旧エルナ（エシュット）", "26gパルプ品"])
    monthly_cases = st.number_input("現在の出荷ケース数（月間）", value=50)
    st.markdown("### 単価入力（200枚あたり）")
    new_price_per_pack = st.number_input("新エルナ 単価", value=products["新エルナ"]["default_price_per_pack"])
    target_price_per_pack = st.number_input(f"{target_product} 単価", value=products[target_product]["default_price_per_pack"])

# 対象と比較元のデータ取得
new_product = products["新エルナ"].copy()
target = products[target_product].copy()

# 入力価格で上書き
new_product["price_per_pack"] = new_price_per_pack
target["price_per_pack"] = target_price_per_pack

# 単価と1人1日コスト
def calculate_cost(product):
    unit_price = product["price_per_pack"] / product["pack_size"]
    daily_cost = product["daily_usage"] * unit_price
    case_price = product["price_per_pack"] * product["packs_per_case"]
    return unit_price, daily_cost, case_price

new_unit, new_daily, new_case = calculate_cost(new_product)
target_unit, target_daily, target_case = calculate_cost(target)

# 月間コスト
new_required_cases = monthly_cases * (new_product["daily_usage"] / target["daily_usage"])
new_monthly_cost = new_required_cases * new_case
target_monthly_cost = monthly_cases * target_case

# 表示
st.subheader("📊 1人1日あたりのコスト")
st.table(pd.DataFrame({
    "製品": ["新エルナ", target_product],
    "使用枚数": [new_product["daily_usage"], target["daily_usage"]],
    "単価（◯枚）": [new_product["price_per_pack"], target["price_per_pack"]],
    "枚数/パック": [new_product["pack_size"], target["pack_size"]],
    "1人1日コスト (円)": [round(new_daily, 2), round(target_daily, 2)]
}))

st.subheader("📦 月間コスト比較")
st.write(f"{target_product}：{monthly_cases:.2f}ケース × {target_case:.0f}円 = {target_monthly_cost:.0f}円")
st.write(f"新エルナ：約{new_required_cases:.2f}ケース × {new_case:.0f}円 = {new_monthly_cost:.0f}円")

diff = target_monthly_cost - new_monthly_cost
rate = (diff / target_monthly_cost) * 100

st.success(f"差額：{diff:.0f}円（約{rate:.1f}% 削減）")

if diff > 0:
    st.markdown("✅ **新エルナはコスト削減につながります。**")
else:
    st.markdown("⚠️ **新エルナはコスト増加となっています。使用条件をご確認ください。**")

st.caption("ver 2.1 - 製品比較＆単価入力対応版")
