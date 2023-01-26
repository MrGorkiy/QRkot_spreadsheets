# Приложение QRKot
![example workflow](https://github.com/MrGorkiy/cat_charity_fund/actions/workflows/cat_charity_fund.yml/badge.svg)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=ffffff&color=043A6B)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/-FastAPI-464646?style=flat&logo=FastAPI&logoColor=ffffff&color=043A6B)](https://fastapi.tiangolo.com/)
[![FastAPI-Users](https://img.shields.io/badge/-FastAPI_Users-464646?style=flat&logo=FastAPI&logoColor=ffffff&color=043A6B)](https://pypi.org/project/fastapi-users/)
[![Pydantic](https://img.shields.io/badge/-Pydantic-464646?style=flat&logo=Pydantic&logoColor=ffffff&color=043A6B)](https://docs.pydantic.dev/)
[![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-464646?style=flat&logo=SQLAlchemy%20REST%20Framework&logoColor=ffffff&color=043A6B)](https://www.sqlalchemy.org/)
[![aiosqlite](https://img.shields.io/badge/-aiosqlite-464646?style=flat&logo=aiosqlite&logoColor=ffffff&color=043A6B)](https://pypi.org/project/aiosqlite/)
[![Alembic](https://img.shields.io/badge/-Alembic-464646?style=flat&logo=Alembic&logoColor=ffffff&color=043A6B)](https://alembic.sqlalchemy.org/en/latest/)
[![GoogleAPI](https://img.shields.io/badge/-GoogleAPI-464646?style=flat&logo=GoogleAPI&logoColor=ffffff&color=043A6B)](https://support.google.com/googleapi/?hl=en#topic=7014522)


## Оглавление
- [Описание проекта](#описание-проекта)
  - [Права пользователей (Проекты)](#права-пользователей-проекты)
  - [Права пользователей (Пожертвования)](#права-пользователей-пожертвования)
  - [Процесс инвестирования](#процесс-инвестирования)
- [Заполнение .env файла](#шаблон-наполнения-файла-cat_charity_fundenv)
- [Запуск проекта](#запуск-проекта)


## Описание проекта
QRKot Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

### Проекты
В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается. Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.

### Пожертвования
Каждый пользователь может сделать пожертвование и сопроводить его комментарием. Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект. Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который ещё не набрал нужную сумму. Если пожертвование больше нужной суммы или же в Фонде нет открытых проектов — оставшиеся деньги ждут открытия следующего проекта. При создании нового проекта все неинвестированные пожертвования автоматически вкладываются в новый проект.

### Пользователи
Целевые проекты создаются администраторами сайта. Любой пользователь может видеть список всех проектов, включая требуемые и уже внесенные суммы. Это касается всех проектов — и открытых, и закрытых. Зарегистрированные пользователи могут отправлять пожертвования и просматривать список своих пожертвований.


[:top: Вернуться к оглавлению](#оглавление)

<details><summary>Более подробная информация о проекте:</summary>
<p>

### Права пользователей (Проекты)
Любой посетитель сайта (в том числе неавторизованный) может посмотреть список всех проектов.

**Суперпользователь** может:
- создавать проекты;
- удалять проекты, в которые не было внесено средств;
- изменять название и описание существующего проекта, устанавливать для него новую требуемую сумму (но не меньше уже внесённой).

> *Никто не может менять через API размер внесённых средств, удалять или модифицировать закрытые проекты, изменять даты создания и закрытия проектов.
### Права пользователей (Пожертвования)

Любой **зарегистрированный пользователь** может сделать пожертвование.
**Зарегистрированный пользователь** может просматривать только свои пожертвования, при этом ему выводится только четыре поля:
- id;
- comment;
- full_amount;
- create_date.

> *Информация о том, инвестировано пожертвование в какой-то проект или нет, обычному пользователю **недоступна**.
**Суперпользователь** может просматривать список всех пожертвований, при этом ему выводятся все поля модели.

> *Редактировать или удалять пожертвования **не может никто**.
### Процесс инвестирования

Сразу после создания нового проекта или пожертвования запускается процесс **«инвестирования»** (``execute_investment_process`` в директории ``app/services/investment.py``) (увеличение ``invested_amount`` как в пожертвованиях, так и в проектах, установка значений ``fully_invested`` и ``close_date``, при необходимости).

Если создан новый проект, а в базе были **«свободные»** (не распределённые по проектам) суммы пожертвований — они автоматически инвестируются в новый проект, и в ответе API эти суммы учитываются. То же касается и создания пожертвований: если в момент пожертвования есть открытые проекты, эти пожертвования автоматически зачисляются на их счета.

Функция, отвечающая за инвестирование, вызывается непосредственно из API-функций, отвечающих за создание пожертвований и проектов. Сама функция инвестирования расположена в директории ``app/services/`` в файле ``investment.py``.

[:top: Вернуться к оглавлению](#оглавление)
</p>
</details>

### Шаблон наполнения файла `cat_charity_fund/.env`
```
APP_TITLE=Приложение QRKot
APP_DESCRIPTION=Сервис сбора пожертвований для поддержки котиков.
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=secret
FIRST_SUPERUSER_EMAIL=admin@admin.com
FIRST_SUPERUSER_PASSWORD=admin
EMAIL=your@gmail.com
TYPE=
PROJECT_ID=
PRIVATE_KEY_ID=
PRIVATE_KEY=
CLIENT_EMAIL=
CLIENT_ID=
AUTH_URI=
TOKEN_URI=
AUTH_PROVIDER_X509_CERT_URL=
CLIENT_X509_CERT_URL=
```

## Запуск проекта
- Клонируйте репозиторий и перейдите в папку проекта:
```
git clone git@github.com:MrGorkiy/cat_charity_fund.git
```
- Установите и активируйте виртуальное окружение:
```bash
python -m venv venv
```
```bash
source venv/Scripts/activate
```
- Установите зависимости из файла requirements.txt:
```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```
- Создать и заполнить файл **.env** в соответствии с [рекомендациями](#шаблон-наполнения-файла-cat_charity_fundenv):
- Применение миграций
```bash
alembic upgrade head 
```
- Запустить проект
```bash
uvicorn app.main:app --reload
```
Создание миграции First migration
```bash
alembic revision --autogenerate -m "ADD donation" 
```

После запуска проект будет доступен по адресу: http://127.0.0.1:8000

Документация к API досупна по адресам:
- Swagger: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc

[:top: Вернуться к оглавлению](#оглавление)


Автор: [MrGorkiy](https://github.com/MrGorkiy)