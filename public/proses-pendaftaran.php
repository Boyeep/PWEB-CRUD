<?php
require_once dirname(__DIR__) . '/config.php';
check_post();
[$data,$errors] = validate_student($_POST);
if (count(students()) >= 100) $errors['nama'] = 'Ruang demo maksimal 100 siswa. Hapus data yang tidak diperlukan.';
if ($errors) { http_response_code(422); require_once dirname(__DIR__) . '/app/student-form.php'; form_page($data,$errors); exit; }
$query = db()->prepare('INSERT INTO calon_siswa (workspace_id,nama,alamat,jenis_kelamin,agama,sekolah_asal,created_at) VALUES (?,?,?,?,?,?,?)');
$query->execute([$_SESSION['workspace'],$data['nama'],$data['alamat'],$data['jenis_kelamin'],$data['agama'],$data['sekolah_asal'],date('Y-m-d H:i:s')]);
notice('Pendaftaran ' . $data['nama'] . ' berhasil disimpan.');
redirect('/list-siswa.php');
