from django.db import models

class Cargos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, default='')

    class Meta:
        indexes = [
            models.Index(fields=['nombre'], name='cargos_descripcion'),
        ]

    def __str__(self):
        return self.nombre



class Funcionalidades(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50, default='')

    class Meta:
        indexes = [
            models.Index(fields=['descripcion'], name='funcionalidades_descripcion'),
        ]

    def __str__(self):
        return self.descripcion



class Usuarios(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    password = models.CharField(max_length=10)
    cargo = models.ForeignKey(Cargos, db_column='cargo', related_name='usuario_cargo', on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    correo = models.CharField(max_length=50, blank=True, null=True)
    estado = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['nombre'], name='usuario_nombre'),
        ]

    def __str__(self):
        return self.nombre



class Perfiles(models.Model):
    cargo = models.ForeignKey(Cargos, db_column='cargo', related_name='perfil_cargo', on_delete=models.CASCADE)
    funcionalidad = models.ForeignKey(Funcionalidades, db_column='funcionalidad', related_name='perfil_funcionalidad', on_delete=models.CASCADE)
    permiso = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['funcionalidad'], name='perfil_funcionalidad2'),
        ]
        unique_together = ['cargo', 'funcionalidad', 'permiso']

    def __str__(self):
        return f'Perfil de {self.cargo} para {self.funcionalidad}'


class Permisos(models.Model):
    usuario = models.ForeignKey(Usuarios, db_column='usuario', related_name='permiso_usuario', on_delete=models.CASCADE)
    funcionalidad = models.ForeignKey(Funcionalidades, db_column='funcionalidad', related_name='permiso_funcionalidad', on_delete=models.CASCADE)
    permiso = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['usuario'], name='permiso_usuario'),
            models.Index(fields=['funcionalidad'], name='permiso_funcionalidad'),
        ]
        unique_together = ['usuario', 'funcionalidad', 'permiso']

    def __str__(self):
        return f'Permiso de {self.usuario} para {self.funcionalidad}'



