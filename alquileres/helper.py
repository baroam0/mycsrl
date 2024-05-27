
from datetime import datetime
from types import CodeType

from .models import Contrato, CuotaContrato

def grabarpagocuotacontrato(id_cuotacontrato):
    cuotacontrato = CuotaContrato.objects.get(pk=id_cuotacontrato)
    cuotacontrato.pagado = True
    cuotacontrato.save()

    return True


#def generar_tuplas_meses_anos(inicio_mes, inicio_ano, final_mes, final_ano, contrato, usuario):
def generarcuotas(contrato, usuario):
    
    # Crear la lista de tuplas
    tuplas_meses_anos = []
    #mes_actual, ano_actual = inicio_mes, inicio_ano
    mes_actual, ano_actual = contrato.mes_inicio, contrato.anio_inicio

    while (ano_actual, mes_actual) <= (contrato.anio_fin, contrato.mes_fin):
        tuplas_meses_anos.append((mes_actual, ano_actual))

        # Avanzar al siguiente mes
        mes_actual += 1
        if mes_actual > 12:
            mes_actual = 1
            ano_actual += 1

    for e in tuplas_meses_anos:
        fecha = datetime.today()

        try:
            consultacouta = CuotaContrato.objects.get(                
                contrato=contrato,
                mes=e[0],
                anio=e[1],
            )

            if consultacouta:
                print("Omite")
            else:
                cuota = CuotaContrato(
                    fecha=fecha, 
                    contrato=contrato,
                    mes=e[0],
                    anio=e[1],
                    pagado=False,
                    usuario=usuario
                    )
                cuota.save()
        except:
            
            cuota = CuotaContrato(
                fecha=fecha, 
                contrato=contrato,
                mes=e[0],
                anio=e[1],
                pagado=False,
                usuario=usuario
            )
            cuota.save()
            
        