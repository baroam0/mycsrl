
from locale import dcgettext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse
from contratistas.models import Contratista

from lib.funcionesfechas import formateafecha
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
    facturaproveedor = FacturaProveedor.objects.get(pk=request.GET.get("id_proveedor"))
    detallefacturaproveedor = DetalleFacturaProveedor.objects.filter(factura=facturaproveedor).order_by('-obra')
    proveedorbanco = ProveedorBanco.objects.filter(pk=request.GET.get("id_banco"))
    
    return render(
        request, 
        'detallereporte.html',
        {
            "facturaproveedor": facturaproveedor,
            "detallefacturaproveedor": detallefacturaproveedor,
            "banco": proveedorbanco
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


def gettotalobra(obra):
        obra = Obra.objects.get(descripcion=obra)
        detalles = DetalleFacturaProveedor.objects.filter(obra=obra, factura__pagado=False)
        total = 0
        redondeo = 0
        for d in detalles:
            total = total + d.getpreciototalfinal()
            redondeo = float(d.factura.ajusteglobal)
        total = total + redondeo
        
        return float(round(total,4))


def gettotalempresa(proveedor, empresa, fechadesde, fechahasta):
        proveedor = Proveedor.objects.get(pk=proveedor)
        empresa = Empresa.objects.get(descripcion=empresa)
        obra = Obra.objects.filter(empresa=empresa)

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
    proveedor =  Proveedor.objects.get(pk=request.GET.get("id_proveedor"))
    facturaproveedor = FacturaProveedor.objects.filter(pagado=False,proveedor=proveedor,fecha__range=(fechadesde, fechahasta))
    detallefacturaproveedor = DetalleFacturaProveedor.objects.filter(factura__in = facturaproveedor).order_by("obra__descripcion")
    datadict= dict()
    tmplist = list()

    obraslist = list()
    for df in detallefacturaproveedor:
        obraslist.append(df.obra.pk)
    obraslist = list(set(obraslist))
    obras = Obra.objects.filter(pk__in=obraslist)

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
                            "preciofinal": df.getpreciounitariofinal(),
                            "total": round(df.getpreciototalfinal(),2),
                        })

    
    dicttotales = list()
    obra = ""
    totalgeneral = 0
    totalobra = 0
  
    for o in obras:
        for df in detallefacturaproveedor:
            if o.descripcion == df.obra.descripcion:
                dicttotales.append({
                    "obra": o.descripcion,
                    "empresa": o.empresa.descripcion,
                    "total": round(gettotalobra(o.descripcion),2)
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

    """
    for d in dicttotalempresa:
        d["total"] = gettotalempresa(proveedor.pk, d["empresa"], fechadesde, fechahasta)
    """
    totalempresa = 0

    for d in dicttotalempresa:
        for e in dicttotales:
            if e["empresa"] == d["empresa"]:
                print(e)
                print(d)
                d["total"] =  d["total"] + e["total"]
                



    return render(
        request, 
        'reportes/detallereportesfacturas.html',
        {
            "fechadesde": fechadesde,
            "fechahasta": fechahasta,
            "datadict": datadict,
            "dictotales": dicttotales,
            "dicttotalempresa": dicttotalempresa
        }
    )


"""
def detallereportesporfacturas(request):
    Funcion para reporte de facturas por rango de fechas

    fechadesde = formateafecha(request.GET.get("fechadesde"))
    fechahasta = formateafecha(request.GET.get("fechahasta"))
    proveedor =  Proveedor.objects.get(pk=request.GET.get("id_proveedor"))
    facturaproveedor = FacturaProveedor.objects.filter(pagado=False,proveedor=proveedor,fecha__range=(fechadesde, fechahasta))

    detallefacturaproveedor = DetalleFacturaProveedor.objects.filter(factura__in=facturaproveedor).order_by('-obra')
    proveedorbanco = ProveedorBanco.objects.filter(pk=request.GET.get("id_banco"))

    total = 0
    for d in facturaproveedor:
        total = total + d.gettotalfactura()

    obraslist = list()

    for d in detallefacturaproveedor:
        obraslist.append(d.obra.pk)
    
    obraslist = list(set(obraslist))
    obras = Obra.objects.filter(pk__in=obraslist)
    datadict = dict()

    for o in obras:
        datadict[o.descripcion] = list()
    
    totalgeneral = 0
    itemlist = list()
    tmpdict = dict()

    for d in datadict:
        for df in detallefacturaproveedor:
            if d == df.obra.descripcion:
                tmpdict["fecha"] = str(df.factura.fecha)
                tmpdict["comprobante"] = df.factura.comprobante
                tmpdict["cantidad"] = df.cantidad
                tmpdict["descripcion"] = df.descripciondetalle.descripciondetalle
                tmpdict["preciofinal"] = df.getpreciounitarioiva()
                tmpdict["total"] = df.getpreciounitarioxcantidad()
                itemlist.append(tmpdict)
                datadict[d].append(itemlist) 
                tmpdict = dict()
            itemlist = list()

    dicttotales = dict()

    totalg = 0
    empresa = ""
    for d in datadict:
        for df in detallefacturaproveedor:
            if d == df.obra.descripcion:
                #totalg = totalg + df.getpreciounitarioxcantidad()
                totalg = df.factura.gettotalfactura()
                empresa = df.obra.empresa.descripcion
    
        dicttotales[d] = {"total": totalg, "empresa": empresa}
        totalg = 0
        empresa = ""

    for d in dicttotales:
        totalgeneral = totalgeneral + dicttotales[d]["total"]

    print(dicttotales)
    return render(
        request, 
        'reportes/detallereportesfacturas.html',
        {
            "fechadesde": fechadesde,
            "fechahasta": fechahasta,
            "proveedor": proveedor,
            "facturaproveedor": facturaproveedor,
            "detallefacturaproveedor": detallefacturaproveedor,
            "total": total,
            "banco": proveedorbanco,
            "datadict" : datadict,
            "totalgeneral": totalgeneral,
            "dicttotales": dicttotales
        }
    )
"""

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

    detallesfacturas = DetalleFacturaProveedor.objects.filter(obra=obra.pk)

    detallesfacturas_list = list()
    for i in detallesfacturas:
        detallesfacturas_list.append(i.factura.pk)

    facturas = FacturaProveedor.objects.filter(pk__in=detallesfacturas_list)

    devengamientos = Devengamiento.objects.filter(factura__in=facturas)
    
    cobros = Facturacion.objects.filter(obra=obra.pk)

    totalcobros = 0
    totalpagos = 0
    for i in devengamientos:
        totalpagos = totalpagos + i.monto
    
    if cobros:
        for c in cobros:
            totalcobros = totalcobros +  c.totalfacturacion()
    else:
        totalcobros = 0
    
    saldo = totalcobros - totalpagos

    return render(
        request, 
        'detallereporteingresoegresoobra.html',
        {
            "obras": obra,
            "cobros": cobros,
            "devengamientos": devengamientos,
            "totalpagos": totalpagos,
            "totalcobros": totalcobros,
            "saldo": saldo
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
    detallesfacturas = DetalleFacturaProveedor.objects.filter(obra=obra)

    totalgasto = 0

    facturalist = list()

    for i in detallesfacturas:
        facturalist.append(i.factura.pk)

    facturas = FacturaProveedor.objects.filter(pk__in=facturalist)

    descuento  = 0
    ajuste = 0
    for i in facturas:
        descuento = descuento + i.descuentoglobal
        ajuste = ajuste + i.ajusteglobal


    #totalgasto = obra.getgastoporobra()
        
    for df in detallesfacturas:
        totalgasto = totalgasto + df.getpreciototalfinal()      
    

    #valor = float(totalgasto) - float(descuento) + float(ajuste)
    return render(
        request, 
        'reportes/detallereportegastoporobra.html',
        {
            "obra": obra,
            "detallesfacturas": detallesfacturas,
            "totalgasto": round(totalgasto,4)
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
        totalimporte = totalimporte + d.importe
        totalentregado = totalentregado + d.entregado
    saldo = float(totalimporte) - float(totalentregado)

    totales["totalimporte"] = totalimporte
    totales["totalentregado"] = totalentregado
    totales["totalsaldo"] = saldo
    return totales


def detallereportecontratista(request):

    presupuestos = Presupuesto.objects.filter(cerrado=False)
    detallepresupuestos = DetallePresupuesto.objects.filter(presupuesto__in=presupuestos)
    
    obralist = list()

    for p in presupuestos:
        obralist.append(p.obra.pk)
    
    obralist = list(set(obralist))

    obras = Obra.objects.filter(pk__in=obralist)

    contratistalist = list()

    for d in detallepresupuestos:
        contratistalist.append(d.contratista.pk)
    
    contratistalist = list(set(contratistalist))

    contratistas = Contratista.objects.filter(pk__in=contratistalist)

    datalist = dict()

    """
    for c in contratistas:
        datalist[c.descripcion] = list()
        for d in detallepresupuestos:
            if c.descripcion == d.contratista.descripcion:
                data = dictbuilder(d.contratista.pk, d.presupuesto.obra.pk)
                datalist[c.descripcion].append(data)
    """

    for c in contratistas:
        datalist[c.descripcion] = list()
        for o in obras:
            data = dictbuilder(c.pk, o.pk)
            datalist[c.descripcion].append(data)
        totales = totalescontratistas(c.pk)
        datalist[c.descripcion].append(totales)

    print(datalist)
    return render(
        request, 
        'reportes/detallereportecontratista.html',
        {         
            "result": datalist
        }
    )