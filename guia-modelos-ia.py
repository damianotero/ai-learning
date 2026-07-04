"""
Guía de Modelos de IA — generador de PDF
"""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT

# ─── Paleta de colores ─────────────────────────────────────────────────────────
C_HAIKU   = colors.HexColor('#2563EB')   # Azul
C_SONNET  = colors.HexColor('#16A34A')   # Verde
C_OPUS    = colors.HexColor('#7C3AED')   # Violeta
C_GEMINI  = colors.HexColor('#D97706')   # Ámbar

C_HAIKU_BG   = colors.HexColor('#EFF6FF')
C_SONNET_BG  = colors.HexColor('#F0FDF4')
C_OPUS_BG    = colors.HexColor('#F5F3FF')
C_GEMINI_BG  = colors.HexColor('#FFFBEB')

C_DARK   = colors.HexColor('#1E293B')
C_MUTED  = colors.HexColor('#64748B')
C_BORDER = colors.HexColor('#E2E8F0')
C_BG     = colors.HexColor('#F8FAFC')
C_RULE   = colors.HexColor('#FFF7ED')
C_RULE_B = colors.HexColor('#F59E0B')

W = A4[0] - 4*cm  # ancho útil

# ─── Estilos ───────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def S(name, **kwargs):
    return ParagraphStyle(name, parent=base['Normal'], **kwargs)

TITLE    = S('Title2', fontSize=26, textColor=C_DARK, fontName='Helvetica-Bold', spaceAfter=4, leading=30)
SUBTITLE = S('Subtitle2', fontSize=12, textColor=C_MUTED, fontName='Helvetica', spaceAfter=4)
H1       = S('H1', fontSize=18, textColor=C_DARK, fontName='Helvetica-Bold', spaceBefore=18, spaceAfter=8)
H2       = S('H2', fontSize=13, textColor=C_DARK, fontName='Helvetica-Bold', spaceBefore=12, spaceAfter=5)
H3       = S('H3', fontSize=10, textColor=C_MUTED, fontName='Helvetica-Bold', spaceAfter=3)
BODY     = S('Body2', fontSize=10, textColor=C_DARK, fontName='Helvetica', leading=16, spaceAfter=5, alignment=TA_JUSTIFY)
BULLET   = S('Bullet2', fontSize=10, textColor=C_DARK, fontName='Helvetica', leading=15, leftIndent=12, spaceAfter=3)
EXAMPLE  = S('Example2', fontSize=9, textColor=colors.HexColor('#374151'), fontName='Helvetica-Oblique', leading=14, leftIndent=10, spaceAfter=3)
LABEL    = S('Label2', fontSize=8, textColor=C_MUTED, fontName='Helvetica-Bold', spaceAfter=2, alignment=TA_CENTER)
CELL     = S('Cell', fontSize=9, textColor=C_DARK, fontName='Helvetica', leading=13)
CELL_H   = S('CellH', fontSize=9, textColor=colors.white, fontName='Helvetica-Bold', alignment=TA_CENTER)
CELL_C   = S('CellC', fontSize=9, textColor=C_DARK, fontName='Helvetica', alignment=TA_CENTER)
NOTE     = S('Note', fontSize=9, textColor=colors.HexColor('#78350F'), fontName='Helvetica', leading=14, alignment=TA_JUSTIFY)
PAGE_NUM = S('PageNum', fontSize=8, textColor=C_MUTED, fontName='Helvetica', alignment=TA_RIGHT)
INTRO    = S('Intro', fontSize=11, textColor=C_DARK, fontName='Helvetica', leading=18, spaceAfter=6, alignment=TA_JUSTIFY)

# ─── Helpers ───────────────────────────────────────────────────────────────────
def hr(color=C_BORDER, thick=1):
    return HRFlowable(width='100%', thickness=thick, color=color, spaceAfter=8, spaceBefore=4)

def spacer(h=0.3):
    return Spacer(1, h*cm)

def model_banner(name, tagline, cost, color):
    """Banner coloreado para cada modelo."""
    name_s  = S(f'BN_{name}', fontSize=20, textColor=colors.white, fontName='Helvetica-Bold')
    tag_s   = S(f'BT_{name}', fontSize=10, textColor=colors.HexColor('#E2E8F0'), fontName='Helvetica')
    cost_s  = S(f'BC_{name}', fontSize=9,  textColor=colors.white, fontName='Helvetica-Bold', alignment=TA_RIGHT)
    data = [[Paragraph(name, name_s), Paragraph(tagline, tag_s), Paragraph(cost, cost_s)]]
    t = Table(data, colWidths=[3.5*cm, 9*cm, 3.8*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), color),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING',  (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
    ]))
    return t

def two_col_box(left_title, left_items, right_title, right_items, l_color, r_color, l_bg, r_bg):
    """Dos columnas: usa / no uses."""
    def make_cell(title, items, color, bg):
        lines = [Paragraph(title, S(f'CT_{title}', fontSize=9, textColor=color,
                                     fontName='Helvetica-Bold', spaceAfter=5))]
        for item in items:
            lines.append(Paragraph(f'• {item}',
                S(f'CI_{item[:10]}', fontSize=9, textColor=C_DARK, fontName='Helvetica',
                  leading=14, leftIndent=6, spaceAfter=3)))
        return lines, bg

    left_content,  l_bg2 = make_cell(left_title,  left_items,  l_color, l_bg)
    right_content, r_bg2 = make_cell(right_title, right_items, r_color, r_bg)

    data = [[left_content, right_content]]
    t = Table(data, colWidths=[W/2 - 0.2*cm, W/2 - 0.2*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (0,-1), l_bg2),
        ('BACKGROUND',    (1,0), (1,-1), r_bg2),
        ('BOX',           (0,0), (0,-1), 0.5, l_color),
        ('BOX',           (1,0), (1,-1), 0.5, r_color),
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING',    (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('RIGHTPADDING',  (0,0), (-1,-1), 10),
        ('COLPADDING',    (0,0), (-1,-1), 6),
    ]))
    return t

def example_box(title, text, color, bg):
    """Caja de ejemplo real."""
    t_style = S(f'ET_{title[:8]}', fontSize=9, textColor=color, fontName='Helvetica-Bold', spaceAfter=3)
    b_style = S(f'EB_{title[:8]}', fontSize=9, textColor=C_DARK, fontName='Helvetica-Oblique', leading=14)
    data = [[Paragraph(title, t_style), Paragraph(text, b_style)]]
    t = Table(data, colWidths=[3*cm, W - 3*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('BOX',        (0,0), (-1,-1), 0.5, color),
        ('VALIGN',     (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING',  (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    return t

def rule_box(text):
    data = [[Paragraph(text, NOTE)]]
    t = Table(data, colWidths=[W])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), C_RULE),
        ('BOX',           (0,0), (-1,-1), 1.5, C_RULE_B),
        ('TOPPADDING',    (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING',   (0,0), (-1,-1), 12),
        ('RIGHTPADDING',  (0,0), (-1,-1), 12),
    ]))
    return t

def info_box(text, color, bg):
    data = [[Paragraph(text, S('IB', fontSize=10, textColor=C_DARK, fontName='Helvetica', leading=15, alignment=TA_JUSTIFY))]]
    t = Table(data, colWidths=[W])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), bg),
        ('LEFTBORDERPADDING', (0,0), (0,-1), 4),
        ('LINEBEFORE',    (0,0), (0,-1), 4, color),
        ('TOPPADDING',    (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING',   (0,0), (-1,-1), 14),
        ('RIGHTPADDING',  (0,0), (-1,-1), 12),
    ]))
    return t

# ─── Construcción del documento ────────────────────────────────────────────────
story = []

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 1 — PORTADA + REFERENCIA RÁPIDA
# ══════════════════════════════════════════════════════════════════════════════

story.append(spacer(0.5))
story.append(Paragraph('Guía de Modelos de IA', TITLE))
story.append(Paragraph('Cuándo usar Haiku · Sonnet · Opus · Gemini CLI mientras trabajas', SUBTITLE))
story.append(hr(C_DARK, 2))
story.append(spacer(0.2))

# Intro rápida
story.append(Paragraph(
    'Esta guía está diseñada para consultarla mientras trabajas. '
    'La primera sección es una referencia visual inmediata. '
    'La segunda sección explica cada modelo en profundidad con ejemplos reales.',
    INTRO
))
story.append(spacer(0.3))

# ─── Tabla de referencia rápida ────────────────────────────────────────────────
story.append(Paragraph('REFERENCIA RÁPIDA', H3))

qr_rows = [
    # Header
    [
        Paragraph('TIPO DE TAREA', CELL_H),
        Paragraph('HAIKU', CELL_H),
        Paragraph('SONNET', CELL_H),
        Paragraph('OPUS', CELL_H),
        Paragraph('GEMINI CLI', CELL_H),
    ],
    [Paragraph('Reemplazar texto, colores o números', CELL), Paragraph('✓ IDEAL', CELL_C), Paragraph('—', CELL_C), Paragraph('—', CELL_C), Paragraph('✓ IDEAL', CELL_C)],
    [Paragraph('Copiar estilos o código entre archivos', CELL), Paragraph('✓', CELL_C), Paragraph('—', CELL_C), Paragraph('—', CELL_C), Paragraph('✓', CELL_C)],
    [Paragraph('Actualizar documentación con datos dados', CELL), Paragraph('✓', CELL_C), Paragraph('—', CELL_C), Paragraph('—', CELL_C), Paragraph('✓', CELL_C)],
    [Paragraph('Resumir qué hay pendiente (tareas.md)', CELL), Paragraph('✓', CELL_C), Paragraph('—', CELL_C), Paragraph('—', CELL_C), Paragraph('—', CELL_C)],
    [Paragraph('Crear pantalla nueva (patrón bien definido)', CELL), Paragraph('—', CELL_C), Paragraph('—', CELL_C), Paragraph('—', CELL_C), Paragraph('✓ IDEAL', CELL_C)],
    [Paragraph('Implementación pura > 20 min', CELL), Paragraph('—', CELL_C), Paragraph('—', CELL_C), Paragraph('—', CELL_C), Paragraph('✓ IDEAL', CELL_C)],
    [Paragraph('Debugging de error no obvio', CELL), Paragraph('—', CELL_C), Paragraph('✓ IDEAL', CELL_C), Paragraph('—', CELL_C), Paragraph('—', CELL_C)],
    [Paragraph('Cambios con dependencias entre archivos', CELL), Paragraph('—', CELL_C), Paragraph('✓ IDEAL', CELL_C), Paragraph('—', CELL_C), Paragraph('—', CELL_C)],
    [Paragraph('Revisar código antes de commitear', CELL), Paragraph('—', CELL_C), Paragraph('✓ IDEAL', CELL_C), Paragraph('—', CELL_C), Paragraph('—', CELL_C)],
    [Paragraph('Análisis de estrategia o inversiones', CELL), Paragraph('—', CELL_C), Paragraph('✓', CELL_C), Paragraph('✓ IDEAL', CELL_C), Paragraph('—', CELL_C)],
    [Paragraph('Diseño de arquitectura de proyecto', CELL), Paragraph('—', CELL_C), Paragraph('—', CELL_C), Paragraph('✓ IDEAL', CELL_C), Paragraph('—', CELL_C)],
    [Paragraph('Plan completo de proyecto nuevo', CELL), Paragraph('—', CELL_C), Paragraph('—', CELL_C), Paragraph('✓ IDEAL', CELL_C), Paragraph('—', CELL_C)],
    [Paragraph('Decisión que afecta todo el proyecto', CELL), Paragraph('—', CELL_C), Paragraph('—', CELL_C), Paragraph('✓ IDEAL', CELL_C), Paragraph('—', CELL_C)],
]

col_w = [6.8*cm, 2.1*cm, 2.1*cm, 2.1*cm, 2.5*cm]
qr_table = Table(qr_rows, colWidths=col_w, repeatRows=1)

row_styles = []
for i in range(1, len(qr_rows)):
    bg = C_BG if i % 2 == 0 else colors.white
    row_styles.append(('BACKGROUND', (0, i), (-1, i), bg))

qr_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (0,0), C_DARK),
    ('BACKGROUND', (1,0), (1,0), C_HAIKU),
    ('BACKGROUND', (2,0), (2,0), C_SONNET),
    ('BACKGROUND', (3,0), (3,0), C_OPUS),
    ('BACKGROUND', (4,0), (4,0), C_GEMINI),
    ('GRID',       (0,0), (-1,-1), 0.4, C_BORDER),
    ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING',   (0,0), (-1,-1), 7),
    ('RIGHTPADDING',  (0,0), (-1,-1), 7),
] + row_styles))

story.append(qr_table)
story.append(spacer(0.4))

story.append(rule_box(
    '<b>Regla de oro:</b> Si la tarea es <i>"encuentra X y cambia/copia/pega Y"</i> → Haiku o Gemini CLI. '
    'Si hay razonamiento, debugging o decisiones → Sonnet. '
    'Si está en juego la arquitectura o la estrategia del proyecto → Opus.'
))

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 2+ — GUÍA DETALLADA
# ══════════════════════════════════════════════════════════════════════════════

story.append(Paragraph('Guía Detallada por Modelo', H1))
story.append(hr())
story.append(Paragraph(
    'Cada modelo tiene una función específica en el flujo de trabajo. '
    'Usarlos bien no solo reduce el gasto de tokens — también mejora la calidad de los resultados, '
    'porque cada modelo está optimizado para un tipo de tarea.',
    BODY
))
story.append(spacer(0.2))

# ══════════════════════════════════════════════════════════════════════════════
# HAIKU
# ══════════════════════════════════════════════════════════════════════════════

story.append(KeepTogether([
    model_banner('Haiku 4.5', 'Rápido · Barato · Tareas mecánicas', 'API: ~5x más barato que Sonnet', C_HAIKU),
    spacer(0.3),
]))

story.append(Paragraph('¿Qué es Haiku?', H2))
story.append(Paragraph(
    'Haiku es el modelo más pequeño y rápido de Anthropic. No es menos inteligente en sentido estricto '
    '— simplemente está optimizado para velocidad y costo en tareas donde no se necesita razonamiento complejo. '
    'Piénsalo como un asistente muy eficiente para trabajo de ejecución directa.',
    BODY
))

story.append(Paragraph('Cuándo usarlo / cuándo no', H2))
story.append(two_col_box(
    'USA HAIKU CUANDO...',
    [
        'Reemplazar texto, colores o números en archivos',
        'Copiar estilos o bloques de código entre archivos',
        'Actualizar un .md con datos que tú le das',
        'Leer tareas.md y decirte qué hay pendiente',
        'Formatear o reorganizar contenido existente',
        'Generar texto repetitivo con un patrón claro',
        'Ajustar valores concretos (opacidades, tamaños, fechas)',
    ],
    'NO USES HAIKU CUANDO...',
    [
        'Hay un error y no sabes por qué ocurre',
        'El cambio afecta múltiples archivos con dependencias',
        'Necesitas que entienda el contexto completo del proyecto',
        'La tarea requiere decidir entre opciones',
        'Estás diseñando arquitectura o flujo de datos',
        'El resultado incorrecto puede romper funcionalidad',
    ],
    C_HAIKU, colors.HexColor('#DC2626'),
    C_HAIKU_BG, colors.HexColor('#FEF2F2')
))
story.append(spacer(0.3))

story.append(Paragraph('Cómo activar Haiku en Claude Code', H2))
story.append(info_box(
    'En Claude Code escribe el comando <b>/model</b> y selecciona <b>claude-haiku-4-5</b>. '
    'Cuando termines la tarea, vuelve a Sonnet con <b>/model claude-sonnet-4-6</b>. '
    'Alternativamente, usa Gemini CLI para estas tareas — el principio es el mismo y ya tienes el flujo integrado.',
    C_HAIKU, C_HAIKU_BG
))
story.append(spacer(0.3))

story.append(Paragraph('Ejemplos reales de tus proyectos', H2))

story.append(example_box(
    'Fronterra — S016',
    'Cambiar el texto del Hero de "Biobío, Chile · Arquitectos" a "Biobio - Arauco - Arquitectos" '
    'en app1.js y app.transpiled.js. Reemplazo de string en 2 archivos. Sin razonamiento, sin riesgo. '
    'Esta sesión la hizo Gemini CLI — correctamente.',
    C_HAIKU, C_HAIKU_BG
))
story.append(spacer(0.2))
story.append(example_box(
    'Fronterra — S022',
    'Copiar el CSS completo de privacidad.html y aplicarlo a cookies.html y terminos.html. '
    'La lógica es: "lee este archivo, copia esta sección, pégala en estos dos". Mecánico y sin decisión.',
    C_HAIKU, C_HAIKU_BG
))
story.append(spacer(0.2))
story.append(example_box(
    'Fronterra — S020',
    'Ajustar opacidad del mapa topográfico de 0.22 → 0.20 → 0.19 → 0.18. '
    'Cambiar un número en un archivo CSS en cada iteración. Se hicieron 4 rondas con Sonnet — '
    'Haiku o Gemini hubieran costado casi nada.',
    C_HAIKU, C_HAIKU_BG
))
story.append(spacer(0.2))
story.append(example_box(
    'Finances — S013',
    'Una vez investigados los precios de BTC, ETH y NVIDIA, actualizar portfolio.md '
    'y generar el reporte en docs/reportes/. El trabajo de escritura/formateo es Haiku. '
    'La investigación y el análisis son Sonnet.',
    C_HAIKU, C_HAIKU_BG
))

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# SONNET
# ══════════════════════════════════════════════════════════════════════════════

story.append(KeepTogether([
    model_banner('Sonnet 4.6', 'Equilibrado · Tu modelo por defecto · 80% de los casos', 'El modelo que usas normalmente', C_SONNET),
    spacer(0.3),
]))

story.append(Paragraph('¿Qué es Sonnet?', H2))
story.append(Paragraph(
    'Sonnet es el modelo principal de Claude Code — el que tienes activo por defecto. '
    'Combina capacidad de razonamiento sólida con velocidad aceptable. '
    'Cubre la gran mayoría de las tareas de desarrollo: debugging, cambios con dependencias, '
    'revisión de código y análisis moderadamente complejos. '
    'Si no sabes qué modelo usar, Sonnet es la respuesta correcta en el 80% de los casos.',
    BODY
))

story.append(Paragraph('Cuándo usarlo / cuándo no', H2))
story.append(two_col_box(
    'USA SONNET CUANDO...',
    [
        'Hay un error y necesitas entender por qué ocurre',
        'El cambio afecta múltiples archivos con dependencias',
        'Quieres revisar código de Gemini antes de commitear',
        'Necesitas implementar una feature moderadamente compleja',
        'Estás haciendo análisis: inversiones, opciones, comparativas',
        'La tarea dura entre 5 y 30 minutos de trabajo',
        'Necesitas que el modelo entienda el contexto del proyecto',
    ],
    'NO USES SONNET CUANDO...',
    [
        'La tarea es un simple reemplazo de texto o número',
        'Es una implementación pura muy larga sin decisiones (→ Gemini)',
        'Necesitas el máximo razonamiento para decisiones críticas (→ Opus)',
        'Solo quieres leer un archivo y saber qué hay pendiente (→ Haiku)',
    ],
    C_SONNET, colors.HexColor('#DC2626'),
    C_SONNET_BG, colors.HexColor('#FEF2F2')
))
story.append(spacer(0.3))

story.append(Paragraph('Ejemplos reales de tus proyectos', H2))

story.append(example_box(
    'Fronterra — S021',
    'Implementar el sistema CMP completo de cookies: banner, modal, localStorage, '
    'bloqueo de scripts de terceros, tres categorías, tres botones, consentimiento revocable. '
    'Múltiples archivos, lógica de estado, integración con el footer. Sonnet claramente.',
    C_SONNET, C_SONNET_BG
))
story.append(spacer(0.2))
story.append(example_box(
    'Fronterra — S018',
    'Debugging del auto-deploy GitHub Actions → Cloudflare Pages. El primer run falló, '
    'luego el token era incorrecto, luego faltaban permisos. Razonamiento encadenado sobre errores '
    'no obvios en múltiples servicios. Sonnet ideal.',
    C_SONNET, C_SONNET_BG
))
story.append(spacer(0.2))
story.append(example_box(
    'AI Agency — S003',
    'Validar el blueprint de Make.com (portfolio-report-v1.json), revisar que los módulos '
    'estén bien conectados y confirmar que el schedule estaba configurado correctamente. '
    'Revisión con criterio técnico antes de dar el OK. Sonnet.',
    C_SONNET, C_SONNET_BG
))
story.append(spacer(0.2))
story.append(example_box(
    'Finances — S011',
    'Análisis de niveles técnicos de BTC y ETH para dip buying, evaluación de XRP '
    '(mantener vs vender), análisis de NVIDIA con niveles de toma de ganancias. '
    'Análisis moderadamente complejo. Sonnet es el punto de partida; para decisiones '
    'de mayor convicción, considera Opus.',
    C_SONNET, C_SONNET_BG
))

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# OPUS
# ══════════════════════════════════════════════════════════════════════════════

story.append(KeepTogether([
    model_banner('Opus 4.6', 'Máximo razonamiento · Decisiones críticas · Uso selectivo', 'API: ~5x más caro que Sonnet', C_OPUS),
    spacer(0.3),
]))

story.append(Paragraph('¿Qué es Opus?', H2))
story.append(Paragraph(
    'Opus es el modelo más potente de Anthropic. Tiene mayor capacidad de razonamiento profundo, '
    'mejor manejo de contextos largos y complejos, y mejores resultados en tareas que requieren '
    'juicio sofisticado. El costo es proporcionalmente mayor. '
    'Úsalo cuando la decisión que tomes importa mucho y quieres el mejor criterio disponible.',
    BODY
))

story.append(Paragraph('Cuándo usarlo / cuándo no', H2))
story.append(two_col_box(
    'USA OPUS CUANDO...',
    [
        'Diseñas la arquitectura completa de un proyecto nuevo',
        'La decisión técnica afecta todo el desarrollo futuro',
        'Analizas una oportunidad de inversión importante',
        'Necesitas evaluar tradeoffs complejos con muchas variables',
        'Estás planificando un roadmap desde cero',
        'Quieres el mejor criterio posible antes de una decisión irreversible',
        'El contexto del problema es muy largo y requiere mantenerlo todo en mente',
    ],
    'NO USES OPUS CUANDO...',
    [
        'La tarea la puede hacer Sonnet bien (el 80% de los casos)',
        'Es implementación de código (Sonnet es suficiente)',
        'Es un análisis rutinario que haces regularmente',
        'Solo necesitas corregir un error concreto',
        'El resultado es verificable y repetible sin gran riesgo',
    ],
    C_OPUS, colors.HexColor('#DC2626'),
    C_OPUS_BG, colors.HexColor('#FEF2F2')
))
story.append(spacer(0.3))

story.append(Paragraph('Cómo activar Opus en Claude Code', H2))
story.append(info_box(
    'Escribe <b>/model claude-opus-4-6</b> en Claude Code. '
    'También puedes activar el modo <b>/plan</b> — en ese modo Claude usa automáticamente '
    'Opus para planificar y Sonnet para ejecutar, que es la combinación óptima para proyectos grandes.',
    C_OPUS, C_OPUS_BG
))
story.append(spacer(0.3))

story.append(Paragraph('Ejemplos reales de tus proyectos', H2))

story.append(example_box(
    'ChuteBay — Arquitectura',
    'Definir el stack completo del marketplace (Next.js + Supabase + Stripe Connect), '
    'el modelo de datos, las fases del roadmap y las reglas de producto. '
    'Una sesión de arquitectura con Opus al inicio del proyecto vale mucho más '
    'que corregir decisiones equivocadas después.',
    C_OPUS, C_OPUS_BG
))
story.append(spacer(0.2))
story.append(example_box(
    'Finances — Estrategia',
    'Análisis comparativo de mercados inmobiliarios (Dubai, Medellin, Riviera Maya), '
    'evaluación honesta de todos los proyectos activos como fuentes de ingreso, '
    'y definición de la estrategia de ingresos. Decisiones de largo plazo con muchas variables. '
    'Aquí Opus aporta el razonamiento más profundo.',
    C_OPUS, C_OPUS_BG
))
story.append(spacer(0.2))
story.append(example_box(
    'AI Engineer — Roadmap',
    'Diseñar el plan de formación como AI Engineer: qué aprender, en qué orden, '
    'cómo aplicarlo a proyectos reales, qué habilidades priorizar para el mercado. '
    'Un plan estratégico de largo plazo que guiará meses de trabajo merece Opus.',
    C_OPUS, C_OPUS_BG
))

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# GEMINI CLI
# ══════════════════════════════════════════════════════════════════════════════

story.append(KeepTogether([
    model_banner('Gemini CLI', 'Implementación pura · Complemento de Claude · Contexto largo', 'Gratuito con suscripción Gemini', C_GEMINI),
    spacer(0.3),
]))

story.append(Paragraph('¿Qué es Gemini CLI y cómo encaja?', H2))
story.append(Paragraph(
    'Gemini CLI es el complemento de Claude en tu flujo de trabajo. '
    'No es un sustituto — cada uno tiene un rol claro. '
    'Claude diseña, decide, revisa y da el OK. Gemini ejecuta: implementa pantallas, '
    'escribe código según patrones bien definidos, completa tareas de implementación pura '
    'que pueden tardar mucho y consumirían muchos tokens de Claude. '
    'Gemini tiene ventana de contexto muy larga, lo que lo hace ideal para tareas '
    'que requieren leer muchos archivos de referencia.',
    BODY
))

story.append(Paragraph('Cuándo usarlo / cuándo no', H2))
story.append(two_col_box(
    'USA GEMINI CLI CUANDO...',
    [
        'Crear una pantalla nueva con un patrón bien definido',
        'Implementar una feature pura que tardaría > 20 min',
        'Escribir SQL para una tabla nueva siguiendo un esquema',
        'Añadir un método a un servicio siguiendo un patrón claro',
        'Fixes de UI: colores, layout, textos, estilos',
        'Actualizar documentación con datos que tú le das',
        'Hacer cambios repetitivos en múltiples archivos similares',
    ],
    'NO USES GEMINI CUANDO...',
    [
        'Necesitas debuggear un error no obvio',
        'La decisión de arquitectura no está clara aún',
        'El cambio afecta archivos con dependencias complejas',
        'Necesitas que entienda el contexto completo del proyecto',
        'La tarea es pequeña (< 20 min) — el overhead no compensa',
        'Ya has tenido que corregirle el mismo tipo de error antes',
    ],
    C_GEMINI, colors.HexColor('#DC2626'),
    C_GEMINI_BG, colors.HexColor('#FEF2F2')
))
story.append(spacer(0.3))

story.append(Paragraph('El flujo correcto con Gemini CLI', H2))

flow_data = [
    [Paragraph('1', CELL_H), Paragraph('Claude identifica que la tarea es apta para Gemini y lo sugiere', CELL)],
    [Paragraph('2', CELL_H), Paragraph('Claude actualiza docs del proyecto (tareas.md, session-log.md) para que Gemini tenga contexto', CELL)],
    [Paragraph('3', CELL_H), Paragraph('Claude entrega un prompt preciso: archivos a leer, patrón a seguir, archivos que NO tocar', CELL)],
    [Paragraph('4', CELL_H), Paragraph('Tú ejecutas con Gemini CLI', CELL)],
    [Paragraph('5', CELL_H), Paragraph('Claude revisa el resultado antes del commit y da el OK o pide correcciones', CELL)],
]
flow_table = Table(flow_data, colWidths=[0.8*cm, W - 0.8*cm])
flow_table.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (0,-1), C_GEMINI),
    ('BACKGROUND',    (1,0), (-1,-1), C_GEMINI_BG),
    ('BOX',           (0,0), (-1,-1), 0.5, C_GEMINI),
    ('INNERGRID',     (0,0), (-1,-1), 0.3, colors.HexColor('#FDE68A')),
    ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING',    (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ('LEFTPADDING',   (0,0), (-1,-1), 10),
    ('RIGHTPADDING',  (0,0), (-1,-1), 10),
    ('FONTNAME',      (0,0), (0,-1), 'Helvetica-Bold'),
    ('FONTSIZE',      (0,0), (0,-1), 11),
    ('TEXTCOLOR',     (0,0), (0,-1), colors.white),
    ('ALIGN',         (0,0), (0,-1), 'CENTER'),
]))
story.append(flow_table)
story.append(spacer(0.3))

story.append(Paragraph('Ejemplos reales de tus proyectos', H2))

story.append(example_box(
    'Fronterra — S016',
    'Cambiar texto del Hero en app1.js y app.transpiled.js. '
    'Tarea de texto puro, patrón clarísimo, sin dependencias. '
    'Gemini lo hizo correctamente sin intervención.',
    C_GEMINI, C_GEMINI_BG
))
story.append(spacer(0.2))
story.append(example_box(
    'Finances — S006',
    'Investigar precios actuales de BTC, ETH, XRP, NVIDIA, generar reporte '
    'en docs/reportes/ y actualizar tareas.md. Tarea de lookup + formateo. '
    'Gemini la ejecutó bien; Claude revisó y corrigió un error de calibración.',
    C_GEMINI, C_GEMINI_BG
))
story.append(spacer(0.2))
story.append(example_box(
    'ChuteBay — S009',
    'Implementar Light Mode completo en 23 archivos: next-themes, ThemeProvider, '
    'ThemeToggle, refactorización de clases Tailwind en toda la UI. '
    'Implementación pura masiva con un patrón bien definido. Gemini ideal.',
    C_GEMINI, C_GEMINI_BG
))
story.append(spacer(0.2))
story.append(example_box(
    'AI Agency — S001 (Gemini)',
    'Completar la automatización de Make.com (trigger Schedule + módulo HTTP + '
    'Set Variable + Gmail) que Claude había dejado bloqueada por límite de créditos. '
    'Gemini continuó con instrucciones precisas y lo entregó funcionando.',
    C_GEMINI, C_GEMINI_BG
))
story.append(spacer(0.2))

story.append(Paragraph('Advertencia sobre Gemini', H2))
story.append(info_box(
    '<b>Gemini tiende a inventar referencias.</b> En la sesión 010 de Finances se detectó que '
    'Gemini había referenciado "scripts de análisis del 2026-04-01" que no existían. '
    'También usó cifras incorrectas (gasto mensual $1.000 en lugar de $700). '
    'Siempre pide a Claude que revise el trabajo de Gemini antes de commitear, '
    'especialmente cuando hay datos numéricos o referencias a archivos.',
    C_GEMINI, C_GEMINI_BG
))

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN EXTRA — CUÁNDO CAMBIAR DE MODELO EN MITAD DE UNA TAREA
# ══════════════════════════════════════════════════════════════════════════════

story.append(Paragraph('Cuándo cambiar de modelo en mitad de una tarea', H1))
story.append(hr())
story.append(Paragraph(
    'No siempre una sesión usa un solo modelo. Reconocer el momento de cambiar '
    'es una habilidad práctica que reduce el gasto de tokens y mejora los resultados.',
    BODY
))
story.append(spacer(0.2))

switch_data = [
    [
        Paragraph('SEÑAL', CELL_H),
        Paragraph('QUÉ HACER', CELL_H),
    ],
    [
        Paragraph('Estás en Sonnet y te das cuenta de que la tarea es solo copiar/pegar algo', CELL),
        Paragraph('Cambia a Haiku o pásalo a Gemini', CELL),
    ],
    [
        Paragraph('Estás en Sonnet y el error se repite o el modelo no llega a la solución', CELL),
        Paragraph('Sube a Opus para la parte de diagnóstico', CELL),
    ],
    [
        Paragraph('Estás en Opus y ya tomaste la decisión — ahora es implementar', CELL),
        Paragraph('Baja a Sonnet para la ejecución', CELL),
    ],
    [
        Paragraph('La implementación que viene es grande y bien definida (> 20 min)', CELL),
        Paragraph('Cierra con Claude, pásalo a Gemini CLI con prompt preciso', CELL),
    ],
    [
        Paragraph('Empezaste con Gemini y hay un error que no puede resolver', CELL),
        Paragraph('Vuelve a Claude (Sonnet) para el debugging', CELL),
    ],
]

switch_table = Table(switch_data, colWidths=[9*cm, 7.3*cm], repeatRows=1)
row_styles_s = []
for i in range(1, len(switch_data)):
    bg = C_BG if i % 2 == 0 else colors.white
    row_styles_s.append(('BACKGROUND', (0,i), (-1,i), bg))

switch_table.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0), C_DARK),
    ('GRID',          (0,0), (-1,-1), 0.4, C_BORDER),
    ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING',    (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ('LEFTPADDING',   (0,0), (-1,-1), 10),
    ('RIGHTPADDING',  (0,0), (-1,-1), 10),
] + row_styles_s))

story.append(switch_table)
story.append(spacer(0.4))

story.append(Paragraph('Interrumpir a Claude a mitad de una tarea', H2))
story.append(info_box(
    '<b>Si te das cuenta de que Claude va por el camino equivocado, presiona Escape para interrumpirlo.</b> '
    'No esperes a que termine — habrás gastado tokens en trabajo que tendrás que deshacer. '
    'Una vez interrumpido, escribe la aclaración y Claude retoma con el contexto correcto. '
    'Si la aclaración es menor y ya terminó, simplemente escríbela como siguiente mensaje.',
    C_SONNET, C_SONNET_BG
))
story.append(spacer(0.4))

# ══════════════════════════════════════════════════════════════════════════════
# RESUMEN FINAL — MAPA MENTAL
# ══════════════════════════════════════════════════════════════════════════════

story.append(Paragraph('Mapa mental rápido', H1))
story.append(hr())

summary_data = [
    [
        Paragraph('HAIKU', S('SH_H', fontSize=11, textColor=colors.white, fontName='Helvetica-Bold', alignment=TA_CENTER)),
        Paragraph('SONNET', S('SH_S', fontSize=11, textColor=colors.white, fontName='Helvetica-Bold', alignment=TA_CENTER)),
        Paragraph('OPUS', S('SH_O', fontSize=11, textColor=colors.white, fontName='Helvetica-Bold', alignment=TA_CENTER)),
        Paragraph('GEMINI CLI', S('SH_G', fontSize=11, textColor=colors.white, fontName='Helvetica-Bold', alignment=TA_CENTER)),
    ],
    [
        Paragraph('Mecánico\nRápido\nBarato', S('SC_H', fontSize=10, textColor=C_HAIKU, fontName='Helvetica-Bold', alignment=TA_CENTER, leading=16)),
        Paragraph('Razonamiento\nEquilibrado\nDefault', S('SC_S', fontSize=10, textColor=C_SONNET, fontName='Helvetica-Bold', alignment=TA_CENTER, leading=16)),
        Paragraph('Máximo criterio\nEstrategia\nDecisiones clave', S('SC_O', fontSize=10, textColor=C_OPUS, fontName='Helvetica-Bold', alignment=TA_CENTER, leading=16)),
        Paragraph('Implementación\npura larga\nGratuito', S('SC_G', fontSize=10, textColor=C_GEMINI, fontName='Helvetica-Bold', alignment=TA_CENTER, leading=16)),
    ],
    [
        Paragraph('"Cambia X por Y"', S('SQ_H', fontSize=9, textColor=C_DARK, fontName='Helvetica-Oblique', alignment=TA_CENTER)),
        Paragraph('"¿Por qué falla esto?"', S('SQ_S', fontSize=9, textColor=C_DARK, fontName='Helvetica-Oblique', alignment=TA_CENTER)),
        Paragraph('"¿Cómo debería\nestructurar esto?"', S('SQ_O', fontSize=9, textColor=C_DARK, fontName='Helvetica-Oblique', alignment=TA_CENTER, leading=13)),
        Paragraph('"Implementa la\npantalla de login"', S('SQ_G', fontSize=9, textColor=C_DARK, fontName='Helvetica-Oblique', alignment=TA_CENTER, leading=13)),
    ],
]

col_w4 = [W/4] * 4
summary_table = Table(summary_data, colWidths=col_w4)
summary_table.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (0,0), C_HAIKU),
    ('BACKGROUND',    (1,0), (1,0), C_SONNET),
    ('BACKGROUND',    (2,0), (2,0), C_OPUS),
    ('BACKGROUND',    (3,0), (3,0), C_GEMINI),
    ('BACKGROUND',    (0,1), (0,-1), C_HAIKU_BG),
    ('BACKGROUND',    (1,1), (1,-1), C_SONNET_BG),
    ('BACKGROUND',    (2,1), (2,-1), C_OPUS_BG),
    ('BACKGROUND',    (3,1), (3,-1), C_GEMINI_BG),
    ('BOX',           (0,0), (0,-1), 1, C_HAIKU),
    ('BOX',           (1,0), (1,-1), 1, C_SONNET),
    ('BOX',           (2,0), (2,-1), 1, C_OPUS),
    ('BOX',           (3,0), (3,-1), 1, C_GEMINI),
    ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING',    (0,0), (-1,-1), 12),
    ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ('LEFTPADDING',   (0,0), (-1,-1), 6),
    ('RIGHTPADDING',  (0,0), (-1,-1), 6),
    ('INNERGRID',     (0,0), (-1,-1), 0.3, C_BORDER),
]))
story.append(summary_table)
story.append(spacer(0.5))

story.append(rule_box(
    '<b>Para NotebookLM:</b> Este documento está estructurado con secciones y ejemplos reales '
    'pensados para generar infografías, flashcards y resúmenes. Las secciones "Ejemplos reales" '
    'son especialmente útiles para crear casos de uso visuales. '
    'La tabla de referencia rápida puede usarse directamente como base para una infografía de decisión.'
))

# ─── Build ─────────────────────────────────────────────────────────────────────
output_path = str(Path(__file__).resolve().parent / "docs" / "assets" / "guia-modelos-ia.pdf")
doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    rightMargin=2*cm,
    leftMargin=2*cm,
    topMargin=2*cm,
    bottomMargin=2*cm,
    title='Guía de Modelos de IA',
    author='Damian Otero',
    subject='Cuándo usar Haiku, Sonnet, Opus y Gemini CLI'
)
doc.build(story)
print(f'PDF generado: {output_path}')
