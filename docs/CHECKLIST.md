# Daftar fitur

| Fitur | Implementasi |
| --- | --- |
| Halaman utama | public/index.php, statistik dan lima pendaftar terbaru |
| Pendaftaran | public/form-daftar.php dan proses-pendaftaran.php |
| Daftar serta jumlah pendaftar | public/list-siswa.php dan ringkasan |
| id, nama, alamat, jenis_kelamin, agama, sekolah_asal | database/mysql.sql |
| config.php | config.php memuat bootstrap, app/database.php membuka PDO |
| Edit | public/form-edit.php dan proses-edit.php |
| Hapus | public/hapus.php, konfirmasi GET dan penghapusan POST |
| Artikel | docs/blogspot.html dan public/blog.php |
| GitHub | Boyeep/PWEB-CRUD |
| Deployment | Vercel, pweb-crud.vercel.app |

Tambahan: detail siswa, pencarian, filter jenis kelamin, paginasi delapan baris, CSRF, prepared statements, escaping HTML, dan pemisahan ruang demo.

Kolom workspace_id dan created_at mendukung pemisahan ruang demo dan pencatatan waktu pendaftaran. Formulir memuat nama, alamat, jenis kelamin, agama, dan sekolah asal.
