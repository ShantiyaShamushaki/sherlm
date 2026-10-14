import re

def load_titles(list_file):
    """بارگذاری عنوان‌های غزل‌ها از فایل لیست"""
    titles = {}
    with open(list_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # الگو: غزل شمارهٔ ۱ : عنوان
            match = re.match(r'^غزل\s+شمارهٔ\s*([۰-۹0-9]+)\s*:\s*(.+)$', line)
            if match:
                num = match.group(1)
                title = match.group(2).strip()
                titles[num] = title
    return titles


def normalize_num(num):
    """تبدیل اعداد فارسی به انگلیسی برای مقایسه"""
    fa = '۰۱۲۳۴۵۶۷۸۹'
    en = '0123456789'
    return ''.join(en[fa.index(c)] if c in fa else c for c in num)


def process_ghazals(raw_file, list_file, output_file):
    # ۱. بارگذاری عنوان‌ها
    titles = load_titles(list_file)
    # نسخه نرمال‌شده برای جستجو
    titles_norm = {normalize_num(k): v for k, v in titles.items()}

    # ۲. خواندن فایل خام
    with open(raw_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # ۳. حذف خطوط جداکننده (---)
    text = re.sub(r'^\s*-{3,}\s*$', '', text, flags=re.MULTILINE)

    # ۴. پیدا کردن همه شروع غزل‌ها
    pattern = re.compile(r'^غزل\s+شمارهٔ\s*([۰-۹0-9]+)\s*$', re.MULTILINE)
    matches = list(pattern.finditer(text))

    poems = []
    for i, match in enumerate(matches):
        num = match.group(1)
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end]

        # پاک‌سازی: حذف خطوط خالی و فاصله‌های اضافی
        lines = []
        for line in body.split('\n'):
            line = line.strip()
            if line:
                # حذف فاصله‌های اضافی داخل خط
                line = re.sub(r'\s{2,}', ' ', line)
                lines.append(line)

        body_clean = '\n'.join(lines)

        # عنوان از لیست
        num_norm = normalize_num(num)
        title = titles_norm.get(num_norm, f'غزل شمارهٔ {num}')

        if body_clean:
            poems.append((title, body_clean))

    # ۵. نوشتن خروجی
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, (title, body) in enumerate(poems):
            f.write(f'# {title}\n')
            f.write(body + '\n')
            # جداکننده بین غزل‌ها (به جز آخرین)
            if i < len(poems) - 1:
                f.write('---\n')

    print(f'تعداد غزل‌های پردازش‌شده: {len(poems)}')
    return poems


# اجرا
poems = process_ghazals(
    raw_file='data/hafez_ghazal_raw.txt',
    list_file='data/hafez_ghazal_list.txt',
    output_file='data/hafez_ghazal_clean.txt'
)

# نمایش نمونه
print('\n--- نمونه خروجی ---')
for title, body in poems[:2]:
    print(f'# {title}')
    print(body[:200] + '...')
    print('---')