

!pip install -U transformers

# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("text-generation", model="ibm-granite/granite-3.3-2b-instruct")
messages = [
    {"role": "user", "content": "Who are you?"},
]
pipe(messages)

# ============================================================
# HTML QUICK STYLER - SIMPLE SINGLE FILE
# ============================================================

import gradio as gr
from typing import Dict, List
from datetime import datetime


# ============================================================
# COLOR PALETTES
# ============================================================

class ColorPaletteGenerator:

    @staticmethod
    def generate_palette(style: str = "modern") -> Dict[str, str]:

        palettes = {

            "modern": {
                "primary": "#667eea",
                "secondary": "#764ba2",
                "accent": "#f093fb",
                "background": "#0f172a",
                "surface": "#1e293b",
                "text": "#f1f5f9"
            },

            "vibrant": {
                "primary": "#ff6b6b",
                "secondary": "#ff8e72",
                "accent": "#f5576c",
                "background": "#0f172a",
                "surface": "#1e293b",
                "text": "#f1f5f9"
            },

            "ocean": {
                "primary": "#0099cc",
                "secondary": "#006699",
                "accent": "#00ccff",
                "background": "#0f172a",
                "surface": "#1e293b",
                "text": "#f1f5f9"
            }
        }

        return palettes.get(style, palettes["modern"])


# ============================================================
# SECTION DETECTOR
# ============================================================

def extract_sections(description: str) -> List[str]:

    sections = []

    keywords = {
        "hero": ["hero", "banner"],
        "features": ["features", "services"],
        "about": ["about"],
        "portfolio": ["portfolio", "gallery"],
        "contact": ["contact", "form"],
        "footer": ["footer"]
    }

    desc = description.lower()

    for section, words in keywords.items():
        for w in words:
            if w in desc:
                sections.append(section)
                break

    if not sections:
        sections = ["hero", "features", "contact", "footer"]

    return sections


# ============================================================
# SECTION HTML
# ============================================================

def generate_section_html(section: str) -> str:

    year = datetime.now().year

    sections = {

        "hero": """
<section id="hero" class="hero">
<h1>Welcome to Your Website</h1>
<p>Create modern websites instantly</p>
<button>Get Started</button>
</section>
""",

        "features": """
<section id="features">
<h2>Features</h2>
<div class="grid">
<div class="card">Fast</div>
<div class="card">Secure</div>
<div class="card">Scalable</div>
</div>
</section>
""",

        "about": """
<section id="about">
<h2>About Us</h2>
<p>We create modern and responsive websites.</p>
</section>
""",

        "portfolio": """
<section id="portfolio">
<h2>Portfolio</h2>
<div class="grid">
<div class="card">Project 1</div>
<div class="card">Project 2</div>
<div class="card">Project 3</div>
</div>
</section>
""",

        "contact": """
<section id="contact">
<h2>Contact</h2>
<form>
<input placeholder="Your Name">
<input placeholder="Email">
<textarea placeholder="Message"></textarea>
<button>Send</button>
</form>
</section>
""",

        "footer": f"""
<footer>
<p>© {year} Your Company</p>
</footer>
"""
    }

    return sections.get(section, "")


# ============================================================
# CSS GENERATOR
# ============================================================

def generate_css(palette):

    return f"""
<style>

body {{
font-family: Arial;
background:{palette['background']};
color:{palette['text']};
margin:0;
}}

header {{
background:{palette['surface']};
padding:20px;
text-align:center;
}}

section {{
padding:60px;
text-align:center;
}}

.hero {{
background:linear-gradient(135deg,{palette['primary']},{palette['secondary']});
color:white;
}}

button {{
background:{palette['primary']};
border:none;
padding:10px 20px;
color:white;
cursor:pointer;
}}

.grid {{
display:grid;
grid-template-columns:repeat(auto-fit,minmax(200px,1fr));
gap:20px;
}}

.card {{
background:{palette['surface']};
padding:20px;
border-radius:10px;
}}

footer {{
padding:40px;
background:{palette['surface']};
}}

</style>
"""


# ============================================================
# HTML PAGE GENERATOR
# ============================================================

def generate_page(title, description, style):

    palette = ColorPaletteGenerator.generate_palette(style)

    sections = extract_sections(description)

    html_sections = ""

    for s in sections:
        html_sections += generate_section_html(s)

    css = generate_css(palette)

    html = f"""
<!DOCTYPE html>
<html>

<head>
<title>{title}</title>
{css}
</head>

<body>

<header>
<h1>{title}</h1>
</header>

{html_sections}

</body>

</html>
"""

    palette_info = f"""
Primary: {palette['primary']}

Secondary: {palette['secondary']}

Accent: {palette['accent']}
"""

    return html, "✅ HTML Generated", palette_info


# ============================================================
# PREVIEW
# ============================================================

def preview_page(html):

    if not html:
        return "No HTML generated"

    return f'<iframe srcdoc="{html}" width="100%" height="600"></iframe>'


# ============================================================
# GRADIO UI
# ============================================================

with gr.Blocks(title="HTML Quick Styler") as demo:

    gr.Markdown("# 🎨 HTML Quick Styler")

    title = gr.Textbox(label="Page Title", value="My Website")

    description = gr.Textbox(
        label="Page Description",
        value="Hero section, features list, contact form, footer",
        lines=3
    )

    style = gr.Dropdown(
        ["modern","vibrant","ocean"],
        value="modern",
        label="Color Style"
    )

    generate_btn = gr.Button("Generate HTML")

    html_output = gr.Code(language="html")

    status = gr.Markdown()

    palette = gr.Markdown()

    preview = gr.HTML()

    generate_btn.click(
        generate_page,
        inputs=[title,description,style],
        outputs=[html_output,status,palette]
    )

    generate_btn.click(
        preview_page,
        inputs=[html_output],
        outputs=[preview]
    )


# ============================================================
# RUN APP
# ============================================================

print("🚀 Starting HTML Quick Styler...")

demo.launch()
