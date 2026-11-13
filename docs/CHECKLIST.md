# Pemetaan tugas

Sumber: https://fajarbaskoro.blogspot.com/2022/11/crud-2-pendaftaran-siswa-baru.html

| Kebutuhan materi | Implementasi |
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

Kolom workspace_id dan created_at adalah tambahan teknis. Lima isian formulir mengikuti materi. Lampiran studi kasus Laundry pada bagian Latihan adalah referensi pengembangan terpisah; proyek ini mengerjakan judul utama pendaftaran siswa baru.
