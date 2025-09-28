from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
