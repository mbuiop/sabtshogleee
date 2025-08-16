from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# مسیر فایل‌ها
DATA_FILE = os.path.join('data', 'services.json')
REQUESTS_FILE = os.path.join('data', 'requests.json')
MESSAGE_FILE = os.path.join('data', 'm.txt')

# دسته‌بندی‌های شغلی
CATEGORIES = [
    'تعمیرات منزل', 'نظافت و خانه‌داری', 'حمل و نقل', 'آموزش خصوصی',
    'طراحی و گرافیک', 'برنامه‌نویسی', 'مشاوره حقوقی', 'مشاوره مالی',
    'خدمات زیبایی', 'خدمات پزشکی', 'خدمات الکترونیکی', 'باغبانی',
    'نگهداری از کودک', 'نگهداری از حیوانات', 'خدمات آشپزی', 'خدمات خیاطی',
    'عکاسی و فیلمبرداری', 'خدمات ساختمانی', 'خدمات خودرو', 'سایر خدمات'
]

# ایجاد پوشه و فایل‌های داده اگر وجود نداشته باشند
if not os.path.exists('data'):
    os.makedirs('data')

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

if not os.path.exists(REQUESTS_FILE):
    with open(REQUESTS_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

def read_secret_message():
    try:
        with open(MESSAGE_FILE, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return "پیام همگانی (فایل m.txt یافت نشد)"

def save_service(service):
    services = get_services()
    services.append(service)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(services, f, ensure_ascii=False, indent=2)

def get_services():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_request(req):
    requests = get_requests()
    requests.append(req)
    with open(REQUESTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(requests, f, ensure_ascii=False, indent=2)

def get_requests():
    if os.path.exists(REQUESTS_FILE):
        with open(REQUESTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def get_services_by_category(category):
    services = get_services()
    return [s for s in services if s['category'] == category]

@app.route('/')
def index():
    secret_message = read_secret_message()
    return render_template('index.html', 
                         secret_message=secret_message,
                         categories=CATEGORIES)

@app.route('/search')
def search():
    category = request.args.get('category', '')
    query = request.args.get('query', '')
    
    services = get_services()
    
    if category:
        services = [s for s in services if s['category'] == category]
    
    if query:
        query = query.lower()
        services = [s for s in services if 
                   query in s['title'].lower() or 
                   query in s['description'].lower()]
    
    return render_template('search.html', 
                         services=services,
                         categories=CATEGORIES,
                         selected_category=category)

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
        flash('خدمت شما با موفقیت ثبت شد!', 'success')
        return redirect(url_for('add_service'))
    
    return render_template('add_service.html', categories=CATEGORIES)

@app.route('/add_request', methods=['GET', 'POST'])
def add_request():
    if request.method == 'POST':
        job_type = request.form.get('job_type')
        description = request.form.get('description')
        category = request.form.get('category')
        contact = request.form.get('contact')
        
        new_request = {
            'id': len(get_requests()) + 1,
            'job_type': job_type,
            'description': description,
            'category': category,
            'contact': contact,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        save_request(new_request)
        
        # بررسی آیا خدمتی با این دسته‌بندی وجود دارد
        matching_services = get_services_by_category(category)
        
        flash('درخواست شما ثبت شد!', 'success')
        return render_template('add_request.html', 
                             categories=CATEGORIES,
                             matching_services=matching_services)
    
    return render_template('add_request.html', categories=CATEGORIES)

if __name__ == '__main__':
    app.run(debug=True)
