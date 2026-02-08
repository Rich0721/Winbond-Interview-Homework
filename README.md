# Winbond Interview Homework

本專案為 Winbond 面試作業，依照需求信件內容實作，並依 UML Class 設計完成檔案掃描、文件處理、PDF 轉換、頁數計算與 XML Tree 輸出等功能。

---

## I. 需求來源

需求內容來自 Winbond 面試作業信件，並附上 UML Class 設計。

### 1-1 UML Class

請參考下圖：

[imgs/Homework.png]

### 1-2 資料夾架構

project/
│── main.py
│── constants.py
│── requirements.txt
│── imgs/
│ └── Homework.png
│── File
│ ├── File.py
│ ├── ImageFile.py
│ └── TextFile.py
│ └── WordFile.py
│── Directory
│ ├── Directory.py
│── README.md

## II. 需要套件與軟體

### 2-1 安裝 LibreOffice

本專案使用 LibreOffice 進行 `.doc` / `.docx` → PDF 轉換，以便後續計算頁數。

下載連結：  
https://www.libreoffice.org/download/download-libreoffice/

安裝後請確認 `soffice` 路徑是否正確。

---

### 2-2 設定 `constants.py`

請在 `constants.py` 中設定 LibreOffice 執行檔路徑，例如：

```
LIBREOFFICE_PATH = r"C:\Program Files\LibreOffice\program\soffice.exe"
```

### 2-3 安裝所需套件

```
pip install -r requirment.txt
```

## III. 參數說明

| 參數名稱          | 類型   | 是否必填 | 說明                                                 |
| ----------------- | ------ | -------- | ---------------------------------------------------- |
| `--root_dir`      | string | ✔        | 要掃描的根目錄路徑                                   |
| `--extension`     | string | ✘        | 過濾副檔名，例如 `.docx`、`.pdf`，留空則處理所有檔案 |
| `--target_dir`    | string | ✘        | 輸出資料夾，若不存在會自動建立                       |
| `--calucate_size` | flag   | ✘        | 若提供此參數，會計算所有檔案大小                     |
| `--xml_tree`      | flag   | ✘        | 若提供此參數，會輸出 XML Tree 結構                   |

## IV. 使用方式

### 4-1 產出指定資料夾架構

```
python main.py --root_dir="./Root"
```

[imgs/4-1.png]

### 4-2 計算容量

```
python main.py --root_dir="./Root" --target_dir="Folder1"  --calucate_size
```

[imgs/4-2.png]

### 4-3 副檔名搜尋

```
python main.py --root_dir="./Root" --extension=".jpg"
```

[imgs/4-3.png]

### 4-4 xml格式

```
python main.py --root_dir="./Root" --xml_tree
```

[imgs/4-4.png]
