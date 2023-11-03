import click


@click.command()
@click.option("--pub_key", help="--help")
def test_click(pub_key):
    if pub_key:
        click.echo(click.style(f"USE PUB_KEY:{pub_key}", fg="green"))


if __name__ == '__main__':
    test_click()

