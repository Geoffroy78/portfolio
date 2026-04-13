from flask import Blueprint, render_template, jsonify, send_from_directory, request
import os
import json
import re

main = Blueprint('main', __name__)

def merge_dict(base, override):
    if isinstance(base, dict) and isinstance(override, dict):
        merged = base.copy()
        for k, v in override.items():
            if k in merged:
                merged[k] = merge_dict(merged[k], v)
            else:
                merged[k] = v
        return merged
    return override

# Charger les données depuis JSON
def load_data(lang="fr"):
    with open("data/portfolio.json", "r", encoding="utf-8") as f:
        base = json.load(f)

    if lang == "fr":
        return base

    # load translation file
    try:
        with open(f"data/i18n/{lang}.json", "r", encoding="utf-8") as f:
            base = json.load(f)
    except FileNotFoundError:
        return base

    # merge (EN override FR)
    # return merge_dict(base, translation)
    return base

def detect_languages(i18n_folder="data/i18n"):
    if not os.path.exists(i18n_folder):
        return ["fr"]

    languages = []

    for file in os.listdir(i18n_folder):
        if file.endswith(".json"):
            lang = os.path.splitext(file)[0]
            languages.append(lang)

    # always ensure base language exists
    if "fr" not in languages:
        languages.insert(0, "fr")

    return sorted(languages)

def generate_static_html():
    with open("data/portfolio.json", "r", encoding="utf-8") as f:
        portfolio_data = json.load(f)

    rendered_html = render_template(
        'index.html',
        data=portfolio_data
    )

    rendered_html = rendered_html.replace("/static/", "./app/static/")

    rendered_html = rendered_html.replace(
        '<a class="btn-cv" href="/download-cv">Télécharger CV</a>',
        '<a class="btn-cv" href="./app/static/cv/CV_Geoffroy_GRANIER.pdf" download="CV_Geoffroy_GRANIER.pdf" target="_blank">Télécharger CV</a>'
    )

    output_path = "index.html"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)

    return output_path

def lang_prefix(lang):
    return "" if lang == "fr" else f"/{lang}"

def generate_static_html_files():
    languages = detect_languages()
    files = []

    for lang in languages:
        # =========================
        # LOAD DATA (i18n merge)
        # =========================
        portfolio_data = load_data(lang)

        # =========================
        # RENDER HTML
        # =========================
        html = render_template(
            "index.html",
            data=portfolio_data,
            lang=lang
        )

        # =========================
        # FIX STATIC PATHS
        # =========================

        # =========================
        # CV BUTTON FIX
        # =========================
        if lang == "fr":
            html = html.replace("/static/", "./app/static/")
        else:
            html = html.replace("/static/", "../app/static/")
            html = html.replace(
                f'<a class="btn-cv" href="/download-cv">{portfolio_data["download"]}</a>',
                f'<a class="btn-cv" href="../app/static/cv/CV_Geoffroy_GRANIER.pdf" download target="_blank">{portfolio_data["download"]}</a>'
            )
        
        
        langs_in_html = set(re.findall(r"\?lang=([a-zA-Z-]+)", html))
        if lang == "fr":
            for l in langs_in_html:
                if l == "fr":
                    html = re.sub(rf"/\?lang=fr\b", "./", html)
                else:
                    html = re.sub(rf"/\?lang={l}\b", f"./{l}/", html)
        else:
            for l in langs_in_html:
                if l == "fr":
                    html = re.sub(rf"/\?lang=fr\b", "../", html)
                else:
                    html = re.sub(rf"/\?lang={l}\b", f"../{l}/", html)
        
        cv_lang = set(re.findall(r"/download-cv\?lang=([a-zA-Z-]+)", html))
        cv_lang = next(iter(cv_lang))
        if cv_lang == "fr":
            directory = "./app/static/cv/"
            cv_name = "CV_Geoffroy_GRANIER.pdf"
        else:
            directory = "../app/static/cv/"
            cv_name = "CV_Geoffroy_GRANIER_english.pdf"

        print(f'<a class="btn-cv" href="/download-cv?lang={cv_lang}">{portfolio_data["download"]}</a>')
        print(f'<a class="btn-cv" href="{directory}{cv_name}" download target="_blank">{portfolio_data["download"]}</a>')
        
        html = html.replace(
            f'<a class="btn-cv" href="/download-cv?lang={cv_lang}">{portfolio_data["download"]}</a>',
            f'<a class="btn-cv" href="{directory}{cv_name}" download target="_blank">{portfolio_data["download"]}</a>'
        )


        # =========================
        # CREATE FOLDER PER LANGUAGE
        # =========================
        if lang == "fr":
            output_dir = "."  # racine
            output_path = os.path.join(output_dir, "index.html")
        else:
            output_dir = os.path.join(lang)
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, "index.html")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        files.append(output_path)

    return files

@main.route('/')
def index():
    lang = request.args.get("lang", "fr")
    portfolio_data = load_data(lang)
    return render_template('index.html', data=portfolio_data, lang=lang)

@main.route('/download-cv')
def download_cv():
    lang = request.args.get("lang", "fr")
    directory = os.path.join(os.path.dirname(__file__), '.', 'static', 'cv')
    if lang == "fr":
        cv_path = 'CV_Geoffroy_GRANIER.pdf'
    else:
        cv_path = 'CV_Geoffroy_GRANIER_english.pdf'

    return send_from_directory(
        directory=directory,
        path=cv_path,
        as_attachment=True
    )

@main.route('/export')
def export():
    # path = generate_static_html()
    files = generate_static_html_files()
    return jsonify({
        "status": "ok",
        "files": files
    })