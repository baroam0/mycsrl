
import decimal

import time

from locale import dcgettext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum, Func, ExpressionWrapper, DecimalField, Count

from django.db.models.functions import Round

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse
from contratistas.models import Contratista

from lib.funcionesfechas import formateafecha, formateafechaestandar
from devengamientos.models import Devengamiento
from empresas.models import Empresa
from pagos.models import Obra, Proveedor, ProveedorBanco
from facturas.models import FacturaProveedor, DetalleFacturaProveedor
from facturacion.models import Facturacion, DetalleFacturacion
from presupuestos.models import Presupuesto, DetallePresupuesto


@login_required(login_url='/login')
def home(request):
    return render(request, 'base.html')


def loginusuario(request):
    if request.POST:
        acceso = authenticate(
            username=request.POST['input-usuario'],
            password=request.POST['input-clave']
        )

        if acceso is not None:
            login(request, acceso)
            return redirect('/')
        else:
            mensaje = "Usuario o Clave invalida"
            return render(
                request,
                'login.html',
                {
                    'mensaje': mensaje,
                })
    else:
        return render(request, 'login.html')


def salir(request):
    logout(request)
    return redirect('/login')


def ajaxcomprobanteproveedor(request, idproveedor):
    proveedor = Proveedor.objects.get(pk=idproveedor)
    comprobantes =FacturaProveedor.objects.filter(proveedor=proveedor)
    data = [{"id": c.pk, "text": c.comprobante} for c in comprobantes]
    return JsonResponse(data, safe=False)


def ajaxbancoproveedor(request, pk):
    proveedor = FacturaProveedor.objects.get(pk=pk)
    bancos = ProveedorBanco.objects.filter(proveedor=proveedor.proveedor)
    data = [{"id": b.pk, "text": b.descripcionbanco} for b in bancos]
    return JsonResponse(data, safe=False)


def ajaxproveedor(request, pk):
    proveedor = Proveedor.objects.get(pk=pk)
    bancos = ProveedorBanco.objects.filter(proveedor=proveedor)
    data = [{"id": b.pk, "text": b.descripcionbanco} for b in bancos]
    return JsonResponse(data, safe=False)


def reporteporfactura(request):    
    proveedores = FacturaProveedor.objects.all()
    return render(
        request, 
        'reporte.html',
        {
            "proveedores": proveedores,
        }
    )


def detallereporteporfactura(request):
    
    fechadesde = formateafechaestandar(request.GET.get("id_fechadesde"))
    fechahasta = formateafechaestandar(request.GET.get("id_fechahasta"))
    
    #facturaproveedor = FacturaProveedor.objects.filter(pagado=False,proveedor=proveedor)
    facturaproveedor = FacturaProveedor.objects.get(pk=request.GET.get("id_proveedor"))
    proveedor =  Proveedor.objects.get(pk=facturaproveedor.proveedor.pk)
    #detallefacturaproveedor = DetalleFacturaProveedor.objects.filter(factura__in = facturaproveedor).order_by("obra__descripcion")
    detallefacturaproveedor = DetalleFacturaProveedor.objects.filter(factura=facturaproveedor).order_by('-obra')
    
    #banco = ProveedorBanco.objects.filter(proveedor=proveedor.pk)
    proveedorbanco = ProveedorBanco.objects.filter(pk=request.GET.get("id_banco"))
    banco = proveedorbanco
    datadict= dict()

    obraslist = list()
    for df in detallefacturaproveedor:
        obraslist.append(df.obra.pk)
    obraslist = list(set(obraslist))
    obras = Obra.objects.filter(pk__in=obraslist, finalizada=False)

    empresaslist = list()
    for df in detallefacturaproveedor:
        empresaslist.append(df.obra.empresa.pk)
    empresaslist = list(set(empresaslist))
    empresas = Empresa.objects.filter(pk__in=empresaslist)

    datadict[proveedor.razonsocial] = list()

    for e in empresas:
        datadict[proveedor.razonsocial].append(
            {
                "empresa": e.descripcion,
                "data": list()
            }
        )

    for d in datadict[proveedor.razonsocial]:
        for o in obras:
            if o.empresa.descripcion == d["empresa"]:
                d["data"].append({
                    "obra": o.descripcion,
                    "data": list()
                })
 
    for d in datadict[proveedor.razonsocial]:
        for df in detallefacturaproveedor:
            if df.obra.empresa.descripcion == d["empresa"]:              
                for e in d["data"]:
                    if df.obra.descripcion == e["obra"]:
                        indice =  d["data"].index(e)
                        d["data"][indice]["data"].append({
                            "fecha": df.factura.fecha,
                            "comprobante" : df.factura.comprobante,
                            "detalle": df.descripciondetalle.descripciondetalle,
                            "cantidad": df.cantidad,
                            "preciofinal": round(df.getpreciounitariofinal(),2),
                            "total": df.getpreciofinaltotalitem()
                        })

    
    dicttotales = list()
  
    for o in obras:
        for df in detallefacturaproveedor:
            
            if o.descripcion == df.obra.descripcion:
                dicttotales.append({
                    "obra": o.descripcion,
                    "empresa": o.empresa.descripcion,
                    #"total": round(gettotalobra(o.descripcion, df.factura.pk),2)
                    "total": df.modeltotalobra(o.pk, df.factura.pk)
                })
            

    dicttotales = list(
        {
            dictionary['obra']: dictionary
            for dictionary in dicttotales
        }.values()
    )

    dicttotalempresa = list()

    for e in empresas:
        dicttotalempresa.append(
            {
                "empresa": e.descripcion,
                "total": 0
            }
        )

    for d in dicttotalempresa:
        for e in dicttotales:
            if e["empresa"] == d["empresa"]:
                d["total"] =  d["total"] + e["total"]
                d["total"] =  round(d["total"],2)

    return render(
        request, 
        'detallereporte.html',
        {
            "fechadesde": fechadesde,
            "fechahasta": fechahasta,
            "datadict": datadict,
            "dictotales": dicttotales,
            "dicttotalempresa": dicttotalempresa,
            "banco": banco,
            "facturaproveedor": facturaproveedor
        }
    ) 


def reportesfacturas(request):
    proveedores = Proveedor.objects.all()
    return render(
        request, 
        'reportes/reportesfacturas.html',
        {
            "proveedores": proveedores,
        }
    )


def gettotalobra(obra, factura):
        obra = Obra.objects.get(descripcion=obra)
        factura = FacturaProveedor.objects.filter(pk__in=factura)
        detalles = DetalleFacturaProveedor.objects.filter(obra=obra, factura__in=factura, factura__pagado=False)
        total = 0
        
        for d in detalles:
            total = total + d.getpreciofinaltotalitem()
        
        return round(total,4)


def gettotalempresa(proveedor, empresa, fechadesde, fechahasta):
        proveedor = Proveedor.objects.get(pk=proveedor)
        empresa = Empresa.objects.get(descripcion=empresa)
        obra = Obra.objects.filter(empresa=empresa, finalizada=False)

        facturaproveedor = FacturaProveedor.objects.filter(
            pagado=False,
            proveedor=proveedor,fecha__range=(fechadesde, fechahasta)
        )

        detalles = DetalleFacturaProveedor.objects.filter(factura__in=facturaproveedor, obra__in=obra)
        total = 0
        redondeo = 0
        for d in detalles:
            total = total + round(d.getpreciototalfinal(),2)
            redondeo = redondeo + float(d.factura.ajusteglobal)
        return float(round(total,4))


def detallereportesporfacturas(request):
    fechadesde = formateafecha(request.GET.get("fechadesde"))
    fechahasta = formateafecha(request.GET.get("fechahasta"))

    fechadesdetemplate = formateafechaestandar(request.GET.get("fechadesde"))
    fechahastatemplate = formateafechaestandar(request.GET.get("fechahasta"))

    proveedor =  Proveedor.objects.get(pk=request.GET.get("id_proveedor"))
    facturaproveedor = FacturaProveedor.objects.filter(pagado=False,proveedor=proveedor,fecha__range=(fechadesde, fechahasta))
    detallefacturaproveedor = DetalleFacturaProveedor.objects.filter(factura__in = facturaproveedor).order_by("obra__descripcion")
    banco = ProveedorBanco.objects.filter(proveedor=proveedor.pk)
    datadict= dict()

    obraslist = list()
    for df in detallefacturaproveedor:
        obraslist.append(df.obra.pk)
    obraslist = list(set(obraslist))
    obras = Obra.objects.filter(pk__in=obraslist, finalizada=False)

    empresaslist = list()
    for df in detallefacturaproveedor:
        empresaslist.append(df.obra.empresa.pk)
    empresaslist = list(set(empresaslist))
    empresas = Empresa.objects.filter(pk__in=empresaslist)

    datadict[proveedor.razonsocial] = list()

    for e in empresas:
        datadict[proveedor.razonsocial].append(
            {
                "empresa": e.descripcion,
                "data": list()
            }
        )
    
    for d in datadict[proveedor.razonsocial]:
        for o in obras:
            if o.empresa.descripcion == d["empresa"]:
                d["data"].append({
                    "obra": o.descripcion,
                    "data": list()
                })
 
    for d in datadict[proveedor.razonsocial]:
        for df in detallefacturaproveedor:
            if df.obra.empresa.descripcion == d["empresa"]:              
                for e in d["data"]:
                    if df.obra.descripcion == e["obra"]:
                        indice =  d["data"].index(e)
                        d["data"][indice]["data"].append({
                            "fecha": df.factura.fecha,
                            "comprobante" : df.factura.comprobante,
                            "detalle": df.descripciondetalle.descripciondetalle,
                            "cantidad": df.cantidad,
                            "preciofinal": format(df.getpreciounitariofinal(),'.2f'),
                            "total": format(df.getpreciofinaltotalitem(),'.2f') 
                        })

    
    dicttotales = list()
  
    for o in obras:
        for df in detallefacturaproveedor:
            if o.descripcion == df.obra.descripcion:
                dicttotales.append({
                    "obra": o.descripcion,
                    "empresa": o.empresa.descripcion,
                    "total": df.modeltotalobra(o.pk, df.factura.pk)
                })

    dicttotales = list(
        {
            dictionary['obra']: dictionary
            for dictionary in dicttotales
        }.values()
    )

    lsttotaobra = list()

    for o in obras:
        lsttotaobra.append({
            "idobra": o.pk,
            "obra": o.descripcion,
            "idempresa": o.empresa.pk,
            "empresa": o.empresa.descripcion,
            "total": 0
        })
    
    dicttotalempresa = list()

    inicio = time.time()

    for e in lsttotaobra:
        for df in detallefacturaproveedor:
            if e["obra"] == df.obra.descripcion:
                e["total"] = gettotalobra(df.obra.descripcion, facturaproveedor)

    fin = time.time()
    tiempo_ejecucion = fin - inicio
    print(f"Tiempo de ejecución: {tiempo_ejecucion:.6f} segundos")
    
    for e in empresas:
        dicttotalempresa.append(
            {
                "empresa": e.descripcion,
                "total": 0
            }
        )

    for d in dicttotalempresa:
        for e in lsttotaobra:
            if e["empresa"] == d["empresa"]:
                d["total"] = d["total"] + e["total"]
                d["total"] = round(d["total"],2)


    return render(
        request, 
        'reportes/detallereportesfacturas.html',
        {
            "fechadesde": fechadesdetemplate,
            "fechahasta": fechahastatemplate,
            "datadict": datadict,
            "dictotales": dicttotales,
            "dicttotalempresa": dicttotalempresa,
            "banco": banco,
            "lstobra": lsttotaobra
        }
    )


def reporteingresoegresoobra(request):    
    obras = Obra.objects.all()

    return render(
        request, 
        'reporteingresoegresoobra.html',
        {
            "obras": obras,
        }
    )


def detallereporteingresoegresoobra(request):

    obra = Obra.objects.get(pk=request.GET.get("id_obra"))

    cobros = Facturacion.objects.filter(obra=obra)

    try:
        total_cobros = cobros[0].totalfacturacionporobra(obra.pk)
    except:
        total_cobros = 0


    devengamientos = (
        DetalleFacturaProveedor.objects
        .filter(obra=obra.pk)
        .values('rubro__descripcion')
        .annotate(
            sum_custom_method=Sum(
                ExpressionWrapper(
                    F('preciototal') -
                    F('preciototal') * F('descuentoporcentaje') / 100 +
                    F('preciototal') * F('iva__retencion') / 100 +
                    F('preciototal') * F('ingresosbrutos__retencion') / 100,
                    output_field=DecimalField()
                )
            )
        )
    )

    total_egresos = 0

    for r in devengamientos:
        if r['sum_custom_method']:
            total_egresos = total_egresos + r['sum_custom_method']
            r['sum_custom_method'] = round(r['sum_custom_method'],2)
        else:
            valor = 0
            total_egresos = total_egresos + valor
            #r['sum_custom_method'] = round(r['sum_custom_method'],2)

    saldo = total_cobros - total_egresos
    return render(
        request, 
        'detallereporteingresoegresoobra.html',
        {
            "obras": obra,
            "cobros": cobros,
            "devengamientos": devengamientos,
            "totalpagos": round(total_egresos,2),
            "totalcobros": round(total_cobros,2),
            "saldo": round(saldo,2)
        }
    )


def helperpagado(factura_id, usuario):
    factura = FacturaProveedor.objects.get(pk=factura_id)
    devengamientos = Devengamiento.objects.filter(factura=factura)
    detallefacturas = DetalleFacturaProveedor.objects.filter(factura=factura)
    devengamientos = Devengamiento.objects.filter(factura=factura)

    totaldevengado = 0
    for i in devengamientos:
        totaldevengado = totaldevengado + i.monto

    totalfactura = factura.gettotalfactura()

    totaldevengado = float(round(totaldevengado, 2))
    totalfactura = float(round(totalfactura, 2))


    if totalfactura == totaldevengado:
        factura.pagado = True
        factura.pagoparcial = True
        factura.usuario
        factura.save()

    if totalfactura > totaldevengado:
        if totaldevengado == 0:
            factura.pagoparcial = False
            factura.pagado = False
            factura.usuario
            factura.save()
        else:
            factura.pagoparcial = True
            factura.pagado = False
            factura.usuario
            factura.save()
        
    return True


def reportegastoporobra(request):    
    obras = Obra.objects.all()

    return render(
        request, 
        'reportes/reportegastoporobra.html',
        {
            "obras": obras,
        }
    )


def detallereportesgastosporobra(request):
    """Funcion para reporte de gastos por facturas"""

    obra = Obra.objects.get(pk=request.GET.get("id_obra"))
    detallesfacturas = DetalleFacturaProveedor.objects.filter(obra=obra).order_by('rubro')
    presupuesto = Presupuesto.objects.get(obra=obra)
    detallespresupuestos = DetallePresupuesto.objects.filter(presupuesto=presupuesto).order_by('contratista__descripcion')
    totalgasto = 0

    facturas = FacturaProveedor.objects.filter(pk__in=detallesfacturas)

    descuento = 0
    ajuste = 0

    for i in facturas:
        descuento = descuento + i.descuentoglobal
        ajuste = ajuste + i.ajusteglobal

    list_rubros = list()
    for df in detallesfacturas:
        totalgasto = totalgasto + df.getpreciofinaltotalitem()
        list_rubros.append(df.rubro.descripcion)
    totalentregado = 0

    list_rubros = list(set(list_rubros))
    
    dict_master = dict()
    dict_subtotales = dict()
    for e in list_rubros:
        dict_master[e] = list()
        dict_subtotales[e] = 0

    for d in dict_master:
        for df in detallesfacturas:
            if d == df.rubro.descripcion:
                tmplist = dict()
                tmplist["fecha"] = df.factura.fecha.strftime("%d-%m-%Y")
                tmplist["razonsocial"] = df.factura.proveedor.razonsocial.upper()
                tmplist["comprobante"] = df.factura.comprobante
                tmplist["descripciondetalle"] = df.descripciondetalle.descripciondetalle.upper()
                tmplist["cantidad"] = df.cantidad
                tmplist["preciounitario"] = round(df.getpreciounitario(),2)
                tmplist["preciofinal"] = round(df.getpreciounitariofinal(),2)
                tmplist["preciototal"] = round(df.getpreciofinaltotalitem(),2)
                if df.factura.pagado:
                    tmplist["pagado"] = "SI"
                else:
                    tmplist["pagado"] = "NO"
                dict_master[d].append(tmplist)
                dict_subtotales[d] = round(dict_subtotales[d],2) + round(df.getpreciofinaltotalitem(),2)
                tmplist = dict()

    for d in dict_subtotales:
        dict_subtotales[d] = round(dict_subtotales[d],2)

    list_contratistas = list()
    for dp in detallespresupuestos:
        list_contratistas.append(dp.contratista.descripcion)

    list_contratistas = list(set(list_contratistas))
    dict_contratistas = dict()
    dict_subtotales_contratistas = dict()
    for l in list_contratistas:
        dict_contratistas[l] = list()
        dict_subtotales_contratistas[l] = 0

    for c in dict_contratistas:
        for dp in detallespresupuestos:
            if c == dp.contratista.descripcion:
                tmplist = dict()
                tmplist["fecha"] = dp.fecha.strftime("%d-%m-%Y")
                tmplist["descripcion"] = c
                tmplist["motivo"] = dp.descripcion
                tmplist["monto"] = dp.entregado
                totalentregado = totalentregado + dp.entregado
                dict_contratistas[c].append(tmplist)
                dict_subtotales_contratistas[c] = round(dict_subtotales_contratistas[c],2) + round(tmplist["monto"],2)
                tmplist = dict()
    
    print(dict_subtotales_contratistas)

    total = float(totalgasto) + float(totalentregado)


    return render(
        request, 
        'reportes/detallereportegastoporobra.html',  
        { 
            "dictmaster": dict_master,
            "dictcontratistas": dict_contratistas,
            "dictsubtotalescontratistas":dict_subtotales_contratistas,
            "obra": obra,
            "detallesfacturas": detallesfacturas,
            "totalgasto": round(totalgasto,4),
            "totalentregado": totalentregado,
            "subtotales": dict_subtotales,
            "total": round(total,2)
        }
    )


def reportecontratista(request):
    obras = Obra.objects.all()
    return render(
        request, 
        'reportes/reportecontratistas.html',
        {
            "obras": obras,
        }
    )


def dictbuilder(contratista_id, obra_id):
    contratista = Contratista.objects.get(pk=contratista_id)
    obra = Obra.objects.get(pk=obra_id)
    presupuesto = Presupuesto.objects.get(obra=obra.pk)

    if presupuesto:
        detallepresupuesto = (DetallePresupuesto.objects
                              .filter(contratista=contratista.pk, presupuesto=presupuesto.pk)
                              .order_by("contratista__descripcion")
                              )

        totalimporte = 0
        totalentregado = 0
        saldo = 0
        for d in detallepresupuesto:
            totalimporte = totalimporte + d.importe
            totalentregado = totalentregado + d.entregado
        
        saldo = totalimporte - totalentregado

        result = dict()
        for d in detallepresupuesto:
            valor = d.getsaldocontratistaexcluyente(d.contratista.pk, d.presupuesto.obra.pk)
            if valor != 0:
                tmpdict = {
                    "codigo": obra.pk,
                    "obra": obra.descripcion,
                    "importe": totalimporte,
                    "entregado": totalentregado,
                    "saldo": saldo
                }
                result = tmpdict
    else:
        result = None
    return result


def totalescontratistas(contratista_id):
    contratista = Contratista.objects.get(pk=contratista_id)
    detallespresupuestos = DetallePresupuesto.objects.filter(contratista=contratista.pk)
    totales = {}
    totalimporte = 0
    totalentregado = 0
    saldo = 0

    for d in detallespresupuestos:
        valor = d.getsaldocontratistaexcluyente(contratista.pk, d.presupuesto.obra.pk)
        if valor != 0:
            totalimporte = totalimporte + d.importe
            totalentregado = totalentregado + d.entregado
    
    saldo = float(totalimporte) - float(totalentregado)

    totales["totalimporte"] = totalimporte
    totales["totalentregado"] = totalentregado
    totales["totalsaldo"] = format(saldo, '.2f')
    return totales


def detallereportecontratista(request):

    presupuestos = Presupuesto.objects.filter(cerrado=False)
    detallepresupuestos = DetallePresupuesto.objects.filter(presupuesto__in=presupuestos)
    
    obralist = list()

    contratistalist = list()

    for d in detallepresupuestos:
        obralist.append(d.presupuesto.obra.pk)
        contratistalist.append(d.contratista.pk)
    
    obralist = list(set(obralist))
    obras = Obra.objects.filter(pk__in=obralist)
    contratistalist = list(set(contratistalist))

    contratistas = Contratista.objects.filter(pk__in=contratistalist)

    datalist = dict()

    for c in contratistas:
        datalist[c.descripcion] = list()
        for o in obras:
            data = dictbuilder(c.pk, o.pk)
            datalist[c.descripcion].append(data)
        totales = totalescontratistas(c.pk)
        datalist[c.descripcion].append(totales)

    
    return render(
        request, 
        'reportes/detallereportecontratista.html',
        {         
            "result": datalist
        }
    )


def reporteingresoobra(request):
    obras = Obra.objects.all()
    return render(
        request, 
        'reportes/reporte_ingreso_obra.html',
        {
            "obras": obras,
        }
    )


def detallereporteingresoobra(request):
    """Funcion para reporte de gastos por facturas"""

    obra = Obra.objects.get(pk=request.GET.get("id_obra"))
    texto = request.GET.get("id_texto")

    try:
        resultados = Facturacion.objects.filter(obra=obra)
        total = resultados[0].totalfacturacionporobra(obra.pk)
    except:
        resultados = None
        total = None

    return render(
        request, 
        'reportes/detalleingresoporobra.html',
        {
            "obra": obra,
            "resultados": resultados,
            "texto": texto,
            "total": total
        }
    )   


def reporteegresoobra(request):
    obras = Obra.objects.all()
    return render(
        request, 
        'reportes/reporte_egreso_obra.html',
        {
            "obras": obras,
        }
    )


def detallereporteegresoobra(request):
    """Funcion para reporte de egreso por obra agrupado por rubro """

    obra = Obra.objects.get(pk=request.GET.get("id_obra"))
    texto = request.GET.get("id_texto")

    try:

        resultados = (
            DetalleFacturaProveedor.objects
            .filter(obra=obra.pk)
            .values('rubro__descripcion')
            .annotate(
                sum_custom_method=Sum(
                    ExpressionWrapper(
                        F('preciototal') - 
                        F('preciototal') * F('descuentoporcentaje') / 100 + 
                        F('preciototal') * F('iva__retencion') / 100 +
                        F('preciototal') * F('ingresosbrutos__retencion') / 100 +
                        F('factura__ajusteglobal'),
                        output_field=DecimalField()
                    )
                )
            )
        )
        total_egresos = 0

        for r in resultados:
            total_egresos = float(total_egresos) + float(r['sum_custom_method'])
            r['sum_custom_method'] = round(r['sum_custom_method'],2)
    except:
        resultados = None
    
    return render(
        request, 
        'reportes/detalleegresoporobra.html',
        {
            "obra": obra,
            "resultados": resultados,
            "texto": texto,
            "total_egresos": round(total_egresos,2)
        }
    )


def reporteobrasactivas(request):
    resultados = Obra.objects.filter(finalizada=False)

    return render(
        request, 
        'reportes/reporte_obras_activas.html',
        {
            "resultados": resultados
        }
    )


def reporteprespuestogeneral(request):

    datadict = dict()
    totalesgenerales = dict()
    #excludes = [True, None]
    obra = Obra.objects.filter(finalizada=False)

    presupuestos = Presupuesto.objects.filter(obra__in=obra, cerrado=False)
    
    detallepresupuestos = (
        DetallePresupuesto.objects.filter(presupuesto__in=presupuestos)
        .values(
            "presupuesto__obra__pk", 
            "presupuesto__obra__finalizada",
            "presupuesto__obra__descripcion", 
            "contratista__pk",
            "contratista__descripcion",
            "presupuesto__pk",
        )
        .annotate(
            totalimporte=Sum('importe'),
            totalentregado=Sum("entregado"),
            saldogeneral=F("totalimporte") - F("totalentregado"),
        )
        .order_by(
            "contratista__pk"
        )
    )

    array_contratista = list()

    for d in detallepresupuestos:
        array_contratista.append(d["contratista__pk"])
    
    array_contratista = list(set(array_contratista))

    contratistas = Contratista.objects.filter(pk__in=array_contratista).order_by("descripcion")

    for c in contratistas:
        datadict[c.descripcion] = list()
        totalesgenerales[c.descripcion] = list()
    
    for d in detallepresupuestos:
        datadict[d['contratista__descripcion']].append(
            {
                "presupuesto__obra__pk": d["presupuesto__obra__pk"],
                "presupuesto__obra__descripcion": d["presupuesto__obra__descripcion"],
                "presupuesto__pk": d["presupuesto__pk"],
                "totalimporte": round(d["totalimporte"],2),
                "totalentregado": round(d["totalentregado"],2),
                "saldogeneral": round(d["saldogeneral"],2),
            }
            
        )
    
    sumatoria_saldogeneral = dict()

    for clave, entradas in datadict.items():
        total_importe = sum(entry['totalimporte'] for entry in entradas)
        total_entregado = sum(entry['totalentregado'] for entry in entradas)
        total_saldogeneral = sum(entry['saldogeneral'] for entry in entradas)
        sumatoria_saldogeneral[clave] = {
            "total_importe": total_importe,
            "total_entregado": total_entregado,
            "total_saldogeneral": total_saldogeneral
        }

    return render(
        request, 
        'reportes/reporte_presupuesto_general.html',
        {
             "presupuestos": datadict,
             "totales": sumatoria_saldogeneral
        }
    )


def reporteprespuestoindividual(request):

    presupuestos = (DetallePresupuesto.objects
        .values('pk','presupuesto__obra__descripcion', 'contratista__descripcion')
        .annotate(dcount=Count('presupuesto__obra__descripcion'))
        .order_by()
    )

    return render(
        request, 
        'reportes/reporte_presupuesto_individual.html',
        {
            "presupuestos": presupuestos,
        }
    )


def reportedetalleprespuestoindividual(request):
    detallepresupuesto  = DetallePresupuesto.objects.get(pk=request.GET.get("id"))
    contratista = Contratista.objects.get(pk=detallepresupuesto.contratista.pk)
    presupuesto = Presupuesto.objects.get(pk=detallepresupuesto.presupuesto.pk)

    detallespresupuestos = DetallePresupuesto.objects.filter(
        presupuesto=presupuesto.pk, contratista=contratista
    )

    montoimporte = 0
    montoentregado = 0

    for d in detallespresupuestos:
        montoimporte = montoimporte + d.importe
        montoentregado = montoentregado + d.entregado

    return render(
        request, 
        'reportes/detallereportepresupuesto.html',
        {
            "contratista": contratista,
            "detallespresupuestos": detallespresupuestos,
            "presupuesto": presupuesto,
            "montoimporte": montoimporte,
            "montoentregado" : montoentregado
        }
    )
