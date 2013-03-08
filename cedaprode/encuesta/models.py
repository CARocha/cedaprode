# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

from lugar.models import Municipio

TIPOS_ORG = (
             ('1', 'Alcaldía'), 
             ('2', 'Sociedad civil'),
             ('3', 'Gremios'), 
             ('4', 'Instituciones del estado'), 
             ('5', 'Empresa')
            )

class Organizacion(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=2, choices = TIPOS_ORG)
    descripcion = models.TextField() 
    creado_por = models.ForeignKey(User)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    municipio = models.ForeignKey(Municipio)
    representante = models.CharField('Representante legal', max_length=100)
    celular_repre = models.CharField('Celular', max_length=100, null=True, blank=True)
    correo_repre = models.CharField('Correo', max_length=100, null=True, blank=True)
    gerente = models.CharField(max_length=100, null=True, blank=True)
    celular_gerente = models.CharField('Celular', max_length=100, null=True, blank=True)
    correo_gerente = models.CharField('Correo', max_length=100, null=True, blank=True)
    fecha_fundacion = models.DateField()

    class Meta:
        verbose_name_plural = 'Organizaciones'
        verbose_name = 'Organización'

    def __unicode__(self):
        return self.nombre

   
class Encuesta(models.Model):
    organizacion = models.ForeignKey(Organizacion)
    fecha = models.DateTimeField(auto_now_add = True)
    usuario = models.ForeignKey(User)

    def save(self, *args, **kwargs):
        super(Encuesta, self).save(*args, **kwargs)
        #se registra cada pregunta en la encuesta
        for pregunta in Pregunta.objects.all():
            respuesta = Respuesta(pregunta = pregunta, encuesta = self)
            try:
                respuesta.save()
            except:
                pass

    def __unicode__(self):
        return 'Encuesta a %s con fecha %s' % (self.organizacion.nombre, self.fecha)
    
    def puntaje(self):
        puntos = Respuesta.objects.filter(encuesta = self).aggregate(p=Sum('respuesta__puntaje'))['p']
        if puntos:
            return puntos 
        else:
            return 0

class Adjunto(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    archivo = models.FileField(upload_to="adjuntos")

    def __unicode__(self):
        return "Adjunto para %s" % self.encuesta
 
class Categoria(models.Model):
    '''Categoria principal'''
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()

    class Meta:
        verbose_name_plural = 'Categorías'

    def __unicode__(self):
        return self.titulo

class Pregunta(models.Model):
    categoria = models.ForeignKey(Categoria)
    titulo = models.TextField()

    def __unicode__(self):
        return self.titulo

class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta)
    titulo = models.TextField()
    puntaje = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'Opciones'
        unique_together = ['pregunta', 'puntaje']

    def __unicode__(self):
        return '%s= %s' % (self.puntaje, self.titulo)

class Respuesta(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    pregunta = models.ForeignKey(Pregunta)
    respuesta = models.ForeignKey(Opcion, blank = True, null=True)
    comentario = models.TextField(blank=True, default='')

    class Meta:
        unique_together = ['encuesta', 'pregunta']
        ordering = ['pregunta__categoria']

    def __unicode__(self):
        if self.respuesta:
            return '%s - %s(%s)' % (self.pregunta.titulo, 
                    self.respuesta.titulo, 
                    self.encuesta.usuario.username)
        else:
            return '%s - Sin responder(%s)' % (self.pregunta.titulo, 
                    self.encuesta.usuario.username)

#modelo nuevo para acicafoc
CHOICE_INTEGRADAS = (
                        (1, "Asamblea"),
                        (2, "Junta directiva"),
                        (3, "Junta de vigilancia"),
                        (4, "Comisión de formación"),
                        (5, "Comisión de género"),
                        (6, "Gerencia"),
                        (7, "Empleados")
                    )

CHOICE_FRECUENCIA = (
                        (1, "Semanal"),
                        (2, "Mensual"),
                        (3, "Bimensual"),
                        (4, "Trimestral"),
                        (5, "Semestral"),
                        (6, "Anual")
                    )

CHOICE_INTEGRADAS_FRECUENCIA = (
                        (1, "Sesiones de asamblea"),
                        (2, "Sesiones de junta directiva"),
                        (3, "Sesiones de junta de vigilancia"),
                        (4, "Sesiones de comisión de formación"),
                        (5, "Sesiones de comisión de género")
                    )

class ExtraInformacion(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    integradas = models.IntegerField(choices=CHOICE_INTEGRADAS, null=True, blank=True)
    hombres = models.IntegerField(null=True, blank=True)
    mujeres = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return u'%s hombre - %s mujeres' % (str(self.hombres),str(self.mujeres))

    class Meta:
        verbose_name_plural = "Extra información"

class RubrosManejados(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    rubros = models.TextField('Rubros Manejados', null=True, blank=True)
    volumen_global = models.FloatField(null=True, blank=True)
    volumen_cacao = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return u'%s - %s' % (str(self.volumen_global),str(self.volumen_cacao))

    class Meta:
        verbose_name_plural = "Rubros manejados"

class FrecuenciaInfo(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    tipos = models.IntegerField(choices=CHOICE_INTEGRADAS_FRECUENCIA)
    respuesta = models.IntegerField(choices=CHOICE_FRECUENCIA)

    def __unicode__(self):
        return u'%s tipos - %s respuesta' % (self.get_tipos_display(), self.get_respuesta_display())

    class Meta:
        verbose_name_plural = "Frecuencia Info"