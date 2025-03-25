# 📦 Gestor de Estoque Django

Sistema simples e moderno de gestão de estoque com Django, voltado para vendedores autônomos. Permite controle por tamanho, gênero, tipo de produto, imagem com preview, classificação, avaliações e muito mais.

---

## 🚀 Tecnologias

- Python 3.10+
- Django 5+
- Bootstrap 5 (local)
- SQLite3 (padrão)
- Django Crispy Forms + Widget Tweaks

---

## ✅ Pré-requisitos

- [Python](https://www.python.org/) instalado
- [Git](https://git-scm.com/) instalado

---

## ⚙️ Como rodar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/matheuslima25/django-sustainable-ecommerce.git
cd django-sustainable-ecommerce
```

### 2. Crie e ative um ambiente virtual

**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

### 4. Realize as migrações

```bash
python manage.py migrate
```

---

### 5. Crie um superusuário

```bash
python manage.py createsuperuser
```

---

### 6. Rode o servidor local

```bash
python manage.py runserver
```

Acesse em: [http://localhost:8000](http://localhost:8000)

---

## 🗂️ Estrutura esperada

```
.
├── core/
│   ├── templates/
│   ├── views.py
│   ├── models.py
│   └── ...
├── sustainableecommerce/
│   ├── static/
│   ├── settings.py
│   ├── urls.py
├── db.sqlite3
├── manage.py
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ✨ Features

- Upload de imagem com preview
- Dropdowns dependentes por tipo de produto
- Classificação com estrelas
- Filtros e busca com AJAX
- Histórico de saídas (somente admin)
- Interface responsiva com Bootstrap

---

## 📜 Licença

Este projeto é livre para uso e modificação pessoal.
