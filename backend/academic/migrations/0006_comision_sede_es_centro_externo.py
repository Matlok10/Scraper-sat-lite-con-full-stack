# Generated manually to add sede and es_centro_externo fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0005_comision_bibliografia_info_comision_llegada_docente_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comision',
            name='es_centro_externo',
            field=models.BooleanField(default=False, help_text='Indica si la comisión corresponde a un centro externo', verbose_name='Centro externo'),
        ),
        migrations.AddField(
            model_name='comision',
            name='sede',
            field=models.CharField(blank=True, default='', help_text='Orientación (General, Penal, Notarial) o nombre de la institución en centros externos', max_length=150, verbose_name='Sede u orientación'),
        ),
        migrations.AlterUniqueTogether(
            name='comision',
            unique_together={('codigo', 'docente', 'horario', 'cuatrimestre', 'sede')},
        ),
        migrations.AddIndex(
            model_name='comision',
            index=models.Index(fields=['sede'], name='academic_co_sede_12ab86_idx'),
        ),
        migrations.AddIndex(
            model_name='comision',
            index=models.Index(fields=['es_centro_externo'], name='academic_co_es_cent_7f2f53_idx'),
        ),
    ]
