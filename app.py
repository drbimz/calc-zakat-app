import streamlit as st

st.title("🕌 Kalkulator Zakat - BAZNAS Kabupaten Banyumas 🕌")

# Fungsi callback untuk format ribuan otomatis
def format_input(key):
    try:
        val = st.session_state[key]
        val = val.replace(".", "").replace(",", "")
        val = int(val)
        st.session_state[key] = f"{val:,}".replace(",", ".")
    except:
        st.session_state[key] = "0"

# Input nama
nama = st.text_input("Siapa namamu?")

if nama:
    st.write(f"Assalamualaikum kak {nama}!")
    st.write("Aku Raju, Kang Amil dari BAZNAS Kabupaten Banyumas. Salam kenal ya kak. Ini adalah mini aplikasi resmi milik BAZNAS Kabupaten Banyumas untuk hitung cepat zakat. Yuk kita mulai hitung zakatmu! ✨")

    st.write("### Masukkan Penghasilan Bulananmu")
    st.caption("Ketik nominal penghasilan, otomatis akan diformat dengan titik pemisah ribuan ya kak!")

    # Input dengan auto-format ribuan
    st.text_input("Penghasilan ke-1", "0", key="a", on_change=format_input, args=("a",))
    st.text_input("Penghasilan ke-2", "0", key="b", on_change=format_input, args=("b",))
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
