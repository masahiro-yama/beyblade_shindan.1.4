import streamlit as st
import random

# ------------------------
# 初期化
# ------------------------
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = []
    st.session_state.questions = []

# ------------------------
# 質問データ
# ------------------------
base_questions = [
    ("やすみじかん、なにしてる？", [
        "A はしりまわってあそぶ",
        "B みんなのようすを見てうごく",
        "C すわってしずかにあそぶ",
        "D きぶんであそびかえる"
    ]),
    ("ともだちとけんかしたら？", [
        "A すぐいいかえす",
        "B いちどきいてからはなす",
        "C あまり気にしない",
        "D あいてにあわせてかえる"
    ]),
    ("ゲームでだいじなのは？", [
        "A はやくかつこと",
        "B まけないこと",
        "C ながくつづけること",
        "D あいてにあわせること"
    ]),
    ("しゅくだいはどうする？", [
        "A いっきにおわらせる",
        "B ていねいにやる",
        "C すこしずつやる",
        "D きぶんでやりかたをかえる"
    ]),
    ("あたらしいあそびをするときは？", [
        "A すぐやってみる",
        "B ルールを見てからやる",
        "C ゆっくりなれる",
        "D みんなにあわせる"
    ]),
]

extra_questions = [
    ("ヒーローになるなら？", [
        "A こうげきでたたかう",
        "B まもりながらたたかう",
        "C ずっとがんばる",
        "D なんでもできる"
    ]),
    ("すきなどうぶつは？", [
        "A ライオン",
        "B ゾウ",
        "C カメ",
        "D サル"
    ]),
    ("ふしぎなちからをみにつけるなら？", [
        "A いっしゅんでパワーアップ",
        "B なんでもまもるバリアー",
        "C どんなダメージもすぐにかいふく",
        "D あいてにあわせていろんなちからがつかえる"
    ]),
]

def generate_questions():
    q = base_questions.copy()
    q.append(random.choice(extra_questions))
    random.shuffle(q)
    return q

# ------------------------
# 判定（同点対策あり）
# ------------------------
def get_result(answers):
    count = {"A":0, "B":0, "C":0, "D":0}
    for a in answers:
        count[a] += 1

    max_score = max(count.values())
    top = [k for k, v in count.items() if v == max_score]

    if len(top) > 1:
        return "バランス"

    return {
        "A": "アタック",
        "B": "ディフェンス",
        "C": "スタミナ",
        "D": "バランス"
    }[top[0]]

# ------------------------
# トップ画面
# ------------------------
if st.session_state.step == 0:
    st.title("🌀 ベイブレードしんだん")
    st.write("キミにぴったりのタイプをみつけよう！")

    if st.button("▶ スタート！"):
        st.session_state.questions = generate_questions()
        st.session_state.answers = []
        st.session_state.step = 1
        st.rerun()

# ------------------------
# 質問画面
# ------------------------
elif st.session_state.step <= len(st.session_state.questions):

    q_index = st.session_state.step - 1
    question, options = st.session_state.questions[q_index]

    st.write(f"Q{st.session_state.step}")
    st.subheader(question)

    selected = st.radio(
        "えらんでね！",
        options,
        index=None,
        key=f"q_{q_index}"
    )

    if selected is not None:
        st.session_state.answers.append(selected[0])
        st.session_state.step += 1
        st.rerun()

# ------------------------
# 結果画面（リンクあり）
# ------------------------
else:
    result = get_result(st.session_state.answers)

    st.title("🎉 けっか！")

    if result == "アタック":
        st.header("💥 アタックタイプ！")
        st.write("ドカンと決める！はやくうごいて勝つ！")

        st.image("https://m.media-amazon.com/images/I/61MpAh-qOsL._AC_SY450_.jpg", width=200)
        st.link_button("👉 これほしい！", "https://www.amazon.co.jp/dp/B0C52R16P1")

    elif result == "ディフェンス":
        st.header("🛡 ディフェンスタイプ！")
        st.write("まもってチャンス！")

        st.image("https://m.media-amazon.com/images/I/61N7ksTpjhL._AC_SY450_.jpg", width=200)
        st.link_button("👉 これほしい！", "https://www.amazon.co.jp/dp/B0GMDYS21K")

    elif result == "スタミナ":
        st.header("🔄 スタミナタイプ！")
        st.write("ながくがんばる！")

        st.image("https://m.media-amazon.com/images/I/61qO6OBNzBL._AC_SY450_.jpg", width=200)
        st.link_button("👉 これほしい！", "https://www.amazon.co.jp/dp/B0DWSRHP7J")

    else:
        st.header("⚡ バランスタイプ！")
        st.write("なんでもできる！")

        st.image("https://m.media-amazon.com/images/I/61WEAT7WNKL._AC_SY450_.jpg", width=200)
        st.link_button("👉 これほしい！", "https://www.amazon.co.jp/dp/B0FV6Y4MH4")

    st.divider()

    if st.button("🔁 もういちどやる"):
        st.session_state.step = 0
        st.rerun()