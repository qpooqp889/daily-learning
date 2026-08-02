# 📚 每日學習 (Daily Learning)

國小六年級每日學習內容：英文單字 + 例句、國語成語（各 7 則）。

👉 **線上瀏覽**：https://<你的帳號>.github.io/daily-learning/

## 功能
- 🇺🇸 **英文分頁**：單字（詞性、中文意思、Google 翻譯發音連結）+ 對應句子（中文翻譯、Google 翻譯發音連結）
- 🀄 **國語分頁**：成語（解釋、造句範例）
- ☀️ **白天模式**：藍白配色 ／ 🌙 **黑夜模式**：桃紅 + 黑（自動記憶）
- 💾 **JSON 儲存**：`data/words.json`、`data/idioms.json`，純靜態網頁，GitHub Pages 直接託管

## 檔案結構
```
daily-learning/
├── index.html          # 主網頁（純靜態）
├── data/
│   ├── words.json      # 英文單字 + 句子
│   └── idioms.json     # 國語成語
├── add.py              # 新增資料工具（含重複檢查）
├── db.py / app.py      # （舊版 SQLite + Flask，可刪除）
└── seed_today.py       # 種子資料（一次性）
```

## 新增資料（本地執行）

```bash
# 新增單字（自動檢查重複；發音連結自動生成 Google 翻譯）
python add.py word celebrate --pos "v." --meaning "慶祝"

# 新增句子
python add.py sentence celebrate --en "We celebrate my grandma's birthday every year." --zh "我們每年都慶祝奶奶的生日。" --gtranslate "https://translate.google.com/?hl=zh-TW&eotf=0&sl=en&tl=zh-TW&text=We%20celebrate%20my%20grandma%E2%80%99s%20birthday%20every%20year.&op=translate"

# 新增成語
python add.py idiom 畫蛇添足 --explain "比喻多此一舉，做了多餘的事，反而不恰當。" --example "文章已經寫得很完整了，再加這段話反而是畫蛇添足。"

# 檢查重複 / 列出資料
python add.py check
python add.py list
```

> ⚠️ 重複的單字（不分大小寫）與成語會自動跳過，不會重複儲存。

## 部署到 GitHub Pages

1. 建立 GitHub 儲存庫（例如 `daily-learning`）
2. 上傳所有檔案（**確認 `data/*.json` 有被提交**）
3. Settings → Pages → Source 選 `main` 分支 / `root` 資料夾
4. 開啟 https://<你的帳號>.github.io/daily-learning/

新增資料後：`python add.py ...` → commit & push，網頁即自動更新。
