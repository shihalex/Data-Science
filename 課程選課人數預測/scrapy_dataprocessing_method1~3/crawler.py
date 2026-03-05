import os
from bs4 import BeautifulSoup
import csv
import sys
import io

# 設定輸出為 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 定義資料夾與輸出檔案
RAW_FOLDER = './raw'
OUTPUT_CSV = 'course_data05.csv'

# 定義需要排除的 class 名稱
excluded_classes = [
    "R57b649be008ef905fc6ccb19d241dc46",
    "l5be8960b04225655e085135e272b70f5",
    "Dd0050fef915e5566c72e175d306bd3b3",
    "Re2e5af6fffb7a8f42970a4eeee172ebc"
]

def process_html_file(filepath):
    """處理單一 HTML 檔案，提取課程資訊與課程大綱連結"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

            # 找到表格
            table = soup.find('table', class_='table-bordered')
            if not table:
                print(f"No table found in {filepath}")
                return []

            # 找到表格的標題 (headers)
            headers = [th.text.strip() for th in table.find_all('th')]
            if not headers:
                print(f"Warning: No headers found in {filepath}")
                return []
            
            headers.append("Syllabus Link")  # 新增課程大綱連結的標題
            data = [headers]  # 將標題加入資料

            # 找到表格的資料行 (rows)
            for row in table.find_all('tr'):
                columns = row.find_all('td')
                if columns:
                    row_data = []
                    for column in columns:
                        # 找到所有 <i> 或 <span> 並刪除
                        for class_name in excluded_classes:
                            for span in column.find_all(['span'], class_=class_name):
                                span.decompose()  # 完全刪除該元素
                                
                        # 嘗試提取 course_name                                
                        course_name = column.find('span', class_='course_name')
                        if course_name:
                            # 提取 course_name 的內容
                            processed_text = course_name.get_text(strip=True)
                            row_data.append(processed_text)
                        else:
                            # 如果沒有找到 course_name，處理整個 <td> 的文字內容
                            processed_text = column.get_text(separator="", strip=True)
                            row_data.append(processed_text)

                    # 嘗試從所有列中提取超連結
                    syllabus_link = ""
                    for column in columns:
                        link_tag = column.find('a', href=True)
                        if link_tag and "syllabus" in link_tag['href']:
                            syllabus_link = link_tag['href']
                            break
                    row_data.append(syllabus_link)

                    data.append(row_data)

            return data
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return []

def process_all_files(raw_folder, output_csv):
    """處理資料夾中的所有 HTML 檔案，並匯出到 CSV"""
    all_data = []
    headers_written = False

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for root, _, files in os.walk(raw_folder):
            for file in files:
                if file.endswith('.html'):
                    filepath = os.path.join(root, file)
                    print(f"Processing {filepath}...")
                    file_data = process_html_file(filepath)
                    if file_data:
                        if not headers_written:
                            writer.writerow(file_data[0])  # 寫入標題
                            headers_written = True
                        writer.writerows(file_data[1:])  # 寫入資料

    print(f"所有資料已儲存至 {output_csv}")

if __name__ == '__main__':
    # 處理所有 HTML 檔案並輸出 CSV
    process_all_files(RAW_FOLDER, OUTPUT_CSV)