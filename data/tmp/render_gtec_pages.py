# -*- coding: utf-8 -*-
"""Render all GEPT PDF pages to PNG images for OCR."""
import os
import pypdfium2 as pdfium

src = r'C:\Users\twric\.qclaw\workspace\daily-learning\data\gtec_raw.bin'
outdir = r'C:\Users\twric\.qclaw\workspace\daily-learning\data\gtec_pages'
os.makedirs(outdir, exist_ok=True)

pdf = pdfium.PdfDocument(src)
n = len(pdf)
print('pages:', n)
for i in range(n):
    page = pdf[i]
    bitmap = page.render(scale=2.0)  # 2x for better OCR
    pil_image = bitmap.to_pil()
    out = os.path.join(outdir, f'p{i+1:03d}.png')
    pil_image.save(out)
    print('saved', out, pil_image.size)
print('done')
