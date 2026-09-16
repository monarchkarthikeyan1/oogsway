import re
import bleach

ALLOWED_TAGS = [
    'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol',
    'p', 'strong', 'ul', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'span',
    'table', 'thead', 'tbody', 'tr', 'th', 'td', 'img', 'hr', 'br', 'pre',
    'svg', 'path', 'circle', 'rect', 'line', 'polyline', 'polygon', 'g',
    'button', 'input', 'form', 'label', 'select', 'option', 'canvas', 'style'
]

ALLOWED_ATTRIBUTES = {
    '*': ['class', 'id', 'style', 'title', 'data-*'],
    'a': ['href', 'title', 'target', 'rel'],
    'img': ['src', 'alt', 'width', 'height', 'title'],
    'input': ['type', 'placeholder', 'value', 'name', 'checked'],
    'button': ['type', 'name', 'value'],
    'svg': ['width', 'height', 'viewbox', 'fill', 'stroke', 'xmlns', 'stroke-width'],
    'path': ['d', 'fill', 'stroke', 'stroke-width', 'stroke-linecap', 'stroke-linejoin'],
    'circle': ['cx', 'cy', 'r', 'fill', 'stroke'],
    'rect': ['x', 'y', 'width', 'height', 'rx', 'ry', 'fill', 'stroke'],
}

def sanitize_html(raw_html: str) -> str:
    """
    Sanitizes HTML content to prevent XSS attacks while allowing rich UI components.
    Strips dangerous tags like <script> requiring iframe sandboxing or direct injection protection.
    """
    if not raw_html:
        return ""
    
    # Strip script tags for safe static preview if necessary
    sanitized = bleach.clean(
        raw_html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True
    )
    return sanitized

def prepare_iframe_document(html_content: str, title: str = "Artifact Preview") -> str:
    """
    Wraps HTML content in a self-contained document with security meta tags, CSS reset,
    and dark-mode aesthetic styling.
    """
    # Enforce safe document container with CSP headers embedded in meta tag
    csp_meta = """
    <meta http-equiv="Content-Security-Policy" content="default-src 'self' 'unsafe-inline' data: blob: https://fonts.googleapis.com https://cdn.jsdelivr.net; img-src 'self' data: https:; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;">
    """
    
    document = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    {csp_meta}
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent-cyan: #38bdf8;
            --accent-emerald: #34d399;
            --border-color: #334155;
        }}
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            padding: 24px;
        }}
        code, pre {{
            font-family: 'JetBrains Mono', monospace;
        }}
        a {{
            color: var(--accent-cyan);
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        h1, h2, h3, h4 {{
            color: #ffffff;
            margin-bottom: 0.75em;
            font-weight: 700;
        }}
        h1 {{ font-size: 1.875rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem; }}
        h2 {{ font-size: 1.5rem; margin-top: 1.5rem; }}
        h3 {{ font-size: 1.25rem; margin-top: 1.25rem; }}
        p {{ margin-bottom: 1rem; }}
        ul, ol {{ margin-bottom: 1rem; padding-left: 1.5rem; }}
        li {{ margin-bottom: 0.25rem; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            background: var(--bg-secondary);
            border-radius: 8px;
            overflow: hidden;
        }}
        th, td {{
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }}
        th {{
            background: #334155;
            color: #f1f5f9;
            font-weight: 600;
        }}
        blockquote {{
            border-left: 4px solid var(--accent-cyan);
            padding-left: 16px;
            margin: 1rem 0;
            color: var(--text-secondary);
            font-style: italic;
            background: rgba(56, 189, 248, 0.05);
            padding: 12px 16px;
            border-radius: 0 8px 8px 0;
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>"""
    return document
