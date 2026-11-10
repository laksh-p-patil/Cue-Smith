from nicegui import app, ui
from pages.home import home
from pages.lesson import lesson_page

CSS = '''
:root {
    --font: "Fraunces", Georgia, "Times New Roman", serif;
    --page-bg: linear-gradient(180deg, #f3f3f3 0%, #e4e4e4 100%);
    --text: #111111;
    --muted: #7b7b7b;
    --fill: linear-gradient(180deg, rgba(255, 255, 255, 0.45), rgba(255, 255, 255, 0.12));
    --rim: rgba(255, 255, 255, 0.95);
    --inner-light: rgba(255, 255, 255, 0.9);
    --inner-dark: rgba(0, 0, 0, 0.05);
    --drop: 0 10px 28px -8px rgba(0, 0, 0, 0.12);
    --drop-hover: 0 16px 36px -8px rgba(0, 0, 0, 0.18);
    --btn-drop: 0 6px 16px -6px rgba(0, 0, 0, 0.14);
    --btn-drop-hover: 0 10px 22px -6px rgba(0, 0, 0, 0.20);
    --round-fill: rgba(255, 255, 255, 0.70);
    --surface-inset: inset 4px -4px 10px var(--inner-light), inset -2px 3px 8px var(--inner-dark);
    --btn-inset: inset 2px -2px 5px var(--inner-light), inset -1px 2px 4px var(--inner-dark);
    --cur-fill: rgba(255, 255, 255, 0.92);
    --cur-edge: rgba(0, 0, 0, 0.14);
    --cur-shadow: 0 3px 10px rgba(0, 0, 0, 0.25);
    --cur-ring-fill: rgba(0, 0, 0, 0.05);
    --cur-ring-edge: rgba(0, 0, 0, 0.30);
    --ok: #34c759;
    --bad: #ff3b30;
}
body.body--dark {
    --page-bg: linear-gradient(180deg, #1c1c1e 0%, #121213 100%);
    --text: #f2f2f2;
    --muted: #9a9a9f;
    --fill: linear-gradient(180deg, rgba(255, 255, 255, 0.07), rgba(255, 255, 255, 0.02));
    --rim: rgba(255, 255, 255, 0.16);
    --inner-light: rgba(255, 255, 255, 0.07);
    --inner-dark: rgba(0, 0, 0, 0.35);
    --drop: 0 10px 28px -8px rgba(0, 0, 0, 0.60);
    --drop-hover: 0 16px 36px -8px rgba(0, 0, 0, 0.75);
    --btn-drop: 0 6px 16px -6px rgba(0, 0, 0, 0.60);
    --btn-drop-hover: 0 10px 22px -6px rgba(0, 0, 0, 0.75);
    --round-fill: rgba(255, 255, 255, 0.10);
    --surface-inset: inset 4px -4px 10px var(--inner-light), inset -2px 3px 8px var(--inner-dark);
    --btn-inset: inset 2px -2px 5px var(--inner-light), inset -1px 2px 4px var(--inner-dark);
    --cur-fill: rgba(255, 255, 255, 0.92);
    --cur-edge: rgba(255, 255, 255, 0.90);
    --cur-shadow: 0 0 14px rgba(255, 255, 255, 0.28), 0 3px 10px rgba(0, 0, 0, 0.60);
    --cur-ring-fill: rgba(255, 255, 255, 0.08);
    --cur-ring-edge: rgba(255, 255, 255, 0.55);
    --ok: #30d158;
    --bad: #ff453a;
}
body, .q-btn, .q-card, .nicegui-content {
    font-family: var(--font) !important;
}
body {
    background: var(--page-bg) !important;
    background-attachment: fixed !important;
    color: var(--text) !important;
}
.q-card.panel, .slab, .q-btn.glass-btn {
    background: var(--fill) !important;
    color: var(--text) !important;
    border: 1.5px solid var(--rim) !important;
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
}
.q-card.panel, .slab {
    box-shadow: var(--surface-inset), var(--drop) !important;
}
.q-btn.glass-btn {
    box-shadow: var(--btn-inset), var(--btn-drop) !important;
}
.q-btn.glass-btn::before {
    box-shadow: none !important;
}
.q-card.panel {
    border-radius: 28px;
    padding: 40px 48px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.q-card.panel:hover {
    transform: translateY(-4px);
    box-shadow: var(--surface-inset), var(--drop-hover) !important;
}
.slab {
    max-width: 92vw;
    padding: 44px clamp(28px, 7vw, 80px);
    border-radius: 32px;
    transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.3s ease;
}
.slab:hover {
    transform: translateY(-1px) scale(1.02);
    box-shadow: var(--surface-inset), var(--drop-hover) !important;
}
.slab:active {
    transform: scale(0.98);
}
.slab .subtitle {
    text-align: center;
}
.q-btn.glass-btn {
    border-radius: 999px;
    padding: 10px 28px;
    font-size: 16px;
    font-weight: 500;
    transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.3s ease;
}
.q-btn.glass-btn:hover {
    transform: translateY(-1px) scale(1.03);
    box-shadow: var(--btn-inset), var(--btn-drop-hover) !important;
}
.q-btn.glass-btn:active {
    transform: scale(0.96);
}
.q-btn.glass-btn.q-btn--round {
    padding: 0;
    background: var(--round-fill) !important;
}
.q-btn.glass-btn.opt-ok,
.q-btn.glass-btn.opt-bad {
    opacity: 1 !important;
}
.q-btn.glass-btn.opt-ok {
    background: linear-gradient(color-mix(in srgb, var(--ok) 18%, transparent),
                                color-mix(in srgb, var(--ok) 18%, transparent)), var(--fill) !important;
    border-color: var(--ok) !important;
    animation: pop 0.3s ease;
}
.q-btn.glass-btn.opt-bad {
    background: linear-gradient(color-mix(in srgb, var(--bad) 18%, transparent),
                                color-mix(in srgb, var(--bad) 18%, transparent)), var(--fill) !important;
    border-color: var(--bad) !important;
    animation: shake 0.3s ease;
}
@keyframes pop {
    0% { transform: scale(1); }
    50% { transform: scale(1.04); }
    100% { transform: scale(1); }
}
@keyframes shake {
    0%, 100% { transform: translateX(0); }
    20% { transform: translateX(-6px); }
    40% { transform: translateX(5px); }
    60% { transform: translateX(-4px); }
    80% { transform: translateX(2px); }
}
@media (prefers-reduced-motion: reduce) {
    .q-btn.glass-btn.opt-ok, .q-btn.glass-btn.opt-bad { animation: none; }
}
.title {
    font-size: 40px;
    font-weight: 600;
    letter-spacing: -0.02em;
    color: var(--text);
}
.card-title {
    font-size: 24px;
    font-weight: 600;
    letter-spacing: -0.01em;
    color: var(--text);
}
.subtitle {
    font-size: 17px;
    color: var(--muted);
}
.lesson-body {
    width: 100%;
    max-width: 880px;
    padding: 0 20px;
}
.section-title {
    font-size: 26px;
    font-weight: 600;
    letter-spacing: -0.01em;
    color: var(--text);
    margin-top: 36px;
}
.body-text {
    font-size: 17px;
    line-height: 1.6;
    max-width: 720px;
    color: var(--text);
}
.part-name {
    font-weight: 600;
    color: var(--text);
}
.quote {
    color: var(--muted);
}
.card-link {
    text-decoration: none;
    color: inherit;
}
.mode-toggle {
    position: fixed !important;
    top: 16px;
    right: 16px;
    z-index: 10;
}
.cue-cursor {
    position: fixed;
    top: 0;
    left: 0;
    width: 0;
    height: 0;
    z-index: 9999;
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.2s ease;
}
.cue-cursor.on {
    opacity: 1;
}
.cue-cursor::before {
    content: '';
    position: absolute;
    left: -9px;
    top: -9px;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: var(--cur-fill);
    border: 1.5px solid var(--cur-edge);
    box-shadow: inset 1px 1px 2px rgba(255, 255, 255, 0.9), var(--cur-shadow);
    transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), background 0.2s ease,
                border-color 0.2s ease, border-width 0.2s ease;
}
.cue-cursor.big::before {
    transform: scale(2.4);
    background: var(--cur-ring-fill);
    border-color: var(--cur-ring-edge);
    border-width: 0.7px;
    box-shadow: none;
}
.cue-cursor.down::before {
    transform: scale(0.8);
}
.cue-cursor.big.down::before {
    transform: scale(2);
}
html.has-cue-cursor, html.has-cue-cursor * {
    cursor: none !important;
}
html.has-cue-cursor input, html.has-cue-cursor textarea {
    cursor: text !important;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}
.fade-in { animation: fadeUp 0.6s ease backwards; }
.fade-in-2 { animation: fadeUp 0.6s ease 0.15s backwards; }
'''

CURSOR_JS = """
<script>
(function () {
  if (!matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  window.__cueReady = true;
  var root = document.documentElement, dot = document.createElement('div');
  dot.className = 'cue-cursor';
  document.body.appendChild(dot);
  var tx = 0, ty = 0, x = 0, y = 0;
  var ease = matchMedia('(prefers-reduced-motion: reduce)').matches ? 1 : 0.22;
  addEventListener('mousemove', function (e) {
    tx = e.clientX; ty = e.clientY;
    root.classList.add('has-cue-cursor');
    dot.classList.add('on');
  });
  root.addEventListener('mouseleave', function () { dot.classList.remove('on'); });
  document.addEventListener('mouseover', function (e) {
    dot.classList.toggle('big', !!e.target.closest('a, button, .q-btn, .slab'));
  });
  addEventListener('mousedown', function () { dot.classList.add('down'); });
  addEventListener('mouseup', function () { dot.classList.remove('down'); });
  (function loop() {
    x += (tx - x) * ease; y += (ty - y) * ease;
    dot.style.transform = 'translate(' + x + 'px,' + y + 'px)';
    requestAnimationFrame(loop);
  })();
})();
</script>
"""


def setup_page():
    is_dark = app.storage.user.setdefault('dark_mode', True)
    bg, text = ('#171718', '#f2f2f2') if is_dark else ('#ececec', '#111111')
    ui.add_head_html(f'''
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
    body:not(.body--dark):not(.body--light) {{
        background: {bg} !important;
        color: {text} !important;
    }}
    </style>
    ''')
    ui.add_css(CSS)
    ui.add_body_html(CURSOR_JS)
    dark = ui.dark_mode().bind_value(app.storage.user, 'dark_mode')
    ui.button(icon='brightness_6', on_click=dark.toggle, color=None) \
        .props('flat round').classes('mode-toggle glass-btn')


def root():
    setup_page()
    ui.sub_pages({'/': home, '/lesson/{number}': lesson_page}).classes('w-full')


ui.run(root, storage_secret='cue-smith-dev-secret')