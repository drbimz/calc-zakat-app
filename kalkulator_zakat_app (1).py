import streamlit as st

# ================= CONFIG =================
st.set_page_config(page_title="Kalkulator Zakat BAZNAS Banyumas", page_icon="🕌")

# ================ UTIL ====================
def fmt_rp_int(n: int) -> str:
    """Format Rupiah untuk bilangan bulat (titik ribuan)."""
    return f"Rp {n:,}".replace(",", ".")

def fmt_rp_smart(x: float) -> str:
    """Format Rupiah pintar:
       - jika nilainya bulat -> tanpa desimal
       - jika ada pecahan   -> 2 desimal dengan format Indonesia (.,)
    """
    # toleransi untuk error floating point
    if abs(x - round(x)) < 1e-9:
        return fmt_rp_int(int(round(x)))
    # format US: 1,234,567.89  -> ubah ke ID: 1.234.567,89
    s = f"{x:,.2f}"
    s = s.replace(",", "_").replace(".", ",").replace("_", ".")
    return f"Rp {s}"

# ============ SESSION DEFAULTS ============
if "lanjut" not in st.session_state:
    st.session_state.lanjut = False
if "has_extra" not in st.session_state:
    st.session_state.has_extra = True            # ✅ default: toggle aktif
if "extra_count" not in st.session_state:
    st.session_state.extra_count = 1             # ✅ default: 1 baris tambahan
if "extra_vals" not in st.session_state:
    st.session_state.extra_vals = {"extra_1": 0} # ✅ siapkan nilai awal

# ================ HEADER ==================
st.title("🕌 Kalkulator Zakat — BAZNAS Kabupaten Banyumas")
st.caption("Mini aplikasi resmi untuk **hitung cepat zakat**. Mudah, aman, dan ramah digunakan.")

# ============ LANGKAH 1: NAMA ============
nama = st.text_input("Siapa namamu?", placeholder="contoh: Abdullah")

cols = st.columns([1, 1, 1])
with cols[1]:
    if st.button("Lanjutkan ➡️", use_container_width=True, disabled=not bool(nama)):
        st.session_state.lanjut = True

# Reset jika nama dihapus
if not nama:
    st.session_state.lanjut = False

# ======= LANGKAH 2: INPUT PENGHASILAN =======
if st.session_state.lanjut:
    st.success(
        f"👋 Assalamualaikum kak **{nama}**!\n\n"
        "Aku Raju, Kang Amil dari BAZNAS Kabupaten Banyumas. Senang bisa bantu kakak "
        "menghitung zakat dengan cepat dan tepat. Yuk mulai ya! ✨"
    )

    st.subheader("1) Masukkan Penghasilan Bulanan")
    st.caption("Isi nominal penghasilan (jika tidak ada, isi **0**).")

    # ---- Pertanyaan penghasilan tambahan (default: ON) ----
    st.session_state.has_extra = st.toggle(
        "Apakah ada **penghasilan tambahan**?",
        value=st.session_state.has_extra,
        help="Contoh: bonus proyek, freelance, komisi, dll."
    )

    # Jika toggle dinyalakan tapi belum ada baris, buat 1 baris default
    if st.session_state.has_extra and st.session_state.extra_count == 0:
        st.session_state.extra_count = 1
        st.session_state.extra_vals["extra_1"] = st.session_state.extra_vals.get("extra_1", 0)

    # Tombol tambah/hapus baris
    act_col1, act_col2, _ = st.columns([1, 1, 4])
    with act_col1:
        add_clicked = st.button("➕ Tambah baris", disabled=not st.session_state.has_extra)
    with act_col2:
        remove_clicked = st.button(
            "➖ Hapus terakhir",
            disabled=not (st.session_state.has_extra and st.session_state.extra_count > 1)
        )

    if add_clicked and st.session_state.has_extra:
        st.session_state.extra_count += 1
        key = f"extra_{st.session_state.extra_count}"
        st.session_state.extra_vals.setdefault(key, 0)
        st.rerun()

    if remove_clicked and st.session_state.has_extra and st.session_state.extra_count > 1:
        key = f"extra_{st.session_state.extra_count}"
        st.session_state.extra_vals.pop(key, None)
        st.session_state.extra_count -= 1
        st.rerun()

    # ---------------- FORM ----------------
    with st.form("form_penghasilan", clear_on_submit=False):
        # Penghasilan pokok
        pokok = st.number_input(
            "Penghasilan Pokok (gaji utama/rutin)",
            min_value=0, step=1000, key="pokok", help="Gaji bulanan / penghasilan rutin"
        )
        st.caption(f"➡️ {fmt_rp_int(pokok)}")

        # Daftar penghasilan tambahan dinamis
        total_tambahan = 0
        if st.session_state.has_extra:
            st.markdown("**Penghasilan Tambahan**")
            cols_extra = st.columns(2)
            for i in range(1, st.session_state.extra_count + 1):
                key = f"extra_{i}"
                col = cols_extra[(i - 1) % 2]
                with col:
                    st.session_state.extra_vals[key] = st.number_input(
                        f"Tambahan #{i}",
                        min_value=0, step=1000, key=key,
                        help="Bonus/proyek/komisi/lainnya"
                    )
                    st.caption(f"➡️ {fmt_rp_int(st.session_state.extra_vals[key])}")
                    total_tambahan += st.session_state.extra_vals[key]
        else:
            total_tambahan = 0

        # Tombol submit
        hitung = st.form_submit_button("Hitung Zakat 🧮", use_container_width=True)

    # --------- PARAMETER (sesuaikan berkala) ----------
    nishab = 7_140_498          # ≈ 85 gram emas (update berkala sesuai harga emas)
    kadar_zakat = 2.5 / 100     # 2.5%

    # --------------- HASIL -----------------
    if hitung:
        total = pokok + total_tambahan
        zakat = total * kadar_zakat

        st.subheader("2) Ringkasan Hasil")
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Penghasilan", fmt_rp_int(total))
        m2.metric("Zakat 2.5%", fmt_rp_smart(zakat))   # ✅ tanpa .00 jika bulat
        m3.metric("Nishab", fmt_rp_int(nishab))

        if total >= nishab:
            st.success(
                f"✅ Alhamdulillah kak **{nama}**, kamu **sudah wajib zakat** 🙌\n\n"
                "Silakan tunaikan zakat melalui kanal berikut:"
            )
            st.markdown("[💳 Rekening BAZNAS Banyumas](https://bazn.as/rekeningbms)")
            st.markdown("[🌐 Donasi Digital](https://baznasbanyumas.com)")
        else:
            st.info(
                f"ℹ️ Kak **{nama}**, kamu **belum wajib zakat** karena total penghasilan **di bawah nishab**.\n\n"
                "Semoga Allah segera melapangkan rezekinya. Aamiin 🤲"
            )
            st.markdown("[🌐 Website BAZNAS Banyumas](https://baznasbanyumas.com)")

        with st.expander("Bagaimana perhitungannya?"):
            st.write(
                f"- **Kadar zakat**: {kadar_zakat*100:.1f}% dari total penghasilan.\n"
                f"- **Nishab**: batas minimal penghasilan untuk wajib zakat (saat ini {fmt_rp_int(nishab)}).\n"
                "- Jika total penghasilan ≥ nishab → **wajib zakat**; jika belum mencapai → **tidak wajib**."
            )

        st.warning("Tips: perbarui **nilai nishab** mengikuti harga emas terkini agar perhitungan selalu akurat.")

        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔄 Hitung Ulang", use_container_width=True):
                for k in list(st.session_state.keys()):
                    if k not in ("lanjut", "has_extra", "extra_count", "extra_vals"):
                        del st.session_state[k]
                st.rerun()
        with c2:
            if st.button("⬅️ Ganti Nama", use_container_width=True):
                st.session_state.lanjut = False
                st.rerun()
