# Project 0001 – Django Bible with OpenAI API

This is a small Django project that demonstrates integrating the **OpenAI API** to generate Bible verses dynamically in multiple languages. The project provides a web interface where users can select a language and view Bible verses along with related images.

---

## Features

- Multi-language support: English (`en`), Español (`es`), Français (`fr`)
- Fetches Bible verses dynamically using **OpenAI** based on a list of Catholic Bible books
- Displays verse text along with a related image
- Simple, responsive web interface with styled clickable links and buttons

---

## Project Structure

```
project-0001-django-bible-openai/
├── .gitignore         # Ignored files (Python, virtual env, .env, etc.)
├── .venv              # Python virtual environment
├── bible_project/     
│   ├── bible/         # Django app
│   │   ├── views.py   # Main logic for interacting with OpenAI API and rendering pages
│   │   ├── urls.py
│   │   ├── models.py
│   │   └── ...
│   ├── bible_project/ # Django project configuration
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   ├── db.sqlite3     # SQLite database (ignored in git)
│   └── manage.py
└── requirements.txt   # Python dependencies
```

---

## Setup

1. Clone the repository:
```bash
git clone git@github.com:YOUR_USERNAME/learning-projects.git
cd learning-projects/project-0001-django-bible-openai
```

2. Create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file inside `bible_project/` and add your OpenAI API key:
```env
OPEN_API_KEY=your_openai_api_key_here
```

5. Run Django migrations:
```bash
python bible_project/manage.py migrate
```

6. Start the development server:
```bash
python bible_project/manage.py runserver
```

7. Open your browser at:
```
http://127.0.0.1:8000/bible/
```

---

## Notes

- The OpenAI API key **must not be committed** to GitHub. Make sure `.env` is included in `.gitignore`.
- Currently uses **SQLite** for simplicity; suitable for local development.
- Designed as a learning/demo project to practice Django + OpenAI API integration.

---

## Dependencies

- Django
- OpenAI Python client
- python-dotenv (for loading `.env`)

---

## License

This is a personal learning project.