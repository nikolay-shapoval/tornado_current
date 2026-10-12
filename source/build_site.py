"""Build a portable static website from recovered content. Python standard library only."""
from pathlib import Path
from html import escape
from urllib.parse import quote
from collections import Counter
import json
import re
import shutil

SOURCE = Path(__file__).resolve().parent
ROOT = SOURCE.parent
DIST = ROOT / 'docs'
REPORTS = ROOT / 'build-reports'
REPORTS.mkdir(exist_ok=True)
DATA = json.loads((SOURCE / 'content.json').read_text(encoding='utf-8'))
CATS = DATA['categories']
DIST.mkdir(exist_ok=True)
shutil.copytree(ROOT / 'assets', DIST / 'assets', dirs_exist_ok=True)
for name in ['styles.css', 'app.js']:
    shutil.copyfile(SOURCE / name, DIST / 'assets' / name)

def e(value):
    return escape(str(value), quote=True)

def link(slug, depth):
    return '../' * depth + (slug + '/index.html' if slug else 'index.html')

def asset(name, depth):
    return '../' * depth + 'assets/' + name

def arrow():
    return '<span aria-hidden="true">↗</span>'

def header(slug, depth):
    items = ''.join(f'<a href="{e(link(c["slug"], depth))}">{e(c["title"])}</a>' for c in CATS)
    symbol = f'<img class="brand-symbol" src="{e(asset(DATA["brand_symbol"], depth))}" alt="">' if DATA.get('brand_symbol') else ''
    brand = symbol + '<span class="brand-name"><span>ПИЩЕВЫЕ</span><strong>механизмы</strong></span>'
    return f'''<a class="skip-link" href="#content">Перейти к содержимому</a>
    <header class="header"><div class="header-inner">
      <a class="brand" href="{e(link('', depth))}">{brand}</a>
      <button class="menu-button" type="button" aria-label="Открыть меню" aria-expanded="false" aria-controls="navigation"><span></span><span></span><span></span></button>
      <nav id="navigation" class="navigation" aria-label="Основная навигация">
        <a href="{e(link('', depth))}" {'aria-current="page"' if not slug else ''}>Главная</a>
        <details class="catalog-dropdown"><summary>Оборудование <span aria-hidden="true">⌄</span></summary><div class="dropdown-panel"><a class="dropdown-all" href="{e(link('оборудование', depth))}">Весь каталог {arrow()}</a>{items}</div></details>
        <a href="{e(link('проекты', depth))}">Наши работы</a><a href="{e(link('контакты', depth))}">Контакты</a>
      </nav>
      <a class="header-phone" href="tel:{DATA['phone_digits']}">{DATA['phone']}</a>
    </div></header>'''

def footer(depth):
    return f'''<section class="contact-strip"><div class="container strip-inner"><div><span class="eyebrow light">Обсудим вашу задачу</span><h2>Подберём решение для производства.</h2></div><a class="button light-button" href="tel:{DATA['phone_digits']}">{DATA['phone']} {arrow()}</a></div></section>
      <footer class="footer"><div class="container footer-top"><div><strong>Пищевые механизмы</strong><p>{DATA['owner']} · {DATA['city']}</p></div><div class="footer-links"><a href="{e(link('оборудование', depth))}">Оборудование</a><a href="{e(link('проекты', depth))}">Наши работы</a><a href="{e(link('контакты', depth))}">Контакты</a></div></div><div class="container footer-bottom"><span>Оборудование для пищевой промышленности</span><a href="{e(link('политика-конфиденциальности', depth))}">Политика конфиденциальности</a></div></footer>
      <dialog id="image-dialog" class="image-dialog"><button type="button" class="dialog-close" aria-label="Закрыть изображение">×</button><img src="" alt=""><p></p></dialog>'''

def document(title, body, slug='', depth=0, description='Оборудование для пищевой промышленности: проектирование, изготовление и ремонт.'):
    canonical = ''
    if DATA.get('site_url'):
        canonical_slug = '' if slug == 'index' else slug
        url = DATA['site_url'].rstrip('/') + '/' + (quote(canonical_slug) + '/' if canonical_slug else '')
        canonical = f'<link rel="canonical" href="{e(url)}">'
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{e(description)}"><title>{e(title)} — Пищевые механизмы</title>{canonical}<link rel="stylesheet" href="{e(asset('styles.css', depth))}"><script defer src="{e(asset('app.js', depth))}"></script></head><body>{header(slug, depth)}<main id="content">{body}</main>{footer(depth)}</body></html>'''

def category_card(c, depth, number=None):
    if c['image']:
        visual = f'<img src="{e(asset(c["image"], depth))}" alt="{e(c["title"])}" loading="lazy">'
    else:
        visual = f'<div class="typographic-visual"><span>{e(c["group"])}</span><strong>{e(c["title"])}</strong><span class="drawing-lines" aria-hidden="true"></span></div>'
    return f'''<a class="category-card" href="{e(link(c['slug'], depth))}" data-group="{e(c['group'])}" data-search="{e(c['title'] + ' ' + c['description'] + ' ' + c.get('body', '') + ' ' + c.get('verbatim_body', ''))}"><div class="category-image">{visual}<span class="card-number">{number:02d}</span></div><div class="category-card-body"><span class="eyebrow">{e(c['group'])}</span><h3>{e(c['title'])} {arrow()}</h3><p>{e(c['description'])}</p></div></a>'''

def home_category(c, depth):
    image = f'<img src="{e(asset(c["image"], depth))}" alt="{e(c["title"])}" loading="lazy">' if c['image'] else ''
    return f'<a class="home-category" href="{e(link(c["slug"], depth))}"><div class="home-category-heading"><h2>{e(c["title"])}</h2>{arrow()}</div><div class="home-category-image">{image}</div></a>'

def home(depth=0):
    cards = ''.join(home_category(c, depth) for c in CATS)
    return f'''<section class="container home-heading"><span class="eyebrow">{e(DATA['owner'])} · {e(DATA['city'])}</span><h1>Предлагаем оборудование</h1><p>Проектирование, изготовление и ремонт оборудования для пищевой промышленности.</p></section>
      <section class="container home-catalog" aria-label="Разделы оборудования"><div class="home-category-grid">{cards}</div></section>
      <section class="container section about-grid home-about"><div><span class="eyebrow">Наши работы</span><h2>От чертежа<br>до работающего механизма.</h2></div><div><p class="large-text">Конструкторское бюро и производственная площадка для изготовления пищевого оборудования по желанию заказчика.</p><p>Разработка, производство, запуск и обслуживание предприятий. Импортозамещающее оборудование и запасные части к импортным машинам.</p><a class="text-link" href="{e(link('проекты', depth))}">Подробнее о нашей работе →</a></div></section>'''

def breadcrumbs(title, depth):
    return f'<div class="breadcrumbs"><a href="{e(link("", depth))}">Главная</a><span>/</span><a href="{e(link("оборудование", depth))}">Оборудование</a><span>/</span><span>{e(title)}</span></div>'

def catalog(depth):
    cards = ''.join(category_card(c, depth, i + 1) for i, c in enumerate(CATS))
    groups = ['Все'] + list(dict.fromkeys(c['group'] for c in CATS))
    buttons = ''.join(f'<button class="filter-button {"selected" if i == 0 else ""}" type="button" data-filter="{e(g)}" aria-pressed="{"true" if i == 0 else "false"}">{e(g)}</button>' for i, g in enumerate(groups))
    return f'''<section class="container page-heading"><div class="breadcrumbs"><a href="{e(link('', depth))}">Главная</a><span>/</span><span>Оборудование</span></div><span class="eyebrow">Каталог</span><h1>Оборудование<br>для вашего производства.</h1><p>Машины для подготовки, обработки, перемешивания, перемещения и упаковки пищевых продуктов.</p></section><section class="container section catalog-section"><div class="catalog-controls"><label class="search-field"><span class="sr-only">Поиск по оборудованию</span><span aria-hidden="true">⌕</span><input id="catalog-search" type="search" placeholder="Название оборудования или модель" autocomplete="off"></label><div class="filters" aria-label="Группы оборудования">{buttons}</div></div><p id="catalog-count" class="catalog-count" aria-live="polite">Разделов: {len(CATS)}</p><div class="catalog-grid">{cards}</div><p class="empty-search" hidden>Ничего не найдено. Попробуйте другое название или позвоните нам.</p></section>'''

def render_recovered(body):
    """Preserve recovered facts and units; render simple headings, lists and spec rows."""
    output, rows, bullets = [], [], []
    def flush():
        if rows:
            output.append('<div class="spec-table-wrap"><table class="spec-table"><tbody>' + ''.join(f'<tr><th scope="row">{e(k)}</th><td>{e(v)}</td></tr>' for k, v in rows) + '</tbody></table></div>')
            rows.clear()
        if bullets:
            output.append('<ul class="body-list">' + ''.join(f'<li>{e(x)}</li>' for x in bullets) + '</ul>')
            bullets.clear()
    for raw in body.splitlines():
        line = raw.strip()
        if not line or line.startswith('+7') or line == '(C) Все права защищены. 2024' or 'Image' in line:
            continue
        if line.startswith('# '):
            continue
        if re.match(r'^#+\s*$', line) or line == '*':
            continue
        if line.startswith('##'):
            flush()
            title = line.lstrip('#').strip()
            output.append('<h2>' + e(title) + '</h2>')
            continue
        if line.startswith(('- ', '* ', '-УПБ')):
            if rows:
                flush()
            bullets.append(line.lstrip('-*').strip())
            continue
        if bullets:
            flush()
        if line.endswith(':'):
            flush()
            if line not in ['Потребление энергии:', 'Описание:', 'Техническая спецификация:']:
                output.append('<h3>' + e(line[:-1]) + '</h3>')
            continue
        spec = re.match(r'^([^:]{1,100}):\s*(.+)$', line)
        if spec and spec[1] not in ['Описание', 'Принцип работы']:
            rows.append((spec[1], spec[2]))
        else:
            flush()
            output.append('<p>' + e(line) + '</p>')
    flush()
    return '<div class="recovered-body">' + ''.join(output) + '</div>'

ASSET_CAPTIONS = {x['file'].removeprefix('assets/'): x['caption'] for x in DATA['assets']}
def gallery(names, depth):
    if not names:
        return ''
    pictures = ''.join(f'<button class="gallery-item" type="button" data-image="{e(asset(name, depth))}" data-caption="{e(ASSET_CAPTIONS.get(name, "Оборудование"))}"><img src="{e(asset(name, depth))}" alt="{e(ASSET_CAPTIONS.get(name, "Оборудование"))}" loading="lazy"><span>{e(ASSET_CAPTIONS.get(name, "Оборудование"))} {arrow()}</span></button>' for name in names)
    return f'<section class="gallery-section"><h2>Фото и схемы</h2><div class="gallery-grid">{pictures}</div></section>'

def render_verbatim(body):
    # All text and punctuation stay unchanged. Only CRLF becomes an HTML newline.
    lines = body.replace('\r\n', '\n').split('\n')
    formatted = []
    for i, line in enumerate(lines):
        value = e(line)
        if i == 0 or line.endswith(':') or line.startswith(('Стоимость изготовления', 'Срок изготовления', 'Линия упаковки льда')):
            value = '<strong>' + value + '</strong>'
        formatted.append(value)
    return '<div class="source-document">' + '\n'.join(formatted) + '</div>'

def video_section(c, depth):
    clips = []
    for v in c.get('videos', []):
        href = e(asset(v['file'], depth))
        poster = f' poster="{e(asset(v["poster"], depth))}"' if v.get('poster') else ''
        clips.append(f'<figure class="video-card"><video controls playsinline preload="metadata"{poster} aria-label="{e(v["title"])}"><source src="{href}" type="video/mp4">Ваш браузер не поддерживает видео. <a href="{href}">Скачать видео</a></video><figcaption><span>{e(v["title"])}</span><a href="{href}" download>Скачать видео ↓</a></figcaption></figure>')
    external = c.get('external_video')
    if external:
        clips.append(f'<p><a class="text-link" href="{e(external["url"])}" target="_blank" rel="noopener">{e(external["title"])} ↗</a></p>')
    return '<section class="video-section"><h2>Видео работы</h2><div class="video-grid">' + ''.join(clips) + '</div></section>' if clips else ''

def product(c, depth):
    image = f'<div class="product-visual"><img src="{e(asset(c["image"], depth))}" alt="{e(c["title"])}"></div>' if c['image'] else f'<div class="product-visual text-visual"><span class="eyebrow">{e(c["group"])}</span><strong>Пищевые<br>механизмы.</strong><span class="round-arrow" aria-hidden="true">↗</span></div>'
    hero = f'<section class="container product-heading">{breadcrumbs(c["title"], depth)}<div class="product-hero"><div><span class="eyebrow">{e(c["group"])}</span><h1>{e(c["title"])}</h1><p>{e(c["description"])}</p><a class="button" href="{e(link("контакты", depth))}">Обсудить оборудование {arrow()}</a></div>{image}</div></section>'
    specs = ''
    if c['specs']:
        specs = '<section><h2>Характеристики</h2><div class="spec-table-wrap"><table class="spec-table"><tbody>' + ''.join(f'<tr><th scope="row">{e(k)}</th><td>{e(v)}</td></tr>' for k, v in c['specs']) + '</tbody></table></div></section>'
    body = render_recovered(c['body']) if c['body'] else ''
    if c.get('verbatim_body'):
        body = render_verbatim(c['verbatim_body'])
    for section in c.get('historical_sections', []):
        body += f'<details class="historical-section"><summary>{e(section["title"])}</summary><p>{e(section["intro"])}</p>{render_recovered(section["body"])}</details>'
    if not specs and not body:
        body = '<section><h2>Обсудить конфигурацию</h2><p>Расскажите, с каким продуктом вы работаете, какая производительность требуется и где планируется разместить оборудование. Позвоните, чтобы обсудить вашу задачу.</p></section>'
    side = f'<aside class="product-aside"><span class="eyebrow">Пищевые механизмы</span><h3>Есть задача<br>для производства?</h3><p>Обсудим продукт, требуемую производительность и компоновку оборудования.</p><a href="tel:{DATA["phone_digits"]}">{DATA["phone"]}</a><a class="text-link" href="{e(link("контакты", depth))}">Контакты →</a></aside>'
    supplier_images = {x['file'].removeprefix('assets/') for x in DATA['assets'] if x.get('kind') == 'manufacturer publication image'}
    attribution = f'<p class="image-credit">Дополнительные фото и схемы: <a href="{e(DATA["supplier_publication"])}" target="_blank" rel="noopener">публикация производителя на Foodretail</a>.</p>' if supplier_images.intersection(c['gallery'] + [c['image']]) else ''
    other = [x for x in CATS if x['group'] == c['group'] and x['slug'] != c['slug']][:3]
    related = ''.join(f'<a href="{e(link(x["slug"], depth))}">{e(x["title"])} {arrow()}</a>' for x in other)
    return hero + f'<section class="container section product-content"><div>{specs}{body}{video_section(c, depth)}{gallery(c["gallery"], depth)}{attribution}</div>{side}</section>' + (f'<section class="container section related-section"><span class="eyebrow">Другие разделы</span><div class="related-links">{related}</div></section>' if related else '')

def projects(depth):
    photos = ['production-line.webp', 'mixing-vessel.webp', 'mushroom-machine.webp', 'inclined-conveyor.webp', 'vertical-conveyor.webp', 'mixing-drum.webp']
    return f'<section class="container page-heading"><div class="breadcrumbs"><a href="{e(link("", depth))}">Главная</a><span>/</span><span>Наши работы</span></div><span class="eyebrow">Проектирование и производство</span><h1>От идеи до готового<br>оборудования.</h1><p>Производство и ремонт пищевого оборудования с 2005 года.</p></section><section class="container section about-grid"><div><h2>Конструкторское бюро.<br>Производственная площадка.</h2></div><div>{render_recovered(DATA["projects_body"])}</div></section><section class="container section">{gallery(photos, depth)}<p class="image-credit">Фото и схемы оборудования из <a href="{e(DATA["supplier_publication"])}" target="_blank" rel="noopener">публикации производителя на Foodretail</a>.</p></section>'

def contacts(depth):
    details = f'<p>{e(DATA.get("address", DATA["city"]))}</p>'
    if DATA.get('email'):
        details += f'<p><a class="text-link" href="mailto:{e(DATA["email"])}">{e(DATA["email"])}</a></p>'
    return f'<section class="container page-heading"><div class="breadcrumbs"><a href="{e(link("", depth))}">Главная</a><span>/</span><span>Контакты</span></div><span class="eyebrow">Связаться с нами</span><h1>Начнём с вашей задачи.</h1><p>Обсудим оборудование, продукт и требования к производству.</p></section><section class="container section contacts-grid"><div class="contact-card"><span class="eyebrow">Телефон</span><a class="contact-number" href="tel:{DATA["phone_digits"]}">{DATA["phone"]}</a><div class="hero-actions"><a class="button" href="tel:{DATA["phone_digits"]}">Позвонить {arrow()}</a><button type="button" class="copy-phone" data-copy="{DATA["phone_digits"]}">Скопировать номер</button></div><p class="copy-status" role="status" aria-live="polite"></p></div><div class="contact-details"><span class="eyebrow">Пищевые механизмы</span><h2>{e(DATA["owner"])}</h2>{details}<h3>Что поможет обсудить проект</h3><ul class="body-list"><li>Продукт и этап его обработки.</li><li>Требуемая производительность.</li><li>Размеры помещения и условия размещения.</li><li>Связь с другими машинами в линии.</li></ul></div></section>'

def privacy(depth):
    blocks = []
    for line in (SOURCE / 'privacy.txt').read_text(encoding='utf-8').splitlines():
        if line.startswith('## '):
            blocks.append('<h2>' + e(line[3:]) + '</h2>')
        elif line.strip():
            blocks.append('<p>' + e(line) + '</p>')
    sources = [
        ('152-ФЗ «О персональных данных»', 'https://mintrud.gov.ru/docs/laws/130'),
        ('Политика конфиденциальности GitHub', 'https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement'),
        ('Технические данные на GitHub Pages', 'https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages#data-collection'),
    ]
    references = ''.join(f'<li><a href="{e(url)}" target="_blank" rel="noopener">{e(title)}</a></li>' for title, url in sources)
    return f'<section class="container page-heading privacy-heading"><div class="breadcrumbs"><a href="{e(link("", depth))}">Главная</a><span>/</span><span>Политика конфиденциальности</span></div><h1>Политика<br>конфиденциальности.</h1><p>Политика обработки персональных данных. Редакция от 12.10.2026.</p></section><section class="container section privacy-body">{"".join(blocks)}<div class="policy-references"><h2>Упомянутые документы</h2><ul class="body-list">{references}</ul></div></section>'

pages = [('', 'Главная', home(0)), ('оборудование', 'Оборудование', catalog(1)),
         ('проекты', 'Наши работы', projects(1)), ('контакты', 'Контакты', contacts(1)),
         ('политика-конфиденциальности', 'Политика конфиденциальности', privacy(1))]
pages.extend((c['slug'], c['title'], product(c, 1)) for c in CATS)
for slug, title, body in pages:
    path = DIST / slug / 'index.html' if slug else DIST / 'index.html'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(document(title, body, slug, 1 if slug else 0), encoding='utf-8')
(DIST / 'index').mkdir(exist_ok=True)
(DIST / 'index' / 'index.html').write_text(document('Главная', home(1), 'index', 1), encoding='utf-8')
page_lookup = {slug: (title, body) for slug, title, body in pages}
for alias, canonical in DATA.get('legacy_routes', {}).items():
    title, body = page_lookup[canonical]
    path = DIST / alias / 'index.html'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(document(title, body, canonical, 1), encoding='utf-8')

status_labels = {'indexed_text': 'Текст поискового индекса', 'fragment': 'Фрагменты выдачи',
                 'supplemented': 'Название сайта + публикация производителя',
                 'title_only': 'Подтверждено название; текста нет',
                 'assembled_from_catalog': 'Сохранённый каталог и отдельная архивная страница',
                 'database_snapshot': 'Полный опубликованный текст из локального снимка БД',
                 'email_content': 'Оригинальные описания, характеристики и фото из писем владельца',
                 'email_media': 'Оригинальные фото и видео из писем владельца',
                 'fragment_with_original_image': 'Подтверждённые фрагменты и оригинальное изображение из БД'}
statuses = [dict(slug=c['slug'], title=c['title'], status=c['status'],
                 status_label=status_labels[c['status']], sources=c['sources'],
                 original_url_confirmed=c['original_url_confirmed'], notes=c['notes'],
                 local_file='../docs/' + c['slug'] + '/index.html') for c in CATS]
statuses.extend([
    {'slug': '', 'title': 'Главная', 'status': 'archived_html_and_indexed_text', 'status_label': 'Архивный HTML и более свежая выдача', 'original_url_confirmed': True, 'notes': 'Оформление создано заново; оригинальный HTML отдельно в html/.', 'local_file': '../docs/index.html'},
    {'slug': 'оборудование', 'title': 'Оборудование', 'status': 'indexed_text', 'status_label': 'Текст поискового индекса', 'original_url_confirmed': True, 'notes': 'Описание фритюрниц перенесено в отдельную локальную страницу /фритюрницы.', 'local_file': '../docs/оборудование/index.html'},
    {'slug': 'проекты', 'title': 'Наши работы', 'status': 'database_snapshot', 'status_label': 'Полный текст из локального снимка БД от 15.05.2024', 'original_url_confirmed': True, 'notes': 'Восстановлены введение и полный перечень разработанного оборудования. Исходник сохранён в database-public/.', 'local_file': '../docs/проекты/index.html'},
    {'slug': 'контакты', 'title': 'Контакты', 'status': 'email_content', 'status_label': 'Телефон, адрес и email подтверждены исходными материалами', 'original_url_confirmed': True, 'notes': 'Телефон подтверждён архивом и письмами. Адрес и email из ЛУ-5-200.docx; имя ИП Зурначёв А.А. подтверждено владельцем. Работают tel:, mailto: и копирование номера. Отправка формы не подключена.', 'local_file': '../docs/контакты/index.html'},
    {'slug': 'политика-конфиденциальности', 'title': 'Политика конфиденциальности', 'status': 'new_legal_template', 'status_label': 'Новый шаблон по 152-ФЗ для текущего сайта', 'original_url_confirmed': True, 'notes': 'Старая политика отсутствует в проверенном дампе. Новый текст составлен по просьбе владельца; учтены email/телефон, отсутствие форм и аналитики и журналирование IP-адресов GitHub Pages.', 'local_file': '../docs/политика-конфиденциальности/index.html'},
])
video_count = sum(len(c.get('videos', [])) for c in CATS)
aliases = ['/index'] + ['/' + x for x in DATA.get('legacy_routes', {})]
report = {'content_pages': len(pages), 'html_files': len(pages) + len(aliases), 'aliases': aliases,
          'original_routes_found': len(DATA['original_page_urls']), 'images': len(DATA['assets']),
          'videos': video_count, 'local_sources': DATA.get('local_sources', {}),
          'counts_by_status': dict(Counter(x['status'] for x in statuses)), 'pages': statuses,
          'limits': ['Старый сайт восстановлен из снимка БД 15.05.2024 и последующих материалов. Исходная политика не найдена; на сайте опубликован новый шаблон по просьбе владельца.',
                     'Оформление создано заново. Источники изображений: оригинальная БД, вложения писем, публикация производителя и поисковые превью.',
                     'Для лукореза новое видео показано первым, старое вторым. На странице МГБ-250 только новое видео; старое сохранено в архиве письма.',
                     'Тексты вложений перенесены дословно по указанию владельца, включая цены, сроки и реквизиты. В документе ЛУ-5-200 даты нет; дата письма 09.07.2026 не является датой документа.',
                     'Реальная отправка обращений не подключена. Телефон, email и копирование номера работают локально.']}
(REPORTS / 'restoration-status.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
table_rows = ''.join(f'<tr><td>{e(x["title"])}<br><code>/{e(x["slug"])}</code></td><td>{e(x["status_label"])}</td><td>{e(x["notes"])}</td><td><a href="{e(x["local_file"])}">Открыть</a></td></tr>' for x in statuses)
limits_html = ''.join('<li>' + e(item) + '</li>' for item in report['limits'])
report_html = f'''<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Отчёт о восстановлении</title><style>body{{font:16px/1.5 system-ui;margin:30px;color:#172923}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #ccd4ce;padding:12px;text-align:left;vertical-align:top}}code{{overflow-wrap:anywhere}}a{{color:#126b49}}.table{{overflow:auto}}</style><h1>Восстановление ипзурначеваа.рус</h1><p>Локальный сайт: {len(pages)} страница, {len(aliases)} совместимых старых адресов, {len(DATA['assets'])} изображений и {video_count} видео. Содержание собрано из архива, поисковой выдачи, локальной БД и писем владельца.</p><p><a href="../docs/index.html">Открыть сайт</a></p><div class="table"><table><thead><tr><th>Страница</th><th>Что восстановлено</th><th>Ограничения и источник содержания</th><th>Локальная версия</th></tr></thead><tbody>{table_rows}</tbody></table></div><h2>Исходные материалы и ограничения</h2><ul>{limits_html}</ul><p>Из старого проекта восстановлены 11 опубликованных страниц, 47 записей контента и 36 уникальных встроенных изображений. Прочитаны все 10 предоставленных писем. Письмо «Надо кое-что добавить на сайт…» содержит только подпись, без вложений.</p><p>Путь /бункер-затариватель-весовой назначен локально: оригинальный адрес неизвестен, содержание теперь восстановлено из письма.</p><p>В письме «На сайт.» от 09.07.2026 вложен недатированный документ ЛУ-5-200.docx с ценой 870 000 ₽ и сроком изготовления 35 рабочих дней. Текст вложения полностью опубликован по указанию владельца без исправлений, включая цену, сроки и ИП Зурначева Е.Н. В общих реквизитах сайта указано подтверждённое владельцем ИП Зурначёв А.А. Оригинальный документ сохранён в email-data/.</p><p>Численные параметры не дописаны по аналогии с другими машинами. Обе редакции фритюрниц сохранены отдельно, поскольку характеристики ФНД-55 в источниках различаются. Подробные сведения об источниках — site/content.json и metadata/local-sources.json.</p></html>'''
(REPORTS / 'restoration-report.html').write_text(report_html, encoding='utf-8')
(DIST / '.nojekyll').touch()
print(f'Built {len(pages)} content pages, {len(aliases)} aliases, {len(DATA["assets"])} images and {video_count} videos. Output: {DIST}')
