from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchhistory',
            name='feels_like',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='searchhistory',
            name='humidity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='searchhistory',
            name='wind_speed',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='searchhistory',
            name='description',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='searchhistory',
            name='icon',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
    ]
