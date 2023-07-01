import logging
import re
import markdown as md
import markmoji
from pathlib import Path


encoding = 'utf-8'
__folder__ = Path(__file__).parent
logging.getLogger().setLevel(logging.INFO)


def normalize(self, target):
    """
    Inverse of relative_to, honestly no idea why this isn't already in pathlib.Path
    """
    rel = target.relative_to(self)
    norm = Path()
    for p in rel.parents:
        if p != Path():
            norm /= ".."
    return norm
Path.normalize = normalize


class NavLink:
    def __init__(self, label="", href=""):
        self.label = label
        self.href= href
    
    def __str__(self):
        return f"<a href={self.href}>{self.label}</a>\n"


class NavBar(list):    
    def appendLink(self, label:str, href:str):
        self.append(
            NavLink(label=label, href=href)
        )
    
    def __str__(self):
        # Work out how much to offset by
        offset = 3*len(self)
        # Open tag
        code = f"<nav style='margin-bottom: -{offset}rem;'>\n"
        # Add each link
        for link in self:
            code += f"  {link}"
        # Close tag
        code += "</nav>\n"

        return code


class Page:
    def __init__(self, file:Path, template:Path):
        # Store paths
        self.file = file
        self.template = template
        # Read in template
        with open(str(template), "r", encoding=encoding) as f:
            self.base = f.read()
        logging.info(f"Read template.html.")
        # Store namespace dict
        self.namespace = {}
        # Read in markdown
        with open(str(file), "r", encoding=encoding) as f:
            content_md = f.read()
        logging.info(f"Written {file.relative_to(__folder__)}")
        self.namespace['content_md'] = content_md
        # Get relative src link
        src = __folder__.normalize(file)
        self.namespace['src'] = src
    
    def preprocess(self, content:str):
        """
        Markdown processing to do before converting to HTML
        """

        return content
    
    def process(self, content:str):
        content = md.markdown(content, extensions=[markmoji.Markmoji(), "extra", "admonition", "nl2br", "toc"])

        return content
    
    def postprocess(self, content:str):
        # Build nav bar
        navbar = NavBar()
        matches = re.findall("<h1 id=\"([\w\-]*)\">(.*)</h1>", content)
        if len(matches) > 1:
            # If there is more than 1 heading...
            for match in matches:
                # Add a link for each heading
                href = f"#{match[0]}"
                label = match[1]
                navbar.appendLink(label=label, href=href)
        # Store nav bar
        self.namespace['navbar'] = navbar

        # Build breadcrumbs
        breadcrumbs = ""
        if self.file != __folder__ / "index.md":
            breadcrumbs = f"<a class=breadcrumbs href='{self.namespace['src'] / 'index.html'}'>🏠</a>"
        # Store breadcrumbs
        self.namespace['breadcrumbs'] = breadcrumbs

        return content

    def transpile(self):
        """
        Convert markdown to HTML, including pre- and post- processing
        """
        # Get raw markdown
        content = self.namespace['content_md']
        # Preprocess markdown
        content = self.preprocess(content)
        # Convert to HTML
        content = self.process(content)
        # Postprocess HTML
        content = self.postprocess(content)
        # Store processed HTML
        self.namespace['content_html'] = self.namespace['content'] = content
    
    def __str__(self):
        self.transpile()

        def _name(match):
            # Get name
            name = match.group(1)
            if name in self.namespace:
                # If name is valid, use corresponding value
                return str(self.namespace[name])
            else:
                # Raise error if no value found
                logging.warning(f"Could not replace: {name}")
        # Replace all names in base with values from namespace
        content = re.sub(r"\{\{(\w*)\}\}", _name, self.base, flags=re.MULTILINE)

        return content

# Write all markdown files
for file in __folder__.glob("**/*.md"):
    # Create Page object
    page = Page(file, template=__folder__ / "template.html")

    # Write output
    outfile = file.parent / (file.stem + ".html")
    with open(str(outfile), "w", encoding=encoding) as f:
        f.write(str(page))
        logging.info(f"Written {outfile.relative_to(__folder__)}")