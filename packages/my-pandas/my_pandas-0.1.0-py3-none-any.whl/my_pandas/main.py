import typer


app = typer.Typer()


@app.command()
def create():
    print("Creating a user")


@app.command()
def delete():
    print("Deleting a user")


if __name__ == "__main__":
    app()