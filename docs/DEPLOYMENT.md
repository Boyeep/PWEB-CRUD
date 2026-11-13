# Deployment RuangSiswa

Target: https://pweb-crud.vercel.app

Vercel menjalankan PHP menggunakan community runtime vercel-php@0.9.0. Router api/index.php memakai allowlist halaman. Aset pada public/assets dilayani secara statis.

Demo online menggunakan SQLite dan Vercel Blob privat khusus proyek pweb-crud-data. Ini berbeda dari mode MySQL lokal. Snapshot sesi dan database diambil setiap request dan ditulis sebelum redirect sukses. Conditional write dengan ETag menolak pembaruan bersamaan yang berbenturan. TTL snapshot dan cookie demo tujuh hari. Menghapus cookie membuat ruang baru.

Environment produksi yang dibutuhkan: BLOB_READ_WRITE_TOKEN dan BLOB_STORE_ID. Token tidak disimpan pada source. Jika penyimpanan belum terhubung, aplikasi mengembalikan kegagalan layanan dan tidak menampilkan keberhasilan palsu.

Deployment produksi berstatus Ready. Repository GitHub telah dihubungkan ke Vercel untuk deployment pada push berikutnya. Empat belas pemeriksaan alur normal lolos melalui kredensial automation resmi pada alias deployment, termasuk konfirmasi isi snapshot Blob setelah penghapusan. Domain utama memberi Security Checkpoint pada trafik otomatis dari lingkungan uji. Firewall tidak diubah. Akses anonim melalui browser belum dapat diperiksa karena browser host tidak tersedia.

Jalankan deployment melalui `npx vercel --prod --yes` dari folder proyek yang sudah terhubung. Untuk hosting MySQL operasional, gunakan server PHP dengan database jaringan dan konfigurasi autentikasi yang sesuai. Versi ini merupakan demo pembelajaran.
