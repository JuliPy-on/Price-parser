# 🛍️ Price Parser

**Price Parser** is a simple yet powerful Python script designed to scrape product data from a test e-commerce site. It extracts product names, prices, categories, and links, then saves them into a CSV file and logs the process step by step.

## 🚀 Features

- 🔍 Extracts product titles, prices, categories, and links
- 📄 Saves data to `products.csv`
- 🌐 Supports pagination (multiple pages)
- 🧠 Error handling and logging to `parser.log`
- 🕓 Includes delay between requests for polite scraping

## 🧰 Technologies Used

- [`requests`](https://docs.python-requests.org/)
- [`BeautifulSoup`](https://www.crummy.com/software/BeautifulSoup/)
- [`pandas`](https://pandas.pydata.org/)
- Python standard libraries: `logging`, `typing`, `pathlib`

## 📦 Installation and Usage

1. **Clone the repository**:

```bash
git clone https://github.com/JuliPy-on/Price-parser.git
cd Price-parser
```

2. **(Optional) Create and activate a virtual environment**:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install the dependencies**:

```bash
pip install -r requirements.txt
```

4. **Run the script**:

```bash
python main.py
```

## 📝 Output

- The scraped data will be saved in `products.csv`.
- All logs will be recorded in `parser.log`.

## 📂 Configuration

You can adjust the scraping behavior by modifying the `CONFIG` dictionary in `main.py`. For example, you can change the base URL, headers, number of pages to scrape, timeout, or output file name.

## ⚠️ Disclaimer

This script is intended for educational and testing purposes only. Please do not use it to scrape real websites without permission.

---


