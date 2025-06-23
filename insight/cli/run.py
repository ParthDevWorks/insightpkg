from argparse import ArgumentParser

from insight.fetch_and_store_pypi import execute


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

    args = parser.parse_args()

    if args.store:
        execute()


if __name__ == "__main__":
    main()
