# -*- coding: utf-8 -*-
import io
html = io.open('_online.html', encoding='utf-8').read()
# 找 pickIdioms 附近的完整 HTML
i = html.find('pickIdioms')
start = html.rfind('<div', 0, i-100)
end = html.find('</div>', i) + 20
print(html[start-200:end+300])
