from argparse import ArgumentParser
import sys

from insight.main import ingest_pypi


def main():
    parser = ArgumentParser(
        description="Fetch PyPI package data and store it in the database."
    )

    parser.add_argument(
        "-s",
        "--store",
        action="store_true",
        help="Scrapes the PyPI website and extracts the packages which were uploaded today and then enters into DB. Make sure PostgreSQL DB Server is Running.",
    )

    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        default="dev",
        choices=["dev", "prod"],
        help="Which Mode you want to Run Project on",
    )

    args = parser.parse_args()
    mode = args.mode

    if args.store:
        status = ingest_pypi(mode=mode)
        if not status:
            sys.exit(1)


if __name__ == "__main__":
    main()
