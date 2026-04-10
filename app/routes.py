from flask import Blueprint, render_template, jsonify, send_from_directory
import os
import json

main = Blueprint('main', __name__)

# Charger les données depuis JSON
with open("data/portfolio.json", "r", encoding="utf-8") as f:
    portfolio_data = json.load(f)

print(portfolio_data)

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

@main.route('/')
def index():
    with open("data/portfolio.json", "r", encoding="utf-8") as f:
        portfolio_data = json.load(f)
    return render_template('index.html', data=portfolio_data)

@main.route('/download-cv')
def download_cv():
    return send_from_directory(
        directory=os.path.join(os.path.dirname(__file__), '..', 'static', 'cv'),
        path='CV_Geoffroy_GRANIER.pdf',
        as_attachment=True
    )

@main.route('/export')
def export():
    path = generate_static_html()
    return jsonify({
        "status": "ok",
        "file": path
    })