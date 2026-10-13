# Пищевые механизмы

Статический сайт ИП ЗУРНАЧЁВА E.Н., подготовленный для GitHub Pages.
На главной — все 16 разделов с фотографиями, на страницах оборудования —
описания, галереи и видео. Тексты вложений перенесены дословно, включая
формулировки, единицы, цену, сроки и реквизиты внутри документов.

## Запуск локально

Запустите `start-site.bat` или откройте `docs/index.html`.
После свежего клонирования сначала соберите сайт:

```sh 
python3 source/build_site.py
python3 source/check_site.py
python3 -m http.server 8765 --bind 127.0.0.1 --directory docs
```

В Windows вместо `python3` можно использовать `py`. Сайт работает без
серверной базы данных, PHP, Node.js и сторонних библиотек.

## GitHub Pages

1. В репозитории откройте **Settings → Pages → Build and deployment → Source → GitHub Actions**.
2. Закоммитьте файлы проекта и выполните push в `main`.

Workflow `.github/workflows/pages.yml` соберёт сайт, проверит локальные ссылки
и опубликует только готовую папку `docs`. Его также можно запустить вручную
через **Actions → Deploy website to GitHub Pages → Run workflow**.

Основной адрес после настройки домена: <https://ипзурначеваа.рус/>.
Переходы и изображения используют относительные пути и работают как в корне
этого домена, так и в пути `/tornado_current/` стандартного адреса GitHub Pages.

### Домен ипзурначеваа.рус

В **Settings → Pages → Custom domain** укажите ASCII-представление домена и нажмите Save:

```text
xn--80aaagokg5bql6a3c.xn--p1acf
```

DNS-зона обслуживается `ns1.reg.ru` и `ns2.reg.ru`. В панели управления зоной
REG.RU замените существующую A-запись корня домена (`@`) на четыре записи:

| Тип | Имя / Subdomain | Значение |
| --- | --- | --- |
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | nikolay-shapoval.github.io |

Для `www` замените прежнюю A-запись на приведённую CNAME-запись. При проверке
12.10.2026 корень и `www` указывали на `94.142.142.104`.
Для текущего workflow GitHub Actions пользовательский домен задаётся именно
в настройках GitHub Pages. CNAME-файл сборки для этого workflow не используется.

После обновления DNS и выпуска сертификата включите **Enforce HTTPS**.
DNS-изменения могут распространяться до 24 часов. При желании подтвердите владение
доменом в **настройках аккаунта → Pages → Add a domain**, добавив TXT-запись,
значение которой покажет GitHub.

[Настройка домена на GitHub](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)
и [управление зоной REG.RU](https://help.reg.ru/support/dns-servery-i-nastroyka-zony/nastroyka-resursnykh-zapisey-dns/nastroyka-resursnykh-zapisey-dns-dlya-domena).

## Изменение сайта

- `source/content.json` — содержание страниц; `verbatim_body` хранит точный текст вложения.
- `site_url` в `source/content.json` — основной адрес для canonical-ссылок страниц.
- `source/privacy.txt` — новая политика обработки персональных данных.
- `source/styles.css` и `source/app.js` — оформление и поведение интерфейса.
- `assets/` — исходные публичные изображения и видео.
- `source/build_site.py` — сборка HTML; `docs/` — её результат, исключённый из Git.

После редактирования повторите сборку. Отчёты появляются в `build-reports/`
и не публикуются. Исходный SQL, письма `.eml`, частные заголовки писем и
учётные данные в проект не перенесены.

## Источники политики

Исходная политика не найдена в старом дампе от 15.05.2024. На сайте размещён
новый шаблон для текущей конфигурации: связь по email и телефону, без форм и
счётчиков аналитики. Он учитывает техническое журналирование GitHub Pages.
Это шаблон; фактический порядок обработки у оператора и требования к локализации
должны быть проверены владельцем отдельно от текста сайта.

- [152-ФЗ — публикация Минтруда России](https://mintrud.gov.ru/docs/laws/130).
- [Рекомендации Роскомнадзора от 31.07.2017](https://www.garant.ru/products/ipo/prime/doc/71634598/).
- [Обработка IP-адресов GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages#data-collection).
- [Политика конфиденциальности GitHub](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement).
- [Официальная инструкция по workflow GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

Четыре ролика работают локально. Пятый ролик, для ФНД-55, доступен по ссылке на
Яндекс Диск: скачать исходный файл пока не удалось.
