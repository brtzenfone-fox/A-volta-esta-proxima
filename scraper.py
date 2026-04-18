"""
A Volta Esta Proxima - Gerador de Site
Portal cristao protestante premium
v1.0
"""

import json
import os
from datetime import datetime, date

ARTIGOS_FILE = "artigos.json"
VERSICULOS_FILE = "versiculos.json"
ESTUDOS_FILE = "estudos.json"

CATEGORIAS = {
    "perseguicao": {"nome": "Perseguicao aos Cristaos", "icone": "✝", "cor": "#8b1538"},
    "milagres": {"nome": "Milagres e Maravilhas", "icone": "✦", "cor": "#c9a961"},
    "testemunhos": {"nome": "Testemunhos", "icone": "❖", "cor": "#5a7d2a"},
    "sinais": {"nome": "Sinais dos Tempos", "icone": "◈", "cor": "#1a3a52"},
    "noticias": {"nome": "Noticias do Mundo Cristao", "icone": "❋", "cor": "#3d3d3d"},
    "documentarios": {"nome": "Documentarios e Reportagens", "icone": "▣", "cor": "#7a5c2e"},
}

TIPOS = {
    "noticia": "Noticia",
    "testemunho": "Testemunho",
    "interpretacao": "Interpretacao",
    "reflexao": "Reflexao",
}

def carregar_json(arquivo, padrao=None):
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return padrao if padrao is not None else []

def versiculo_do_dia(versiculos):
    if not versiculos:
        return {"texto": "", "ref": ""}
    idx = date.today().toordinal() % len(versiculos)
    return versiculos[idx]

def estudo_do_dia(estudos):
    if not estudos:
        return None
    idx = date.today().toordinal() % len(estudos)
    return estudos[idx]

def formatar_data(data_str):
    try:
        d = datetime.strptime(data_str, "%Y-%m-%d")
        meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
                 "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
        return f"{d.day} {meses[d.month-1]} {d.year}"
    except:
        return data_str

def gerar_card_artigo(art, idx=0):
    cat = art.get("categoria", "noticias")
    cat_info = CATEGORIAS.get(cat, CATEGORIAS["noticias"])
    tipo = TIPOS.get(art.get("tipo", "noticia"), "Noticia")
    delay = f"animation-delay:{idx*0.05}s"
    img = art.get("imagem", "")
    img_html = f'<div class="card-img" style="background-image:url(\'{img}\')"></div>' if img else ''

    return f'''<article class="art-card" style="{delay}" onclick="abreArtigo({idx})">
{img_html}
<div class="card-body">
<div class="card-meta">
<span class="card-cat" style="color:{cat_info['cor']}">{cat_info['icone']} {cat_info['nome']}</span>
<span class="card-tipo">{tipo}</span>
</div>
<h3 class="card-title">{art['titulo']}</h3>
<p class="card-resumo">{art['resumo']}</p>
<div class="card-footer">
<span class="card-fonte">{art.get('fonte','')}</span>
<span class="card-data">{formatar_data(art.get('data',''))}</span>
</div>
</div>
</article>'''

def gerar_modal_artigo(art, idx):
    cat = art.get("categoria", "noticias")
    cat_info = CATEGORIAS.get(cat, CATEGORIAS["noticias"])
    tipo = TIPOS.get(art.get("tipo", "noticia"), "Noticia")
    img = art.get("imagem", "")
    img_html = f'<div class="modal-art-img" style="background-image:url(\'{img}\')"></div>' if img else ''
    url_ext = art.get("url", "#")
    fonte_link = f'<a href="{url_ext}" target="_blank" class="modal-fonte-link">Ler na fonte original →</a>' if url_ext and url_ext != "#" else ''

    return f'''<div class="modal" id="art-{idx}" onclick="if(event.target===this)fechaModal('art-{idx}')">
<div class="modal-box">
<button class="modal-close" onclick="fechaModal('art-{idx}')">×</button>
{img_html}
<div class="modal-body">
<div class="modal-meta">
<span class="modal-cat" style="color:{cat_info['cor']}">{cat_info['icone']} {cat_info['nome']}</span>
<span class="modal-tipo">{tipo}</span>
</div>
<h2 class="modal-title">{art['titulo']}</h2>
<div class="modal-info">
<span>{art.get('fonte','')}</span>
<span>·</span>
<span>{formatar_data(art.get('data',''))}</span>
</div>
<p class="modal-resumo">{art['resumo']}</p>
<div class="modal-analise">
<div class="modal-analise-titulo">Analise Biblica</div>
<p class="modal-analise-texto">{art.get('analise_biblica', '')}</p>
</div>
{fonte_link}
</div>
</div>
</div>'''

def gerar_secao_categoria(cat_id, artigos_cat):
    if not artigos_cat:
        return ""
    cat_info = CATEGORIAS.get(cat_id, CATEGORIAS["noticias"])
    cards = ""
    for a in artigos_cat:
        cards += gerar_card_artigo(a, a["_idx"])
    return f'''<section class="secao" id="sec-{cat_id}">
<div class="secao-header">
<div class="secao-titulo-wrap">
<span class="secao-icone" style="color:{cat_info['cor']}">{cat_info['icone']}</span>
<h2 class="secao-titulo">{cat_info['nome']}</h2>
</div>
<span class="secao-count">{len(artigos_cat)}</span>
</div>
<div class="secao-grid">{cards}</div>
</section>'''

CSS = r"""
* {margin:0; padding:0; box-sizing:border-box; -webkit-font-smoothing:antialiased}

:root {
--ouro: #c9a961;
--ouro-claro: #e8d5a0;
--ouro-escuro: #b8924a;
--ouro-suave: #d4b87a;
--branco: #ffffff;
--off-white: #fbfaf7;
--bege: #f5f1e8;
--cinza-claro: #ede9e0;
--cinza: #6b6358;
--cinza-escuro: #3d3830;
--preto: #1a1612;
--linha: rgba(201, 169, 97, 0.18);
--sombra: 0 4px 24px rgba(26, 22, 18, 0.06);
--sombra-forte: 0 12px 40px rgba(26, 22, 18, 0.10);
}

html { scroll-behavior:smooth }
body {
font-family: 'Inter', -apple-system, sans-serif;
background: var(--off-white);
color: var(--cinza-escuro);
font-size: 15px;
line-height: 1.65;
overflow-x: hidden;
position: relative;
min-height: 100vh;
}

::selection { background: var(--ouro-claro); color: var(--preto) }
::-webkit-scrollbar { width:8px }
::-webkit-scrollbar-track { background: var(--bege) }
::-webkit-scrollbar-thumb { background: var(--ouro-suave); border-radius:999px }

/* RELOGIO GIGANTE NO FUNDO */
.relogio-fundo {
position: fixed;
top: 50%;
left: 50%;
transform: translate(-50%, -50%);
width: 800px;
height: 800px;
max-width: 110vw;
max-height: 110vw;
pointer-events: none;
z-index: 0;
opacity: 0.06;
}
.relogio-fundo svg { width: 100%; height: 100% }
.ponteiro-h {
transform-origin: 400px 400px;
animation: girarH 720s linear infinite;
}
.ponteiro-m {
transform-origin: 400px 400px;
animation: girarM 60s linear infinite;
}
@keyframes girarH { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }
@keyframes girarM { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }

/* CONTAINER GERAL */
.wrap { position: relative; z-index: 1 }

/* HEADER */
header {
position: sticky;
top: 0;
z-index: 100;
background: rgba(251, 250, 247, 0.92);
backdrop-filter: blur(20px);
border-bottom: 1px solid var(--linha);
padding: 0 28px;
height: 76px;
display: flex;
align-items: center;
justify-content: space-between;
}
.logo {
font-family: 'Cormorant Garamond', serif;
font-size: 22px;
font-weight: 600;
letter-spacing: -0.4px;
color: var(--preto);
text-decoration: none;
display: flex;
align-items: center;
gap: 12px;
}
.logo-mark {
display: inline-block;
width: 30px;
height: 30px;
border: 1.5px solid var(--ouro);
border-radius: 50%;
position: relative;
}
.logo-mark::before, .logo-mark::after {
content: '';
position: absolute;
background: var(--ouro);
left: 50%;
top: 50%;
transform-origin: 0 0;
}
.logo-mark::before {
width: 1.5px; height: 9px;
transform: translate(-50%, -100%) rotate(40deg);
}
.logo-mark::after {
width: 1.5px; height: 6px;
transform: translate(-50%, -100%) rotate(-20deg);
}
.logo-text { display: flex; flex-direction: column; line-height: 1.1 }
.logo-text small { font-size: 9px; color: var(--ouro-escuro); letter-spacing: 2.5px; text-transform: uppercase; font-family: 'Inter', sans-serif; font-weight: 500 }
nav.menu { display: flex; gap: 24px }
nav.menu a {
font-size: 12px;
color: var(--cinza);
text-decoration: none;
font-weight: 500;
letter-spacing: 0.3px;
transition: color 0.2s;
}
nav.menu a:hover { color: var(--ouro-escuro) }

/* HERO */
.hero {
text-align: center;
padding: 100px 24px 80px;
position: relative;
}
.hero-eyebrow {
display: inline-block;
font-size: 10px;
font-weight: 600;
color: var(--ouro-escuro);
letter-spacing: 3.5px;
text-transform: uppercase;
margin-bottom: 28px;
padding: 8px 20px;
border: 1px solid var(--linha);
border-radius: 999px;
background: rgba(255,255,255,0.6);
backdrop-filter: blur(8px);
}
.hero h1 {
font-family: 'Cormorant Garamond', serif;
font-size: clamp(42px, 8vw, 84px);
font-weight: 500;
line-height: 1.05;
letter-spacing: -2px;
color: var(--preto);
margin-bottom: 20px;
max-width: 880px;
margin-left: auto;
margin-right: auto;
}
.hero h1 .destaque {
font-style: italic;
color: var(--ouro-escuro);
font-weight: 500;
}
.hero-sub {
font-size: 16px;
color: var(--cinza);
max-width: 520px;
margin: 0 auto;
line-height: 1.75;
font-weight: 400;
}
.hero-divider {
width: 60px;
height: 1px;
background: var(--ouro);
margin: 36px auto 0;
position: relative;
}
.hero-divider::before, .hero-divider::after {
content: '';
position: absolute;
top: 50%;
width: 6px;
height: 6px;
background: var(--ouro);
transform: translateY(-50%) rotate(45deg);
}
.hero-divider::before { left: -10px }
.hero-divider::after { right: -10px }

/* VERSICULO DO DIA */
.versiculo {
max-width: 720px;
margin: 70px auto 80px;
padding: 56px 40px;
background: rgba(255, 255, 255, 0.7);
backdrop-filter: blur(10px);
border: 1px solid var(--linha);
border-radius: 4px;
position: relative;
text-align: center;
box-shadow: var(--sombra);
}
.versiculo::before, .versiculo::after {
content: '';
position: absolute;
width: 24px;
height: 24px;
border: 1.5px solid var(--ouro);
}
.versiculo::before { top: -1px; left: -1px; border-right: none; border-bottom: none }
.versiculo::after { bottom: -1px; right: -1px; border-left: none; border-top: none }
.versiculo-label {
font-size: 10px;
color: var(--ouro-escuro);
letter-spacing: 3px;
text-transform: uppercase;
margin-bottom: 22px;
font-weight: 600;
}
.versiculo-texto {
font-family: 'Cormorant Garamond', serif;
font-size: clamp(20px, 3.5vw, 28px);
font-weight: 400;
line-height: 1.45;
color: var(--preto);
font-style: italic;
margin-bottom: 18px;
letter-spacing: -0.3px;
}
.versiculo-ref {
font-size: 11px;
color: var(--ouro-escuro);
letter-spacing: 2.5px;
text-transform: uppercase;
font-weight: 600;
}

/* ESTUDO DO DIA */
.estudo {
max-width: 880px;
margin: 0 auto 80px;
padding: 0 24px;
}
.estudo-card {
background: var(--branco);
border: 1px solid var(--linha);
border-radius: 4px;
padding: 44px;
box-shadow: var(--sombra);
position: relative;
}
.estudo-eyebrow {
font-size: 10px;
color: var(--ouro-escuro);
letter-spacing: 3px;
text-transform: uppercase;
margin-bottom: 16px;
font-weight: 600;
display: flex;
align-items: center;
gap: 12px;
}
.estudo-eyebrow::before {
content: '';
width: 24px;
height: 1px;
background: var(--ouro);
}
.estudo-titulo {
font-family: 'Cormorant Garamond', serif;
font-size: clamp(24px, 4vw, 34px);
font-weight: 500;
line-height: 1.15;
color: var(--preto);
margin-bottom: 8px;
letter-spacing: -0.8px;
}
.estudo-base {
font-size: 12px;
color: var(--ouro-escuro);
letter-spacing: 1.5px;
text-transform: uppercase;
margin-bottom: 24px;
font-weight: 600;
}
.estudo-texto {
font-size: 15px;
color: var(--cinza-escuro);
line-height: 1.85;
margin-bottom: 24px;
white-space: pre-line;
}
.estudo-aplicacao {
padding-top: 24px;
border-top: 1px solid var(--linha);
font-size: 13px;
color: var(--cinza);
font-style: italic;
line-height: 1.7;
}
.estudo-aplicacao strong {
color: var(--ouro-escuro);
font-weight: 600;
font-style: normal;
letter-spacing: 1px;
text-transform: uppercase;
font-size: 11px;
display: block;
margin-bottom: 8px;
}

/* CONTEUDO PRINCIPAL */
.conteudo {
max-width: 1100px;
margin: 0 auto;
padding: 0 24px 80px;
}

.secao { margin-bottom: 80px }
.secao-header {
display: flex;
align-items: baseline;
justify-content: space-between;
margin-bottom: 32px;
padding-bottom: 16px;
border-bottom: 1px solid var(--linha);
}
.secao-titulo-wrap {
display: flex;
align-items: center;
gap: 14px;
}
.secao-icone {
font-size: 20px;
}
.secao-titulo {
font-family: 'Cormorant Garamond', serif;
font-size: clamp(22px, 4vw, 30px);
font-weight: 500;
color: var(--preto);
letter-spacing: -0.6px;
}
.secao-count {
font-size: 11px;
color: var(--ouro-escuro);
font-weight: 600;
letter-spacing: 1.5px;
text-transform: uppercase;
}

.secao-grid {
display: grid;
grid-template-columns: 1fr;
gap: 24px;
}
@media(min-width: 720px) {
.secao-grid { grid-template-columns: repeat(2, 1fr) }
}
@media(min-width: 1000px) {
.secao-grid { grid-template-columns: repeat(3, 1fr) }
}

.art-card {
background: var(--branco);
border: 1px solid var(--linha);
border-radius: 4px;
overflow: hidden;
cursor: pointer;
transition: all 0.3s ease;
animation: fadeUp 0.5s ease both;
display: flex;
flex-direction: column;
}
@keyframes fadeUp {
from { opacity: 0; transform: translateY(20px) }
to { opacity: 1; transform: translateY(0) }
}
.art-card:hover {
transform: translateY(-4px);
box-shadow: var(--sombra-forte);
border-color: var(--ouro-suave);
}
.card-img {
width: 100%;
height: 200px;
background-size: cover;
background-position: center;
background-color: var(--bege);
position: relative;
}
.card-img::after {
content: '';
position: absolute;
inset: 0;
background: linear-gradient(180deg, transparent 50%, rgba(26, 22, 18, 0.15));
}
.card-body {
padding: 22px 22px 20px;
display: flex;
flex-direction: column;
flex: 1;
}
.card-meta {
display: flex;
align-items: center;
gap: 10px;
font-size: 10px;
margin-bottom: 12px;
}
.card-cat {
font-weight: 700;
letter-spacing: 1.2px;
text-transform: uppercase;
}
.card-tipo {
color: var(--cinza);
padding: 2px 8px;
border: 1px solid var(--linha);
border-radius: 999px;
font-size: 9px;
font-weight: 600;
letter-spacing: 1px;
text-transform: uppercase;
}
.card-title {
font-family: 'Cormorant Garamond', serif;
font-size: 20px;
font-weight: 600;
line-height: 1.25;
color: var(--preto);
margin-bottom: 10px;
letter-spacing: -0.4px;
}
.card-resumo {
font-size: 13px;
color: var(--cinza);
line-height: 1.65;
margin-bottom: 16px;
flex: 1;
}
.card-footer {
display: flex;
justify-content: space-between;
font-size: 10px;
color: var(--cinza);
padding-top: 14px;
border-top: 1px solid var(--linha);
letter-spacing: 0.5px;
}
.card-fonte { font-weight: 600 }
.card-data { font-style: italic }

/* MODAL ARTIGO */
.modal {
display: none;
position: fixed;
inset: 0;
background: rgba(26, 22, 18, 0.6);
backdrop-filter: blur(10px);
z-index: 1000;
padding: 16px;
overflow-y: auto;
}
.modal.aberto {
display: flex;
align-items: flex-start;
justify-content: center;
animation: fadeIn 0.25s ease;
}
@keyframes fadeIn { from{opacity:0} to{opacity:1} }
.modal-box {
background: var(--branco);
border: 1px solid var(--linha);
border-radius: 4px;
max-width: 720px;
width: 100%;
margin: auto;
position: relative;
animation: slideUp 0.35s ease;
overflow: hidden;
}
@keyframes slideUp {
from { opacity: 0; transform: translateY(20px) }
to { opacity: 1; transform: translateY(0) }
}
.modal-close {
position: absolute;
top: 18px;
right: 18px;
width: 36px;
height: 36px;
border-radius: 50%;
background: rgba(255,255,255,0.95);
border: 1px solid var(--linha);
color: var(--preto);
font-size: 22px;
font-weight: 300;
cursor: pointer;
z-index: 10;
display: flex;
align-items: center;
justify-content: center;
transition: all 0.2s;
}
.modal-close:hover { background: var(--ouro); color: white; border-color: var(--ouro) }
.modal-art-img {
width: 100%;
height: 280px;
background-size: cover;
background-position: center;
background-color: var(--bege);
}
.modal-body { padding: 36px 32px 32px }
.modal-meta {
display: flex;
gap: 12px;
align-items: center;
margin-bottom: 14px;
font-size: 10px;
}
.modal-cat {
font-weight: 700;
letter-spacing: 1.5px;
text-transform: uppercase;
}
.modal-tipo {
padding: 3px 10px;
border: 1px solid var(--linha);
border-radius: 999px;
font-weight: 600;
letter-spacing: 1px;
text-transform: uppercase;
font-size: 9px;
color: var(--cinza);
}
.modal-title {
font-family: 'Cormorant Garamond', serif;
font-size: clamp(24px, 4.5vw, 34px);
font-weight: 500;
line-height: 1.15;
color: var(--preto);
margin-bottom: 14px;
letter-spacing: -0.6px;
}
.modal-info {
display: flex;
gap: 8px;
font-size: 11px;
color: var(--cinza);
margin-bottom: 24px;
padding-bottom: 18px;
border-bottom: 1px solid var(--linha);
letter-spacing: 0.5px;
}
.modal-resumo {
font-size: 15px;
color: var(--cinza-escuro);
line-height: 1.8;
margin-bottom: 28px;
}
.modal-analise {
background: var(--bege);
padding: 22px 24px;
border-left: 3px solid var(--ouro);
margin-bottom: 24px;
border-radius: 0 4px 4px 0;
}
.modal-analise-titulo {
font-size: 10px;
letter-spacing: 2.5px;
text-transform: uppercase;
font-weight: 700;
color: var(--ouro-escuro);
margin-bottom: 10px;
}
.modal-analise-texto {
font-family: 'Cormorant Garamond', serif;
font-size: 17px;
line-height: 1.55;
color: var(--cinza-escuro);
font-style: italic;
}
.modal-fonte-link {
display: inline-block;
font-size: 12px;
color: var(--ouro-escuro);
text-decoration: none;
font-weight: 600;
letter-spacing: 0.5px;
border-bottom: 1px solid var(--ouro-suave);
padding-bottom: 2px;
transition: all 0.2s;
}
.modal-fonte-link:hover { color: var(--preto); border-color: var(--ouro-escuro) }

/* NEWSLETTER */
.newsletter {
max-width: 620px;
margin: 0 auto 80px;
padding: 50px 32px;
text-align: center;
background: var(--branco);
border: 1px solid var(--linha);
border-radius: 4px;
position: relative;
box-shadow: var(--sombra);
}
.newsletter::before {
content: '';
position: absolute;
top: 0;
left: 50%;
transform: translateX(-50%);
width: 60px;
height: 1px;
background: var(--ouro);
}
.nl-eyebrow {
font-size: 10px;
letter-spacing: 3px;
text-transform: uppercase;
font-weight: 600;
color: var(--ouro-escuro);
margin-bottom: 14px;
}
.nl-titulo {
font-family: 'Cormorant Garamond', serif;
font-size: 28px;
font-weight: 500;
color: var(--preto);
margin-bottom: 8px;
letter-spacing: -0.5px;
}
.nl-desc {
font-size: 13px;
color: var(--cinza);
margin-bottom: 28px;
}
.nl-form {
display: flex;
gap: 8px;
max-width: 420px;
margin: 0 auto;
}
.nl-input {
flex: 1;
border: 1px solid var(--linha);
background: var(--off-white);
padding: 13px 16px;
font-size: 13px;
color: var(--preto);
font-family: inherit;
border-radius: 2px;
outline: none;
transition: border 0.2s;
}
.nl-input:focus { border-color: var(--ouro) }
.nl-btn {
background: var(--preto);
color: var(--branco);
border: none;
padding: 13px 22px;
font-size: 12px;
font-weight: 600;
letter-spacing: 1.5px;
text-transform: uppercase;
cursor: pointer;
font-family: inherit;
transition: all 0.2s;
border-radius: 2px;
}
.nl-btn:hover { background: var(--ouro-escuro) }
.nl-ok {
display: none;
margin-top: 12px;
font-size: 12px;
color: var(--ouro-escuro);
font-weight: 600;
}

/* FOOTER */
footer {
border-top: 1px solid var(--linha);
padding: 50px 24px 40px;
text-align: center;
background: var(--branco);
}
.footer-mark {
display: inline-block;
width: 40px;
height: 40px;
border: 1.5px solid var(--ouro);
border-radius: 50%;
margin-bottom: 16px;
position: relative;
}
.footer-mark::before, .footer-mark::after {
content: '';
position: absolute;
background: var(--ouro);
left: 50%;
top: 50%;
transform-origin: 0 0;
}
.footer-mark::before {
width: 1.5px; height: 12px;
transform: translate(-50%, -100%) rotate(40deg);
}
.footer-mark::after {
width: 1.5px; height: 8px;
transform: translate(-50%, -100%) rotate(-20deg);
}
.footer-titulo {
font-family: 'Cormorant Garamond', serif;
font-size: 18px;
font-weight: 600;
color: var(--preto);
letter-spacing: -0.3px;
margin-bottom: 4px;
}
.footer-sub {
font-size: 10px;
color: var(--ouro-escuro);
letter-spacing: 2.5px;
text-transform: uppercase;
margin-bottom: 20px;
font-weight: 600;
}
.footer-versiculo {
font-family: 'Cormorant Garamond', serif;
font-style: italic;
font-size: 14px;
color: var(--cinza);
max-width: 480px;
margin: 0 auto 16px;
line-height: 1.6;
}
.footer-ref {
font-size: 10px;
color: var(--ouro-escuro);
letter-spacing: 2px;
font-weight: 600;
}

@media (max-width: 720px) {
header { padding: 0 16px; height: 64px }
.logo { font-size: 18px; gap: 10px }
.logo-mark { width: 26px; height: 26px }
.logo-text small { font-size: 8px; letter-spacing: 2px }
nav.menu { display: none }
.hero { padding: 60px 18px 50px }
.versiculo { padding: 40px 24px; margin: 50px 16px 60px }
.estudo-card { padding: 28px 22px }
.modal-body { padding: 28px 22px }
.modal-art-img { height: 200px }
.nl-form { flex-direction: column }
.relogio-fundo { width: 130vw; height: 130vw }
}
"""

JS = r"""
function abreArtigo(idx) {
const m = document.getElementById('art-' + idx);
if (m) {
m.classList.add('aberto');
document.body.style.overflow = 'hidden';
}
}
function fechaModal(id) {
const m = document.getElementById(id);
if (m) {
m.classList.remove('aberto');
document.body.style.overflow = '';
}
}
document.addEventListener('keydown', function(e) {
if (e.key === 'Escape') {
document.querySelectorAll('.modal.aberto').forEach(m => fechaModal(m.id));
}
});
function newsletter() {
const e = document.getElementById('nl-email').value;
if (!e || e.indexOf('@') < 0) { alert('Email invalido'); return; }
fetch('https://formsubmit.co/ajax/SEU_EMAIL@gmail.com', {
method: 'POST',
headers: {'Content-Type': 'application/json', 'Accept': 'application/json'},
body: JSON.stringify({email: e, _subject: 'Newsletter A Volta Esta Proxima'})
}).catch(() => {});
document.getElementById('nl-ok').style.display = 'block';
document.getElementById('nl-email').value = '';
}
if ('serviceWorker' in navigator) {
window.addEventListener('load', function() {
navigator.serviceWorker.register('/service-worker.js').catch(() => {});
});
}
"""

RELOGIO_SVG = """<div class="relogio-fundo" aria-hidden="true">
<svg viewBox="0 0 800 800" xmlns="http://www.w3.org/2000/svg">
<circle cx="400" cy="400" r="380" fill="none" stroke="#c9a961" stroke-width="2"/>
<circle cx="400" cy="400" r="350" fill="none" stroke="#c9a961" stroke-width="0.5"/>
<g stroke="#c9a961" stroke-width="2">
<line x1="400" y1="40" x2="400" y2="80"/>
<line x1="400" y1="720" x2="400" y2="760"/>
<line x1="40" y1="400" x2="80" y2="400"/>
<line x1="720" y1="400" x2="760" y2="400"/>
</g>
<g stroke="#c9a961" stroke-width="1" opacity="0.5">
<line x1="400" y1="40" x2="400" y2="60" transform="rotate(30 400 400)"/>
<line x1="400" y1="40" x2="400" y2="60" transform="rotate(60 400 400)"/>
<line x1="400" y1="40" x2="400" y2="60" transform="rotate(120 400 400)"/>
<line x1="400" y1="40" x2="400" y2="60" transform="rotate(150 400 400)"/>
<line x1="400" y1="40" x2="400" y2="60" transform="rotate(210 400 400)"/>
<line x1="400" y1="40" x2="400" y2="60" transform="rotate(240 400 400)"/>
<line x1="400" y1="40" x2="400" y2="60" transform="rotate(300 400 400)"/>
<line x1="400" y1="40" x2="400" y2="60" transform="rotate(330 400 400)"/>
</g>
<text x="400" y="105" text-anchor="middle" font-family="Cormorant Garamond,serif" font-size="36" fill="#c9a961" font-weight="500">XII</text>
<text x="690" y="415" text-anchor="middle" font-family="Cormorant Garamond,serif" font-size="36" fill="#c9a961" font-weight="500">III</text>
<text x="400" y="720" text-anchor="middle" font-family="Cormorant Garamond,serif" font-size="36" fill="#c9a961" font-weight="500">VI</text>
<text x="115" y="415" text-anchor="middle" font-family="Cormorant Garamond,serif" font-size="36" fill="#c9a961" font-weight="500">IX</text>
<line class="ponteiro-h" x1="400" y1="400" x2="400" y2="200" stroke="#c9a961" stroke-width="4" stroke-linecap="round"/>
<line class="ponteiro-m" x1="400" y1="400" x2="400" y2="120" stroke="#c9a961" stroke-width="2.5" stroke-linecap="round"/>
<circle cx="400" cy="400" r="10" fill="#c9a961"/>
<circle cx="400" cy="400" r="3" fill="#fbfaf7"/>
</svg>
</div>"""

def gerar_html():
    artigos = carregar_json(ARTIGOS_FILE, [])
    versiculos = carregar_json(VERSICULOS_FILE, [])
    estudos = carregar_json(ESTUDOS_FILE, [])

    for i, a in enumerate(artigos):
        a["_idx"] = i

    artigos.sort(key=lambda a: a.get("data",""), reverse=True)

    vd = versiculo_do_dia(versiculos)
    ed = estudo_do_dia(estudos)

    por_cat = {}
    for a in artigos:
        cat = a.get("categoria", "noticias")
        por_cat.setdefault(cat, []).append(a)

    html = '<!DOCTYPE html><html lang="pt-BR"><head>'
    html += '<meta charset="UTF-8">'
    html += '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
    html += '<title>A Volta Esta Proxima | Portal Cristao Premium</title>'
    html += '<meta name="description" content="Portal cristao protestante premium com noticias globais, perseguicao, milagres, sinais dos tempos e analise biblica.">'
    html += '<link rel="manifest" href="manifest.json">'
    html += '<meta name="theme-color" content="#fbfaf7">'
    html += '<meta name="apple-mobile-web-app-capable" content="yes">'
    html += '<meta name="apple-mobile-web-app-title" content="A Volta">'
    html += '<link rel="apple-touch-icon" href="icon-192.svg">'
    html += '<link rel="icon" type="image/svg+xml" href="icon-192.svg">'
    html += '<link rel="preconnect" href="https://fonts.googleapis.com">'
    html += '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    html += '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">'
    html += '<style>' + CSS + '</style></head><body>'

    html += RELOGIO_SVG
    html += '<div class="wrap">'

    html += '<header><a class="logo" href="#">'
    html += '<span class="logo-mark"></span>'
    html += '<span class="logo-text">A Volta Esta Proxima<small>Portal Cristao</small></span></a>'
    html += '<nav class="menu">'
    html += '<a href="#sec-perseguicao">Perseguicao</a>'
    html += '<a href="#sec-milagres">Milagres</a>'
    html += '<a href="#sec-sinais">Sinais</a>'
    html += '<a href="#sec-documentarios">Reportagens</a>'
    html += '</nav></header>'

    html += '<section class="hero">'
    html += '<div class="hero-eyebrow">Vigilancia & Discernimento</div>'
    html += '<h1>Discernindo os <span class="destaque">sinais</span> dos nossos tempos</h1>'
    html += '<p class="hero-sub">Um portal de curadoria global sobre perseguicao, milagres, testemunhos e os acontecimentos do mundo cristao protestante - com analise biblica e sem sensacionalismo.</p>'
    html += '<div class="hero-divider"></div>'
    html += '</section>'

    if vd.get("texto"):
        html += '<div class="versiculo">'
        html += '<div class="versiculo-label">Versiculo do Dia</div>'
        html += f'<div class="versiculo-texto">"{vd["texto"]}"</div>'
        html += f'<div class="versiculo-ref">{vd["ref"]}</div>'
        html += '</div>'

    if ed:
        html += '<section class="estudo"><div class="estudo-card">'
        html += '<div class="estudo-eyebrow">Estudo do Dia</div>'
        html += f'<h2 class="estudo-titulo">{ed["titulo"]}</h2>'
        html += f'<div class="estudo-base">{ed["texto_base"]} · {ed["tema"]}</div>'
        html += f'<div class="estudo-texto">{ed["conteudo"]}</div>'
        html += f'<div class="estudo-aplicacao"><strong>Aplicacao</strong>{ed["aplicacao"]}</div>'
        html += '</div></section>'

    html += '<div class="conteudo">'

    ordem = ["perseguicao", "milagres", "testemunhos", "sinais", "documentarios", "noticias"]
    for cat_id in ordem:
        if cat_id in por_cat:
            html += gerar_secao_categoria(cat_id, por_cat[cat_id])

    html += '<section class="newsletter">'
    html += '<div class="nl-eyebrow">Receba a curadoria</div>'
    html += '<div class="nl-titulo">Mantenha-se vigilante</div>'
    html += '<p class="nl-desc">Conteudo selecionado, sem sensacionalismo, no seu email.</p>'
    html += '<div class="nl-form">'
    html += '<input class="nl-input" type="email" id="nl-email" placeholder="seu@email.com">'
    html += '<button class="nl-btn" onclick="newsletter()">Inscrever</button>'
    html += '</div>'
    html += '<div class="nl-ok" id="nl-ok">Inscricao confirmada.</div>'
    html += '</section>'

    html += '</div>'

    for a in artigos:
        html += gerar_modal_artigo(a, a["_idx"])

    html += '<footer>'
    html += '<div class="footer-mark"></div>'
    html += '<div class="footer-titulo">A Volta Esta Proxima</div>'
    html += '<div class="footer-sub">Portal Cristao Protestante</div>'
    html += '<p class="footer-versiculo">"Eis que venho sem demora; e o meu galardao esta comigo, para retribuir a cada um segundo as suas obras."</p>'
    html += '<div class="footer-ref">Apocalipse 22:12</div>'
    html += '</footer>'

    html += '</div>'
    html += '<script>' + JS + '</script>'
    html += '</body></html>'

    return html

MANIFEST = """{
  "name": "A Volta Esta Proxima",
  "short_name": "A Volta",
  "description": "Portal cristao protestante premium",
  "start_url": "/",
  "display": "standalone",
  "orientation": "portrait",
  "background_color": "#fbfaf7",
  "theme_color": "#c9a961",
  "lang": "pt-BR",
  "icons": [
    {"src": "icon-192.svg", "sizes": "192x192", "type": "image/svg+xml", "purpose": "any maskable"},
    {"src": "icon-512.svg", "sizes": "512x512", "type": "image/svg+xml", "purpose": "any maskable"}
  ]
}"""

SERVICE_WORKER = """const CACHE = 'avolta-v1';
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(['/', '/index.html']).catch(() => {})));
  self.skipWaiting();
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ns => Promise.all(ns.map(n => n !== CACHE && caches.delete(n)))));
  self.clients.claim();
});
self.addEventListener('fetch', e => {
  e.respondWith(fetch(e.request).catch(() => caches.match(e.request)));
});
"""

ICON_SVG = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 512 512'>
<rect width='512' height='512' rx='90' fill='#fbfaf7'/>
<circle cx='256' cy='256' r='190' fill='none' stroke='#c9a961' stroke-width='8'/>
<circle cx='256' cy='256' r='170' fill='none' stroke='#c9a961' stroke-width='2' opacity='0.5'/>
<line x1='256' y1='256' x2='256' y2='130' stroke='#c9a961' stroke-width='10' stroke-linecap='round'/>
<line x1='256' y1='256' x2='340' y2='256' stroke='#c9a961' stroke-width='6' stroke-linecap='round'/>
<circle cx='256' cy='256' r='14' fill='#c9a961'/>
<circle cx='256' cy='256' r='5' fill='#fbfaf7'/>
<text x='256' y='95' text-anchor='middle' font-family='Georgia,serif' font-size='32' fill='#c9a961' font-weight='600'>XII</text>
</svg>"""

def main():
    print("\nA Volta Esta Proxima - " + datetime.now().strftime("%d/%m/%Y %H:%M"))
    print("=" * 50)
    html = gerar_html()
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    with open("manifest.json", "w", encoding="utf-8") as f:
        f.write(MANIFEST)
    with open("service-worker.js", "w", encoding="utf-8") as f:
        f.write(SERVICE_WORKER)
    with open("icon-192.svg", "w", encoding="utf-8") as f:
        f.write(ICON_SVG)
    with open("icon-512.svg", "w", encoding="utf-8") as f:
        f.write(ICON_SVG)
    print("Site gerado com sucesso!")
    print(f"  index.html ({len(html)} bytes)")

if __name__ == "__main__":
    main()
