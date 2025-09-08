import streamlit as st

st.title("🕌 Kalkulator Zakat - BAZNAS Banyumas")

# Input nama
nama = st.text_input("Siapa namamu?")

# Jika nama sudah diisi, tampilkan sapaan dan form perhitungan
if nama:
    st.write(f"Assalamualaikum kak {nama}!")
    st.write("Aku Raju, Kang Amil dari BAZNAS Kabupaten Banyumas. Salam kenal ya kak. Yuk kita hitung zakatmu! ✨")

    st.write("### Masukkan Penghasilan Bulananmu")
    st.caption("Input nominal penghasilan tanpa titik pemisah ribuan yaa, kak!")

    # Input penghasilan
    a = st.number_input("Penghasilan ke-1", min_value=0, step=1000)
    b = st.number_input("Penghasilan ke-2", min_value=0, step=1000)
    c = st.number_input("Penghasilan ke-3", min_value=0, step=1000)

    # Variabel nishab dan kadar zakat
    nishab = 7140498
    kadar_zakat = 2.5 / 100

    # Tombol hitung
    if st.button("Hitung Zakat"):
        total_penghasilan = a + b + c
        besaran_zakat = total_penghasilan * kadar_zakat
        st.subheader("📊 Hasil Perhitungan")
        st.write(f"*Total Penghasilan:* Rp {total_penghasilan:,}")
        st.write(f"*Besaran Zakat (2.5%):* Rp {besaran_zakat:,.2f}")
        st.write(f"*Nishab Zakat:* Rp {nishab:,}")

        if besaran_zakat >= (nishab * kadar_zakat):
            st.success(f"Alhamdulillah kak {nama}, kamu sudah wajib zakat yaa 🙌")
            st.markdown('[💳 Rekening BAZNAS Banyumas](https://bazn.as/rekeningbms)', unsafe_allow_html=True)
            st.markdown('[🌐 Donasi Digital](https://baznasbanyumas.com)', unsafe_allow_html=True)
        else:
            st.info(f"Kamu belum wajib zakat kak {nama}. Semoga segera ditambah rezekinya yaa. Amiin 🤲")
            st.markdown('[🌐 Website BAZNAS Banyumas](https://baznasbanyumas.com)', unsafe_allow_html=True)
