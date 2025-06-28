import argparse
import sys

from insight.main import ingest_pypi


def main():
    parser = argparse.ArgumentParser(
        description="Fetch PyPI package data and store it in the database."
    )

    parser.add_argument(
        "--pypi-ingestion",
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

    parser.add_argument(
        "--minimum-stars",
        type=int,
        default=10,
        help="(Only used with --pypi-ingestion) Minimum number of GitHub stars a package's repository must have to be stored in the database.",
    )

    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Runs the program without connecting to Database. No Data is inserted into Database. This is for Development Purpose",
    )

    args = parser.parse_args()
    mode = args.mode
    dry_run = args.dry_run
    minimum_stars = args.minimum_stars

    if not args.pypi_ingestion and minimum_stars:
        raise argparse.ArgumentError(
            "'--minimum-stars' cannot be used without '--pypi-ingestion'."
        )

    if args.pypi_ingestion:
        status = ingest_pypi(mode=mode, dry_run=dry_run, minimum_stars=minimum_stars)

    if not status:
        sys.exit(1)


if __name__ == "__main__":
    main()
