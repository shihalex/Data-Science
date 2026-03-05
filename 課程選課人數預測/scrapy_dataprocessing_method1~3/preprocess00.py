import pandas as pd
import os
import sys
import io

# 設定輸出為 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def split_by_department_and_year(input_csv, output_folder, year_filter):
    """按系所分割課程資料，指定年份分開處理"""
    os.makedirs(output_folder, exist_ok=True)
    df = pd.read_csv(input_csv)

    if '系所名稱' not in df.columns:
        print("資料缺少 '系所名稱' 欄位，無法分割。")
        return
    
    # 刪除教師姓名欄位為空的資料
    if '教師姓名*:主負責老師' in df.columns:
        df = df.dropna(subset=['教師姓名*:主負責老師'])
    else:
        print("資料缺少 '教師姓名' 欄位，無法檢查空值。")
        return
    
    # 刪除特定課程（根據課程名稱）
    if '科目名稱(連結課程地圖)             備註 \n             限選條件' in df.columns:
        excluded_courses = ["體育（一）", "體育（二）", "服務學習（一）", "服務學習（二）", "服務學習（三）"]
        df = df[~df['科目名稱(連結課程地圖)             備註 \n             限選條件'].isin(excluded_courses)]
    else:
        print("資料缺少 '科目名稱' 欄位，無法刪除特定課程。")
        return
    
        # 替換課程名稱中的 ':' 為 '_'
    if '科目名稱(連結課程地圖)             備註 \n             限選條件' in df.columns:
        df['科目名稱(連結課程地圖)             備註 \n             限選條件'] = df['科目名稱(連結課程地圖)             備註 \n             限選條件'].str.replace(':', '_', regex=False)
    
    # 確保學年期格式一致（不轉為整數）
    if '學年期' in df.columns:
        df['學年期'] = df['學年期'].astype(str)
    else:
        print("資料缺少 '學年期' 欄位，無法篩選年份。")
        return

    # 分開指定年份和其他年份的資料
    specific_year_df = df[df['學年期'] == year_filter]
    other_years_df = df[df['學年期'] != year_filter]

    # 按系所分組並輸出
    departments = df['系所名稱'].unique()
    for dept in departments:
        dept_specific_year_df = specific_year_df[specific_year_df['系所名稱'] == dept]
        dept_other_years_df = other_years_df[other_years_df['系所名稱'] == dept]

        # 儲存指定年份的資料
        if not dept_specific_year_df.empty:
            specific_year_file = os.path.join(output_folder, f"{dept}_{year_filter}.csv")
            dept_specific_year_df.to_csv(specific_year_file, index=False, encoding='utf-8')
            print(f"已儲存 {dept} {year_filter} 的資料至 {specific_year_file}")

        # 儲存其他年份的資料
        if not dept_other_years_df.empty:
            other_years_file = os.path.join(output_folder, f"{dept}_other_years.csv")
            dept_other_years_df.to_csv(other_years_file, index=False, encoding='utf-8')
            print(f"已儲存 {dept} 的其他年份資料至 {other_years_file}")

INPUT_CSV = 'course_data05.csv'
YEAR_FILTER = '0113-1'  # 修改為你想篩選的年份
OUTPUT_FOLDER = f'processed_data_{YEAR_FILTER}/'

if __name__ == '__main__':
    split_by_department_and_year(INPUT_CSV, OUTPUT_FOLDER, YEAR_FILTER)
