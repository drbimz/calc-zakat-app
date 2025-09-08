import streamlit as st

st.title("🕌 Kalkulator Zakat - BAZNAS Kabupaten Banyumas 🕌")

# Input nama
nama = st.text_input("Siapa namamu?")

# Fungsi bantu: input dengan auto-format ribuan
def input_uang(label, key):
    raw = st.text_input(label, "0", key=key)
    try:
        # Bersihkan karakter non-angka
        val = int(raw.replace(".", "").replace(",", ""))
    except:
        val = 0
    # Format ulang dengan titik ribuan
    formatted = f"{val:,}".replace(",", ".")
    # Update input box agar selalu terformat
    st.session_state[key] = formatted
    return val

# Jika nama sudah diisi, tampilkan sapaan dan form perhitungan
if nama:
    st.write(f"Assalamualaikum kak {nama}!")
    st.write("Aku Raju, Kang Amil dari BAZNAS Kabupaten Banyumas. Salam kenal ya kak. Ini adalah mini aplikasi resmi milik BAZNAS Kabupaten Banyumas untuk hitung cepat zakat. Yuk kita hitung zakatmu! ✨")

    st.write("### Masukkan Penghasilan Bulananmu")
    st.caption("Ketik nominal penghasilan, otomatis akan ada titik pemisah ribuan ya kak!")

    # Input penghasilan dengan auto-format
    a = input_uang("Penghasilan ke-1", "a")
    b = input_uang("Penghasilan ke-2", "b")
    c = input_uang("Penghasilan ke-3", "c")

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
            st.success(f"Alhamdulillah kak {nama}, kamu sudah wajib zakat yaa. Mau transfer atau lewat digital, kini lebih mudah. Tinggal klik link di bawah ini yaa 🙌")
            st.markdown('[💳 Rekening BAZNAS Banyumas](https://bazn.as/rekeningbms)', unsafe_allow_html=True)
            st.markdown('[🌐 Donasi Digital](https://baznasbanyumas.com)', unsafe_allow_html=True)
        else:
            st.info(f"Kamu belum wajib zakat kak {nama}. Semoga segera ditambah rezekinya yaa. Amiin 🤲")
            st.markdown('[🌐 Website BAZNAS Banyumas](https://baznasbanyumas.com)', unsafe_allow_html=True)
