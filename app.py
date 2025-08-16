from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # برای session ها لازم است

# مسیر فایل داده‌ها
DATA_FILE = os.path.join('data', 'services.json')
MESSAGE_FILE = os.path.join('data', 'm.txt')  # فایل پیام مخفی

# ایجاد فایل داده‌ها اگر وجود نداشته باشد
if not os.path.exists('data'):
    os.makedirs('data')

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

# خواندن پیام مخفی
def read_secret_message():
    try:
        with open(MESSAGE_FILE, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return "پیام همگانی (فایل m.txt یافت نشد)"

# ذخیره خدمات جدید
def save_service(service):
    services = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            services = json.load(f)
    
    services.append(service)
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(services, f, ensure_ascii=False, indent=2)

# خواندن همه خدمات
def get_services():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# روت‌های اصلی
@app.route('/')
def index():
    secret_message = read_secret_message()
    return render_template('index.html', secret_message=secret_message)

@app.route('/search')
def search():
    services = get_services()
    return render_template('search.html', services=services)

@app.route('/add_service', methods=['GET', 'POST'])
def add_service():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        contact = request.form.get('contact')
        category = request.form.get('category')
        
        new_service = {
            'id': len(get_services()) + 1,
            'title': title,
            'description': description,
            'contact': contact,
            'category': category,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        save_service(new_service)
        return redirect(url_for('search'))
    
    return render_template('add_service.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)
