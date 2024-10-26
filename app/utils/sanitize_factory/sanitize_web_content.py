import html
import bleach

def sanitize_web_content(content):
    """
    Sanitizes a web content string to prevent XSS (Cross-Site Scripting) attacks.
    
    Parameters:
    - content (str): The web content to sanitize.
    
    Returns:
    - str: The sanitized content.
    """

    # Step 1: Decode HTML entities
    content = html.unescape(content)

    # Step 2: Strip out JavaScript, iframes, and other unsafe tags/attributes
    safe_content = bleach.clean(
        content,
        tags=[
            "b", "i", "u", "em", "strong", "p", "br", "ul", "li", "ol", "a", "span", "div", "img",
            "header", "footer", "nav", "section", "article", "aside", "h1", "h2", "h3", "h4", "h5", "h6",
            "button", "form", "input", "label", "select", "option", "textarea", "small", "table", "tr", "td", "th",
            "thead", "tbody", "tfoot", "caption", "blockquote", "pre", "code", "hr", "figure", "figcaption"
        ],
        attributes={
            "a": ["href", "title", "target", "rel"],
            "img": ["src", "alt", "title", "width", "height"],
            "button": ["type", "class"],
            "input": ["type", "name", "value", "placeholder", "class"],
            "form": ["action", "method", "class"],
            "table": ["class", "border", "cellpadding", "cellspacing"],
            "div": ["class", "id"],
            "span": ["class"],
            "header": ["class"],
            "footer": ["class"],
            "nav": ["class"],
            "section": ["class"],
            "article": ["class"],
            "aside": ["class"],
            "label": ["for", "class"],
            "select": ["name", "class"],
            "option": ["value", "class"],
            "textarea": ["name", "rows", "cols", "class"],
            "h1": ["class"],
            "h2": ["class"],
            "h3": ["class"],
            "h4": ["class"],
            "h5": ["class"],
            "h6": ["class"],
            "table": ["class"],
            "tr": ["class"],
            "td": ["class", "colspan", "rowspan"],
            "th": ["class", "colspan", "rowspan"],
        },
        protocols=["http", "https"],
        strip=True
    )

    # Step 3: Encode any remaining HTML entities (for added safety)
    safe_content = html.escape(safe_content)

    return safe_content

# Example usage:
input_content = '''
<script>alert("This is an attack!")</script>
<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand" href="#">Brand</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
            <li class="nav-item active">
                <a class="nav-link" href="#">Home</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#">Features</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#">Pricing</a>
            </li>
            <li class="nav-item">
                <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">Disabled</a>
            </li>
        </ul>
    </div>
</nav>
'''

print(sanitize_web_content(input_content))
