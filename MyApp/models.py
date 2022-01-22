from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at', blank=True, null=True,
                                      verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, db_column='modified_at', blank=True, null=True,
                                      verbose_name=_('Updated at'))
    created_by = models.CharField(max_length=100, db_column='created_by', blank=True, null=True, default='',
                                  verbose_name=_('Created by'))
    updated_by = models.CharField(max_length=100, db_column='modified_by', blank=True, null=True, default='',
                                  verbose_name=_('Updated by'))

    class Meta:
        abstract = True

#   1
class SaleProjectPaymentPolicy(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    uniprime_project_id = models.IntegerField(db_column='uniprime_project_id', blank=True, null=True)
    payment_policy_name = models.CharField(max_length=255, db_column='name', verbose_name=_('Name'))
    payment_policy_date_from = models.DateField(db_column='start_date', verbose_name=_('Start Date'))
    payment_policy_date_to = models.DateField(db_column='end_date', verbose_name=_('End Date'))
    payment_policy_active_flag = models.BooleanField(db_column='active_flag', default=False)
    project_sell_open_id = models.IntegerField(db_column='project_sell_open_id', blank=True, null=True)
    payment_policy_deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)
    # project_sale_id = models.IntegerField(db_column='project_sale_id')
    class Meta:
        db_table = 'sale_project_payment_policy'
    
#   2
class SaleProjectPaymentPolicyGroup(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    project_payment_policy_id = models.ForeignKey(SaleProjectPaymentPolicy, on_delete=models.PROTECT, blank=True, null=True, db_column='project_payment_policy_id')
    group_type_id = models.IntegerField(db_column='c_project_sale_group', blank=True, null=True, verbose_name=_('Project Sale Group'))
    group_description = models.TextField(db_column='description', verbose_name=_('Description'))
    group_start_date = models.DateField(db_column='start_date', verbose_name=_('Start Date'))
    group_end_date = models.DateField(db_column='end_date', verbose_name=_('End Date'))
    group_active_flag = models.BooleanField(db_column='active_flag', default=False)
    deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)

    class Meta: 
        db_table = 'sale_project_payment_policy_group'

#   3
class SaleProjectPaymentPolicyGroupDetail(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    project_payment_policy_group_id = models.ForeignKey(SaleProjectPaymentPolicyGroup, on_delete=models.PROTECT, blank=True, null=True, db_column='project_payment_policy_group_id') 
    detail_time_type = models.IntegerField(db_column='c_payment_type', verbose_name=_('Payment Type'))
    detail_name = models.CharField(max_length=255, db_column='name', verbose_name=_('Name'))
    detail_payment_type = models.IntegerField(db_column='c_payment_time_type', verbose_name=_('Payment Time Type'))
    detail_time_value = models.IntegerField(db_column='payment_time_value', verbose_name=_('Payment Time Value'))
    detail_time_value_master_unit = models.IntegerField(db_column='payment_time_value_master_unit_id', blank=True, null=True)
    detail_time_to_date = models.DateField(db_column='payment_time_to_date', verbose_name=_('Payment Time Value'))
    detail_progressive_percent = models.FloatField(db_column='progressive_percent', verbose_name=_('Progressive Percent'))
    detail_discount_percent = models.FloatField(db_column='discount_percent', verbose_name=_('Discount Percent'))
    detail_content = models.TextField(db_column='content', verbose_name=_('Content'))
    deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)
    detail_discount_note = models.TextField(db_column='note', verbose_name=_('Note'))
    class Meta:
        db_table = 'sale_project_payment_policy_group_detail'

#   4
class SaleProjectPaymentPolicyGroupDetailValue(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    project_payment_policy_group_detail_id = models.ForeignKey(SaleProjectPaymentPolicyGroupDetail, on_delete=models.PROTECT, db_column='project_payment_policy_group_detail_id')
    detail_value_payment_method = models.IntegerField(db_column='c_payment_method', verbose_name=_('Payment Method'))
    detail_value_payment_value = models.FloatField(db_column='payment_value', verbose_name=_('Payment Value'))
    detail_value_payment_master_unit = models.IntegerField(db_column='payment_value_master_unit_id', blank=True, null=True)
    detail_value_payment_progressive_percent = models.FloatField(db_column='progressive_percent', verbose_name=_('Progressive Percent'))
    deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)
    class Meta:
        db_table = 'sale_project_payment_policy_group_detail_value'

#   5
class SaleProjectPaymentPolicyDetailValue(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    project_payment_policy_group_detail_id = models.ForeignKey(SaleProjectPaymentPolicyGroupDetail, on_delete=models.PROTECT, blank=True, null=True, db_column='project_payment_policy_group_detail_id')
    detail_value_payment_method = models.IntegerField(db_column='c_payment_method', verbose_name=_('Payment Type'))
    detail_value_payment_value = models.FloatField(db_column='payment_value', verbose_name=_('Payment Value'))
    detail_value_payment_master_unit = models.IntegerField(db_column='payment_value_master_unit_id', blank=True, null=True)
    detail_value_payment_progressive_percent = models.FloatField(db_column='progressive_percent', verbose_name=_('Progressive Percent'))
    deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)
    class Meta:
        db_table = 'sale_project_payment_policy_detail_value'

#   6
class SaleProjectPaymentPolicyGroupDetailValueFile(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    project_payment_policy_group_detail_value_id =  models.ForeignKey(SaleProjectPaymentPolicyGroupDetailValue, on_delete=models.PROTECT, db_column='project_payment_policy_group_detail_value_id')
    file_url = models.CharField(max_length=255, db_column='file_url', verbose_name=_('File Url'))
    file_content_type = models.CharField(max_length=255, db_column='file_content_type', verbose_name=_('File Content Type'), blank=True, null=True)
    file_name = models.CharField(max_length=255, db_column='file_name', verbose_name=_('file Name'))
    file_size = models.IntegerField(db_column='file_size', verbose_name=_('File Size'))
    file_type = models.IntegerField(db_column='file_type', verbose_name=_('File Type'), blank=True, null=True)
    deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)
    class Meta:
        db_table = 'sale_project_payment_policy_group_detail_value_file'

#   7
class SaleProjectPaymentPolicyGroupFile(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    project_payment_policy_group_id = models.ForeignKey(SaleProjectPaymentPolicyGroup, on_delete=models.PROTECT, db_column='project_payment_policy_group_id')
    group_file_url = models.CharField(max_length=255, db_column='file_url', verbose_name=_('File Url'))
    group_file_size = models.IntegerField(db_column='file_size', verbose_name=_('File Size'))
    group_file_name = models.CharField(max_length=255, db_column='file_name', verbose_name=_('File Name'))
    group_file_content_type = models.CharField(max_length=255, db_column='file_content_type', verbose_name=_('File Content Type'))
    group_deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)
    group_file_type = models.IntegerField(db_column='file_type', verbose_name=_('File Type'), blank=True, null=True,)
    class Meta:
        db_table = 'sale_project_payment_policy_group_file'

#   8
class SaleProjectPaymentPolicyFile(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    project_payment_policy_id = models.ForeignKey(SaleProjectPaymentPolicy, on_delete=models.PROTECT, db_column='project_payment_policy_id')
    file_url = models.CharField(max_length=255, db_column='file_url', verbose_name=_('File Url'))
    file_size = models.IntegerField(db_column='file_size', verbose_name=_('File Size'))
    file_name = models.CharField(max_length=255, db_column='file_name', verbose_name=_('File Name'))
    file_content_type = models.CharField(max_length=255, db_column='file_content_type', verbose_name=_('File Content Type'))
    deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)
    file_type = models.IntegerField(db_column='file_type', verbose_name=_('File Type'), blank=True, null=True)
    class Meta:
        db_table = 'sale_project_payment_policy_file'

#   9
class SaleProjectPaymentPolicyDetailValueFile(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    project_payment_policy_detail_value_id =  models.ForeignKey(SaleProjectPaymentPolicyDetailValue, on_delete=models.PROTECT, db_column='project_payment_policy_detail_value_id')
    file_url = models.CharField(max_length=255, db_column='file_url', verbose_name=_('File Url'))
    file_size = models.IntegerField(db_column='file_size', verbose_name=_('File Size'))
    file_name = models.CharField(max_length=255, db_column='file_name', verbose_name=_('File Name'))
    file_content_type = models.CharField(max_length=255, db_column='file_content_type', verbose_name=_('File Content Type'))
    deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)
    file_type = models.IntegerField(db_column='file_type', verbose_name=_('File Type'))
    class Meta:
        db_table = 'sale_project_payment_policy_detail_value_file'

#   10
class SaleProjectPaymentPolicyDetailDiscount(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    project_payment_policy_group_detail_id = models.ForeignKey(SaleProjectPaymentPolicyGroupDetail, on_delete=models.PROTECT, db_column='project_payment_policy_group_detail_id')
    discount_percent = models.FloatField(db_column='discount_percent', verbose_name=_('Discount Percent'))
    note = models.CharField(max_length=500, db_column='note', verbose_name=_('Note'))
    class Meta:
        db_table = 'sale_project_payment_policy_detail_discount'

