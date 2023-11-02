import funcs
import argparse
import inspect


parser = argparse.ArgumentParser(
    description="coki es una CLI para consultar precios en cocos"
)
parser.add_argument("ticker", help="Ticker a consultar")
parser.add_argument(
    "--currency",
    "-C",
    help="Moneda del ticker. Por default lo infiere de la última letra del Ticker (pero va a fallar en casos como AMD)",
    default="auto",
)

parser.add_argument("--plazo", "-P", help="Plazo de la operación", default=48)

parser.add_argument(
    "--refresh",
    "-R",
    help="Intervalo de actualización de los precios (en segundos)",
    default=30,
)


args = parser.parse_args()

ticker = args.ticker.upper()
currency = args.currency.upper()

funcs.screener(ticker, currency, args.plazo, args.refresh)
