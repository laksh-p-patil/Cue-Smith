from nicegui import ui
from loader import load_lesson

ui.add_head_html('''
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@400;600&display=swap" rel="stylesheet">
''')

ui.add_css('''
:root {
    --bg: #f5f5f7;
    --panel: rgba(255, 255, 255, 0.7);
    --border: rgba(0, 0, 0, 0.06);
    --text: #1d1d1f;
    --muted: #6e6e73;
    --shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
    --shadow-hover: 0 12px 32px rgba(0, 0, 0, 0.08);
}
body.body--dark {
    --bg: #121214;
    --panel: rgba(44, 44, 46, 0.6);
    --border: rgba(255, 255, 255, 0.1);
    --text: #f5f5f7;
    --muted: #a1a1a6;
    --shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
    --shadow-hover: 0 12px 32px rgba(0, 0, 0, 0.6);
}
body {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: -apple-system, "SF Pro Display", "Helvetica Neue", sans-serif !important;
    transition: background 0.3s ease, color 0.3s ease;
}
.q-card.panel {
    background: var(--panel) !important;
    color: var(--text) !important;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--border);
    border-radius: 20px;
    box-shadow: var(--shadow);
    padding: 40px 48px;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.q-card.panel:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-hover);
}
.title {
    font-family: "Fraunces", Georgia, serif;
    font-size: 40px;
    font-weight: 600;
    letter-spacing: -0.02em;
    color: var(--text);
}
.subtitle {
    font-size: 17px;
    color: var(--muted);
}
.mode-toggle {
    position: fixed;
    top: 16px;
    right: 16px;
    z-index: 10;
    color: var(--text) !important;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}
.fade-in { animation: fadeUp 0.6s ease both; }
.fade-in-2 { animation: fadeUp 0.6s ease 0.15s both; }
''')

dark = ui.dark_mode(True)
ui.button(icon='brightness_6', on_click=dark.toggle).props('flat round').classes('mode-toggle')

lesson = load_lesson(1)

with ui.column().classes('w-full items-center q-pt-xl'):
    ui.label(lesson['title']).classes('title fade-in')
    ui.label(lesson['summary']).classes('subtitle fade-in-2')
    with ui.row().classes('q-mt-lg fade-in-2'):
        with ui.card().classes('panel').style('max-width: 420px'):
            ui.label('Weak prompt').classes('subtitle')
            ui.label(lesson['bad_prompt'])
        with ui.card().classes('panel').style('max-width: 420px'):
            ui.label('Strong prompt').classes('subtitle')
            ui.label(lesson['good_prompt'])
    ui.label(lesson['takeaway']).classes('subtitle')

ui.run()