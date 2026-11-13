<?php
require_once dirname(__DIR__) . '/config.php';
$row = require_student(student_id($_GET['id'] ?? null));
page_start('Detail siswa','siswa'); heading('PROFIL CALON SISWA','Kenali setiap perjalanan.','Informasi lengkap pendaftaran calon siswa.');
?>
<section class="panel detail-panel"><div class="profile-top"><span class="profile-avatar"><?=e(mb_strtoupper(mb_substr($row['nama'],0,1)))?></span><div><span class="tag">REG-<?=str_pad((string)$row['id'],4,'0',STR_PAD_LEFT)?></span><h2><?=e($row['nama'])?></h2><p><?=e($row['sekolah_asal'])?></p></div><span class="gender-tag <?=$row['jenis_kelamin'] === 'Perempuan' ? 'female' : ''?>"><?=e($row['jenis_kelamin'])?></span></div><dl class="detail-grid"><?php foreach (['nama'=>'Nama lengkap','sekolah_asal'=>'Sekolah asal','jenis_kelamin'=>'Jenis kelamin','agama'=>'Agama','alamat'=>'Alamat lengkap','created_at'=>'Waktu pendaftaran'] as $key=>$label): ?><div class="<?=$key === 'alamat' ? 'full' : ''?>"><dt><?=$label?></dt><dd><?=nl2br(e($row[$key]))?></dd></div><?php endforeach ?></dl><div class="form-actions"><a class="button secondary" href="/list-siswa.php">Kembali</a><a class="button danger-outline" href="/hapus.php?id=<?=$row['id']?>"><?=icon('trash')?> Hapus</a><a class="button" href="/form-edit.php?id=<?=$row['id']?>"><?=icon('edit')?> Edit siswa</a></div></section>
<?php page_end(); ?>
