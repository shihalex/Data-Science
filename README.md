# 資料科學導論 | Introduction to Data Science

本儲存庫整理國立成功大學「資料科學導論」課程的兩項團隊實作成果：**課程選課人數預測系統**與**集成學習應用於二元分類任務**。專案涵蓋網頁資料解析、資料清理、特徵工程、迴歸與分類模型、模型集成、超參數調整，以及利用生成對抗網路（GAN）進行資料增強。相關程式、Jupyter Notebook、期末報告及競賽報告均依主題分類整理。

## 專案資訊

| 項目 | 內容 |
| --- | --- |
| 課程名稱 | 資料科學導論（Introduction to Data Science） |
| 開課學校／單位 | 國立成功大學（NCKU）資訊工程學系 |
| 開課學期 | 2024 Fall |
| 專案性質 | 課程期末專題與 Competition 1 分類競賽 |
| 團隊 | 施淳譯、蔡譯潁、陳亭蓁 |
| 課程大綱 | [NCKU 課程大綱](https://class-qry.acad.ncku.edu.tw/syllabus/online_display.php?syear=0113&sem=1&co_no=F725000&class_code=) |
| GitHub Repository | [shihalex/Data-Science](https://github.com/shihalex/Data-Science) |

## 目錄

- [專案資訊](#專案資訊)
- [競賽一：集成學習應用於二元分類任務](#競賽一集成學習應用於二元分類任務)
- [期末專題：課程選課人數預測系統](#期末專題課程選課人數預測系統)
- [團隊分工與參考資料](#團隊分工與參考資料)


## 競賽一：集成學習應用於二元分類任務

本專題參與課程 **DS34 Competition 1**，針對多個資料集進行二元分類（標籤 0／1），以 **ROC-AUC** 作為主要評估指標。各資料集的特徵數量、類別欄位、數值範圍及樣本數不同，部分資料集亦存在類別不平衡。

### 特徵工程與資料處理

- **數值特徵：** 使用 `StandardScaler` 或 `MinMaxScaler` 進行標準化／縮放。
- **類別特徵：** 探索 `OneHotEncoder`、`TargetEncoder` 等編碼方法。
- **類別不平衡：** 依資料型態使用 **SMOTE** 或 **SMOTENC** 進行少數類別過採樣。
- **其他嘗試：** 特徵篩選與交互特徵曾納入實驗，但報告指出其結果未穩定優於原始設定，因此未作為主要最終方案。

### 模型設計與集成策略

| 模型 | 核心架構 | 驗證與用途 |
| --- | --- | --- |
| **Model 1** | 以神經網路（NN）、Random Forest 與 XGBoost 為基模型，使用 Logistic Regression 整合預測；NN 加入 ELU、Batch Normalization、Dropout、L2 Regularization，並使用 Optuna 進行 **10 次 Trial** 的超參數搜尋 | 以 5-fold 交叉驗證進行模型評估與集成實驗 |
| **Model 2** | 將 Bagging Random Forest、Extra Trees、SVM、NuSVC、MLP，與 XGBoost、LightGBM、CatBoost、三種 Boosting 模型及內部 Stacking 模型的預測，彙整成 **12 組機率特徵**，最後由 Logistic Regression 輸出分類機率 | 使用 **5-fold Stratified K-Fold**，並依各折 AUC 對測試預測加權平均；**實際競賽提交版本** |
| **Model 3** | 簡化為 Random Forest、SVM、MLP、XGBoost、LightGBM、CatBoost 六類基模型，透過 StackingClassifier（Logistic Regression 為最終分類器）整合；嘗試加入 GAN 生成資料 | 採用 80%／20% 分割驗證；屬於**後續實驗，未成功提交競賽** |

`Gan.py` 透過 PyTorch 建立生成器（Generator）與判別器（Discriminator），使用 **10 維隨機噪聲**作為生成器輸入，透過全連接層學習少數類別資料的特徵分布，並以 Binary Cross-Entropy（BCE）作為對抗訓練損失。程式針對具有類別不平衡的資料集，嘗試額外生成 **500 筆少數類別樣本**。 Dataset 26、31 在資料生成過程中出現問題。

### 競賽結果與分析

以下結果來自本專題的 **Competition 1 正式報告**：

| 項目 | 結果 |
| --- | ---: |
| 最終提交模型 | Model 2 |
| Public ROC-AUC | **0.863360** |
| Private ROC-AUC | **0.850839** |
| 報告記載的 Private 排名 | **第 25 名／68 組** |

**Model 3 並非上述排行榜分數的來源。** 報告指出，加入 GAN 資料後的 Model 3 在部分本地驗證中有較高 AUC，但因未於截止前完成提交，無法以競賽 Private ROC-AUC 證實其優於 Model 2。報告也指出，少樣本資料集（例如 Dataset 3）對分類模型較具挑戰性，顯示資料量與資料分布會影響模型表現。

## 期末專題：課程選課人數預測系統

本專題以國立成功大學歷年課程選課資訊為基礎，目標是**預測課程選課人數與剩餘名額、將課程熱門度分為高／中／低三類，以及估計新開課程的選課情形**，協助分析課程需求與選課趨勢。

### 資料來源與前處理

- **資料範圍：** 成大數學、資訊、統計及測量等四個系所，涵蓋約 108 至 113 學年度的歷年課程資訊，並針對 **113-1、113-2** 進行預測分析。報告註記資料蒐集時間截至 2025 年 1 月 4 日。
- **資料欄位：** 學年期、系所、課程名稱、年級、學分、必選修、授課教師、已選課人數／餘額、時間與教室，以及課綱連結等。
- **網頁資料處理：** 專題報告說明採用 Beautiful Soup、Requests 蒐集資料，將課程網頁保存為 HTML，再解析其中的課程表格；儲存庫中的 `crawler.py` 主要負責**解析已下載的 HTML 表格**，並彙整輸出 CSV，而非提供完整的線上下載流程。
- **資料清理：** 依學年期及系所拆分資料、排除部分體育與服務學習課程、處理教師與選課人數等欄位的缺失值，並將預測學期與歷史學期資料分開保存。

### 選課人數預測：三種方法

| 方法 | 核心概念 | 實作重點 |
| --- | --- | --- |
| 方法一 | 歷史時間特徵與隨機森林集成 | 使用歷年選課人數、餘額、學年期等資訊，強調近期資料，結合 **5 個 Random Forest 模型**進行預測 |
| 方法二 | 依歷史學期加權平均 | 配對相同課程名稱的歷年紀錄，排除待預測學期，按學期先後設定倒數排名權重並正規化，再預測 113-1、113-2 的選課人數；歷史資料不足的課程不予預測 |
| 方法三 | 多特徵 Random Forest Regression | 加入課程類別、分班、必選修、教師、學分、年級與學期等特徵，進行 One-Hot Encoding，並以 Bagging 集成 **10 個 Random Forest Regressor** |

報告指出方法一未充分對應 113-1／113-2 實際開課清單，因此未將其初步評估結果視為可靠的最終比較依據；後續分析主要著重方法二與方法三。模型評估使用 **MSE、MAE**，並比較實際與預測的選課人數。

### 課程熱門度分類

以已選課人數占總名額的比例作為熱門度基礎：

$$
\text{Popularity Ratio} = \frac{\text{已選課人數}}{\text{已選課人數} + \text{剩餘名額}}
$$


- **高熱門度：** 高於第 75 百分位數。
- **中熱門度：** 介於第 25 與第 75 百分位數。
- **低熱門度：** 低於第 25 百分位數。
- **分類調整：** 比較固定分位數閾值與使用 **Optuna** 調整閾值的方式；程式亦探索將選課比例與剩餘名額轉換後進行加權的熱門度定義。
- **評估指標：** Confusion Matrix、Accuracy、Recall、F1-score。

### 新開課程選課情形預測

對沒有足夠歷史紀錄的新課程，進一步透過**課程主題特徵標註**建立迴歸模型：

1. 以 `Cleaning_Data.ipynb`、`Data_analysis.ipynb` 清理並檢視課程資料。
2. 透過 `fill_new_features.py` 的 **Tkinter GUI**，對數學、統計、資訊及測量等主題進行人工特徵勾選。
3. 以 `predict.ipynb` 使用 **RandomForestRegressor**（100 棵樹，80%／20% 訓練測試切分）預測選課比例，並匯出 `rf_model.pkl`。
4. 以 `predict_course.py` 提供課程特徵勾選介面，使用已儲存模型預測比例，並透過 **Cosine Similarity** 尋找特徵相近的既有課程。

這一部分預測的主要目標是 **已選課人數／（已選課人數＋餘額）的百分比**，而非直接預測確切的選課人數。`predict_course.py` 的互動介面可讓使用者勾選新課程主題，顯示預測選課比例，並使用 Cosine Similarity 列出 **5 門特徵最相近的既有課程**，作為新課程規劃與課程探索的初步參考。這個介面需要事先準備 `rf_model.pkl` 與 `enhanced_math_course_data.csv`。

### 實驗結果與觀察

以下為 Notebook **保存的輸出紀錄**，並非重新執行或重新驗證後的結果：

| 實驗項目 | 指標 | 紀錄結果 |
| --- | --- | ---: |
| 113-2 課程熱門度分類（`accuracy.ipynb`） | Accuracy | **0.38** |
| 113-2 課程熱門度分類（`accuracy.ipynb`） | Weighted F1-score | **0.37** |
| 113-2 選課人數預測（`accuracy.ipynb`） | MAE | **19.55 人** |
| 113-2 選課人數預測（`accuracy.ipynb`） | MSE | **909.80** |
| 新開課程選課比例預測（`predict.ipynb`） | R² | **0.2755** |
| 新開課程選課比例預測（`predict.ipynb`） | MSE | **324.51** |

**結果解讀：** 課程需求受到開課學期、名額上限、修課規定及選課階段等因素影響。報告指出 113-2 資料蒐集時選課人數仍可能變動，因而影響人數預測的評估結果；另外，「額滿」不一定代表真正熱門，部分必修課也可能因修課要求而有較高選課比例，因此僅以選課比例建立熱門度標籤仍有侷限。新開課程模型的 R² 約為 **0.276**，顯示目前特徵只能解釋部分選課比例變異，仍受到主題標註品質、課程容量及未納入教師、修課條件等因素的限制。

## 團隊分工與參考資料

### 期末專題: 課程選課人數預測系統

依據期末專題報告：

| 組員 | 報告記載的主要分工 |
| --- | --- |
| 施淳譯 | 資料爬蟲、方法二及方法三實作、報告撰寫、簡報製作與口頭報告 |
| 蔡譯潁 | 課程特徵勾選與預測方法實作、報告撰寫、簡報製作與口頭報告 |
| 陳亭蓁 | 資料爬蟲、方法一實作、報告撰寫及簡報製作 |

### 原始報告與延伸資源

- `課程選課人數預測/ChenPolo_FinalProject_Report.pdf` — 課程人數預測系統期末報告。
- `課程選課人數預測/Chenpolo_FinalProject_Slides.pdf` — 期末專題簡報。
- `集成學習應用於二元分類任務/Chen Polo CP1 report.pdf` — Competition 1 技術與競賽成果報告。
- [課程人數預測系統 Demo 影片](https://youtu.be/yG_qT8fr9iY?si=yKth5gwhPxBzTqoa)
- [scikit-learn Documentation](https://scikit-learn.org/stable/)
- [Optuna Documentation](https://optuna.readthedocs.io/)
- [imbalanced-learn Documentation](https://imbalanced-learn.org/stable/)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)
- [LightGBM Documentation](https://lightgbm.readthedocs.io/)
- [CatBoost Documentation](https://catboost.ai/)