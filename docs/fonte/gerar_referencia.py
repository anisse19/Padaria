"""Gera docs/Referencia_do_Codigo.pdf (versão Java).

Uso: python3 docs/fonte/gerar_referencia.py docs/Referencia_do_Codigo.pdf
Precisa de reportlab e das fontes Liberation e DejaVu (caminhos de Linux em F).
"""
import re
import sys

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Flowable, Frame, KeepTogether,
                                NextPageTemplate, PageBreak, PageTemplate, Paragraph, Spacer,
                                Table, TableStyle)

SAIDA = sys.argv[1]

# ---------------- FONTES ----------------
F = "/usr/share/fonts/truetype/"
pdfmetrics.registerFont(TTFont("Serif-B", F + "liberation/LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Serif-I", F + "liberation/LiberationSerif-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Sans", F + "liberation/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Sans-B", F + "liberation/LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans-I", F + "liberation/LiberationSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Sans-BI", F + "liberation/LiberationSans-BoldItalic.ttf"))
pdfmetrics.registerFont(TTFont("Mono", F + "dejavu/DejaVuSansMono.ttf"))
pdfmetrics.registerFont(TTFont("Mono-B", F + "dejavu/DejaVuSansMono-Bold.ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-BI")

# ---------------- CORES (as mesmas do programa) ----------------
FUNDO = HexColor("#FBF3E4")
PAINEL = HexColor("#F3E1C7")
CROSTA = HexColor("#8B5A2B")
CROSTA_ESCURA = HexColor("#5C3A1E")
DOURADO = HexColor("#D9A441")
TEXTO = HexColor("#3E2A1E")
TEXTO_SUAVE = HexColor("#7A6555")
NO_FUNDO = HexColor("#F6DDAA")
REMOVIDO = HexColor("#F4C7C3")
VERMELHO = HexColor("#B3261E")
CINZA = HexColor("#888888")

# ---------------- ESTILOS ----------------
corpo = ParagraphStyle("corpo", fontName="Sans", fontSize=10.5, leading=16, textColor=TEXTO, spaceAfter=7)
pequeno = ParagraphStyle("pequeno", parent=corpo, fontSize=9, leading=13, spaceAfter=4)
legenda = ParagraphStyle("legenda", parent=corpo, fontName="Sans-I", fontSize=8, leading=11,
                         textColor=TEXTO_SUAVE, alignment=TA_CENTER, spaceAfter=10)
titulo_parte = ParagraphStyle("parte", fontName="Serif-B", fontSize=22, leading=27, textColor=CROSTA, spaceAfter=4)
subtitulo_parte = ParagraphStyle("subparte", fontName="Serif-I", fontSize=11.5, leading=15,
                                 textColor=TEXTO_SUAVE, spaceAfter=14)
h2 = ParagraphStyle("h2", fontName="Serif-B", fontSize=15, leading=19, textColor=CROSTA,
                    spaceBefore=12, spaceAfter=6, keepWithNext=1)
h3 = ParagraphStyle("h3", fontName="Serif-B", fontSize=12, leading=15, textColor=CROSTA_ESCURA,
                    spaceBefore=10, spaceAfter=3, keepWithNext=1)
celula = ParagraphStyle("celula", fontName="Sans", fontSize=8, leading=10.5, textColor=TEXTO)
celula_mono = ParagraphStyle("celula_mono", parent=celula, fontName="Mono", fontSize=7.3, textColor=TEXTO_SUAVE)
celula_cab = ParagraphStyle("celula_cab", parent=celula, fontName="Sans-B", textColor=white)
caixa_titulo = ParagraphStyle("caixa_t", parent=pequeno, fontName="Sans-B", fontSize=8.5, spaceAfter=2)
caixa_texto = ParagraphStyle("caixa_x", parent=pequeno, fontSize=8.5, leading=12.5, spaceAfter=0)


def md(texto):
    """Mini-markup: `código`, **negrito**, _itálico_. Escapa < > &."""
    texto = texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    texto = re.sub(r"`([^`]+)`", r'<font name="Mono" size="0.92em" color="#5C3A1E">\1</font>', texto)
    texto = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", texto)
    texto = re.sub(r"(?<![\w/])_([^_]+?)_(?![\w])", r"<i>\1</i>", texto)
    texto = texto.replace("&lt;br/&gt;", "<br/>")
    return texto.replace('size="0.92em"', 'size="9.5"')


def P(texto, estilo=corpo):
    t = md(texto)
    if estilo in (celula, pequeno, caixa_texto):
        t = t.replace('size="9.5"', 'size="%.1f"' % (estilo.fontSize * 0.92))
    return Paragraph(t, estilo)


def caixa_programador(texto):
    """Caixa creme 'Em linguagem de programador' com barra dourada à esquerda."""
    t = Table([[[P("Em linguagem de programador", caixa_titulo), P(texto, caixa_texto)]]], colWidths=[None])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PAINEL),
        ("LINEBEFORE", (0, 0), (0, -1), 3, DOURADO),
        ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return KeepTogether([Spacer(1, 4), t, Spacer(1, 12)])


LARGURA_UTIL = A4[0] - 2 * 22 * mm


def tabela(cabecalho, linhas, larguras, mono_col0=True):
    dados = [[Paragraph(c, celula_cab) for c in cabecalho]]
    for linha in linhas:
        dados.append([P(c, celula_mono if (i == 0 and mono_col0) else celula) for i, c in enumerate(linha)])
    total = sum(larguras)
    t = Table(dados, colWidths=[LARGURA_UTIL * l / total for l in larguras], repeatRows=1)
    estilo = [
        ("BACKGROUND", (0, 0), (-1, 0), CROSTA),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW", (0, 1), (-1, -1), 0.4, PAINEL),
    ]
    for i in range(2, len(dados), 2):
        estilo.append(("BACKGROUND", (0, i), (-1, i), FUNDO))
    t.setStyle(TableStyle(estilo))
    return t


def variaveis(linhas):
    return [tabela(["Variável", "Tipo", "Significado"], linhas, [30, 20, 50]), Spacer(1, 8)]


def funcoes(linhas):
    return [tabela(["Função", "O que faz", "Como"], linhas, [31, 22, 47]), Spacer(1, 8)]


def classe(nome, descricao):
    d = P(descricao, pequeno)
    return [CondPageBreak(60 * mm), Paragraph(md(nome), h3), d]


# ---------------- DIAGRAMAS ----------------

class Diagrama(Flowable):
    def __init__(self, altura):
        super().__init__()
        self.altura = altura

    def wrap(self, aw, ah):
        self.largura = aw
        return aw, self.altura

    # utilitários
    def caixa(self, c, x, y, w, h, linha1, linha2, cor=NO_FUNDO, borda=DOURADO, serif=False, tracejada=False):
        c.setFillColor(cor)
        c.setStrokeColor(borda)
        c.setLineWidth(1.2)
        if tracejada:
            c.setDash(2, 2)
        c.roundRect(x, y, w, h, 6, stroke=1, fill=1)
        c.setDash()
        if serif:
            c.setFillColor(CROSTA)
            c.setFont("Serif-B", 11)
            c.drawCentredString(x + w / 2, y + h - 17, linha1)
            c.setFillColor(TEXTO_SUAVE)
            c.setFont("Sans", 7.5)
            c.drawCentredString(x + w / 2, y + 9, linha2)
        else:
            c.setFillColor(TEXTO_SUAVE)
            c.setFont("Sans", 7)
            if linha2:
                c.drawCentredString(x + w / 2, y + h - 12, linha1)
                c.setFillColor(TEXTO)
                c.setFont("Sans-B", 8)
                c.drawCentredString(x + w / 2, y + 8, linha2)
            else:
                c.drawCentredString(x + w / 2, y + h / 2 - 3, linha1)

    def seta(self, c, x1, y1, x2, y2, cor, largura=1.4):
        import math
        c.setStrokeColor(cor)
        c.setFillColor(cor)
        c.setLineWidth(largura)
        c.line(x1, y1, x2, y2)
        a = math.atan2(y2 - y1, x2 - x1)
        p = c.beginPath()
        p.moveTo(x2, y2)
        p.lineTo(x2 - 6 * math.cos(a - 0.4), y2 - 6 * math.sin(a - 0.4))
        p.lineTo(x2 - 6 * math.cos(a + 0.4), y2 - 6 * math.sin(a + 0.4))
        p.close()
        c.drawPath(p, fill=1, stroke=0)

    def texto(self, c, x, y, s, fonte="Sans-I", tam=7, cor=TEXTO, centrado=True):
        c.setFont(fonte, tam)
        c.setFillColor(cor)
        (c.drawCentredString if centrado else c.drawString)(x, y, s)


class Ecras(Diagrama):
    """A porta -> O porteiro -> A loja, com a seta de 'Sair'."""

    def __init__(self):
        super().__init__(78)

    def draw(self):
        c = self.canv
        w, h, y = 100, 44, 26
        xs = [0, (self.largura - w) / 2, self.largura - w]
        nomes = [("A porta", "TelaInicial"), ("O porteiro", "TelaLogin"), ("A loja", "AplicacaoPadaria")]
        for x, (a, b) in zip(xs, nomes):
            self.caixa(c, x, y, w, h, a, b, serif=True)
        for i, rot in enumerate(["Acessar", "senha certa"]):
            x1, x2 = xs[i] + w + 4, xs[i + 1] - 4
            self.seta(c, x1, y + h / 2, x2, y + h / 2, CROSTA)
            self.texto(c, (x1 + x2) / 2, y + h / 2 + 5, rot)
        c.setStrokeColor(DOURADO)
        c.setLineWidth(1.4)
        c.line(xs[2] + w / 2, y, xs[2] + w / 2, 8)
        c.line(xs[2] + w / 2, 8, xs[0] + w / 2, 8)
        self.seta(c, xs[0] + w / 2, 8, xs[0] + w / 2, y - 1, DOURADO)
        self.texto(c, self.largura / 2, 11, "Sair")


class Fila(Diagrama):
    """Nós ligados nos dois sentidos, com primeiro/ultimo e null nas pontas."""

    def __init__(self, nos, rot_primeiro="primeiro", rot_ultimo="último", legenda_frente="mão da frente",
                 legenda_tras="mão de trás", mono=False):
        super().__init__(110)
        self.nos, self.rp, self.ru = nos, rot_primeiro, rot_ultimo
        self.lf, self.lt, self.mono = legenda_frente, legenda_tras, mono

    def draw(self):
        c = self.canv
        n = len(self.nos)
        margem = 34
        w, h = 66, 34
        passo = (self.largura - 2 * margem - w) / (n - 1)
        y = 40
        xs = [margem + i * passo for i in range(n)]
        for x, (a, b) in zip(xs, self.nos):
            self.caixa(c, x, y, w, h, a, b)
        for i in range(n - 1):
            self.seta(c, xs[i] + w + 2, y + h - 10, xs[i + 1] - 2, y + h - 10, CROSTA_ESCURA)
            self.seta(c, xs[i + 1] - 2, y + 10, xs[i] + w + 2, y + 10, DOURADO)
        self.seta(c, xs[0] - 2, y + 10, 14, y + 2, DOURADO, 1)
        self.seta(c, xs[-1] + w + 2, y + h - 10, self.largura - 14, y + h - 2, CROSTA_ESCURA, 1)
        self.texto(c, 8, y - 4, "null", "Sans", 7, TEXTO_SUAVE)
        self.texto(c, self.largura - 8, y + h - 10, "null", "Sans", 7, TEXTO_SUAVE)
        fonte = "Mono-B" if self.mono else "Sans-B"
        for x, rot in [(xs[0], self.rp), (xs[-1], self.ru)]:
            self.texto(c, x + w / 2, y + h + 26, rot, fonte, 8, CROSTA_ESCURA)
            self.seta(c, x + w / 2, y + h + 22, x + w / 2, y + h + 3, CROSTA_ESCURA, 1)
        # legenda
        lx = self.largura / 2 - 110
        c.setStrokeColor(CROSTA_ESCURA)
        c.setLineWidth(1.6)
        c.line(lx, 12, lx + 18, 12)
        self.texto(c, lx + 24, 9, self.lf, "Mono" if self.mono else "Sans", 7, TEXTO, False)
        c.setStrokeColor(DOURADO)
        c.line(lx + 120, 12, lx + 138, 12)
        self.texto(c, lx + 144, 9, self.lt, "Mono" if self.mono else "Sans", 7, TEXTO, False)


class Remocao(Diagrama):
    def __init__(self):
        super().__init__(175)

    def draw(self):
        c = self.canv
        w, h = 88, 36
        x0, x2 = 70, self.largura - 88 - 10
        x1 = (x0 + x2) / 2
        # Antes
        y = 125
        self.texto(c, 0, y + 13, "Antes", "Serif-B", 10, CROSTA, False)
        self.caixa(c, x0, y, w, h, "n.º 1", "Pão de forma")
        self.caixa(c, x1, y, w, h, "n.º 2", "Bolo", REMOVIDO, VERMELHO)
        self.caixa(c, x2, y, w, h, "n.º 3", "Pastel")
        for a, b in [(x0, x1), (x1, x2)]:
            self.seta(c, a + w + 2, y + h - 10, b - 2, y + h - 10, CROSTA_ESCURA)
            self.seta(c, b - 2, y + 10, a + w + 2, y + 10, DOURADO)
        self.texto(c, x1 + w / 2, y - 11, "vai-se embora", "Sans-BI", 7.5, VERMELHO)
        # Depois
        y = 55
        self.texto(c, 0, y + 13, "Depois", "Serif-B", 10, CROSTA, False)
        self.caixa(c, x0, y, w, h, "n.º 1", "Pão de forma")
        self.caixa(c, x2, y, w, h, "n.º 3", "Pastel")
        self.seta(c, x0 + w + 2, y + h - 10, x2 - 2, y + h - 10, CROSTA_ESCURA)
        self.seta(c, x2 - 2, y + 10, x0 + w + 2, y + 10, DOURADO)
        self.caixa(c, x1 + 8, 8, w - 16, 22, "Bolo (fora da fila)", None, FUNDO, CINZA, tracejada=True)


class Bolha(Diagrama):
    def __init__(self):
        super().__init__(92)

    def draw(self):
        c = self.canv
        w, h = 46, 26
        for y, rot, vals in [(56, "Antes:", [45, 15, 80, 350]), (8, "Depois:", [15, 45, 80, 350])]:
            self.texto(c, 0, y + 9, rot, "Sans-B", 9, TEXTO, False)
            for i, v in enumerate(vals):
                troca = rot == "Antes:" and i < 2
                self.caixa(c, 60 + i * 62, y, w, h, str(v), None, REMOVIDO if troca else NO_FUNDO,
                           VERMELHO if troca else DOURADO)
                c.setFont("Sans-B", 9)
                c.setFillColor(TEXTO)
                c.drawCentredString(60 + i * 62 + w / 2, y + 9, str(v))
        self.texto(c, 330, 72, "45 é maior que 15 e está à frente,", "Sans-I", 7.5, TEXTO_SUAVE, False)
        self.texto(c, 330, 62, "por isso trocam de lugar.", "Sans-I", 7.5, TEXTO_SUAVE, False)


# ---------------- PÁGINAS ----------------

def capa(c, doc):
    c.saveState()
    c.setFillColor(FUNDO)
    c.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    c.setFillColor(CROSTA)
    c.rect(0, 0, A4[0], 70 * mm, fill=1, stroke=0)
    c.setFillColor(DOURADO)
    c.rect(0, 70 * mm, A4[0], 3 * mm, fill=1, stroke=0)
    cx = A4[0] / 2
    c.setFillColor(CROSTA)
    c.setFont("Serif-B", 40)
    c.drawCentredString(cx, A4[1] - 115 * mm, "Padaria Adonai")
    c.setFillColor(TEXTO_SUAVE)
    c.setFont("Serif-I", 16)
    c.drawCentredString(cx, A4[1] - 127 * mm, "Referência do Código · Versão Java")
    c.setFillColor(TEXTO)
    c.setFont("Sans", 10.5)
    for i, s in enumerate(["Sistema de Gestão de Padaria",
                           "Trabalho Prático 1 · Algoritmos e Estruturas de Dados",
                           "ISUTC · Engenharia Informática e de Telecomunicações"]):
        c.drawCentredString(cx, A4[1] - 152 * mm - i * 15, s)
    for i, (a, b) in enumerate([("Parte 1", " · Como funciona o sistema"),
                                ("Parte 2", " · Referência técnica: classes, variáveis e funções")]):
        y = A4[1] - 195 * mm - i * 15
        largura = c.stringWidth(a, "Sans-B", 10.5) + c.stringWidth(b, "Sans", 10.5)
        x = cx - largura / 2
        c.setFont("Sans-B", 10.5)
        c.drawString(x, y, a)
        c.setFont("Sans", 10.5)
        c.drawString(x + c.stringWidth(a, "Sans-B", 10.5), y, b)
    c.restoreState()


def pagina(c, doc):
    c.saveState()
    c.setFont("Serif-I", 8.5)
    c.setFillColor(TEXTO_SUAVE)
    c.drawString(22 * mm, A4[1] - 13 * mm, "Padaria Adonai · Referência do Código")
    c.setStrokeColor(PAINEL)
    c.setLineWidth(0.6)
    c.line(22 * mm, A4[1] - 15.5 * mm, A4[0] - 22 * mm, A4[1] - 15.5 * mm)
    c.setFont("Sans", 8.5)
    c.drawRightString(A4[0] - 22 * mm, 12 * mm, str(doc.page))
    c.restoreState()


doc = BaseDocTemplate(SAIDA, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm,
                      topMargin=24 * mm, bottomMargin=20 * mm,
                      title="Padaria Adonai - Referência do Código",
                      subject="Sistema de Gestão de Padaria - TP1 AED (Java)")
moldura = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
doc.addPageTemplates([PageTemplate("capa", [moldura], onPage=capa),
                      PageTemplate("normal", [moldura], onPage=pagina)])

s = [NextPageTemplate("normal"), PageBreak()]
add = s.append
ext = s.extend

# =====================================================================
# PARTE 1
# =====================================================================
add(Paragraph("Parte 1 · Como funciona a Padaria Adonai", titulo_parte))
add(Paragraph("Uma explicação simples, passo a passo", subtitulo_parte))

add(Paragraph("Uma padaria dentro do computador", h2))
add(P("Imagina uma padaria de brincar que vive dentro do computador. Lá dentro não há pão a sério, "
      "mas o computador lembra-se de **todos os pães** que existem: como se chamam, quanto custam, "
      "quantos há na prateleira e até quando podem ser comidos. Também se lembra de **tudo o que foi vendido**."))
add(P("Este programa é o **ajudante** do dono da padaria. Em vez de escrever tudo num caderno, o dono "
      "carrega em botões e o computador faz as contas e arruma tudo."))

add(Paragraph("A porta, o porteiro e a loja", h2))
add(P("Quando abres o programa, passas por três sítios, sempre pela mesma ordem:"))
add(Ecras())
add(P("Os três ecrãs do programa. O botão Sair leva-te outra vez para a porta.", legenda))
add(P("**1. A porta.** Vês uma fotografia de pães com o nome _Padaria Adonai_. Carregas em **Acessar** para entrar."))
add(P("**2. O porteiro.** Pergunta quem és e qual é a tua **palavra secreta** (a senha). Se te enganares, ele "
      "diz _“Utilizador ou senha inválidos”_ e não te deixa passar. Repara que ele não diz _qual_ das duas "
      "está errada: assim, um espertalhão não consegue adivinhar os nomes dos utilizadores."))
add(P("**3. A loja.** À esquerda há uma coluna castanha cheia de botões, um para cada coisa que podes fazer. "
      "À direita há duas tabelas: uma com os **pães** (Registos) e outra com as **vendas**."))
add(caixa_programador(
    "Os três sítios são as classes `TelaInicial`, `TelaLogin` e `AplicacaoPadaria`. Nenhuma conhece as "
    "outras: quem as liga é o método `novaSessao()` da classe `Main` (no pacote `principal`), como um guia que te leva "
    "de sala em sala. Cada ecrã recebe um _callback_ (um `Runnable` ou a interface `TelaLogin.AoAutenticar`) "
    "para chamar quando acaba. Todos os ecrãs usam a mesma janela (`JFrame`): cada um troca o seu conteúdo."))

add(Paragraph("O dono e o ajudante", h2))
add(P("Na padaria trabalham duas pessoas: o **dono** e o **ajudante** (o funcionário). O dono tem **todas as "
      "chaves**: pode pôr pães novos, mudar preços e deitar pães fora. O ajudante pode procurar pães, ver as "
      "listas e vender, mas não pode mexer no que há na loja."))
add(P("E há um truque: os botões que o ajudante não pode usar **nem sequer aparecem** para ele. É como se essas "
      "portas não existissem. E se, por acaso, alguém encontrasse uma dessas portas, há um segundo guarda lá "
      "dentro que diz _“Esta operação está reservada ao Dono da Padaria”_."))
add(caixa_programador(
    "A lista das operações proibidas ao ajudante é `OPERACOES_RESTRITAS_AO_DONO` (em `SistemaPadaria`). "
    "Cada utilizador é um objecto `Utilizador`, e `eDono()` diz se é o dono. O “segundo guarda” é o "
    "método `exigeDono()` de `AplicacaoPadaria`."))

add(Paragraph("A fila de pães de mãos dadas", h2))
add(P("Esta é a parte mais importante. O computador guarda os pães numa **fila**, como meninos numa fila da "
      "escola. Cada pão dá **uma mão ao pão da frente** e **outra mão ao pão de trás**."))
add(Fila([("n.º 1", "Pão de forma"), ("n.º 2", "Bolo"), ("n.º 3", "Pastel"), ("n.º 4", "Pão careca")]))
add(P("Cada pão sabe quem está à frente e quem está atrás. As pontas não dão a mão a ninguém (null).", legenda))
add(P("O computador não precisa de se lembrar de onde está cada pão. Só precisa de saber três coisas:"))
add(P("• quem é o **primeiro** da fila;<br/>• quem é o **último** da fila;<br/>• **quantos** pães há."))
add(P("Para encontrar um pão, começa pelo primeiro e pergunta: _“És tu o número 3?”_ Se não for, segue a mão "
      "da frente para o próximo e pergunta outra vez, até o encontrar ou até a fila acabar. A isto chama-se "
      "**percorrer** a fila."))
add(caixa_programador(
    "A fila é uma **lista duplamente ligada**: a classe `ListaLigadas`, que segue a interface `IntefaceGeral`. "
    "Cada pão fica dentro de um **nó** (`No`) com `getProximo()` (mão da frente) e `getAnterior()` (mão de "
    "trás). A lista guarda `primeiro`, `ultimo` e `totalElem`. Quem “anda” pela fila é a variável `actual`: "
    "`actual = actual.getProximo();`. A fila dos pães é a `ListaProdutos`, que **herda** de `ListaLigadas` "
    "(`extends`) e faz tudo com os métodos dela (`adicionaFim`, `pega`, `removePosicao`...)."))

add(Paragraph("Chega um pão novo", h2))
add(P("Quando o dono carrega em **Cadastrar**, abre-se uma janela onde escreve os dados do pão novo. O pão novo "
      "vai para o **fim da fila**: o último pão dá-lhe a mão, e o pão novo passa a ser o último."))
add(P("Antes disso, o computador confirma que não há outro pão com o mesmo número, tal como numa equipa de "
      "futebol não pode haver dois jogadores com o mesmo número na camisola. Se houver, aparece um aviso, e "
      "a janela fica aberta para o dono corrigir sem ter de escrever tudo outra vez."))
add(caixa_programador(
    "`cadastrar(produto)` pergunta à lista `contem(produto)`. Isto funciona porque `Produto.equals` só "
    "compara o código: dois produtos com o mesmo número são “o mesmo”. Se não existir, chama `adicionaFim(produto)`."))

add(Paragraph("Um pão vai-se embora", h2))
add(P("Quando o dono deita um pão fora (**Eliminar**), esse pão sai da fila. Mas a fila não pode ficar partida! "
      "Por isso, o pão que estava atrás e o que estava à frente **dão as mãos um ao outro**."))
add(Remocao())
add(P("O Bolo sai, e o Pão de forma e o Pastel passam a dar as mãos.", legenda))
add(P("Se quem sai é o primeiro, o segundo passa a ser o primeiro. Se é o último, o penúltimo passa a ser o "
      "último. E aqui as duas mãos dão jeito: para saber quem é o novo último, basta seguir a **mão de trás** "
      "do último, sem ter de percorrer a fila toda."))
add(P("Também dá para dizer _“tira o 3.º da fila”_. Para nós a fila começa no 1, mas o computador conta a "
      "partir do 0, por isso o 3.º é a posição 2 para ele."))
add(caixa_programador(
    "`eliminarPorPosicao(posicao)` verifica `posicaoValida(posicao - 1)`, guarda o produto com "
    "`pega(posicao - 1)` (para dizer o nome a quem eliminou) e chama `removePosicao(posicao - 1)`. Esse "
    "método usa `removeInicio()` ou `removeFim()` nas pontas e, no meio, liga os dois vizinhos entre si."))

add(Paragraph("Procurar pães", h2))
add(P("Há várias maneiras de procurar:"))
add(P("• **Buscar Produto**: pelo número. _“Quero o pão número 3.”_<br/>"
      "• **Buscar (1 atributo)**: por uma característica. _“Mostra todos os que são Pão.”_<br/>"
      "• **Buscar (2 atributos)**: por duas ao mesmo tempo. _“Os que são Pão e custam 15.”_"))
add(P("O computador não liga a maiúsculas: “PÃO”, “pão” e “Pão” são a mesma coisa para ele. O que encontra "
      "vai para **uma fila nova** (outra `ListaLigadas`), que é a que aparece na tabela."))

add(Paragraph("Mudar um pão", h2))
add(P("Se o preço do bolo subir, o dono carrega em **Alterar**, diz o número do bolo, e abre-se a janela já "
      "preenchida. Ele muda só o que quer e carrega em **Guardar alterações**. É como trocar a etiqueta do "
      "preço. O número do pão (o da camisola) nunca muda, e por isso esse campo aparece bloqueado."))

add(Paragraph("Pôr os pães por ordem", h2))
add(P("Para ver os pães do mais barato para o mais caro, o computador usa um método chamado **bolha** "
      "(_bubble sort_). Olha para dois pães vizinhos; se o mais caro estiver à frente, trocam de lugar. Faz "
      "isto ao longo da fila, muitas vezes, até ninguém precisar de trocar. Os mais caros vão “subindo” para o "
      "fim, como bolhas de ar na água."))
add(Bolha())
add(Spacer(1, 6))
add(P("Um segredo: o computador ordena uma **cópia** da fila, só para mostrar. A fila verdadeira fica igual."))
add(caixa_programador(
    "`listarOrdenado(atributo, decrescente)` copia os produtos para um array `Produto[]` (com `pega(i)`), "
    "ordena o array com bubble sort e devolve uma `ListaLigadas` nova, preenchida com `adicionaFim`."))

add(Paragraph("Vender pão", h2))
add(P("Chega um cliente e pede 3 pães de forma. Carregas em **Registar Venda**, escreves o número do pão e a "
      "quantidade. Antes de vender, o computador confirma três coisas:"))
add(P("1. escreveste números a sério, e a quantidade é maior que zero?<br/>2. esse pão existe?<br/>"
      "3. há pães suficientes na prateleira?"))
add(P("Só se as três estiverem certas é que tira os pães da prateleira e escreve a venda no **caderno de "
      "vendas**. E o caderno de vendas... é outra fila de mãos dadas! Lá em baixo, o computador soma quantos "
      "pães se venderam e quanto dinheiro entrou."))
add(P("O caderno guarda o preço daquele dia. Se amanhã o pão ficar mais caro, a venda de hoje continua com o "
      "preço antigo, como num talão de compras."))
add(caixa_programador(
    "As vendas ficam na `ListaVendas`, que também herda de `ListaLigadas`; cada elemento é um objecto "
    "`Venda`. As três verificações estão em `registarVenda()` de `AplicacaoPadaria`, e o stock só é "
    "descontado depois de todas passarem."))

add(Paragraph("As cores da padaria", h2))
add(P("Todas as cores estão guardadas numa só caixa de lápis: castanho de crosta, dourado de pão acabado de "
      "sair do forno e creme de miolo. Se trocares um lápis dessa caixa, a padaria inteira muda de cor de uma vez."))
add(caixa_programador(
    "A caixa de lápis é a parte “Tema visual” de `SistemaPadaria`: as constantes `FUNDO`, `PAINEL`, "
    "`CROSTA`, `DOURADO`... (objectos `Color`), as fontes `FONTE_*` e o método `aplicarTema()`."))

add(Paragraph("Porque é que tudo desaparece quando fecho?", h2))
add(P("A padaria escreve tudo num **quadro de giz** (a memória do computador), e não num caderno (um ficheiro). "
      "Quando fechas o programa, o quadro é apagado. Na próxima vez, começa outra vez com os 4 pães de "
      "exemplo e 3 vendas de exemplo."))

add(CondPageBreak(90 * mm))
add(Paragraph("Onde está cada coisa", h2))
add(P("O ficheiro que liga o programa está sozinho no pacote `principal`. Todos os outros estão no pacote "
      "`listas_duplamente_ligadas`, como as salas de uma casa:"))
add(tabela(["Sala", "Ficheiro", "Para que serve"], [
    ["O interruptor e o guia", "principal/Main.java",
     "Liga o programa (`main`) e leva-te da porta ao porteiro e do porteiro à loja. É este que se corre."],
    ["O livro de regras", "SistemaPadaria.java",
     "Nome da padaria, moeda, utilizadores, senhas e quem pode fazer o quê."],
    ["A caixa de lápis", "SistemaPadaria.java", "Cores, letras e o aspecto dos botões e tabelas."],
    ["As mãos dadas", "IntefaceGeral.java, No.java, ListaLigadas.java",
     "A fila de mãos dadas em si. Serve para qualquer coisa: pães, vendas..."],
    ["O armazém", "ListaProdutos.java, ListaVendas.java", "A fila dos pães e a fila das vendas."],
    ["As etiquetas", "Produto.java, Venda.java, Utilizador.java",
     "O que se sabe de cada pão, de cada venda e de cada pessoa."],
    ["A loja", "TelaInicial.java, TelaLogin.java, AplicacaoPadaria.java", "Tudo o que se vê: porta, porteiro, loja e janelas."],
    ["A fotografia", "src/imagens/fundo_inicial.png", "A imagem de pães da porta."],
    ["O inspector", "test/.../TestesListas.java",
     "Verifica que as filas continuam de mãos dadas depois de cada mudança."],
], [20, 34, 46], mono_col0=False))

# =====================================================================
# PARTE 2
# =====================================================================
add(PageBreak())
add(Paragraph("Parte 2 · Referência técnica", titulo_parte))
add(Paragraph("Todas as classes, as suas variáveis e o que cada função faz e como", subtitulo_parte))

add(Paragraph("Visão geral", h2))
add(P("O programa arranca em `principal.Main`, a única classe do pacote `principal`. Todas as outras estão no "
      "pacote `listas_duplamente_ligadas`. `Main.main()` aplica o tema e abre três ecrãs por ordem: `TelaInicial` → `TelaLogin` → "
      "`AplicacaoPadaria`. Os produtos e as vendas ficam em `ListaProdutos` e `ListaVendas`, que **herdam** "
      "de `ListaLigadas`. A interface lê os dados das janelas, converte os valores, chama um método da lista e "
      "volta a desenhar as tabelas. Nada é gravado em disco: cada execução começa com os dados de exemplo.",
      pequeno))
add(P("A lista guarda `Object`: cada nó leva um `Produto` ou uma `Venda`, e quem o lê faz o _cast_, por "
      "exemplo `(Produto) pega(i)`. As listas da padaria **nunca mexem nas ligações** entre nós: fazem tudo "
      "através dos métodos de `ListaLigadas`. As estruturas também não conhecem a interface, e é isso que "
      "permite testá-las sozinhas.", pequeno))
add(Fila([("posição 0", "No"), ("posição 1", "No"), ("posição 2", "No")], "primeiro", "ultimo",
         "getProximo()", "getAnterior()", mono=True))
add(P("Cada nó aponta para o anterior e para o próximo. A lista guarda primeiro, ultimo e totalElem. "
      "As posições começam em 0.", legenda))

add(Paragraph("Invariantes da lista", h3))
add(P("Verdadeiras antes e depois de qualquer método público:", pequeno))
add(P("• lista vazia ↔ `primeiro == null` ↔ `ultimo == null` ↔ `totalElem == 0`<br/>"
      "• `primeiro.getAnterior() == null` e `ultimo.getProximo() == null`<br/>"
      "• para todo o nó n com próximo: `n.getProximo().getAnterior() == n`<br/>"
      "• as posições válidas vão de 0 a `totalElem - 1` (`posicaoValida`)", pequeno))

# ---------------- 1. BASE ----------------
add(CondPageBreak(120 * mm))
add(Paragraph("1. A lista duplamente ligada (a base)", h2))
add(P("Estas três classes são a base do projecto. Todas as outras estruturas usam-nas.", pequeno))

ext(classe("interface IntefaceGeral", "As operações que qualquer lista tem de oferecer. "
           "`ListaLigadas` implementa-a, e por isso também `ListaProdutos` e `ListaVendas`."))
ext(funcoes([
    ["adicionaInicio(elemento)", "Insere no início.", "Ver `ListaLigadas`."],
    ["adicionaPosicao(posicao, elemento)", "Insere numa posição.", "Ver `ListaLigadas`."],
    ["adicionaFim(elemento)", "Insere no fim.", "Ver `ListaLigadas`."],
    ["pega(posicao)", "Devolve o elemento de uma posição.", "Ver `ListaLigadas`."],
    ["removeInicio() / removePosicao(posicao) / removeFim()", "Removem um elemento.", "Ver `ListaLigadas`."],
    ["contem(elemento)", "Diz se o elemento está na lista.", "Compara com `equals`."],
    ["tamanho()", "Número de elementos.", "Devolve `totalElem`."],
    ["posicaoValida(posicao)", "Diz se a posição existe.", "0 ≤ posicao < tamanho()."],
    ["estaVazio()", "Diz se a lista está vazia.", "tamanho() == 0."],
]))

ext(classe("class No", "Um nó: um elemento e as ligações aos vizinhos."))
ext(variaveis([
    ["elemento", "Object", "O que o nó guarda (um `Produto`, uma `Venda`...)."],
    ["anterior", "No (ou null)", "Nó anterior; null no primeiro nó."],
    ["proximo", "No (ou null)", "Nó seguinte; null no último nó."],
]))
ext(funcoes([
    ["No(elemento)", "Cria um nó solto.", "anterior = proximo = null."],
    ["No(elemento, proximo)", "Cria um nó já ligado à frente.", "anterior = null."],
    ["No(anterior, elemento, proximo)", "Cria um nó ligado aos dois lados.", "Guarda os três valores."],
    ["getElemento()", "Lê o elemento.", "Não há `setElemento`: o elemento de um nó não muda."],
    ["getProximo() / setProximo(no)", "Lê / muda a mão da frente.", "—"],
    ["getAnterior() / setAnterior(no)", "Lê / muda a mão de trás.", "—"],
]))

ext(classe("class ListaLigadas implements IntefaceGeral", "A lista duplamente ligada."))
ext(variaveis([
    ["primeiro", "No (ou null)", "Primeiro nó (cabeça). null quando a lista está vazia."],
    ["ultimo", "No (ou null)", "Último nó (cauda). Permite inserir e remover no fim sem percorrer a lista."],
    ["totalElem", "int", "Número de nós. Actualizado em cada inserção e remoção."],
]))
ext(funcoes([
    ["ListaLigadas()", "Cria uma lista vazia.", "primeiro = ultimo = null, totalElem = 0."],
    ["adicionaInicio(elemento)", "Insere no início.",
     "Cria um `No` com proximo = primeiro. Se a lista estiver vazia passa a ser primeiro e ultimo; senão "
     "primeiro.setAnterior(novo) e primeiro = novo. O(1)."],
    ["adicionaPosicao(posicao, elemento)", "Insere numa posição (0 = início).",
     "IndexOutOfBoundsException fora de 0..totalElem. Posição 0 → adicionaInicio; posição totalElem → "
     "adicionaFim; senão liga o novo nó entre pegaNo(posicao - 1) e pegaNo(posicao). O(n)."],
    ["adicionaFim(elemento)", "Insere no fim.",
     "Lista vazia → adicionaInicio. Senão ultimo.setProximo(novo), novo.setAnterior(ultimo) e "
     "ultimo = novo. O(1)."],
    ["pega(posicao)", "Devolve o elemento da posição.",
     "IndexOutOfBoundsException se a posição não for válida. Anda `posicao` vezes a partir de primeiro "
     "com getProximo(). O(n)."],
    ["removeInicio()", "Remove o primeiro.",
     "IllegalStateException se vazia. Com 1 elemento: primeiro = ultimo = null. Senão primeiro passa "
     "para o seguinte, que fica com anterior = null. O(1)."],
    ["removePosicao(posicao)", "Remove o elemento da posição.",
     "IndexOutOfBoundsException se inválida. Posição 0 → removeInicio; última → removeFim; no meio, "
     "pegaNo(posicao) e liga o anterior e o próximo entre si. O(n)."],
    ["removeFim()", "Remove o último.",
     "NullPointerException se vazia. Com 1 elemento: lista fica vazia. Senão ultimo = ultimo.getAnterior() "
     "e ultimo.setProximo(null). O(1), graças à mão de trás."],
    ["contem(elemento)", "Procura um elemento.",
     "Percorre a partir de primeiro e compara com `equals`. O(n)."],
    ["tamanho()", "Número de elementos.", "Devolve totalElem. O(1)."],
    ["posicaoValida(posicao)", "Valida uma posição.", "true se 0 ≤ posicao < totalElem."],
    ["estaVazio()", "Lista vazia?", "true se totalElem == 0."],
    ["pegaNo(posicao) [privado]", "Devolve o nó (não o elemento).",
     "Como pega, mas devolve o `No`. Usado por adicionaPosicao e removePosicao."],
    ["concatenar(lista)", "Junta outra lista no fim desta.",
     "NullPointerException se a outra estiver vazia. Liga ultimo ↔ lista.primeiro e soma os tamanhos. "
     "As duas listas passam a partilhar os nós. O(1)."],
    ["RemoverTudo(obj)", "Remove todas as ocorrências de obj.",
     "NullPointerException se obj for null. Percorre a lista e remove cada nó igual, religando os vizinhos. O(n)."],
    ["contem(IntefaceGeral lista)", "Elementos de outra lista que também estão nesta.",
     "Para cada elemento da outra lista chama contem(elemento); devolve uma ListaLigadas nova. O(n·m)."],
    ["Ocorrencias(IntefaceGeral lista)", "Quantas vezes aparece cada elemento.",
     "Devolve um int[] com, para cada elemento da outra lista, o número de nós iguais nesta. O(n·m)."],
]))
add(caixa_programador(
    "Três correcções feitas nesta classe ao passar o projecto para Java: (1) `adicionaFim` criava o nó com "
    "`new No(elemento, this.ultimo)`, o que ligava o novo último ao antigo e fechava a fila num círculo "
    "(o `contem` nunca terminava). Passou a `new No(elemento)`. (2) `public void ListaLigada()` não era um "
    "construtor e passou a `public ListaLigadas()`. (3) `lista.ArrayList` não existe neste projecto e foi "
    "trocada por `IntefaceGeral` / `ListaLigadas`."))

# ---------------- 2. DADOS ----------------
add(CondPageBreak(120 * mm))
add(Paragraph("2. Os dados da padaria", h2))
add(P("São os objectos que vão dentro dos nós (o `elemento`).", pequeno))

ext(classe("class Produto", "Um produto. É o elemento de cada nó da `ListaProdutos`."))
ext(variaveis([
    ["codigo", "int", "Código único do produto. Não tem `set`: nunca muda."],
    ["nome", "String", "Nome do produto."],
    ["categoria", "String", "Categoria (ex.: Pão, Bolo, Doce)."],
    ["preco", "double", "Preço unitário (MT)."],
    ["quantidade", "int", "Unidades em stock."],
    ["validade", "String", "Data de validade (dd/mm/aaaa)."],
]))
ext(funcoes([
    ["Produto(codigo, nome, categoria, preco, quantidade, validade)", "Cria um produto.", "Guarda os seis valores."],
    ["getX() / setX(valor)", "Lêem e mudam cada atributo.", "Só existe `getCodigo()`, sem `setCodigo`."],
    ["equals(obj)", "Compara produtos.",
     "Iguais se tiverem o **mesmo código**. É isto que deixa `contem(produto)` detectar códigos repetidos."],
    ["hashCode()", "Coerente com equals.", "Calculado a partir do código."],
    ["toString()", "Texto do produto.", "“código - nome”."],
]))

ext(classe("enum Produto.Atributo", "Os seis atributos do produto, pela ordem em que aparecem na tabela, "
           "na janela de produto e nas buscas: `CODIGO`, `NOME`, `CATEGORIA`, `PRECO`, `QUANTIDADE`, `VALIDADE`."))
ext(variaveis([
    ["rotulo", "String", "Nome amigável (ex.: PRECO → “Preço”)."],
    ["dica", "String (ou null)", "Texto ao lado do campo (preço → MT, validade → dd/mm/aaaa)."],
]))
ext(funcoes([
    ["valorEm(produto)", "Valor deste atributo num produto.",
     "switch que chama o get certo. Devolve um `Comparable` (Integer, Double ou String), para as buscas "
     "e para a ordenação."],
    ["getRotulo() / getDica()", "Lêem o rótulo e a dica.", "—"],
    ["toString()", "Texto mostrado nas listas de escolha.", "Devolve o rótulo (“Preço” e não “PRECO”)."],
]))

ext(classe("class Venda", "Uma venda. É o elemento de cada nó da `ListaVendas`. Guarda uma cópia do nome e "
           "do preço do momento da venda, e não muda depois de criada."))
ext(variaveis([
    ["codigoProduto", "int", "Código do produto vendido."],
    ["nomeProduto", "String", "Nome do produto no momento da venda."],
    ["quantidade", "int", "Unidades vendidas."],
    ["precoUnitario", "double", "Preço por unidade no momento da venda."],
    ["total", "double", "quantidade × precoUnitario, calculado no construtor."],
    ["data", "String", "Data e hora da venda (dd/MM/yyyy HH:mm)."],
    ["FORMATO_DATA", "DateTimeFormatter", "Formato usado em data (constante)."],
]))
ext(funcoes([
    ["Venda(codigoProduto, nomeProduto, quantidade, precoUnitario)", "Cria uma venda.",
     "Calcula total e data (`LocalDateTime.now()`)."],
    ["getX()", "Lêem cada atributo.", "Não há `set`: uma venda não se altera."],
]))

ext(classe("class Utilizador", "Um utilizador do sistema. É o “perfil” que a `AplicacaoPadaria` recebe "
           "depois do login."))
ext(variaveis([
    ["senha", "String", "Senha (privada: só se compara, nunca se lê)."],
    ["tipo", "String", "PERFIL_DONO ou PERFIL_FUNCIONARIO."],
    ["nome", "String", "Nome mostrado na saudação."],
]))
ext(funcoes([
    ["senhaCorrecta(senha)", "Verifica a senha.", "equals entre a senha guardada e a escrita."],
    ["eDono()", "É o dono?", "Compara tipo com PERFIL_DONO."],
    ["getTipo() / getNome()", "Lêem o tipo e o nome.", "—"],
]))

# ---------------- 3. LISTAS DA PADARIA ----------------
add(CondPageBreak(120 * mm))
add(Paragraph("3. As listas da padaria", h2))
add(P("As duas herdam de `ListaLigadas` (`extends`) e só usam os métodos dela: não têm variáveis próprias.",
      pequeno))

ext(classe("class ListaProdutos extends ListaLigadas", "Todos os produtos. As posições que o utilizador vê "
           "começam em 1; as de `ListaLigadas` começam em 0. “Listar todos” é a própria lista."))
ext(funcoes([
    ["cadastrar(produto)", "Acrescenta um produto no fim.",
     "IllegalArgumentException se `contem(produto)` (código repetido); senão `adicionaFim(produto)`. O(n)."],
    ["buscarPorCodigo(codigo)", "Encontra um produto pelo código.",
     "`posicaoDoCodigo`; devolve `(Produto) pega(posicao)` ou null."],
    ["buscarPorUmAtributo(atributo, valor)", "Produtos em que um atributo é igual a um valor.",
     "Percorre com `pega(i)` e usa `coincide`. Os encontrados vão para uma `ListaLigadas` nova com `adicionaFim`."],
    ["buscarPorDoisAtributos(a1, v1, a2, v2)", "Produtos que cumprem dois atributos.",
     "Mesmo percurso; guarda o produto só se as duas comparações forem verdadeiras (E lógico)."],
    ["alterarPorCodigo(codigo, nome, categoria, preco, quantidade, validade)", "Edita um produto.",
     "buscarPorCodigo (IllegalArgumentException se não existir) e chama os `set`. Valores null ou \"\" "
     "são ignorados: o campo mantém o valor antigo."],
    ["eliminarPorPosicao(posicao)", "Remove o produto na posição (1 = primeiro).",
     "IndexOutOfBoundsException se `!posicaoValida(posicao - 1)`; guarda `pega(posicao - 1)`, chama "
     "`removePosicao(posicao - 1)` e devolve o produto removido."],
    ["eliminarPorCodigo(codigo)", "Remove o produto com esse código.",
     "IllegalStateException se `estaVazio()`; IllegalArgumentException se o código não existir; senão "
     "`pega` + `removePosicao`."],
    ["listarPorCriterio(atributo, valor)", "Produtos que cumprem um critério.", "Delega em buscarPorUmAtributo."],
    ["listarOrdenado(atributo, decrescente)", "Produtos ordenados por um atributo.",
     "Copia para um `Produto[]` com `pega(i)`, aplica bubble sort (compara com `compareTo` sobre "
     "`atributo.valorEm`) e devolve uma `ListaLigadas` nova. O(n²). A lista original não muda."],
    ["posicaoDoCodigo(codigo) [privado]", "Posição (a partir de 0) de um código.", "Percorre com `pega(i)`; -1 se não existir."],
    ["coincide(produto, atributo, valor) [privado]", "Compara um atributo com um texto.",
     "Os dois lados como texto, sem espaços e em minúsculas (“pão” encontra “Pão”)."],
]))

ext(classe("class ListaVendas extends ListaLigadas", "Todas as vendas, pela ordem em que aconteceram. "
           "Só se acrescenta: as vendas não se alteram nem se apagam."))
ext(funcoes([
    ["registarVenda(codigoProduto, nomeProduto, quantidade, precoUnitario)", "Regista uma venda no fim.",
     "Cria uma `Venda` e chama `adicionaFim`. Devolve a venda. Não valida stock (isso é feito na interface)."],
    ["totalVendas()", "Receita total.", "Percorre com `pega(i)` somando `getTotal()`."],
    ["totalQuantidade()", "Total de unidades vendidas.", "Percorre com `pega(i)` somando `getQuantidade()`."],
]))

# ---------------- 4. INTERFACE ----------------
add(CondPageBreak(120 * mm))
add(Paragraph("4. Arranque, configuração e interface", h2))
add(P("A interface usa **Swing**. Todos os ecrãs usam a mesma janela (`JFrame root`): cada ecrã troca o "
      "conteúdo dela e recebe um _callback_ para chamar quando termina, por isso os ecrãs não precisam de se "
      "conhecer. Os diálogos são `JDialog` modais.", pequeno))

ext(classe("class principal.Main", "Ponto de entrada: é a classe que se corre. Está sozinha no pacote "
           "`principal`, separada de todas as outras, e só usa classes públicas de `listas_duplamente_ligadas`."))
ext(funcoes([
    ["main(args)", "Início do programa.",
     "`SistemaPadaria.aplicarTema()` e depois novaSessao() na thread do Swing (invokeLater)."],
    ["novaSessao() [privado]", "Encadeia os três ecrãs.",
     "Cria a janela; define aoAutenticar (abre AplicacaoPadaria) e aoAcessar (abre TelaLogin); mostra "
     "TelaInicial. É também o callback do botão Sair, por isso sair recomeça numa janela nova."],
]))

ext(classe("class SistemaPadaria", "Configuração e tema visual, usados por todos os ecrãs."))
add(Paragraph("Configuração", h3))
ext(variaveis([
    ["NOME_PADARIA", "String", "“Padaria Adonai”. Usado nos títulos e ecrãs."],
    ["MOEDA", "String", "“MT”. Usado em todos os valores monetários."],
    ["PERFIL_DONO / PERFIL_FUNCIONARIO", "String", "Nomes dos perfis; compara-se sempre com estas constantes."],
    ["UTILIZADORES", "Map<String, Utilizador>", "utilizador → Utilizador. Dois: dono / dono123 (Dono da Padaria) e "
     "funcionario / func123 (Funcionário)."],
    ["OPERACOES_RESTRITAS_AO_DONO", "Set<String>", "Texto dos botões que só o dono vê: Cadastrar, Alterar (por "
     "código), Eliminar por posição, Eliminar por código."],
]))
add(Paragraph("Tema visual", h3))
ext(variaveis([
    ["FUNDO, PAINEL, CROSTA, CROSTA_ESCURA, DOURADO, DOURADO_CLARO, TEXTO, TEXTO_SUAVE, BRANCO, ERRO",
     "Color", "Paleta de toda a aplicação. As outras classes não têm cores escritas à mão."],
    ["FONTE_TITULO, FONTE_SUBTITULO, FONTE_SECCAO", "Font", "Georgia (títulos)."],
    ["FONTE_NORMAL, FONTE_NEGRITO, FONTE_PEQUENA", "Font", "SansSerif (texto)."],
]))
ext(funcoes([
    ["aplicarTema()", "Configura o aspecto geral.",
     "Activa o aspecto Metal (o do macOS/Windows ignora as cores dos botões) e define cores e fontes por "
     "omissão no UIManager. Chamar uma vez, antes de criar janelas."],
    ["botao / botaoSecundario / botaoSidebar(texto)", "Criam botões com o estilo da padaria.",
     "Dourado, castanho, ou castanho alinhado à esquerda. Todos usam botaoBase."],
    ["botaoBase(...) [privado]", "Botão com cor normal e cor com o rato por cima.",
     "Cores, cursor de mão e um MouseListener que troca as cores em mouseEntered/mouseExited."],
    ["rotulo(texto, fonte, cor)", "Cria um JLabel.", "—"],
    ["configurarTabela(tabela)", "Estilo das tabelas.",
     "Cabeçalho castanho, texto centrado, selecção dourada e linhas alternadas (um DefaultTableCellRenderer)."],
    ["centrarJanela(janela)", "Centra a janela no ecrã.", "Um pouco acima do meio (altura / 3)."],
    ["margem(componente, v, h)", "Margem interior vazia.", "EmptyBorder."],
]))

ext(classe("class TelaInicial", "Ecrã de abertura: imagem de fundo, nome da padaria e botão “Acessar”."))
ext(variaveis([
    ["CAMINHO_IMAGEM_FUNDO", "String", "“/imagens/fundo_inicial.png”, procurada no classpath."],
    ["LARGURA", "int", "Largura da janela: 640 px."],
    ["ALTURA_IMAGEM", "int", "Altura da zona da imagem: 320 px."],
    ["ALTURA_RODAPE", "int", "Altura do rodapé com o botão: 90 px."],
]))
ext(funcoes([
    ["TelaInicial(janela, aoAcessar)", "Constrói o ecrã.",
     "Um JPanel que desenha a imagem centrada e os textos (paintComponent); rodapé escuro com o botão. "
     "Enter também entra (setDefaultButton). O tamanho mínimo é o da imagem + rodapé."],
    ["carregarImagem() [privado]", "Lê a imagem.",
     "Primeiro do classpath (getResource); se não estiver lá, de `src/imagens`. Sem imagem fica só o fundo castanho."],
    ["textoComSombra(...) [privado]", "Texto legível sobre a imagem.",
     "Desenha o texto duas vezes: uma sombra escura deslocada 2 px e o texto claro por cima."],
]))

ext(classe("class TelaLogin", "Ecrã de login. Só passa quem estiver em `UTILIZADORES`."))
ext(variaveis([
    ["AoAutenticar", "interface", "Callback `autenticado(utilizador)`, chamado depois de um login certo."],
    ["LARGURA / ALTURA", "int", "Tamanho da janela: 420 × 460 px."],
    ["aoAutenticar", "AoAutenticar", "O callback recebido no construtor."],
    ["entradaUtilizador", "JTextField", "Campo do utilizador."],
    ["entradaSenha", "JPasswordField", "Campo da senha (mostra •)."],
    ["labelErro", "JLabel", "Mostra “Utilizador ou senha inválidos.”"],
]))
ext(funcoes([
    ["TelaLogin(janela, aoAutenticar)", "Constrói o formulário.",
     "Nome da padaria, dois campos, etiqueta de erro e botão “Entrar”. Enter no utilizador salta para a "
     "senha; Enter na senha tenta entrar."],
    ["tentarLogin() [privado]", "Verifica as credenciais.",
     "Procura o utilizador em UTILIZADORES e usa senhaCorrecta. Errado: mostra o erro e limpa a senha. "
     "Certo: chama aoAutenticar.autenticado(registo)."],
    ["campo(...) / adicionar(...) [privados]", "Estilo dos campos e arrumação no BoxLayout.", "—"],
]))

ext(classe("class AplicacaoPadaria", "Janela principal depois do login: barra de topo, sidebar com as operações "
           "e duas abas (Registos / Vendas). Os dados do produto são pedidos numa janela própria."))
ext(variaveis([
    ["LARGURA, ALTURA", "int", "Tamanho inicial: 1150 × 700 px (mínimo 950 × 600)."],
    ["lista", "ListaProdutos", "Todos os produtos."],
    ["listaVendas", "ListaVendas", "Todas as vendas."],
    ["root", "JFrame", "Janela principal."],
    ["perfil", "Utilizador", "O utilizador autenticado."],
    ["eDono", "boolean", "true se o perfil for o dono."],
    ["aoTerminarSessao", "Runnable", "Callback chamado ao sair (recomeça na tela inicial)."],
    ["abas", "JTabbedPane", "O controlo das abas."],
    ["tabRegistos / tabVendas", "JPanel", "As duas abas."],
    ["tabelaRegistos", "JTable", "Tabela de produtos (uma coluna por Atributo)."],
    ["modeloRegistos / modeloVendas", "DefaultTableModel", "Os dados das duas tabelas (só de leitura)."],
    ["labelTotalQtd / labelTotalVendas", "JLabel", "Total de unidades vendidas e receita total (MT)."],
    ["AoGravar", "interface", "Callback da janela de produto: `gravar(dados, janela)` devolve true para fechar."],
    ["Criterio", "classe interna", "Atributo + valor escolhidos numa janela de busca."],
]))
add(Paragraph("Construção do ecrã", h3))
ext(funcoes([
    ["AplicacaoPadaria(root, perfil, aoTerminarSessao)", "Inicia a janela principal.",
     "Guarda o perfil, calcula eDono, carrega os dados de exemplo, constrói o layout, define tamanho e centra."],
    ["construirLayout()", "Constrói a janela toda.", "BorderLayout: barra de topo (norte), sidebar (oeste) e abas (centro)."],
    ["construirBarraTopo()", "Barra de topo.", "Nome da padaria, saudação, perfil e botão “Sair”."],
    ["saudacao()", "Texto de boas-vindas.", "Bom dia / Boa tarde / Boa noite conforme a hora, com o nome do utilizador."],
    ["terminarSessao()", "Sair.", "Pede confirmação, fecha a janela (dispose) e chama aoTerminarSessao."],
    ["construirSidebar()", "Botões das operações.",
     "Um LinkedHashMap texto → método. Cria um botão para cada um e salta os que estão em "
     "OPERACOES_RESTRITAS_AO_DONO quando o utilizador não é o dono."],
    ["construirAbas()", "As duas abas.",
     "Registos: JTable com uma coluna por Atributo. Vendas: JTable de vendas, totais e botão “+ Registar Venda”."],
    ["popularExemplo()", "Dados de exemplo.", "Cadastra 4 produtos e regista 3 vendas."],
]))
add(Paragraph("Auxiliares", h3))
ext(funcoes([
    ["actualizarTabelaRegistos()", "Mostra todos os produtos.", "Chama a versão abaixo com `lista`."],
    ["actualizarTabelaRegistos(IntefaceGeral produtos)", "Mostra os produtos de qualquer lista.",
     "Limpa o modelo e acrescenta uma linha por produto com `tamanho()`/`pega(i)`. Serve para a lista "
     "principal e para os resultados das buscas."],
    ["actualizarTabelaVendas()", "Redesenha a tabela de vendas.", "Volta a preencher a partir de listaVendas e actualiza os dois totais."],
    ["exigeDono()", "Verificação de permissão.", "Se o utilizador não for o dono, mostra “Acesso restrito” e devolve true (quem chamou pára)."],
    ["novaJanela(titulo) / corpo(janela)", "Cria um diálogo.", "JDialog modal com um corpo em GridBagLayout e margens de 24 px."],
    ["mostrarJanela(janela)", "Mostra o diálogo.", "pack, centra sobre a janela principal e setVisible(true), que bloqueia até fechar."],
    ["grelha(corpo, componente, linha, coluna, largura)", "Coloca um componente no diálogo.", "GridBagConstraints com margens; rótulos à direita, botões centrados."],
    ["janelaProduto(titulo, textoBotao, aoConfirmar, produto)", "Janela com os dados do produto (Cadastrar e Alterar).",
     "Um campo por Atributo, com dicas. Com produto, vem preenchida e com o código bloqueado. Ao confirmar "
     "chama aoConfirmar.gravar(dados, janela); se devolver false a janela fica aberta."],
    ["comboAtributos()", "JComboBox de atributos.", "Mostra os rótulos (“Preço”), sem nenhum escolhido."],
    ["pedirAtributoValor(titulo)", "Diálogo: escolher atributo e escrever valor.", "Avisa se não houver atributo; devolve um Criterio ou null."],
    ["pedirValorSimples(titulo, textoRotulo)", "Diálogo: escrever um valor.", "Mesmo padrão com um só campo; devolve o texto ou null."],
    ["info / aviso / erro(...)", "Mensagens.", "JOptionPane com o ícone certo."],
    ["lerInteiro(texto) / lerDecimal(texto)", "Converte texto em número.", "Devolvem null se não for um número; lerDecimal aceita “12,5” e “12.5”."],
]))
add(Paragraph("Acções (botões da sidebar)", h3))
ext(funcoes([
    ["acaoBuscarProduto()", "Busca por código.", "Diálogo pede o código; buscarPorCodigo; mostra só esse produto e selecciona a linha."],
    ["acaoCadastrar() [dono]", "Novo produto.",
     "janelaProduto vazia. Converte código/quantidade com lerInteiro e preço com lerDecimal, chama "
     "lista.cadastrar e actualiza a tabela. Números inválidos ou código repetido mostram erro e mantêm a janela aberta."],
    ["acaoAlterar() [dono]", "Editar produto.", "Pede o código, abre janelaProduto preenchida; campos vazios mantêm o valor; chama alterarPorCodigo."],
    ["acaoBuscarUmAtributo()", "Busca por 1 atributo.", "pedirAtributoValor + buscarPorUmAtributo; mostra os resultados ou “Nenhum produto encontrado”."],
    ["acaoBuscarDoisAtributos()", "Busca por 2 atributos.", "Diálogo com dois pares atributo/valor; buscarPorDoisAtributos."],
    ["acaoEliminarPosicao() [dono]", "Eliminar por posição.", "pedirValorSimples; eliminarPorPosicao; mostra o nome do produto removido."],
    ["acaoEliminarCodigo() [dono]", "Eliminar por código.", "pedirValorSimples; eliminarPorCodigo."],
    ["acaoListarTodos()", "Mostrar todos.", "Actualiza a tabela e selecciona a aba Registos."],
    ["acaoListarCriterio()", "Listar por critério.", "pedirAtributoValor + listarPorCriterio."],
    ["acaoListarOrdenado()", "Listar ordenado.", "Diálogo com JComboBox de atributo e caixa “Ordem decrescente”; listarOrdenado."],
    ["registarVenda()", "Registar venda (sidebar e aba Vendas).",
     "Pede código e quantidade. Verifica: inteiros positivos, produto existe, stock suficiente. Só depois "
     "desconta o stock, chama listaVendas.registarVenda, actualiza as duas tabelas e mostra o total."],
]))

# ---------------- 5. TESTES E LIMITES ----------------
add(CondPageBreak(120 * mm))
add(Paragraph("5. Testes", h2))
add(P("`test/listas_duplamente_ligadas/TestesListas.java` tem 13 testes (cadastro, código repetido, buscas, "
      "alteração, eliminação nas pontas e no meio, esvaziar e voltar a encher, ordenação e totais de vendas). "
      "Não usa bibliotecas: corre como um programa normal e termina com o código 1 se algum teste falhar.",
      pequeno))

add(CondPageBreak(120 * mm))
add(Paragraph("6. Limites conhecidos", h2))
add(P("• Ordenar por validade compara texto, por isso “01/12/2026” fica antes de “15/09/2026”. Solução: "
      "guardar a validade como `LocalDate`.<br/>"
      "• Os dados perdem-se ao sair ou fechar. Solução: gravar num ficheiro e carregar no construtor de "
      "`AplicacaoPadaria`.<br/>"
      "• Percorrer a lista com `pega(i)` recomeça sempre do primeiro nó, por isso um percurso completo custa "
      "O(n²) em vez de O(n). Para uma padaria chega; para muitos produtos, a lista precisaria de um iterador.<br/>"
      "• Buscas por código são O(n). Solução para muitos produtos: um `HashMap<Integer, Produto>` ao lado da lista.<br/>"
      "• Senhas em texto simples no código: aceitável só num trabalho académico.", pequeno))

doc.build(s)
