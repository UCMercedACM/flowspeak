import argparse
import os
import sys
from pathlib import Path

from utils.config import VoiceConfig
from core import VoiceApp


config_path = Path(__file__).parent / "config.yml"
config = VoiceConfig(config_path)

app = VoiceApp()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-H",
        "--host",
        default=config["app"]["host"],
        help="The host to bind to. Defaults to value set in config",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=config["app"]["port"],
        help="The port to bind to. Defaults to value set in config",
        type=int,
    )
    parser.add_argument(
        "-nw",
        "--no-workers",
        action="store_true",
        default=False,
        help="Runs no workers",
    )
    parser.add_argument("-w", "--workers", default=os.cpu_count() or 1, type=int)

    args = parser.parse_args(sys.argv[1:])
    use_workers = not args.no_workers
    worker_count = args.workers

    # We should NOT do this but whatever
    app.run(host=args.host, port=args.port, debug=True)
