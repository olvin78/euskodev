import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_blog_resumen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='resumen',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
    ]
