# Generated migrations - run python manage.py makemigrations face_app

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='FaceImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='face_images/')),
                ('face_encoding', models.TextField()),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='face_images', to='face_app.person')),
            ],
            options={
                'ordering': ['-uploaded_at'],
            },
        ),
        migrations.CreateModel(
            name='RecognitionResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confidence', models.FloatField()),
                ('confidence_level', models.CharField(choices=[('high', 'High (>0.8)'), ('medium', 'Medium (0.5-0.8)'), ('low', 'Low (<0.5)')], default='low', max_length=10)),
                ('recognized_at', models.DateTimeField(auto_now_add=True)),
                ('capture_image', models.ImageField(blank=True, null=True, upload_to='recognition_captures/')),
                ('matched_person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recognition_results', to='face_app.person')),
            ],
            options={
                'ordering': ['-recognized_at'],
            },
        ),
    ]
