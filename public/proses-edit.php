<?php
require_once dirname(__DIR__) . '/config.php';
check_post();
$row = require_student(student_id($_POST['id'] ?? null));
[$data,$errors] = validate_student($_POST);
if ($errors) { http_response_code(422); require_once dirname(__DIR__) . '/app/student-form.php'; form_page($data + ['id'=>$row['id']],$errors,true); exit; }
$query = db()->prepare('UPDATE calon_siswa SET nama=?, alamat=?, jenis_kelamin=?, agama=?, sekolah_asal=? WHERE id=? AND workspace_id=?');
$query->execute([$data['nama'],$data['alamat'],$data['jenis_kelamin'],$data['agama'],$data['sekolah_asal'],$row['id'],$_SESSION['workspace']]);
notice('Data ' . $data['nama'] . ' berhasil diperbarui.');
redirect('/detail.php?id=' . $row['id']);
