import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import joblib
from sklearn.metrics.pairwise import cosine_similarity

# 加載已保存的模型
rf_model = joblib.load("rf_model.pkl")

# 加載數據
data = pd.read_csv("enhanced_math_course_data.csv")
data['必選修'] = data['必選修'].replace({'必修': 0, '選修': 1, '必選': 2})
data = data.replace({True: 1, False: 0})

# 分離 "已選課人數" 和 "餘額"
data[['已選課人數', '餘額']] = data['已選課人數/餘額'].str.split('/', expand=True)

# 移除 '餘額' 列中值為 "網路選課不開放" 的行
data = data[data['餘額'] != '網路選課不開放']

# 處理 "餘額" 中的特殊值
data['餘額'] = data['餘額'].replace(['額滿'], 0)

# 將 "餘額" 列轉換為整數，非數字的值替換為 NaN 並填充為 0
data['餘額'] = pd.to_numeric(data['餘額'], errors='coerce').fillna(0).astype(int)

# 將 "已選課人數" 轉換為整數
data['已選課人數'] = pd.to_numeric(data['已選課人數'], errors='coerce').fillna(0).astype(int)

# 確保 "已選課人數" 列中沒有零，避免零除錯誤
data['已選課人數'] = data['已選課人數'].replace(0, 1)

# 新增 "餘額/已選課人數" 特徵
data['餘額_已選課人數比'] = data['已選課人數'] / (data['已選課人數'] + data['餘額']) * 100

# 特徵列表
features = list(data.drop(columns=[
    '系所名稱', '已選課人數', '餘額', '餘額_已選課人數比', '已選課人數/餘額', '學年期',
    '科目名稱(連結課程地圖)             備註 \n             限選條件', '類別_講義',
    '教師姓名*:主負責老師', '學分', '時間', '教室']).columns)

# 構造 GUI
root = tk.Tk()
root.title("課程預測與查找工具")
root.geometry("900x600")

# 標題
title_label = tk.Label(root, text="課程預測與相似課查找工具", font=("Arial", 16))
title_label.pack(pady=10)

# 特徵選擇框
feature_frame = tk.Frame(root)
feature_frame.pack(pady=10)
feature_label = tk.Label(feature_frame, text="選擇課程特徵：", font=("Arial", 12))
feature_label.grid(row=0, column=0, sticky=tk.W, pady=5)

feature_vars = {feature: tk.BooleanVar() for feature in features}
for i, feature in enumerate(features):
    row, col = divmod(i, 4)
    tk.Checkbutton(feature_frame, text=feature, variable=feature_vars[feature]).grid(row=row + 1, column=col, sticky=tk.W, padx=10)

# 結果顯示區域
result_frame = tk.Frame(root)
result_frame.pack(pady=10)

prediction_label = tk.Label(result_frame, text="預測餘額/已選課人數比例：", font=("Arial", 12))
prediction_label.grid(row=0, column=0, sticky=tk.W, padx=10)

similar_courses_label = tk.Label(result_frame, text="相似課程：", font=("Arial", 12))
similar_courses_label.grid(row=1, column=0, sticky=tk.W, padx=10)

prediction_result = tk.Label(result_frame, text="無", font=("Arial", 12), fg="blue")
prediction_result.grid(row=0, column=1, sticky=tk.W, padx=10)

similar_courses_result = tk.Text(result_frame, width=80, height=10, wrap=tk.WORD, font=("Arial", 10))
similar_courses_result.grid(row=1, column=1, padx=10)

# 功能函數
def get_input_features():
    selected_features = [feature for feature, var in feature_vars.items() if var.get()]
    if not selected_features:
        messagebox.showerror("錯誤", "請至少選擇一個課程特徵！")
        return None
    return [1 if feature in selected_features else 0 for feature in features]

def predict_and_find_similar():
    try:
        input_features = get_input_features()
        if input_features is None:
            return

        # 預測選課比例
        predicted_count = rf_model.predict([input_features])[0]
        prediction_result.config(text=f"{predicted_count:.2f}")

        # 查找相似課程
        feature_matrix = data[features].values
        similarities = cosine_similarity([input_features], feature_matrix)[0]
        similar_indices = similarities.argsort()[-5:][::-1]  # 找出相似度最高的 5 個課程
        similar_courses = data.iloc[similar_indices]

        # 顯示相似課程名稱
        similar_courses_result.delete(1.0, tk.END)
        for idx, row in similar_courses.iterrows():
            similar_courses_result.insert(
                tk.END,
                f"課程名稱: {row['科目名稱(連結課程地圖)             備註 \n             限選條件']}, "
                f"比例: {row['餘額_已選課人數比']:.2f}%, 相似度: {similarities[idx]:.2f}\n"
            )

    except Exception as e:
        messagebox.showerror("錯誤", f"發生錯誤：{str(e)}")

# 預測按鈕
predict_button = tk.Button(root, text="預測並查找相似課程", command=predict_and_find_similar, font=("Arial", 12))
predict_button.pack(pady=10)

# 啟動主循環
root.mainloop()
