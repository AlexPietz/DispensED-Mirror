(TeX-add-style-hook
 "main"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("scrreprt" "a4paper" "10pt" "DIV10" "openright" "openbib")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("inputenc" "utf8") ("fontenc" "T1") ("babel" "english") ("babelbib" "fixlanguage") ("varioref" "english") ("footmisc" "stable")))
   (add-to-list 'LaTeX-verbatim-environments-local "lstlisting")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "lstinline")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "lstinline")
   (TeX-run-style-hooks
    "latex2e"
    "scrreprt"
    "scrreprt10"
    "inputenc"
    "fontenc"
    "babel"
    "babelbib"
    "float"
    "scrpage2"
    "tocloft"
    "graphicx"
    "wrapfig"
    "array"
    "tabularx"
    "tikz"
    "pdfpages"
    "varioref"
    "makeidx"
    "listings"
    "textcomp"
    "hyperref"
    "caption"
    "rotating"
    "mathtools"
    "amsmath"
    "booktabs"
    "titling"
    "footmisc"
    "color")
   (TeX-add-symbols
    "oldbibliography"
    "chapter")
   (LaTeX-add-bibliographies
    "Bibl")
   (LaTeX-add-listings-lstdefinestyles
    "mystyle")
   (LaTeX-add-color-definecolors
    "codegreen"
    "codegray"
    "codepurple"
    "backcolour"))
 :latex)

