import funcs
import argparse
import inspect


def get_default_args(func):
    signature = inspect.signature(func)
    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    }


defaults = get_default_args(funcs.gen_credentials)

parser = argparse.ArgumentParser(
    description="Herramienta para generar credenciales para Coki"
)
parser.add_argument(
    "user", help="Email de la cuenta de Cocos (en la app nueva, no de la página vieja)"
)
parser.add_argument(
    "password",
    help="Clave de la cuenta de Cocos (en la app nueva, no de la página vieja)",
)
parser.add_argument(
    "--key",
    help="Clave de encriptación de las credenciales. Tiene que ser compatible con cryptography.fernet.Fernet (no esta implementado)",
    default=defaults["key"],
)
parser.add_argument(
    "--path",
    help="Ruta para almacenar los datos encriptados. Por defecto quedan en coki_credentials.txt en la misma carpeta que se encuentra coki (no esta implementado)",
    default=defaults["path"],
)

args = parser.parse_args()

funcs.gen_credentials(args.user, args.password, args.key, args.path)

print("Credenciales generadas!")
