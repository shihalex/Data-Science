# NCKU CSIE 2024 Fall Data Science Course
contribute by shihalex

## 課程選課人數預測
專案內容：
- 使用爬蟲爬取成大選課網站兩年、4個科系的選課情況
- 使用授課教師、課程名稱、課程屬性等作為特徵
- 分別使用平均、回歸、Random forest 模型預測選課人數情況
- 使用 optuma 進行模型超參數調整
- 使用 confusion matrix, F1-score, accuray 作為評估標準

## 集成學習應用於二元分類任務
專案內容：
- 資料包含數值與名目資料，有多個資料集
- 使用多個 ML, DL 模型進行集成學習，每個資料集個別訓練集成 model
- 使用 grid search 進行模型超參數調整
- 處理資料 label imbalance 問題，並用 GAN 技術生成更多訓練資料
- 以 AUC score 作為訓練之驗證標準
- 在 Private 資料及得到 85% 成績，在 69 組中獲得第 26 名