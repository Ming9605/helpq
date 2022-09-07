# Generated by Django 4.0 on 2022-08-17 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('polls', '0006_remove_userprofile_birthday'),
    ]

    operations = [
        migrations.CreateModel(
            name='QueueNode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='age',
        ),
        migrations.CreateModel(
            name='VipQueue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('head', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.queuenode')),
            ],
        ),
        migrations.CreateModel(
            name='VipNode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.students')),
                ('next', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.vipnode')),
            ],
        ),
        migrations.CreateModel(
            name='TeacherUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(default='None', max_length=1, null=True)),
                ('age', models.IntegerField(default=69, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.AddField(
            model_name='queuenode',
            name='data',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.students'),
        ),
        migrations.AddField(
            model_name='queuenode',
            name='next',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.queuenode'),
        ),
        migrations.CreateModel(
            name='BasicUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(default='None', max_length=1, null=True)),
                ('age', models.IntegerField(default=69, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='BasicQueue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('head', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.queuenode')),
            ],
        ),
    ]
