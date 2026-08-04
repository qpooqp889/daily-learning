# -*- coding: utf-8 -*-
import io
html = io.open('index.html', encoding='utf-8').read()
i = html.find('function renderPickLists')
print(html[i:i+600])
print('======')
# 檢查 pickIdioms 相關
j = html.find("pickIdioms")
while j != -1:
    print('---', html[max(0,j-80):j+80].replace('\n', ' '))
    j = html.find("pickIdioms", j+1)
