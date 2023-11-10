
def formateafecha(parametro):
    if "/" in parametro:
        parametro = parametro.split("/")
    else:
        parametro = parametro.split("-")
    
    fechaformateada = parametro[2] + "-" + parametro[1] + "-" + parametro[0]

    return fechaformateada


