# -*- coding: utf-8 -*-
import urllib.request, io, subprocess, tempfile, os
html = urllib.request.urlopen('https://qpooqp889.github.io/daily-learning/').read().decode('utf-8')
io.open('_online.html', 'w', encoding='utf-8').write(html)
js = html.split('<script>')[1].split('</script>')[0]
with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as f:
    f.write(js); path = f.name
r = subprocess.run(['node', '--check', path], capture_output=True, text=True)
print('線上 JS 語法:', 'OK' if r.returncode == 0 else 'FAIL\n' + r.stderr[:2000])
os.unlink(path)
# 檢查 pickIdioms 容器
print('pickIdioms div 存在:', 'id="pickIdioms"' in html)
print('pickWords div 存在:', 'id="pickWords"' in html)
print('全選/清空按鈕存在:', 'data-sel="cn"' in html and 'data-clear' in html)
