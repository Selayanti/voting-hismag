import streamlit as st
import os

# ============================================================
# KONFIGURASI - UBAH SESUAI KEBUTUHAN
# ============================================================

# Folder foto kandidat
FOTO_FOLDER = r"D:\COLLEGE\HISMAG\foto kandidat"

# Logo HISMAG
LOGO_PATH = r"D:\COLLEGE\HISMAG\foto kandidat\logo_hismag.png"

KANDIDAT = [
    {"id": "K1",  "nama": "Nama Kandidat 1",  "foto": "kandidat_1"},
    {"id": "K2",  "nama": "Nama Kandidat 2",  "foto": "kandidat_2"},
    {"id": "K3",  "nama": "Nama Kandidat 3",  "foto": "kandidat_3"},
    {"id": "K4",  "nama": "Nama Kandidat 4",  "foto": "kandidat_4"},
    {"id": "K5",  "nama": "Nama Kandidat 5",  "foto": "kandidat_5"},
    {"id": "K6",  "nama": "Nama Kandidat 6",  "foto": "kandidat_6"},
    {"id": "K7",  "nama": "Nama Kandidat 7",  "foto": "kandidat_7"},
    {"id": "K8",  "nama": "Nama Kandidat 8",  "foto": "kandidat_8"},
    {"id": "K9",  "nama": "Nama Kandidat 9",  "foto": "kandidat_9"},
    {"id": "K10", "nama": "Nama Kandidat 10", "foto": "kandidat_10"},
]

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "hismag2026"

# ============================================================
# HELPER
# ============================================================

def get_foto_path(nama_file):
    """Cari foto dengan ekstensi apapun"""
    for ext in ["jpg", "jpeg", "png", "webp", "JPG", "JPEG", "PNG"]:
        path = os.path.join(FOTO_FOLDER, f"{nama_file}.{ext}")
        if os.path.exists(path):
            return path
    return None

def show_logo(width=120):
    """Tampilkan logo HISMAG di tengah, fallback ke emoji kalau tidak ada"""
    if os.path.exists(LOGO_PATH):
        _, c, _ = st.columns([1, 1, 1])
        with c:
            st.image(LOGO_PATH, width=width)
    else:
        st.markdown("<div style='text-align:center;font-size:48px'>🗳️</div>", unsafe_allow_html=True)

def get_nama_kandidat(kid):
    for k in KANDIDAT:
        if k["id"] == kid:
            return k["nama"]
    return "-"

def sudah_vote(username):
    return username in st.session_state.vote_data

def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.is_admin = False
    st.session_state.halaman_auth = "login"
    st.session_state.pilihan_vote = None

# ============================================================
# INISIALISASI SESSION STATE
# ============================================================

defaults = {
    "vote_data": {},       # { username: {kandidat_id, nama_user} }
    "users": {},           # { username: {password, nama} }
    "logged_in": False,
    "current_user": None,
    "is_admin": False,
    "halaman_auth": "login",
    "pilihan_vote": None,
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ============================================================
# HALAMAN SIGN UP
# ============================================================

def halaman_signup():
    show_logo()
    st.markdown("## Pemilihan Ketua HISMAG")
    st.markdown("### Buat Akun Baru")
    st.caption("Daftar terlebih dahulu untuk bisa memberikan suara.")
    st.divider()

    with st.form("form_signup"):
        nama     = st.text_input("Nama Lengkap")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        konfirm  = st.text_input("Konfirmasi Password", type="password")
        submit   = st.form_submit_button("Daftar", use_container_width=True, type="primary")

    if submit:
        if not nama.strip() or not username.strip() or not password:
            st.error("Semua kolom wajib diisi.")
        elif len(password) < 6:
            st.error("Password minimal 6 karakter.")
        elif password != konfirm:
            st.error("Password dan konfirmasi tidak cocok.")
        elif username == ADMIN_USERNAME or username in st.session_state.users:
            st.error("Username sudah digunakan. Coba username lain.")
        else:
            st.session_state.users[username] = {
                "password": password,
                "nama": nama.strip(),
            }
            st.success(f"Akun berhasil dibuat! Silakan login, {nama.strip()}.")
            st.session_state.halaman_auth = "login"
            st.rerun()

    st.divider()
    _, c, _ = st.columns([1, 2, 1])
    with c:
        if st.button("Sudah punya akun? Login di sini", use_container_width=True):
            st.session_state.halaman_auth = "login"
            st.rerun()

# ============================================================
# HALAMAN LOGIN
# ============================================================

# def halaman_login():
#     show_logo()
#     st.markdown("## Pemilihan Ketua HISMAG")
#     st.markdown("### Login")
#     st.caption("Masukkan username dan password kamu.")
#     st.divider()

def halaman_login():
    show_logo()

    # paksa kiri
    st.markdown("<h2 style='text-align: left;'>Pemilihan Ketua HISMAG</h2>", unsafe_allow_html=True)

    # tengah
    st.markdown("<h3 style='text-align: center;'>Login</h3>", unsafe_allow_html=True)
    st.caption("<p style='text-align: center;'>Masukkan username dan password kamu.</p>", unsafe_allow_html=True)

    st.divider()

    with st.form("form_login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit   = st.form_submit_button("Masuk", use_container_width=True, type="primary")

    if submit:
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.logged_in    = True
            st.session_state.is_admin     = True
            st.session_state.current_user = {"username": "admin", "nama": "Admin"}
            st.rerun()
        elif username in st.session_state.users:
            if st.session_state.users[username]["password"] == password:
                st.session_state.logged_in    = True
                st.session_state.is_admin     = False
                st.session_state.current_user = {
                    "username": username,
                    "nama": st.session_state.users[username]["nama"],
                }
                st.rerun()
            else:
                st.error("Password salah.")
        else:
            st.error("Username tidak ditemukan. Silakan daftar dulu.")

    st.divider()
    _, c, _ = st.columns([1, 2, 1])
    with c:
        if st.button("Belum punya akun? Daftar di sini", use_container_width=True):
            st.session_state.halaman_auth = "signup"
            st.rerun()

# ============================================================
# HALAMAN VOTE
# ============================================================

def halaman_vote():
    user     = st.session_state.current_user
    username = user["username"]

    show_logo(width=80)
    st.markdown("## Pemilihan Ketua HISMAG")
    st.caption(f"Login sebagai: **{user['nama']}**")
    st.divider()

    # --- Sudah vote ---
    if sudah_vote(username):
        kid     = st.session_state.vote_data[username]["kandidat_id"]
        nama_k  = get_nama_kandidat(kid)
        st.success(f"✅ Kamu sudah memberikan suara untuk **{nama_k}**. Terima kasih!")
        st.info("Hasil voting akan diumumkan oleh admin.")
        if st.button("Keluar", use_container_width=True):
            logout()
            st.rerun()
        return

    # --- Belum vote ---
    st.markdown("### Pilih satu kandidat ketua")
    st.caption("Klik nama kandidat untuk memilih, lalu tekan **Kirim Suara**.")

    selected     = st.session_state.pilihan_vote
    cols_per_row = 5
    chunks       = [KANDIDAT[i:i+cols_per_row] for i in range(0, len(KANDIDAT), cols_per_row)]

    for chunk in chunks:
        cols = st.columns(cols_per_row)
        for col, k in zip(cols, chunk):
            with col:
                foto = get_foto_path(k["foto"])
                if foto:
                    st.image(foto, width=200)
                else:
                    st.markdown(
                        "<div style='height:130px;background:#eee;border-radius:8px;"
                        "display:flex;align-items:center;justify-content:center;"
                        "color:#aaa;font-size:11px;text-align:center;'>Foto tidak<br>ditemukan</div>",
                        unsafe_allow_html=True,
                    )
                is_sel  = selected == k["id"]
                btn_lbl = f"{'✅ ' if is_sel else ''}{k['nama']}"
                if st.button(btn_lbl, key=f"vote_{k['id']}", use_container_width=True):
                    st.session_state.pilihan_vote = k["id"]
                    st.rerun()

    st.divider()

    if selected:
        st.info(f"Pilihanmu saat ini: **{get_nama_kandidat(selected)}**")

    c1, c2 = st.columns([3, 1])
    with c1:
        kirim = st.button(
            "✅ Kirim Suara",
            use_container_width=True,
            type="primary",
            disabled=(selected is None),
        )
    with c2:
        if st.button("Keluar", use_container_width=True):
            logout()
            st.rerun()

    if kirim:
        st.session_state.vote_data[username] = {
            "kandidat_id": selected,
            "nama_user":   user["nama"],
        }
        st.session_state.pilihan_vote = None
        st.rerun()

# ============================================================
# HALAMAN ADMIN
# ============================================================

def halaman_admin():
    show_logo(width=80)
    st.markdown("## 🔐 Panel Admin — Hasil Voting")
    st.caption("Halaman ini hanya bisa diakses oleh admin.")
    st.divider()

    total_user  = len(st.session_state.users)
    total_masuk = len(st.session_state.vote_data)

    c1, c2, c3 = st.columns(3)
    c1.metric("Akun Terdaftar", total_user)
    c2.metric("Suara Masuk",    total_masuk)
    c3.metric("Belum Memilih",  max(total_user - total_masuk, 0))

    st.divider()

    counts   = {k["id"]: 0 for k in KANDIDAT}
    for v in st.session_state.vote_data.values():
        if v["kandidat_id"] in counts:
            counts[v["kandidat_id"]] += 1
    max_vote = max(counts.values()) if any(counts.values()) else 0

    st.markdown("### 📊 Rekap Suara")
    cols_per_row = 5
    chunks       = [KANDIDAT[i:i+cols_per_row] for i in range(0, len(KANDIDAT), cols_per_row)]

    for chunk in chunks:
        cols = st.columns(cols_per_row)
        for col, k in zip(cols, chunk):
            with col:
                foto = get_foto_path(k["foto"])
                if foto:
                    st.image(foto, width=200)
                c     = counts[k["id"]]
                pct   = round(c / total_masuk * 100) if total_masuk > 0 else 0
                crown = "🏆 " if (c == max_vote and max_vote > 0) else ""
                st.markdown(
                    f"<div style='text-align:center;font-size:13px;font-weight:500'>{crown}{k['nama']}</div>"
                    f"<div style='text-align:center;font-size:12px;color:gray'>{c} suara ({pct}%)</div>",
                    unsafe_allow_html=True,
                )
                st.progress(c / max_vote if max_vote > 0 else 0)

    st.divider()
    st.markdown("### 📋 Daftar Pemilih")

    if not st.session_state.vote_data:
        st.info("Belum ada yang memilih.")
    else:
        tabel = [
            {
                "Nama":     v["nama_user"],
                "Username": uname,
                "Memilih":  get_nama_kandidat(v["kandidat_id"]),
            }
            for uname, v in st.session_state.vote_data.items()
        ]
        st.table(tabel)

    st.divider()
    if st.button("Keluar", use_container_width=True):
        logout()
        st.rerun()

# ============================================================
# ROUTING UTAMA
# ============================================================

st.set_page_config(
    page_title="Voting Ketua HISMAG",
    page_icon=LOGO_PATH,
    layout="wide",
)

if not st.session_state.logged_in:
    _, center, _ = st.columns([1, 2, 1])
    with center:
        if st.session_state.halaman_auth == "signup":
            halaman_signup()
        else:
            halaman_login()
elif st.session_state.is_admin:
    halaman_admin()
else:
    halaman_vote()
