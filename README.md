# Пищевые механизмы

Статический сайт ИП Зурначёв А.А., подготовленный для GitHub Pages.
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

Адрес после успешного развёртывания:
<https://nikolay-shapoval.github.io/tornado_current/>.
Ссылки относительные и работают внутри пути `/tornado_current/`.

## Изменение сайта

- `source/content.json` — содержание страниц; `verbatim_body` хранит точный текст вложения.
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
