
from .models import Personal

def activapersonal(id_personal, fechaalta, fechabaja):
    persona = Personal.objects.get(pk=id_personal)

    if fechaalta:
        persona.activo = True
    
    if fechabaja:
        persona.activo = False
    
    persona.save()
