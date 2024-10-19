import argparse
import os
import sys
from pathlib import Path
import db

import uvicorn
from core import VoiceApp
from routes import router
from utils.config import VoiceConfig
from uvicorn.supervisors import Multiprocess

config_path = Path(__file__).parent / "config.yml"
config = VoiceConfig(config_path)

app = VoiceApp(config=config)
app.include_router(router)

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
        "-d",
        "--dev",
        action="store_true",
        default=True,
        help="Runs dev mode",
        
    )
    parser.add_argument(
        "-nw",
        "--no-workers",
        action="store_true",
        default=False,
        help="Runs no workers",
    )
    parser.add_argument("--database", default="database.db", help="Path to database")
    parser.add_argument(
        "--echo-sql",
        action="store_true",
        help="Print SQL queries to stdout",
    )
    parser.add_argument("-w", "--workers", default=os.cpu_count() or 1, type=int)

    args = parser.parse_args(sys.argv[1:])
    use_workers = not args.no_workers # type: ignore
    worker_count = args.workers # type: ignore
    dev_mode = args.dev # type: ignore
    
    db.set_sqlite_path(args.database) # type: ignore
    db.set_echo(args.echo_sql) # type: ignore

    config = uvicorn.Config(
        "launcher:app", port=args.port, host=args.host, access_log=True, reload=dev_mode # type: ignore
    )

    server = uvicorn.Server(config)

    if use_workers:
        config.workers = worker_count
        sock = config.bind_socket()

        runner = Multiprocess(config, target=server.run, sockets=[sock])
    else:
        runner = server

    runner.run()

