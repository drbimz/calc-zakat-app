import streamlit as st

# === CSS Styling ===
st.markdown(
    """
    <style>
    /* Background */
    .main {
        background-color: #f5f7f5;
    }
    /* Chat container */
    .chat-bubble {
        display: flex;
        align-items: flex-start;
        margin-bottom: 12px;
    }
    .chat-avatar {
        width: 42px;
        height: 42px;
        border-radius: 50%;
        margin-right: 10px;
        object-fit: cover;
        border: 2px solid #259148;
    }
    .chat-message {
        background-color: #ffffff;
        padding: 12px 16px;
        border-radius: 14px;
        max-width: 80%;
        font-size: 15px;
        border: 1px solid #e0e0e0;
        line-height: 1.4;
    }
    .chat-message.bot {
        background-color: #eaf5ee;
        border: 1px solid #259148;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# === Judul ===
st.markdown("<h2 style='text-align: center; color:#259148'>🕌 Kalkulator Zakat - BAZNAS Kabupaten Banyumas 🕌</h2>", unsafe_allow_html=True)

# === Fungsi Format Ribuan ===
def format_input(key):
    try:
        val = st.session_state[key]
        val = val.replace(".", "").replace(",", "")
        val = int(val)
        st.session_state[key] = f"{val:,}".replace(",", ".")
    except:
        st.session_state[key] = "0"

# === Input Nama ===
nama = st.text_input("Siapa namamu?")

if nama:
    # Chat intro
    st.markdown(
        f"""
        <div class="chat-bubble">
            <img src="BAZNAS_BANYUMAS.png" class="chat-avatar"/>
            <div class="chat-message bot">
                Assalamualaikum kak {nama}!<br>
                Aku Raju, Kang Amil dari BAZNAS Kabupaten Banyumas. Salam kenal ya kak. 
                Ini adalah mini aplikasi resmi milik BAZNAS Kabupaten Banyumas untuk hitung cepat zakat. 
                Yuk kita mulai hitung zakatmu! ✨
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Input Penghasilan
    st.write("### Masukkan Penghasilan Bulananmu")
    st.caption("Ketik nominal penghasilan, otomatis akan diformat dengan titik pemisah ribuan ya kak!")

    st.text_input("Penghasilan ke-1", "0", key="a", on_change=format_input, args=("a",))
    st.text_input("Penghasilan ke-2", "0", key="b", on_change=format_input, args=("b",))
    st.text_input("Penghasilan ke-3", "0", key="c", on_change=format_input, args=("c",))

    def to_int(val):
        try:
            return int(val.replace(".", "").replace(",", ""))
        except:
            return 0

    a = to_int(st.session_state["a"])
    b = to_int(st.session_state["b"])
    c = to_int(st.session_state["c"])

    # Variabel zakat
    nishab = 7140498
    kadar_zakat = 2.5 / 100

    # Tombol hitung
    if st.button("Hitung Zakat"):
        total_penghasilan = a + b + c
        besaran_zakat = total_penghasilan * kadar_zakat

        # Chat hasil
        st.markdown(
            f"""
            <div class="chat-bubble">
                <img src="BAZNAS_BANYUMAS.png" class="chat-avatar"/>
                <div class="chat-message bot">
                    📊 <b>Hasil Perhitungan</b><br><br>
                    Total Penghasilan: Rp {total_penghasilan:,}".replace(",", ".") <br>
                    Besaran Zakat (2.5%): Rp {besaran_zakat:,.2f}".replace(",", ".") <br>
                    Nishab Zakat: Rp {nishab:,}".replace(",", ".")
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if total_penghasilan >= nishab:
            st.success(f"Alhamdulillah kak {nama}, kamu sudah wajib zakat yaa. 🙌")
            st.markdown('[💳 Rekening BAZNAS Banyumas](https://bazn.as/rekeningbms)', unsafe_allow_html=True)
            st.markdown('[🌐 Donasi Digital](https://baznasbanyumas.com)', unsafe_allow_html=True)
        else:
            st.info(f"Kamu belum wajib zakat kak {nama}. Semoga Allah tambah rezekinya yaa 🤲")
            st.markdown('[🌐 Website BAZNAS Banyumas](https://baznasbanyumas.com)', unsafe_allow_html=True)
