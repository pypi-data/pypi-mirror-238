import click

from testios import __version__
from testios.scaffold import create_scaffold


@click.command()
def create():
    name = input("please input project name: ")
    if not name:
        print("input empty, use default name: my_project")
        name = "my_project"
    create_scaffold(name)


@click.group()
@click.version_option(version=__version__, help="Show version.")
# 老是变，等最后定下来再搞，目前也没啥用
def main():
    pass


main.add_command(create)
