DEBUG = True
SECRET_KEY = 'django-insecure-=!%dlpgnc+4mk7+2h!l4&x^3)r+q4+=nz@y3k&e)8gg^gtgqkn'

LOGGING['formatters']['colored'] = {  # type: ignore
    '()': 'colorlog.ColoredFormatter',
    'format': '%(log_color)s%(asctime)s %(levelname)s %(name)s %(bold_white)s%(message)s',
}
LOGGING['loggers']['cooking_core']['level'] = 'DEBUG'  # type: ignore
LOGGING['handlers']['console']['level'] = 'DEBUG'  # type: ignore
LOGGING['handlers']['console']['formatter'] = 'colored'  # type: ignore
