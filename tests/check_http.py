"""HTTP regression checks against real PHP and PDO. Uses its own demo sessions."""
import http.cookiejar
import json
import os
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

BASE = os.environ.get('TEST_BASE_URL', 'http://127.0.0.1:4200').rstrip('/')
SMOKE = os.environ.get('TEST_SMOKE_ONLY') == '1'
results = []

def client():
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    opener.addheaders = [('User-Agent', 'RuangSiswa-QA/1.0')]
    return opener

def request(c, path, data=None):
    encoded = urllib.parse.urlencode(data).encode() if data is not None else None
    try:
        r = c.open(BASE + path, encoded, timeout=90)
    except urllib.error.HTTPError as e:
        r = e
    return r.status, r.read().decode('utf-8'), r.headers

def soup(body):
    return BeautifulSoup(body, 'html.parser')

def check(name, condition):
    results.append({'name': name, 'passed': bool(condition)})
    if not condition:
        raise AssertionError(name)

def token(body):
    return soup(body).select_one('input[name=csrf]')['value']

c = client()
try:
    status, body, headers = request(c, '/')
    check('Dashboard reads six fictional records', status == 200 and soup(body).select_one('.stat-value').get_text(strip=True).startswith('6'))
    check('Security response headers', headers.get('X-Content-Type-Options') == 'nosniff' and "frame-ancestors 'none'" in headers.get('Content-Security-Policy', ''))
    for path in ['/list-siswa.php','/form-daftar.php','/panduan.php','/blog.php','/assets/style.css','/assets/app.js','/assets/favicon.svg','/assets/inter-latin.woff2','/assets/alur-crud.svg']:
        if path.endswith('.woff2'):
            check('Local font is served', c.open(BASE+path).status == 200)
        else:
            check('Page or asset '+path, request(c,path)[0] == 200)
    status, form, _ = request(c, '/form-daftar.php')
    csrf = token(form)
    check('Five required form fields have labels', all(soup(form).select_one('[name='+key+'][required]') and soup(form).select_one('label[for='+key+']') for key in ['nama','alamat','jenis_kelamin','agama','sekolah_asal']))
    check('GET cannot create', request(c,'/proses-pendaftaran.php')[0] == 405)
    check('GET cannot update', request(c,'/proses-edit.php')[0] == 405)
    check('CSRF blocks create', request(c,'/proses-pendaftaran.php',{'csrf':'invalid'})[0] == 403)
    status, invalid, _ = request(c,'/proses-pendaftaran.php',{'csrf':csrf,'nama':'A'})
    check('Validation preserves input and reports errors', status == 422 and soup(invalid).select_one('#nama')['value'] == 'A' and len(soup(invalid).select('[aria-invalid=true]')) == 5)
    record = {'csrf':csrf,'nama':'QA Siswa Fiktif','alamat':'Jl. Contoh No. 123, Surabaya','jenis_kelamin':'Perempuan','agama':'Islam','sekolah_asal':'SMP Uji Fiktif'}
    if not SMOKE:
        record['nama'] = 'QA Siswa <b>Fiktif</b>'
    status, body, _ = request(c,'/proses-pendaftaran.php',record)
    check('Create commits and redirects to list', status == 200 and 'berhasil disimpan' in body and len(soup(body).select('tbody tr')) == 7)
    if not SMOKE:
        check('Stored HTML is escaped', '&lt;b&gt;Fiktif&lt;/b&gt;' in body and '<b>Fiktif</b>' not in body)
    status, body, _ = request(c,'/list-siswa.php?q=QA+Siswa')
    links = soup(body).select('.student-name')
    check('Search finds persisted record on later request', len(links) == 1)
    detail = links[0]['href']
    record_id = urllib.parse.parse_qs(urllib.parse.urlsplit(detail).query)['id'][0]
    check('Detail shows all fields', all(value in request(c,detail)[1] for value in ['Jl. Contoh No. 123','SMP Uji Fiktif','Perempuan','Islam']))
    other = client()
    request(other,'/')
    check('Other session cannot read record', request(other,detail)[0] == 404)
    check('Other session cannot open edit', request(other,'/form-edit.php?id='+record_id)[0] == 404)
    other_csrf = token(request(other,'/form-daftar.php')[1])
    check('Other session cannot update record', request(other,'/proses-edit.php',record | {'csrf':other_csrf,'id':record_id})[0] == 404)
    check('Other session cannot delete record', request(other,'/hapus.php',{'csrf':other_csrf,'id':record_id})[0] == 404)
    check('CSRF blocks update', request(c,'/proses-edit.php',record | {'csrf':'wrong','id':record_id})[0] == 403)
    status, body, _ = request(c,'/hapus.php?id='+record_id)
    check('GET delete only confirms', status == 200 and 'Hapus data siswa ini?' in body and request(c,detail)[0] == 200)
    record.update(id=record_id,nama='QA Siswa Diperbarui')
    status, body, _ = request(c,'/proses-edit.php',record)
    check('Update persists on later request', status == 200 and 'berhasil diperbarui' in body and 'QA Siswa Diperbarui' in request(c,detail)[1])
    status, body, _ = request(c,'/list-siswa.php?'+urllib.parse.urlencode({'q':'QA Siswa','gender':'Perempuan'}))
    check('Gender filter combines with search', len(soup(body).select('.student-name')) == 1)
    check('Other gender excludes record', not soup(request(c,'/list-siswa.php?q=QA+Siswa&gender=Laki-laki')[1]).select('.student-name'))
    check('CSRF blocks delete', request(c,'/hapus.php',{'csrf':'wrong','id':record_id})[0] == 403)
    status, body, _ = request(c,'/hapus.php',{'csrf':csrf,'id':record_id})
    check('Delete commits with notice', status == 200 and 'berhasil dihapus' in body)
    check('Deleted record returns 404', request(c,detail)[0] == 404)
    check('Empty search offers recovery', 'Siswa belum ditemukan' in request(c,'/list-siswa.php?q=tidakadadataini')[1])
    check('Malformed ID returns 404', request(c,'/form-edit.php?id=abc')[0] == 404)
    if not SMOKE:
        injection = request(c,'/list-siswa.php?'+urllib.parse.urlencode({'q':"' OR 1=1 --"}))[1]
        check('SQL input stays a search parameter', not soup(injection).select('.student-name'))
        check('Wildcard search treats percent literally', not soup(request(c,'/list-siswa.php?q=%25')[1]).select('.student-name'))
        # Create enough records to exercise page boundaries, then remove them.
        for i in range(3):
            request(c,'/proses-pendaftaran.php',record | {'nama':'QA Halaman '+str(i)})
        first = soup(request(c,'/list-siswa.php')[1])
        second = soup(request(c,'/list-siswa.php?page=2')[1])
        check('Pagination splits nine rows into eight and one', len(first.select('tbody tr')) == 8 and len(second.select('tbody tr')) == 1)
        for link in soup(request(c,'/list-siswa.php?q=QA+Halaman')[1]).select('.student-name'):
            rid = urllib.parse.parse_qs(urllib.parse.urlsplit(link['href']).query)['id'][0]
            request(c,'/hapus.php',{'csrf':csrf,'id':rid})
    final_list = soup(request(c,'/list-siswa.php')[1])
    check('All suite records removed from own workspace', len(final_list.select('tbody tr')) == 6 and 'QA Siswa' not in final_list.get_text() and 'QA Halaman' not in final_list.get_text())
    check('Config is outside public document root', request(c,'/config.php')[0] == 404)
    print(str(len(results))+' checks passed against '+BASE)
finally:
    report = {'base_url':BASE,'smoke_only':SMOKE,'passed':sum(r['passed'] for r in results),'total':len(results),'checks':results,'visual_qa':'Not run: browser access host unavailable.'}
    report_path = Path(__file__).resolve().parents[1] / os.environ.get('TEST_REPORT','qa-sqlite.json')
    report_path.write_text(json.dumps(report,indent=2),encoding='utf-8')
