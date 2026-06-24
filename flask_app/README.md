# Ivan Soriano Photography — Flask Edition

A Flask + HTML + Tailwind CSS (CDN) + vanilla JavaScript port of the original React/Vite site.

## Run

```bash
pip install -r requirements.txt
python app.py
```

Then open <http://127.0.0.1:5000>.

## Structure

```
flask_app/
  app.py              Flask server (routes + contact API)
  requirements.txt
  inquiries.json      Created at runtime to store form submissions
  templates/
    index.html        Main page (includes partials)
    partials/         navbar, hero, services, portfolio, about, testimonials, contact, footer
  static/
    css/styles.css    Theme tokens, fonts, animations
    js/main.js        All interactivity
    img/              Photography images
```
