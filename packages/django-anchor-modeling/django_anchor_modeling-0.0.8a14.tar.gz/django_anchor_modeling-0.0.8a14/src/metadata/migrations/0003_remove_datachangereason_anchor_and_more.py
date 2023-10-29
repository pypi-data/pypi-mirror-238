# Generated by Django 4.2.6 on 2023-10-28 19:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataviewer', '0002_businesstodatafieldmap_main_model_class'),
        ('metadata', '0002_alter_datachange_id_alter_functioncall_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datachangereason',
            name='anchor',
        ),
        migrations.RemoveField(
            model_name='functioncallargs',
            name='anchor',
        ),
        migrations.RemoveField(
            model_name='functioncallservicefunction',
            name='anchor',
        ),
        migrations.RemoveField(
            model_name='functioncallservicefunction',
            name='value',
        ),
        migrations.RemoveField(
            model_name='requestcallargs',
            name='anchor',
        ),
        migrations.RemoveField(
            model_name='requestcallurl',
            name='anchor',
        ),
        migrations.RemoveField(
            model_name='requestcallurl',
            name='value',
        ),
        migrations.RemoveField(
            model_name='requestuser',
            name='anchor',
        ),
        migrations.RemoveField(
            model_name='requestuser',
            name='value',
        ),
        migrations.DeleteModel(
            name='DataChange',
        ),
        migrations.DeleteModel(
            name='DataChangeReason',
        ),
        migrations.DeleteModel(
            name='FunctionCall',
        ),
        migrations.DeleteModel(
            name='FunctionCallArgs',
        ),
        migrations.DeleteModel(
            name='FunctionCallServiceFunction',
        ),
        migrations.DeleteModel(
            name='RequestCall',
        ),
        migrations.DeleteModel(
            name='RequestCallArgs',
        ),
        migrations.DeleteModel(
            name='RequestCallUrl',
        ),
        migrations.DeleteModel(
            name='RequestUrl',
        ),
        migrations.DeleteModel(
            name='RequestUser',
        ),
        migrations.DeleteModel(
            name='ServiceFunction',
        ),
    ]
