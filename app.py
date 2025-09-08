import streamlit as st

st.set_page_config(page_title="Kalkulator Zakat - BAZNAS Banyumas", page_icon="🕌")

# Inject CSS biar bubble chat warna branding
st.markdown("""
    <style>
    /* Bubble user */
    .stChatMessage.user {
        background-color: #f1f1f1;
        color: black;
        border-radius: 20px;
        padding: 10px 15px;
        margin: 5px 0;
    }
    /* Bubble assistant (Raju) */
    .stChatMessage.assistant {
        background-color: #259148;
        color: white;
        border-radius: 20px;
        padding: 10px 15px;
        margin: 5px 0;
    }
    /* Biar font lebih rapih */
    .stChatMessage p {
        margin: 0;
    }
    </style>
""", unsafe_allow_html=True)

# Fungsi callback untuk format ribuan otomatis
def format_input(key):
    try:
        val = st.session_state[key]
        val = val.replace(".", "").replace(",", "")
        val = int(val)
        st.session_state[key] = f"{val:,}".replace(",", ".")
    except:
        st.session_state[key] = "0"

# Judul aplikasi
st.title("🕌 Kalkulator Zakat - BAZNAS Kabupaten Banyumas 🕌")

# Input nama
with st.chat_message("assistant"):
    st.write("Halo kak, boleh kenalan dulu? Siapa namamu?")

nama = st.text_input("Ketik namamu di sini...")

if nama:
    with st.chat_message("user"):
        st.write(nama)

    with st.chat_message("assistant"):
        st.write(f"Assalamualaikum kak {nama}!")
        st.write("Aku Raju, Kang Amil dari BAZNAS Kabupaten Banyumas. Salam kenal ya kak. Ini adalah mini aplikasi resmi milik BAZNAS Kabupaten Banyumas untuk hitung cepat zakat. Yuk kita mulai hitung zakatmu! ✨")

    with st.chat_message("assistant"):
        st.write("### Masukkan Penghasilan Bulananmu")
        st.caption("Ketik nominal penghasilan, otomatis akan diformat dengan titik pemisah ribuan ya kak!")

    # Input dengan auto-format ribuan
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("Penghasilan ke-1", "0", key="a", on_change=format_input, args=("a",))
    with col2:
        st.text_input("Penghasilan ke-2", "0", key="b", on_change=format_input, args=("b",))
    with col3:
        st.text_input("Penghasilan ke-3", "0", key="c", on_change=format_input, args=("c",))

    # Ambil nilai numerik
    def to_int(val):
        try:
            return int(val.replace(".", "").replace(",", ""))
        except:
            return 0

    a = to_int(st.session_state["a"])
    b = to_int(st.session_state["b"])
    c = to_int(st.session_state["c"])

    # Variabel nishab dan kadar zakat
    nishab = 7140498
    kadar_zakat = 2.5 / 100

    # Tombol hitung
    if st.button("Hitung Zakat"):
        total_penghasilan = a + b + c
        besaran_zakat = total_penghasilan * kadar_zakat

        with st.chat_message("assistant"):
            st.subheader("📊 Hasil Perhitungan")
            st.write(f"Total Penghasilan: Rp {total_penghasilan:,}".replace(",", "."))
            st.write(f"Besaran Zakat (2.5%): Rp {besaran_zakat:,.2f}".replace(",", "."))
            st.write(f"Nishab Zakat: Rp {nishab:,}".replace(",", "."))

            if total_penghasilan >= nishab:
                st.success(f"Alhamdulillah kak {nama}, kamu sudah wajib zakat yaa. Mau transfer atau lewat digital, kini sudah lebih mudah. Tinggal klik link di bawah ini aja 🙌")
                st.markdown('[💳 Rekening BAZNAS Banyumas](https://bazn.as/rekeningbms)', unsafe_allow_html=True)
                st.markdown('[🌐 Donasi Digital](https://baznasbanyumas.com)', unsafe_allow_html=True)
            else:
                st.info(f"Kamu belum wajib zakat kak {nama}. Semoga segera Allah tambah rezekinya yaa. Amiin 🤲")
                st.markdown('[🌐 Website BAZNAS Banyumas](https://baznasbanyumas.com)', unsafe_allow_html=True)
