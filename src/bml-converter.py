import os
from os import listdir
from os.path import isfile, join, dirname
import argparse
from gooey import Gooey, GooeyParser

from bml import about
from bml import bml
from bml import bss
from bml import html
from bml import latex
from bss import bss2bml

@Gooey(default_size=(600, 900),
       progress_regex=r"^progress: (?P<current>\d+)/(?P<total>\d+)$",
       progress_expr="current / total * 100",
       optional_cols=4,
       required_cols=4,
       menu=[{
           'name': 'Help',
           'items': [{
               'type': 'AboutDialog',
               'menuTitle': 'About',
               'name': 'BML converter',
               'description': 'Run the various BML converters',
               'version': about.__version__,
               'copyright': about.__copyright__,
               'website': about.__url__,
               'author(s)': about.__author__,
               'license': about.__license__
           }, {
               'type': 'Link',
               'menuTitle': 'Documentation',
               'url': about.__help_url__
           }]
       }])
def main():
    parser = GooeyParser(description='BML convert')

    file_group = parser.add_argument_group("File options", "Specify input file and output directory")
    file_group.add_argument(
        'inputdir',
        help="Directory with BML/BSS file(s)",
        widget='DirChooser') 
    file_group.add_argument(
        'outputdir',
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
#       action="count",
        type=int,
        choices=range(0, 3),
        default=bml.args.verbose,
        help="increase output verbosity")

    parser.parse_args(namespace=bml.args)

    bml.args.tree = not(bml.args.no_tree)
    bml.args.include_external_files = not(bml.args.dont_include_external_files)

    nr_bml_processes = int(bml.args.bml2bss) + int(bml.args.bml2html) + int(bml.args.bml2latex)
    nr_bss_processes = int(bml.args.bss2bml)

    bml_files = [f for f in listdir(bml.args.inputdir) if isfile(join(bml.args.inputdir, f)) and f[-4:] == '.bml' and nr_bml_processes > 0]
    bss_files = [f for f in listdir(bml.args.inputdir) if isfile(join(bml.args.inputdir, f)) and f[-4:] == '.bss' and nr_bss_processes > 0]
    
    nr_processes = nr_bml_processes * len(bml_files) + nr_bss_processes * len(bss_files)

    assert nr_processes > 0, 'Number of files to process (%d) and number of generators to launch (%d) must be at least 1.' % ((len(bml_files) + len(bss_files)), (nr_bml_processes + nr_bss_processes))

    process_nr = 0

    if nr_bml_processes > 0:
        for f in sorted(bml_files):
            bml.args.inputfile = f
            content = None # parse each input file just once 
            for c in ['bml2bss', 'bml2html', 'bml2latex']:
                if c == 'bml2bss' and bml.args.bml2bss:
                    content = bss.bml2bss(bml.args.inputfile, bml.args.outputdir, content=content)
                elif c == 'bml2html' and bml.args.bml2html:
                    content = html.bml2html(bml.args.inputfile, bml.args.outputdir, content=content)
                elif c == 'bml2latex' and bml.args.bml2latex:
                    content = latex.bml2latex(bml.args.inputfile, bml.args.outputdir, content=content)
                else:
                    continue
                process_nr += 1
                print('progress: %d/%d' % (process_nr, nr_processes))
    
    if nr_bss_processes > 0:
        for f in sorted(bss_files):
            bml.args.inputfile = f
            assert bml.args.bss2bml  # just checking
            bss2bml(bml.args.inputfile, bml.args.outputdir)
            process_nr += 1
            print('progress: %d/%d' % (process_nr, nr_processes))


if __name__ == '__main__':
    main()
