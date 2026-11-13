"""Normal CRUD workflow for production. Run security probes against local services."""
import base64
import hashlib
import http.cookiejar
import json
import os
from pathlib import Path
import sqlite3
import urllib.error
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

base = os.environ.get('TEST_BASE_URL','https://pweb-crud.vercel.app').rstrip('/')
jar = http.cookiejar.CookieJar()
client = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
client.addheaders = [('User-Agent','RuangSiswa-Deployment-QA/1.0')]
if os.environ.get('TEST_BYPASS_TOKEN'):
    client.addheaders.append(('x-vercel-protection-bypass',os.environ['TEST_BYPASS_TOKEN']))
checks = []

def request(path, data=None):
    encoded = urllib.parse.urlencode(data).encode() if data is not None else None
    try:
        r = client.open(base+path,encoded,timeout=90)
    except urllib.error.HTTPError as e:
        r = e
    body = r.read().decode('utf-8')
    return r.status,body

def check(label,condition):
    checks.append({'name':label,'passed':bool(condition)})
    assert condition,label
    print('PASS: '+label,flush=True)

def parse(body):
    return BeautifulSoup(body,'html.parser')

try:
    status,body = request('/')
    check('Dashboard renders PHP and six persisted records',status == 200 and parse(body).select_one('.stat-value').get_text(strip=True).startswith('6') and '<?php' not in body)
    if base.startswith('https:'):
        check('Session cookie is Secure and HttpOnly',any(c.secure and c.has_nonstandard_attr('HttpOnly') for c in jar))
    status,body = request('/form-daftar.php')
    check('Registration form renders',status == 200 and parse(body).select_one('[name=csrf]') is not None)
    csrf = parse(body).select_one('[name=csrf]')['value']
    data = {'csrf':csrf,'nama':'QA Smoke Fiktif','alamat':'Jalan Uji Nomor 88, Surabaya','jenis_kelamin':'Perempuan','agama':'Islam','sekolah_asal':'SMP Contoh Fiktif'}
    status,body = request('/proses-pendaftaran.php',data)
    check('Create persists and returns success',status == 200 and 'berhasil disimpan' in body and 'QA Smoke Fiktif' in body)
    status,body = request('/list-siswa.php?q=QA+Smoke+Fiktif')
    links = parse(body).select('.student-name')
    check('Search reads saved record on later request',status == 200 and len(links) == 1)
    detail = links[0]['href']
    rid = urllib.parse.parse_qs(urllib.parse.urlsplit(detail).query)['id'][0]
    status,body = request('/form-edit.php?id='+rid)
    check('Edit form loads existing values',status == 200 and parse(body).select_one('#nama')['value'] == 'QA Smoke Fiktif')
    data.update(id=rid,nama='QA Smoke Diperbarui')
    status,body = request('/proses-edit.php',data)
    check('Update persists with success notice',status == 200 and 'berhasil diperbarui' in body)
    status,body = request(detail)
    check('Later request reads updated data',status == 200 and 'QA Smoke Diperbarui' in body)
    status,body = request('/hapus.php?id='+rid)
    check('GET delete shows confirmation',status == 200 and 'Hapus data siswa ini?' in body)
    status,body = request('/hapus.php',{'csrf':csrf,'id':rid})
    check('Confirmed deletion returns success',status == 200 and 'berhasil dihapus' in body)
    status,body = request('/list-siswa.php?q=QA+Smoke')
    check('Deleted record absent on later request',status == 200 and not parse(body).select('.student-name'))
    status,body = request('/blog.php')
    check('Blog article available',status == 200 and 'Membuat CRUD Pendaftaran Siswa Baru' in body)
    status,body = request('/list-siswa.php')
    check('Own test data cleaned up',status == 200 and len(parse(body).select('tbody tr')) == 6)
    if os.environ.get('TEST_BLOB_TOKEN') and os.environ.get('TEST_BLOB_STORE'):
        sid = next(c.value for c in jar if c.name == 'ruangsiswa_session')
        pathname = 'ruangsiswa/sessions/'+hashlib.sha256(sid.encode()).hexdigest()+'.json'
        url = 'https://'+os.environ['TEST_BLOB_STORE'].lower()+'.private.blob.vercel-storage.com/'+pathname+'?cache=0'
        req = urllib.request.Request(url,headers={'Authorization':'Bearer '+os.environ['TEST_BLOB_TOKEN']})
        with urllib.request.urlopen(req,timeout=30) as r:
            snapshot = json.load(r)
        connection = sqlite3.connect(':memory:')
        connection.deserialize(base64.b64decode(snapshot['database']))
        remaining = connection.execute('SELECT COUNT(*) FROM calon_siswa').fetchone()[0]
        qa_remaining = connection.execute("SELECT COUNT(*) FROM calon_siswa WHERE nama LIKE 'QA Smoke%'").fetchone()[0]
        check('Private Blob snapshot contains persisted cleanup',remaining == 6 and qa_remaining == 0)
finally:
    report = {'base_url':base,'passed':sum(c['passed'] for c in checks),'total':len(checks),'checks':checks,'automation_auth':bool(os.environ.get('TEST_BYPASS_TOKEN')),'visual_qa':'Not run: browser access host unavailable.','security_tests':'See qa-sqlite.json and qa-mysql.json.'}
    Path(__file__).resolve().parents[1].joinpath(os.environ.get('TEST_REPORT','qa-production.json')).write_text(json.dumps(report,indent=2),encoding='utf-8')
