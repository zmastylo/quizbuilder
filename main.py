"""Main module."""

import os

import click
import uvicorn

from core.config import get_config


@click.command()
@click.option(
    "--env",
    type=click.Choice(["local", "dev", "prod"], case_sensitive=False),
    default="local",
)
@click.option(
    "--debug",
    type=click.BOOL,
    is_flag=True,
    default=False,
)
def main(env: str = "local", debug: bool = False):
    """The main method."""

    os.environ["ENV"] = env
    os.environ["DEBUG"] = str(debug)

    config = get_config()

    reload = config.ENV != "production"
    uvicorn.run(
        app="app.server:app", host=config.APP_HOST, port=config.APP_PORT, reload=reload
    )


if __name__ == "__main__":
    main()
