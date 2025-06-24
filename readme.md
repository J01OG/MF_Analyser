# 📊 Mutual Fund Holdings Analyzer

A powerful desktop-friendly Streamlit application to **track**, **analyze**, and **visualize mutual fund portfolios** month-wise using Excel files. This project is split into two core modules:

---

## 📁 1. Excel Preprocessor App

**Purpose:**  
Convert individual monthly Excel files (each containing one month's mutual fund portfolio) into a **cleaned, combined format** ready for analysis.

### ✅ Features:
- Upload multiple `.xls` / `.xlsx` files.
- Assign the correct **month-year** (e.g., `Jan 2024`) for each file manually.
- Automatically cleans, formats, and merges data.
- Standardizes column names across inconsistent Excel files.
- Download the final **combined Excel file**.

### 📦 How to Use:
```bash
streamlit run preprocessor_app.py


1. Upload Excel files (one per month).
2. Assign the correct month from dropdowns.
3. Preview cleaned data.
4. Click **Download Combined Excel** to get your merged sheet.

---

## 📈 2. Mutual Fund Analytics Dashboard

**Purpose:**
Visualize mutual fund holdings over time for selected stocks across months.

### ✅ Features:

* Upload a **combined Excel file** (from the preprocessor).
* Select one or more stocks.
* Choose from 3 chart types: **Line**, **Bar**, **Area**.
* View 3 metrics separately:

  * `% to Net Assets`
  * `Quantity`
  * `Market value (Rs. In lakhs)`
* Automatically sorts months (e.g., Jan → Dec).
* Downloadable raw data table.

### 📦 How to Use:

```bash
streamlit run app.py
```

1. Upload the cleaned file (from the Preprocessor App).
2. Select stocks and months to analyze.
3. View graphs for all 3 metrics.
4. Toggle between chart types in sidebar.
5. Export the raw table if needed.

---

## 🖥 Packaging as a Desktop App (Optional)

Use `pyinstaller` to convert to `.exe`:

```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --console app.py
```

Then double-click the `.exe` file from the `dist/` folder to launch it like a regular app.

---

## 📂 File Structure

```
├── app.py                   # Analytics dashboard
├── preprocessor_app.py      # Preprocessing app for Excel merging
├── combined_mutual_fund_data.xlsx  # Sample output from preprocessor
├── README.md
```

---

## ✨ Coming Soon (Ideas)

* Google Sheets integration
* Stock-wise performance comparison
* Year-over-year summary exports
* Export to PDF charts

---

## 🧠 Built With

* [Streamlit](https://streamlit.io/)
* [Pandas](https://pandas.pydata.org/)
* [Plotly Express](https://plotly.com/python/plotly-express/)

---

## 🙌 Author

**Jayash Prem**
Feel free to modify or contribute!
mail me at jayashprem27@gmail.com

