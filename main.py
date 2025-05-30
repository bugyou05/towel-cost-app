import streamlit as st
import pandas as pd

st.set_page_config(page_title="紙タオル ランニングコスト比較", layout="centered")

st.title("🧻 紙タオル ランニングコスト比較アプリ")

st.markdown("""
このアプリでは、旧製品と新製品の紙タオルについて、使用枚数と価格から1人あたりのコストおよび月間コストを比較できます。

※ 200枚入パック×35パック＝1ケース で計算します
""")

with st.sidebar:
    st.header("📋 入力欄")

    old_usage = st.number_input("旧製品の1人1日使用枚数", value=8.25)
    new_usage = st.number_input("新製品の1人1日使用枚数", value=6.71)

    old_price_per_200 = st.number_input("旧製品の価格（200枚）", value=72)
    new_price_per_200 = st.number_input("新製品の価格（200枚）", value=79)

    monthly_cases = st.number_input("現在の出荷ケース数（月間）", value=50)

# 計算処理
old_unit_price = old_price_per_200 / 200
new_unit_price = new_price_per_200 / 200

old_daily_cost = old_usage * old_unit_price
new_daily_cost = new_usage * new_unit_price

old_case_price = old_price_per_200 * 35
new_case_price = new_price_per_200 * 35

old_monthly_cost = old_case_price * monthly_cases
usage_ratio = new_usage / old_usage
new_required_cases = monthly_cases * usage_ratio
new_monthly_cost = new_case_price * new_required_cases

# 結果表示
st.subheader("📊 1人1日あたりのコスト")
st.table(pd.DataFrame({
    "製品": ["旧製品", "新製品"],
    "使用枚数": [old_usage, new_usage],
    "単価（200枚）": [old_price_per_200, new_price_per_200],
    "1人1日コスト (円)": [round(old_daily_cost, 2), round(new_daily_cost, 2)]
}))

st.subheader("📦 月間コスト比較（35パック/ケース）")
st.write(f"旧製品：{monthly_cases}ケース × {old_case_price:.0f}円 = {old_monthly_cost:.0f}円")
st.write(f"新製品：約{new_required_cases:.2f}ケース × {new_case_price:.0f}円 = {new_monthly_cost:.0f}円")

cost_diff = old_monthly_cost - new_monthly_cost
rate = (new_monthly_cost / old_monthly_cost - 1) * 100

st.success(f"差額：{cost_diff:.0f}円（{rate:.1f}%）")

if cost_diff > 0:
    st.markdown("✅ **新製品はコスト削減につながります。**")
else:
    st.markdown("⚠️ **新製品はコスト増加となっています。使用条件をご確認ください。**")

st.caption("ver 1.0 - 作成協力：ChatGPT")