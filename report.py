
from latex import build_pdf

def make_report():
    min_latex = (r"\documentclass{article}"
                r"\begin{document}"
                r"Hello, world!"
                r"\end{document}")

    # this builds a pdf-file inside a temporary directory
    pdf = build_pdf(min_latex)
    pdf.save_to('pdfs/ex1.pdf')
