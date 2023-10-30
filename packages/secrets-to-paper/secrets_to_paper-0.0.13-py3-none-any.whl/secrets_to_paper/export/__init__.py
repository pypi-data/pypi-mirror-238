import jinja2
from weasyprint import HTML, CSS # type: ignore


templateLoader = jinja2.PackageLoader("secrets_to_paper", "templates")
templateEnv = jinja2.Environment(loader=templateLoader, keep_trailing_newline=True)

def write_pdf_to_disk(rendered_html, output_file):

    html = HTML(string=rendered_html)
    css = templateEnv.get_template("main.css").render()

    css = CSS(string=css)

    html.write_pdf(
        output_file, stylesheets=[css],
    )

    return None
