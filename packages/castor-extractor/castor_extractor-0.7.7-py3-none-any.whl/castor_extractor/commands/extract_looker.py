from argparse import ArgumentParser

from castor_extractor.visualization import looker  # type: ignore


def main():
    parser = ArgumentParser()
    parser.add_argument("-b", "--base-url", help="Looker base url")
    parser.add_argument("-u", "--username", help="Looker client id")
    parser.add_argument("-p", "--password", help="Looker client secret")
    parser.add_argument("-o", "--output", help="Directory to write to")
    parser.add_argument("-t", "--timeout", type=int, help="Timeout in seconds")
    parser.add_argument(
        "--thread-pool-size",
        type=int,
        help="Thread pool size, if searching per folder",
    )
    parser.add_argument(
        "--safe-mode",
        "-s",
        help="Looker safe mode",
        action="store_true",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--all-looks",
        help="Use all_looks endpoint instead of the paginated search_looks",
        action="store_true",
    )
    group.add_argument(
        "--search-per-folder",
        help="Fetches Looks and Dashboards per folder",
        action="store_true",
    )

    args = parser.parse_args()

    looker.extract_all(
        base_url=args.base_url,
        client_id=args.username,
        client_secret=args.password,
        output_directory=args.output,
        timeout=args.timeout,
        thread_pool_size=args.thread_pool_size,
        all_looks=args.all_looks,
        search_per_folder=args.search_per_folder,
        safe_mode=args.safe_mode,
    )
