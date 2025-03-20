####################################################################
# Python x AI Agent
# Regexp, file, dict, CLI - 正則表達式、檔案、命令列參數
#
# [專案]
# 寶貝的名字
# 問題：請詳閱附件 ReadMe_childnames.pdf 說明
#
# 已知：各年度 babyxxxx.html 檔案 (如附件)
# 輸入：命令列指令。
#    usage: [--summaryfile] file [file ...]
#    1)指定要解析的檔案名稱 file (可以多個檔案)
#    2)如果選擇 --summaryfile，則將擷取結果存入 .summary 檔案
#    3)若未選擇 --summaryfile，則將擷取結果輸出在螢幕
# 輸出：
#    1)印出：擷取之年度、名字、排行
#    2)依命令列指令將擷取結果寫入 summary 檔案
#
# Ref. link: https://www.ssa.gov/OACT/babynames/
#####################################################################

import sys
import re

"""專案：寶貝的名字

撰寫函數 extract_names() 如下，並修改 main() 以呼叫它。
要寫好正則表達式(regex)，最好準備目標文字檔的副本以激發靈感。
以下為 baby.html 檔案中我們要搜尋的 html 部份：
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

建議採漸進式開發，切割各階段如下：
 -搜尋、擷取年份 (year) 資料並印出
 -擷取 名字與排行 (name-rank) 資料並列印
 -建立字典，存放名字並列印
 -建立 [year, 'name rank', ... ] 串列並列印
 -修改 main() 以使用 extract_names 串列

"""

def extract_names(filename):
  """
  :param: str filename: 輸入存放 baby.html 的檔案名稱，
  :return: list of str: 傳回一個串列，內含：
    第一個元素為年度字串，接著的是名字-排行字串，依字母排序。
    ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
  """
  # 讀取檔案內容
  try:
    with open(filename, 'r') as f:
      content = f.read()
  except IOError:
    print(f'無法打開檔案: {filename}')
    return []
  
  # 擷取年份
  year_match = re.search(r'<h3 align="center">Popularity in (\d+)</h3>', content)
  if not year_match:
    # 尝试另一种格式
    year_match = re.search(r'<caption><h2>Popularity in (\d+)</h2></caption>', content)
    if not year_match:
      print(f'無法在檔案中找到年份: {filename}')
      return []
  
  year = year_match.group(1)
  
  # 擷取名字和排名
  # 格式: <tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
  # 或者: <tr align="right"><td>1</td><td>Jacob</td><td>Emma</td></tr>
  names_ranks = {}
  pattern = r'<tr align="right"><td>(\d+)</td><td>(\w+)</td><td>(\w+)</td>(?:</tr>)?'
  
  matches = re.findall(pattern, content)
  
  # 遍歷所有匹配項，處理男孩和女孩的名字
  for rank, boy, girl in matches:
    # 將名字和排名存入字典，如果名字已存在，保留較高排名（較小數字）
    if boy not in names_ranks or int(rank) < int(names_ranks[boy]):
      names_ranks[boy] = rank
    if girl not in names_ranks or int(rank) < int(names_ranks[girl]):
      names_ranks[girl] = rank
  
  # 創建結果列表
  result = [year]
  
  # 將字典轉換為 "名字 排名" 格式的字符串列表，並按字母順序排序
  for name in sorted(names_ranks.keys()):
    result.append(f"{name} {names_ranks[name]}")
  
  return result


def main():
  # 本專案已提供 解析命令列 的程式碼.
  # 建立命令列引數串列，略過[0]元素(即程式檔名稱)
  args = sys.argv[1:]

  if not args:
    print('usage: childnames.py [--summaryfile] file [file ...]')
    sys.exit(1)

  # 檢查是否有 --summaryfile 命令列選項參數，如果有則設定旗幟，
  # 並將參數從引數串列中移除，只保留要讀取的檔名在引數串列中.
  summary = False
  if args[0] == '--summaryfile':
    summary = True
    del args[0]

  # 針對每個檔案，擷取名字-排行
  for filename in args:
    names = extract_names(filename)
    
    # 如果沒有找到名字，跳過此檔案
    if not names:
      continue
    
    # 格式化輸出文字
    text = '\n'.join(names)
    
    # 根據命令列參數決定輸出方式
    if summary:
      # 創建.summary文件並寫入結果
      summary_filename = filename + '.summary'
      with open(summary_filename, 'w') as f:
        f.write(text + '\n')
      print(f'已將結果寫入: {summary_filename}')
    else:
      # 輸出到螢幕
      print(text)


if __name__ == '__main__':
  main()

