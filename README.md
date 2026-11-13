# PWEB-CRUD | RuangSiswa

Aplikasi CRUD pendaftaran siswa baru dengan PHP, PDO, HTML, CSS, dan MySQL untuk tugas Pemrograman Web.

- Demo: https://pweb-crud.vercel.app
- Artikel: https://pweb-crud.vercel.app/blog.php
- GitHub: https://github.com/Boyeep/PWEB-CRUD
- [HTML Blogger](docs/blogspot.html) dan [petunjuk artikel](docs/BLOGSPOT.md)
- [Pemetaan tugas](docs/CHECKLIST.md) dan [deployment](docs/DEPLOYMENT.md)
- [Materi tugas](https://fajarbaskoro.blogspot.com/2022/11/crud-2-pendaftaran-siswa-baru.html)

## Fitur

Ringkasan jumlah pendaftar, tambah, daftar, detail, edit, dan hapus dengan konfirmasi. Pencarian nama/sekolah, filter jenis kelamin, paginasi delapan baris, validasi server, pesan kesalahan per kolom, token CSRF, prepared statements, dan escaping HTML.

Lima isian mengikuti tugas: nama, alamat, jenis_kelamin, agama, sekolah_asal. Skema menambahkan workspace_id dan created_at untuk pemisahan demo dan waktu pendaftaran. Enam data fiktif disiapkan pada ruang baru. Maksimum 100 siswa per ruang; data contoh tidak kembali setelah dihapus.

## Menjalankan lokal

PHP 8.2+ dengan PDO, pdo_sqlite, dan mbstring. Gunakan pdo_mysql untuk mode MySQL.

```sh
git clone https://github.com/Boyeep/PWEB-CRUD.git
cd PWEB-CRUD
php -S localhost:8000 -t public
```

Buka http://localhost:8000. SQLite dibuat otomatis pada storage/. Di Windows dengan XAMPP, executable PHP umumnya berada di C:\xampp\php\php.exe. Jadikan public/ sebagai document root. Tidak ada kebutuhan npm atau Composer untuk lokal.

### MySQL

1. Impor database/mysql.sql ke MySQL atau MariaDB pada database kosong khusus proyek ini.
2. Salin .env.example menjadi .env.
3. Atur DB_DRIVER=mysql, DB_HOST, DB_PORT, DB_DATABASE, DB_USERNAME, dan DB_PASSWORD.
4. Jalankan ulang server PHP.

Nama database materi adalah pendaftaran_siswa. Jika nama tersebut sudah dipakai proyek lain, sesuaikan nama database pada SQL dan .env terlebih dahulu. Script CREATE TABLE IF NOT EXISTS tidak memigrasi skema proyek lain.

## Hosting

Demo Vercel menggunakan PHP dan SQLite dengan snapshot di Vercel Blob privat, sedangkan MySQL merupakan implementasi lokal yang diuji. Snapshot disimpan sebelum pesan berhasil dikirim. Setiap request mengambil data terbaru; conditional write mencegah saling menimpa. Ruang demo menggunakan cookie HttpOnly dan SameSite=Lax, serta Secure pada HTTPS. Data demo memiliki masa berlaku tujuh hari.

Pemisahan sesi bukan sistem akun petugas. Gunakan data fiktif. Demo tidak melakukan seleksi penerimaan siswa. Jangan unggah .env, .env.local, .vercel/, token, atau database lokal ke repository.

## Verifikasi

```sh
python -m pip install beautifulsoup4
python tests/check_http.py
```

Ubah TEST_BASE_URL untuk target lain dan TEST_REPORT untuk nama laporan. Jalankan `python tests/check_smoke.py` untuk alur normal pada hosting; pemeriksaan keamanan dijalankan lokal agar tidak memicu firewall hosting. Hasil: **39 pemeriksaan SQLite, 39 pemeriksaan MySQL/MariaDB, dan 14 pemeriksaan produksi lolos**, termasuk pembacaan snapshot SQLite langsung dari Blob privat milik sesi uji. Laporan tersedia di qa-sqlite.json, qa-mysql.json, dan qa-production.json. Setiap suite menggunakan sesi baru dan hanya memodifikasi data fiktif pada ruang ujinya.

QA produksi menggunakan alias deployment dan kredensial automation resmi Vercel yang disimpan dalam memori proses. Domain publik utama memberi Vercel Security Checkpoint pada trafik otomatis dari lingkungan pengerjaan. Firewall tetap aktif; keberhasilan suite dengan kredensial tidak membuktikan akses anonim pada domain utama. Akses publik melalui browser belum dapat diverifikasi di lingkungan ini.

Akses browser otomatis di lingkungan pengerjaan tidak tersedia. Pemeriksaan visual desktop dan ponsel belum dijalankan; pemeriksaan HTTP dan database tidak menjamin kesempurnaan layout.

Font Inter disimpan lokal beserta lisensi OFL. Ikon, ilustrasi header, dan diagram alur berasal dari SVG/CSS dalam proyek. Source dan artikel tidak memakai em dash atau en dash.
