"""
API for the migration
"""

import argparse
import os


from_to = (
    ("{output_path}/revistas/{jacron}/{lng}about.htm",
     "https://{url}/journal/{jacron}/about/#about"),
    ("{output_path}/revistas/{jacron}/{lng}edboard.htm",
     "https://{url}/journal/{jacron}/about/#editors"),
    ("{output_path}/revistas/{jacron}/{lng}instruc.htm",
     "https://{url}/journal/{jacron}/about/#instructions"),
    ("{output_path}/revistas/{jacron}/{lng}subscrp.htm",
     "https://{url}/journal/{jacron}/about/#about"),
)

TEXT = {
    "e": "Contenido disponible solamente en {url}",
    "i": "Updated content only at {url}",
    "p": "Conteúdo disponível somente em {url}",
}


def redirect_journal_new_pages(url, src_path, output_path, jacron):
    try:
        with open(src_path) as fp:
            content = fp.read()
    except:
        content = f'<html><body><a href="URI">TEXT</a></body></html>'

    for _from_to in from_to:
        f, t = _from_to
        dirname = f"{output_path}/revistas/{jacron}"
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

        for lng in ("e", "i", "p"):
            file_path = f.format(
                output_path=output_path,
                jacron=jacron,
                lng=lng,
            )
            uri = t.format(url=url, jacron=jacron)
            new_content = content
            new_content = new_content.replace(
                "TEXT", TEXT[lng].format(url=url))
            new_content = new_content.replace("URI", uri)
            with open(file_path, "w") as fp:
                fp.write(new_content)


def info_new_pages(url, src_path, output_path, acrons):
    if not os.path.isdir(output_path):
        os.makedirs(output_path)
    for acron in acrons:
        redirect_journal_new_pages(url, src_path, output_path, acron)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "generate journal informative pages "
            "to redirect to new website"
        )
    )
    subparsers = parser.add_subparsers(
        title="Commands", metavar="", dest="command")

    info_new_pages_parser = subparsers.add_parser(
        "info_new_pages",
        help=(
            "Migrate journal data from ISIS database to MongoDB."
        )
    )
    info_new_pages_parser.add_argument(
        "--src_path",
        help=(
            "source path"
        )
    )

    info_new_pages_parser.add_argument(
        "--uri",
        help=(
            "uri"
        )
    )

    info_new_pages_parser.add_argument(
        "--output_path",
        help=(
            "output path"
        )
    )

    info_new_pages_parser.add_argument(
        "--acrons",
        help=(
            "journal acrons separated by comma (,)"
        )
    )

    args = parser.parse_args()
    result = None
    if args.command == "info_new_pages":
        acrons = args.acrons
        acrons = acrons.replace(" ", ",")
        if "," in acrons:
            acrons = [a.strip() for a in acrons.split(",")]
        result = info_new_pages(
            args.uri, args.src_path,
            args.output_path, acrons,
        )
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
