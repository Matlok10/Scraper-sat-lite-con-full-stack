from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0007_rename_academic_co_sede_12ab86_idx_academic_co_sede_9f5ed2_idx_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comision',
            name='ciclo',
            field=models.CharField(blank=True, choices=[('CPO', 'Ciclo Profesional Orientado'), ('CPC', 'Ciclo Profesional Común')], default='', help_text='Indica si pertenece al Ciclo Profesional Orientado (CPO) o Común (CPC)', max_length=3, verbose_name='Ciclo (CPO/CPC)'),
        ),
    ]
