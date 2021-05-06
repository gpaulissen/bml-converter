import os
import argparse
from gooey import Gooey, GooeyParser

from bml import bml
from bml import bss
from bml import html
from bml import latex
from bss import bss2bml

#@Gooey(tabbed_groups=True)
@Gooey(default_size=(800, 900),
       progress_regex=r"^progress: (?P<current>\d+)/(?P<total>\d+)$",
       progress_expr="current / total * 100",
       optional_cols=4,
       required_cols=4)
def main():
    # bml.args['bss'] = False
    # bml.args['html'] = False
    # bml.args['latex'] = False

    parser = GooeyParser(description='BML convert')

    file_group = parser.add_argument_group("File options", "Specify input file and output file")
    file_group.add_argument(
        'inputfile',
        help="BML file",
        widget='FileChooser') 
    file_group.add_argument(
        'outputfile',
        help="Output directory",
        widget='DirChooser')

    generate_group = parser.add_argument_group("Generate options", "Specify the generator(s)")
    generate_group.add_argument(
        '--bml2html',
        help='BML => HTML',
        dest='bml2html',
        action='store_true',
        default=True)
    generate_group.add_argument(
        '--bml2latex',
        help='BML => LaTeX',
        dest='bml2latex',
        action='store_true')
    generate_group.add_argument(
        '--bml2bss',
        help='BML => BSS',
        dest='bml2bss',
        action='store_true')
    generate_group.add_argument(
        '--bss2bml',
        help='BSS => BML',
        dest='bss2bml',
        action='store_true')

    layout_group = parser.add_argument_group("Layout options", 'Specify layout options')
    layout_group.add_argument(
        '--no-tree',
        dest='no_tree',
        help='Show simple bidding table (no tree)',
        action='store_true',
        default=False,
        widget='BlockCheckbox')
    layout_group.add_argument(
        '--indentation',
        type=int,
        choices=range(1, 10),
        default=bml.args.indentation,
        help='the indentation of a bidtable')

    other_group = parser.add_argument_group("Other options", 'Specify other options')
    other_group.add_argument(
        '--no-include-external-files',
        dest='dont_include_external_files',
        help='Only reference (do not include) bml.css/bml.tex in HTML/LaTeX output files',
        action='store_true',
        default=False,
        widget='BlockCheckbox')
    other_group.add_argument(
        "--verbose",
        action="count",
        default=bml.args.verbose,
        help="increase output verbosity")

    parser.parse_args(namespace=bml.args)

    bml.args.tree = not(bml.args.no_tree)
    bml.args.include_external_files = not(bml.args.dont_include_external_files)

    process_nr = 0
    nr_processes = int(bml.args.bml2bss) + int(bml.args.bml2html) + int(bml.args.bml2latex) + int(bml.args.bss2bml)

    assert nr_processes > 0, 'Number of generators to launch must be at least 1.'

    for c in ['bml2bss', 'bml2html', 'bml2latex', 'bss2bml']:
        if c == 'bml2bss' and bml.args.bml2bss:
            bss.bml2bss(bml.args.inputfile, bml.args.outputfile)
        elif c == 'bml2html' and bml.args.bml2html:
            html.bml2html(bml.args.inputfile, bml.args.outputfile)
        elif c == 'bml2latex' and bml.args.bml2latex:
            latex.bml2latex(bml.args.inputfile, bml.args.outputfile)
        elif c == 'bss2bml' and bml.args.bss2bml:
            bss2bml(bml.args.inputfile, bml.args.outputfile)
        else:
            continue
        process_nr += 1
        print('progress: %d/%d' % (process_nr, nr_processes))


if __name__ == '__main__':
    main()
