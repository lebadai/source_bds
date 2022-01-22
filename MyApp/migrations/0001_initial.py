# Generated by Django 3.2.9 on 2022-01-17 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SaleProjectPaymentPolicy',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at', null=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='modified_at', null=True, verbose_name='Updated at')),
                ('created_by', models.CharField(blank=True, db_column='created_by', default='', max_length=100, null=True, verbose_name='Created by')),
                ('updated_by', models.CharField(blank=True, db_column='modified_by', default='', max_length=100, null=True, verbose_name='Updated by')),
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False)),
                ('uniprime_project_id', models.IntegerField(blank=True, db_column='uniprime_project_id', null=True)),
                ('payment_policy_name', models.CharField(db_column='name', max_length=255, verbose_name='Name')),
                ('payment_policy_date_from', models.DateField(db_column='start_date', verbose_name='Start Date')),
                ('payment_policy_date_to', models.DateField(db_column='end_date', verbose_name='End Date')),
                ('payment_policy_active_flag', models.BooleanField(db_column='active_flag', default=False)),
                ('project_sell_open_id', models.IntegerField(blank=True, db_column='project_sell_open_id', null=True)),
                ('payment_policy_deleted_flag', models.BooleanField(db_column='deleted_flag', default=False)),
            ],
            options={
                'db_table': 'sale_project_payment_policy',
            },
        ),
        migrations.CreateModel(
            name='SaleProjectPaymentPolicyDetailValue',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at', null=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='modified_at', null=True, verbose_name='Updated at')),
                ('created_by', models.CharField(blank=True, db_column='created_by', default='', max_length=100, null=True, verbose_name='Created by')),
                ('updated_by', models.CharField(blank=True, db_column='modified_by', default='', max_length=100, null=True, verbose_name='Updated by')),
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False)),
                ('detail_value_payment_method', models.IntegerField(db_column='c_payment_method', verbose_name='Payment Type')),
                ('detail_value_payment_value', models.FloatField(db_column='payment_value', verbose_name='Payment Value')),
                ('detail_value_payment_master_unit', models.IntegerField(blank=True, db_column='payment_value_master_unit_id', null=True)),
                ('detail_value_payment_progressive_percent', models.FloatField(db_column='progressive_percent', verbose_name='Progressive Percent')),
                ('deleted_flag', models.BooleanField(db_column='deleted_flag', default=False)),
            ],
            options={
                'db_table': 'sale_project_payment_policy_detail_value',
            },
        ),
        migrations.CreateModel(
            name='SaleProjectPaymentPolicyGroup',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at', null=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='modified_at', null=True, verbose_name='Updated at')),
                ('created_by', models.CharField(blank=True, db_column='created_by', default='', max_length=100, null=True, verbose_name='Created by')),
                ('updated_by', models.CharField(blank=True, db_column='modified_by', default='', max_length=100, null=True, verbose_name='Updated by')),
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False)),
                ('group_type_id', models.IntegerField(blank=True, db_column='c_project_sale_group', null=True, verbose_name='Project Sale Group')),
                ('group_description', models.TextField(db_column='description', verbose_name='Description')),
                ('group_start_date', models.DateField(db_column='start_date', verbose_name='Start Date')),
                ('group_end_date', models.DateField(db_column='end_date', verbose_name='End Date')),
                ('group_active_flag', models.BooleanField(db_column='active_flag', default=False)),
                ('deleted_flag', models.BooleanField(db_column='deleted_flag', default=False)),
                ('project_payment_policy_id', models.ForeignKey(blank=True, db_column='project_payment_policy_id', null=True, on_delete=django.db.models.deletion.PROTECT, to='MyApp.saleprojectpaymentpolicy')),
            ],
            options={
                'db_table': 'sale_project_payment_policy_group',
            },
        ),
        migrations.CreateModel(
            name='SaleProjectPaymentPolicyGroupDetail',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at', null=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='modified_at', null=True, verbose_name='Updated at')),
                ('created_by', models.CharField(blank=True, db_column='created_by', default='', max_length=100, null=True, verbose_name='Created by')),
                ('updated_by', models.CharField(blank=True, db_column='modified_by', default='', max_length=100, null=True, verbose_name='Updated by')),
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False)),
                ('detail_time_type', models.IntegerField(db_column='c_payment_type', verbose_name='Payment Type')),
                ('detail_name', models.CharField(db_column='name', max_length=255, verbose_name='Name')),
                ('detail_payment_type', models.IntegerField(db_column='c_payment_time_type', verbose_name='Payment Time Type')),
                ('detail_time_value', models.IntegerField(db_column='payment_time_value', verbose_name='Payment Time Value')),
                ('detail_time_value_master_unit', models.IntegerField(blank=True, db_column='payment_time_value_master_unit_id', null=True)),
                ('detail_time_to_date', models.DateField(db_column='payment_time_to_date', verbose_name='Payment Time Value')),
                ('detail_progressive_percent', models.FloatField(db_column='progressive_percent', verbose_name='Progressive Percent')),
                ('detail_discount_percent', models.FloatField(db_column='discount_percent', verbose_name='Discount Percent')),
                ('detail_content', models.TextField(db_column='content', verbose_name='Content')),
                ('deleted_flag', models.BooleanField(db_column='deleted_flag', default=False)),
                ('detail_discount_note', models.TextField(db_column='note', verbose_name='Note')),
                ('project_payment_policy_group_id', models.ForeignKey(blank=True, db_column='project_payment_policy_group_id', null=True, on_delete=django.db.models.deletion.PROTECT, to='MyApp.saleprojectpaymentpolicygroup')),
            ],
            options={
                'db_table': 'sale_project_payment_policy_group_detail',
            },
        ),
        migrations.CreateModel(
            name='SaleProjectPaymentPolicyGroupDetailValue',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at', null=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='modified_at', null=True, verbose_name='Updated at')),
                ('created_by', models.CharField(blank=True, db_column='created_by', default='', max_length=100, null=True, verbose_name='Created by')),
                ('updated_by', models.CharField(blank=True, db_column='modified_by', default='', max_length=100, null=True, verbose_name='Updated by')),
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False)),
                ('payment_method', models.IntegerField(db_column='c_payment_method', verbose_name='Payment Method')),
                ('payment_value', models.FloatField(db_column='payment_value', verbose_name='Payment Value')),
                ('payment_value_master_unit_id', models.IntegerField(blank=True, db_column='payment_value_master_unit_id', null=True)),
                ('progressive_percent', models.FloatField(db_column='progressive_percent', verbose_name='Progressive Percent')),
                ('deleted_flag', models.BooleanField(db_column='deleted_flag', default=False)),
                ('project_payment_policy_group_detail_id', models.ForeignKey(db_column='project_payment_policy_group_detail_id', on_delete=django.db.models.deletion.PROTECT, to='MyApp.saleprojectpaymentpolicygroupdetail')),
            ],
            options={
                'db_table': 'sale_project_payment_policy_group_detail_value',
            },
        ),
        migrations.CreateModel(
            name='SaleProjectPaymentPolicyGroupFile',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at', null=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='modified_at', null=True, verbose_name='Updated at')),
                ('created_by', models.CharField(blank=True, db_column='created_by', default='', max_length=100, null=True, verbose_name='Created by')),
                ('updated_by', models.CharField(blank=True, db_column='modified_by', default='', max_length=100, null=True, verbose_name='Updated by')),
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False)),
                ('group_file_url', models.CharField(db_column='file_url', max_length=255, verbose_name='File Url')),
                ('group_file_size', models.IntegerField(db_column='file_size', verbose_name='File Size')),
                ('group_file_name', models.CharField(db_column='file_name', max_length=255, verbose_name='File Name')),
                ('group_file_content_type', models.CharField(db_column='file_content_type', max_length=255, verbose_name='File Content Type')),
                ('group_deleted_flag', models.BooleanField(db_column='deleted_flag', default=False)),
                ('group_file_type', models.IntegerField(blank=True, db_column='file_type', null=True, verbose_name='File Type')),
                ('project_payment_policy_group_id', models.ForeignKey(db_column='project_payment_policy_group_id', on_delete=django.db.models.deletion.PROTECT, to='MyApp.saleprojectpaymentpolicygroup')),
            ],
            options={
                'db_table': 'sale_project_payment_policy_group_file',
            },
        ),
        migrations.CreateModel(
            name='SaleProjectPaymentPolicyGroupDetailValueFile',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at', null=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='modified_at', null=True, verbose_name='Updated at')),
                ('created_by', models.CharField(blank=True, db_column='created_by', default='', max_length=100, null=True, verbose_name='Created by')),
                ('updated_by', models.CharField(blank=True, db_column='modified_by', default='', max_length=100, null=True, verbose_name='Updated by')),
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False)),
                ('file_url', models.CharField(db_column='file_url', max_length=255, verbose_name='File Url')),
                ('file_content_type', models.CharField(blank=True, db_column='file_content_type', max_length=255, null=True, verbose_name='File Content Type')),
                ('file_name', models.CharField(db_column='file_name', max_length=255, verbose_name='file Name')),
                ('file_size', models.IntegerField(db_column='file_size', verbose_name='File Size')),
                ('file_type', models.IntegerField(db_column='file_type', verbose_name='File Type')),
                ('deleted_flag', models.BooleanField(db_column='deleted_flag', default=False)),
                ('project_payment_policy_group_detail_value_id', models.ForeignKey(db_column='project_payment_policy_group_detail_value_id', on_delete=django.db.models.deletion.PROTECT, to='MyApp.saleprojectpaymentpolicygroupdetailvalue')),
            ],
            options={
                'db_table': 'sale_project_payment_policy_group_detail_value_file',
            },
        ),
        migrations.CreateModel(
            name='SaleProjectPaymentPolicyFile',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at', null=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='modified_at', null=True, verbose_name='Updated at')),
                ('created_by', models.CharField(blank=True, db_column='created_by', default='', max_length=100, null=True, verbose_name='Created by')),
                ('updated_by', models.CharField(blank=True, db_column='modified_by', default='', max_length=100, null=True, verbose_name='Updated by')),
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False)),
                ('file_url', models.CharField(db_column='file_url', max_length=255, verbose_name='File Url')),
                ('file_size', models.IntegerField(db_column='file_size', verbose_name='File Size')),
                ('file_name', models.CharField(db_column='file_name', max_length=255, verbose_name='File Name')),
                ('file_content_type', models.CharField(db_column='file_content_type', max_length=255, verbose_name='File Content Type')),
                ('deleted_flag', models.BooleanField(db_column='deleted_flag', default=False)),
                ('file_type', models.IntegerField(blank=True, db_column='file_type', null=True, verbose_name='File Type')),
                ('project_payment_policy_id', models.ForeignKey(db_column='project_payment_policy_id', on_delete=django.db.models.deletion.PROTECT, to='MyApp.saleprojectpaymentpolicy')),
            ],
            options={
                'db_table': 'sale_project_payment_policy_file',
            },
        ),
        migrations.CreateModel(
            name='SaleProjectPaymentPolicyDetailValueFile',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at', null=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='modified_at', null=True, verbose_name='Updated at')),
                ('created_by', models.CharField(blank=True, db_column='created_by', default='', max_length=100, null=True, verbose_name='Created by')),
                ('updated_by', models.CharField(blank=True, db_column='modified_by', default='', max_length=100, null=True, verbose_name='Updated by')),
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False)),
                ('file_url', models.CharField(db_column='file_url', max_length=255, verbose_name='File Url')),
                ('file_size', models.IntegerField(db_column='file_size', verbose_name='File Size')),
                ('file_name', models.CharField(db_column='file_name', max_length=255, verbose_name='File Name')),
                ('file_content_type', models.CharField(db_column='file_content_type', max_length=255, verbose_name='File Content Type')),
                ('deleted_flag', models.BooleanField(db_column='deleted_flag', default=False)),
                ('file_type', models.IntegerField(db_column='file_type', verbose_name='File Type')),
                ('project_payment_policy_detail_value_id', models.ForeignKey(db_column='project_payment_policy_detail_value_id', on_delete=django.db.models.deletion.PROTECT, to='MyApp.saleprojectpaymentpolicydetailvalue')),
            ],
            options={
                'db_table': 'sale_project_payment_policy_detail_value_file',
            },
        ),
        migrations.AddField(
            model_name='saleprojectpaymentpolicydetailvalue',
            name='project_payment_policy_group_detail_id',
            field=models.ForeignKey(blank=True, db_column='project_payment_policy_group_detail_id', null=True, on_delete=django.db.models.deletion.PROTECT, to='MyApp.saleprojectpaymentpolicygroupdetail'),
        ),
        migrations.CreateModel(
            name='SaleProjectPaymentPolicyDetailDiscount',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at', null=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='modified_at', null=True, verbose_name='Updated at')),
                ('created_by', models.CharField(blank=True, db_column='created_by', default='', max_length=100, null=True, verbose_name='Created by')),
                ('updated_by', models.CharField(blank=True, db_column='modified_by', default='', max_length=100, null=True, verbose_name='Updated by')),
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False)),
                ('discount_percent', models.FloatField(db_column='discount_percent', verbose_name='Discount Percent')),
                ('note', models.CharField(db_column='note', max_length=500, verbose_name='Note')),
                ('project_payment_policy_group_detail_id', models.ForeignKey(db_column='project_payment_policy_group_detail_id', on_delete=django.db.models.deletion.PROTECT, to='MyApp.saleprojectpaymentpolicygroupdetail')),
            ],
            options={
                'db_table': 'sale_project_payment_policy_detail_discount',
            },
        ),
    ]
