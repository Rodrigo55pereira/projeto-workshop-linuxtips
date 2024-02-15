import typer
from rich.console import Console
from rich.table import Table
from sqlmodel import Session, select
from .config import settings
from .db import engine
from .models import User, Post, SQLModel
from pamps.security import get_password_hash

main = typer.Typer(name="Pamps CLI")

@main.command()
def shell():
    """Pamps Shell"""
    _vars = {
        "settings": settings,
        "engine": engine,
        "select": select,
        "session": Session(engine),
        "User": User,
        "Post": Post,
    }
    typer.echo(f"Auto imports: {list(_vars.keys())}")
    try:
        from IPython import start_ipython
        start_ipython(
        argv=["--ipython-dir=/tmp", "--no-banner"], user_ns=_vars
        )
    except ImportError:
        import code
        code.InteractiveConsole(_vars).interact()

@main.command()
def user_list():
    """Lista todos os usuários"""
    table = Table(title="Pamps users")
    fields = ["username", "email"]

    for header in fields:
        table.add_column(header, style="magenta")
    with Session(engine) as session:
        users = session.exec(select(User))
        for user in users:
            table.add_row(user.username, user.email)
    Console().print(table)

@main.command()
def create_user(email: str, username: str, password: str):
    """ Cria usuário """
    with Session(engine) as session:
        password_hash = get_password_hash(password)
        user = User(email=email, username=username, password=password_hash)
        session.add(user)
        session.commit()
        session.refresh(user)
        typer.echo(f"criando o usuário {username}")
        return user

@main.command()
def reset_db(
   force: bool = typer.Option(
       False, "--force",
       "-f",
       help="Executar sem confirmação"
   ) 
):
    """Redefine as tabelas do banco de dados"""
    force = force or typer.confirm("Tem certeza?")
    if force:
        SQLModel.metadata.drop_all(engine)