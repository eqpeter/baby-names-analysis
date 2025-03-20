# 寶貝的名字分析工具

## 專案概述
此專案是一個命令列工具，用於分析美國社會安全局(SSA)提供的嬰兒名字數據。程式可以從HTML文件中提取年份及不同名字的排名，並將結果輸出到螢幕或保存為摘要文件。

## 功能特點
- 從SSA嬰兒名字HTML文件中提取年份及名字排名數據
- 支援多個文件的批次處理
- 支援不同格式的HTML文件（1990-2008年）
- 可選擇輸出到螢幕或生成摘要文件
- 對名字進行字母順序排序
- 如果名字在男孩和女孩列表中都出現，保留較高的排名

## 使用方法
```
python childnames.py [--summaryfile] file [file ...]
```

### 參數說明
- `--summaryfile`: 可選參數，如果提供此參數，將結果寫入到 `.summary` 文件而不是輸出到螢幕
- `file [file ...]`: 一個或多個要分析的HTML文件路徑

### 範例
1. 分析單個文件並輸出到螢幕:
```
python childnames.py baby1990.html
```

2. 分析多個文件並輸出到螢幕:
```
python childnames.py baby1990.html baby2000.html baby2008.html
```

3. 分析多個文件並生成摘要文件:
```
python childnames.py --summaryfile baby*.html
```

## 輸出格式
輸出的第一行是年份，之後的每一行是按字母順序排序的「名字 排名」對。例如：
```
1990
Aaron 34
Abbey 482
Abbie 685
...
```

## 使用PowerShell檢索摘要文件數據
在生成了`.summary`文件後，您可以使用PowerShell命令輕鬆檢索和分析數據：

1. 在特定摘要文件中搜索某個名字的排名:
```
Select-String -Path baby2006.html.summary -Pattern 'Alex '
```

2. 在所有摘要文件中搜索某個名字的排名（可查看不同年份的排名變化）:
```
Select-String -Path *.summary -Pattern 'Alex '
```

3. 限制結果數量:
```
Select-String -Path *.summary -Pattern 'Alex ' | Select-Object -First 10
```

4. 查找特定排名區間的名字（例如前10名）:
```
Select-String -Path baby2008.html.summary -Pattern ' [1-9]$| 10$'
```

## 數據來源
美國社會安全局 (SSA) 嬰兒名字數據庫：https://www.ssa.gov/OACT/babynames/

## 技術細節
- 使用正則表達式提取HTML文件中的年份和名字排名數據
- 使用字典數據結構存儲和處理名字-排名對
- 處理命令列參數以支援不同的輸出選項
- 支援兩種不同格式的HTML文件結構 

## 作者
此專案是PETER的Python作業。 