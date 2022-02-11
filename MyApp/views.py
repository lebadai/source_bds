from rest_framework import status
from django.db.models import F, Q
from library.constant.error_codes import JSON_BODY_EMPTY, ERROR_CODE_MESSAGE
from library.functions import string_to_time, check_progressive_percent, save_upload_file, check_body
from MyApp.models import SaleProjectPaymentPolicy, SaleProjectPaymentPolicyGroup, SaleProjectPaymentPolicyGroupDetail, SaleProjectPaymentPolicyGroupDetailValue, SaleProjectPaymentPolicyFile, SaleProjectPaymentPolicyGroupFile, SaleProjectPaymentPolicyGroupDetailValueFile, SaleProjectPaymentPolicyGroupDetailValue, SaleProjectPaymentPolicyDetailValueFile
from MyApp.models import SaleProjectPaymentPolicyGroup
from library.functions import decode_to_json
from MyApp.basic_views import BaseAPIView, BaseAPIAnonymousView
from rest_framework.response import Response
import os
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from urllib.parse import urljoin
from django.conf import settings

class PaymentPolicyView(BaseAPIView):

    def list(self, request, **kwargs):
        params = request.query_params
        list_key_param = list(params.keys())

        if 'payment_policy_name' in list_key_param:
            list_payment_policy = SaleProjectPaymentPolicy.objects.filter(payment_policy_name__contains=params['payment_policy_name'])
        else:
            list_payment_policy = SaleProjectPaymentPolicy.objects.all()

        list_payment_policy = list_payment_policy.annotate(
            payment_policy_id=F('id')
        ).values(
            'payment_policy_id',
            'payment_policy_name',
            'payment_policy_date_from',
            'payment_policy_date_to',                                  
        ).order_by('id')

        for payment_policy in list_payment_policy:
            list_payment_policy_groups = SaleProjectPaymentPolicyGroup.objects.filter(
                deleted_flag=False,
                project_payment_policy_id=payment_policy["payment_policy_id"]
            ).annotate(
                group_id=F('id')
            ).values(
                'group_id',
                'group_type_id',
                'group_start_date',
                'group_end_date',
                'group_description',
                'group_active_flag'
            ) 
            payment_policy['payment_policy_groups'] = list(list_payment_policy_groups)

            for payment_policy_group in list_payment_policy_groups:
                list_payment_policy_details = SaleProjectPaymentPolicyGroupDetail.objects.filter(
                deleted_flag=False,
                project_payment_policy_group_id=payment_policy_group["group_id"]
                ).annotate(
                    detail_id=F('id')
                ).values(
                    'detail_id',
                    'detail_time_type',
                    'detail_name',
                    'detail_time_value',
                    'detail_time_to_date',
                    'detail_payment_type',
                    'detail_time_value_master_unit',
                    'detail_progressive_percent',
                    'detail_discount_percent',
                    'detail_discount_note',
                    'detail_content'
                ) 
            payment_policy_group['payment_policy_details'] = list(list_payment_policy_details)

            for payment_policy_group_detail in list_payment_policy_details:
                list_payment_policy_detail_values = SaleProjectPaymentPolicyGroupDetailValue.objects.filter(
                deleted_flag=False,
                project_payment_policy_group_detail_id=payment_policy_group_detail["detail_id"]
                ).annotate(
                    detail_value_id=F('id')
                ).values(
                    'detail_value_id',
                    'detail_value_payment_method',
                    'detail_value_payment_value',
                    'detail_value_payment_master_unit',
                    'detail_value_payment_progressive_percent'
                )
                payment_policy_group_detail['payment_policy_group_detail'] = list(list_payment_policy_detail_values)

        self.paginate(list_payment_policy)
        return self.response(self.response_paging(self.paging_list))
    
    def payment_policy_validate(self, content, payment_policy_list, is_created=True):

        if is_created:
            self.check_key_content(key_content_list=payment_policy_list,
                                   check_key_list=['payment_policy_name', 'payment_policy_date_from', 'payment_policy_date_to'])
        else:
            check_keys_list = ['id']
            self.check_key_content(key_content_list=payment_policy_list, check_key_list=check_keys_list)
            if len(payment_policy_list) == 1:
                return self.validate_exception('You do not change anything')

        if 'payment_policy_id' in payment_policy_list:
            payment_policy_id = content['payment_policy_id']
            if not isinstance(payment_policy_id, int):
                return self.validate_exception('payment_policy_id must be an integer')
            if not SaleProjectPaymentPolicy.objects.filter(id=payment_policy_id).exists():
                return self.validate_exception('payment_policy_id is not exist')

        if 'payment_policy_name' in payment_policy_list:
            payment_policy_name = content['payment_policy_name']
            if not isinstance(payment_policy_name, str):
                return self.validate_exception('payment_policy_name must be a string')

        if 'payment_policy_date_from' in payment_policy_list:
            payment_policy_date_from = content['payment_policy_date_from']
            if not isinstance(payment_policy_date_from, str):
                return self.validate_exception('payment_policy_date_from must be a string')
            if payment_policy_date_from != '':
                payment_policy_date_from = string_to_time(content['payment_policy_date_from'], "%Y-%m-%d")
                if payment_policy_date_from is None:
                    return self.validate_exception('payment_policy_date_from is invalid format')

        if 'payment_policy_date_to' in payment_policy_list:
            payment_policy_date_to = content['payment_policy_date_to']
            if not isinstance(payment_policy_date_to, str):
                return self.validate_exception('payment_policy_date_to must be a string')
            if payment_policy_date_to != '':
                payment_policy_date_to = string_to_time(content['payment_policy_date_to'], "%Y-%m-%d")
                if payment_policy_date_to is None:
                    return self.validate_exception('payment_policy_date_to is invalid format')

    def payment_policy_group_validate(self, content, group_list, is_created=True):

        if is_created:
            self.check_key_content(key_content_list=group_list,
                                   check_key_list=['group_type_id', 'group_description', 'group_active_flag', 'group_start_date', 'group_end_date'])
        else:
            check_keys_list = ['id']
            self.check_key_content(key_content_list=group_list, check_key_list=check_keys_list)
            if len(group_list) == 1:
                return self.validate_exception('You do not change anything')

        if 'id' in group_list:
            id = content['id']
            if not isinstance(id, int):
                return self.validate_exception('group_id must be an integer')
            if not SaleProjectPaymentPolicyGroup.objects.filter(id=id).exists():
                return self.validate_exception('group_id is not exist')
        
        if 'group_description' in group_list:
            group_description = content['group_description']
            if not isinstance(group_description, str):
                return self.validate_exception('group_description must be a string')
        
        if 'group_active_flag' in group_list:
            group_active_flag = content['group_active_flag']
            if not isinstance(group_active_flag, bool):
                return self.validate_exception('group_active_flag must be a boolean')

        if 'group_start_date' in group_list:
            group_start_date = content['group_start_date']
            if not isinstance(group_start_date, str):
                return self.validate_exception('group_start_date must be a string')
            if group_start_date != '':
                group_start_date = string_to_time(content['group_start_date'], "%Y-%m-%d")
                if group_start_date is None:
                    return self.validate_exception('group_start_date is invalid format')
            if group_start_date == '':
                return self.validate_exception('group_start_date must be not empty')

        if 'group_end_date' in group_list:
            group_end_date = content['group_end_date']
            if not isinstance(group_end_date, str):
                return self.validate_exception('group_end_date must be a string')
            if group_end_date != '':
                group_end_date = string_to_time(content['group_end_date'], "%Y-%m-%d")
                if group_end_date is None:
                    return self.validate_exception('group_end_date is invalid format')
            if group_end_date == '':
                return self.validate_exception('group_end_date must be not empty')
        
    def payment_policy_detail_validate(self, content, detail_list, is_created=True):

        if is_created:
            self.check_key_content(key_content_list=detail_list,
                                   check_key_list=['detail_time_type', 'detail_name', 'detail_time_value', 'detail_time_to_date', 'detail_time_value_master_unit', 'detail_progressive_percent', 'detail_discount_percent', 'detail_content', 'detail_discount_note']), 
        else:
            check_keys_list = ['id']
            self.check_key_content(key_content_list=detail_list, check_key_list=check_keys_list)
            if len(detail_list) == 1:
                return self.validate_exception('You do not change anything')

        if 'id' in detail_list:
            id = content['id']
            if not isinstance(id, int):
                return self.validate_exception('detail_id must be an integer')
            if not SaleProjectPaymentPolicyGroupDetail.objects.filter(id=id).exists():
                return self.validate_exception('detail_id is not exist')

        if 'detail_time_type' in detail_list:
            detail_time_type = content['detail_time_type']
            if not isinstance(detail_time_type, int):
                return self.validate_exception('detail_time_type must be a integer')
           
        if 'detail_name' in detail_list:
            detail_name = content['detail_name']
            if not isinstance(detail_name, str):
                return self.validate_exception('detail_name must be a string')

        if 'detail_time_value' in detail_list:
            detail_time_value = content['detail_time_value']
            if not isinstance(detail_time_value, int):
                return self.validate_exception('detail_time_value must be a integer')

        if 'detail_time_value_master_unit' in detail_list:
            detail_time_value_master_unit = content['detail_time_value_master_unit']
            if not isinstance(detail_time_value_master_unit, int):
                return self.validate_exception('detail_time_value_master_unit must be a integer')
        
        if 'detail_time_to_date' in detail_list:
            detail_time_to_date = content['detail_time_to_date']
            if not isinstance(detail_time_to_date, str):
                return self.validate_exception('detail_time_to_date must be a string')
            if detail_time_to_date != '':
                detail_time_to_date = string_to_time(content['detail_time_to_date'], "%Y-%m-%d")
                if detail_time_to_date is None:
                    return self.validate_exception('detail_time_to_date is invalid format')

            if 'detail_progressive_percent' in detail_list:
                detail_progressive_percent = content['detail_progressive_percent']
            if not isinstance(detail_progressive_percent, float):
                return self.validate_exception('detail_progressive_percent must be a float')
          
            if 'detail_discount_percent' in detail_list:
                detail_discount_percent = content['detail_discount_percent']
            if not isinstance(detail_discount_percent, float):
                return self.validate_exception('detail_discount_percent must be a float')
          
            if 'detail_content' in detail_list:
                detail_content = content['detail_content']
            if not isinstance(detail_content, str):
                return self.validate_exception('detail_content must be a string')


    def payment_policy_detail_value_validate(self, content, detail_values_list, is_created=True):
        if is_created:
            self.check_key_content(key_content_list=detail_values_list,
                                   check_key_list=['detail_value_payment_method', 'detail_value_payment_value', 'detail_value_payment_master_unit', 'detail_value_payment_progressive_percent', ]), 
        else:
            check_keys_list = ['id']
            self.check_key_content(key_content_list=detail_values_list, check_key_list=check_keys_list)

            if len(detail_values_list) == 1:
                return self.validate_exception('You do not change anything')

        if 'id' in detail_values_list:
            id = content['id']
            if not isinstance(id, int):
                return self.validate_exception('detail_value_id must be an integer')
            if not SaleProjectPaymentPolicyGroupDetailValue.objects.filter(id=id).exists():
                return self.validate_exception('detail_value_id is not exist')

        if 'detail_value_payment_method' in detail_values_list:
            detail_value_payment_method = content['detail_value_payment_method']
            if not isinstance(detail_value_payment_method, int):
                return self.validate_exception('detail_value_payment_method must be a integer')

        if 'detail_value_payment_value' in detail_values_list:
            detail_value_payment_value = content['detail_value_payment_value']
            if not isinstance(detail_value_payment_value, float):
                return self.validate_exception('detail_value_payment_value must be a float')

        if 'detail_value_payment_master_unit' in detail_values_list:
            detail_value_payment_master_unit = content['detail_value_payment_master_unit']
            if not isinstance(detail_value_payment_master_unit, int):
                return self.validate_exception('detail_value_payment_master_unit must be a integer')

        if 'detail_value_payment_progressive_percent' in detail_values_list:
            detail_value_payment_progressive_percent = content['detail_value_payment_progressive_percent']
            if not isinstance(detail_value_payment_progressive_percent, float):
                return self.validate_exception('detail_value_payment_progressive_percent must be a float')
          

    def create(self, request):

        content = check_body(request.body)
        key_content_list = list(content.keys())
        self.payment_policy_validate(content=content, payment_policy_list=key_content_list, is_created=True)                   

        if 'payment_policy_groups' in key_content_list:
            policy_group_lst = content['payment_policy_groups']
            payment_policy = SaleProjectPaymentPolicy.objects.create(
                payment_policy_name=content['payment_policy_name'],
                payment_policy_date_from=content['payment_policy_date_from'],
                payment_policy_date_to=content['payment_policy_date_to']
            )

            for policy_group in policy_group_lst:
                if not isinstance(policy_group, dict):
                    return self.http_exception(description='payment policy group must be dict')
                key_grp_lst = list(policy_group.keys())
                total = [] 
                if 'payment_policy_details' in key_grp_lst:
                    group_detais = policy_group['payment_policy_details']
                    for grp_dtl in group_detais:
                        key_values_list = list(grp_dtl.keys())
                        if "detail_values" in key_values_list:
                            detail_value = grp_dtl['detail_values']
                            for dtl_vls in detail_value:
                                total.append(dtl_vls['detail_value_payment_progressive_percent']) 

                check_progressive_percent(total)
                self.payment_policy_group_validate(content=policy_group, group_list=key_grp_lst, is_created=True)

                policy_grp = SaleProjectPaymentPolicyGroup.objects.create(
                    project_payment_policy_id_id=int(payment_policy.id),
                    group_type_id=policy_group['group_type_id'],
                    group_description=policy_group['group_description'],
                    group_start_date=policy_group['group_start_date'],
                    group_end_date=policy_group['group_end_date'],
                    group_active_flag=policy_group['group_active_flag'],
                )

                if 'payment_policy_details' in policy_group:
                    # policy_detail_lst = len(payment_policy_grp['payment_policy_details'])
                    # for policy_detail_index in range(policy_detail_lst):
                    payment_policy_details = policy_group['payment_policy_details']
                    for group_detail in payment_policy_details:
                        
                        if not isinstance(group_detail, dict):
                            return self.http_exception(description='group detail must be dict')

                        key_dtl_lst = list(group_detail.keys())
                        self.payment_policy_detail_validate(content=group_detail, detail_list=key_dtl_lst, is_created=True)
                        if 'detail_values' in group_detail:
                            # policy_detail_values_lst = len(group_detail['detail_values'])
                            group_detail_values_list = group_detail['detail_values']

                            grp_dtl = SaleProjectPaymentPolicyGroupDetail.objects.create(
                                project_payment_policy_group_id_id=policy_grp.id,
                                detail_time_type=group_detail['detail_time_type'],
                                detail_name=group_detail['detail_name'],
                                detail_time_value=group_detail['detail_time_value'],
                                detail_payment_type=group_detail['detail_payment_type'],
                                detail_time_to_date=group_detail['detail_time_to_date'],
                                detail_time_value_master_unit=group_detail['detail_time_value_master_unit'],
                                detail_progressive_percent=group_detail['detail_progressive_percent'],
                                detail_discount_percent=group_detail['detail_discount_percent'],
                                detail_content=group_detail['detail_content'],
                                detail_discount_note=group_detail['detail_discount_note'],
                            )

                            for policy_detail_values_index in group_detail_values_list:
                                group_detail_vls = group_detail
                                if not isinstance(group_detail_vls, dict):
                                    return self.http_exception(description='payment policy group must be dict')
                                
                                key_dtl_vls_lst = list(group_detail_vls.keys())
                                self.payment_policy_detail_value_validate(content=group_detail_vls, detail_values_list=key_dtl_vls_lst, is_created=True)
                                lst_detail_values_ret = []
                                
                                grp_dtl_vl = SaleProjectPaymentPolicyGroupDetailValue.objects.create(
                                    project_payment_policy_group_detail_id_id = grp_dtl.id,
                                    detail_value_payment_method=payment_policy_dtl_vls['detail_value_payment_method'],
                                    detail_value_payment_value=payment_policy_dtl_vls['detail_value_payment_value'],
                                    detail_value_payment_master_unit=payment_policy_dtl_vls['detail_value_payment_master_unit'],
                                    detail_value_payment_progressive_percent=payment_policy_dtl_vls['detail_value_payment_progressive_percent']
                                )

        else:
            return self.validate_exception('payment policy group detal values must be valuable')
                                
        return self.response_success({
            'message': 'Create new payment policy success'
        }, status_code=status.HTTP_201_CREATED)  

    def list_policy_file(self, payment_policy_id):
        list_payment_policy_file = SaleProjectPaymentPolicyFile.objects.filter(project_payment_policy_id=payment_policy_id)
        lst_ppf_name = []
        for payment_policy_file in list_payment_policy_file:
            lst_ppf_name.append({
                "id": payment_policy_file.id,
                "name": str(payment_policy_file.file_name),
                "url": str(payment_policy_file.file_url),
                "file_content_type": str(payment_policy_file.file_content_type)
                })
        return lst_ppf_name

    def list_policy_group_file(self, policy_group_id):
        list_payment_policy_group_file = SaleProjectPaymentPolicyGroupFile.objects.filter(project_payment_policy_group_id=policy_group_id)
        lst_ppgf_name = []

        for payment_policy_group_file in list_payment_policy_group_file:
            lst_ppgf_name.append({
                "id": payment_policy_group_file.id,
                "name": str(payment_policy_group_file.group_file_name),
                "url": str(payment_policy_group_file.group_file_url),
                "file_content_type": str(payment_policy_group_file.group_file_content_type)
                })
        return lst_ppgf_name

    def list_policy_group_detail_value_file(self, detail_value_id):
        list_detail_value_file = SaleProjectPaymentPolicyGroupDetailValueFile.objects.filter(project_payment_policy_group_detail_value_id=detail_value_id)
        lst_ppgdtf_name=[]

        for group_detail_value_file in list_detail_value_file:
            lst_ppgdtf_name.append({
                "id": group_detail_value_file.id,
                "name": str(group_detail_value_file.file_name),
                "url": str(group_detail_value_file.file_url),
                "file_content_type": str(group_detail_value_file.file_content_type)
            })
        return lst_ppgdtf_name

    def get(self, request, **kwargs):
        params = request.query_params
        list_key_param = list(params.keys())

        self.check_key_content(key_content_list=list_key_param, check_key_list=['id'])
        
        payment_policy = SaleProjectPaymentPolicy.objects.filter(
            Q(pk=params['id']),
            Q(payment_policy_deleted_flag=False)
        ).annotate(
            payment_policy_id=F('id')
        ).values(
            'payment_policy_id',
            'payment_policy_name',
            'payment_policy_date_from',
            'payment_policy_date_to'
        ).first()

        if payment_policy:
            pp_file = self.list_policy_file(payment_policy["payment_policy_id"])
            if int(len(pp_file)) == 1:
                payment_policy['payment_policy_file'] = pp_file[0]
            if int(len(pp_file)) > 1:
                payment_policy['payment_policy_files'] = pp_file

            payment_policy_groups = SaleProjectPaymentPolicyGroup.objects.filter(
                deleted_flag=False,
                project_payment_policy_id=payment_policy["payment_policy_id"]
            ).annotate(
                group_id=F('id')
            ).values(
                'group_id',
                'group_type_id',
                'group_start_date',
                'group_end_date',
                'group_description',
                'group_active_flag'
            )
            payment_policy['payment_policy_groups'] = list(payment_policy_groups)

            if payment_policy_groups:
                for payment_policy_group in payment_policy_groups:

                    ppg_file = self.list_policy_group_file(payment_policy_group["group_id"])
                    if int(len(ppg_file)) == 1:
                        payment_policy_group['group_file'] = ppg_file[0]
                    if int(len(ppg_file)) > 1:
                        payment_policy_group['group_files'] = ppg_file
                    payment_policy_details = SaleProjectPaymentPolicyGroupDetail.objects.filter(
                        deleted_flag=False,
                        project_payment_policy_group_id=payment_policy_group["group_id"]
                    ).annotate(
                        detail_id=F('id')
                    ).values(
                        'detail_id',
                        'detail_time_type',
                        'detail_name',
                        'detail_time_value',
                        'detail_time_to_date',
                        'detail_payment_type',
                        'detail_time_value_master_unit',
                        'detail_progressive_percent',
                        'detail_discount_percent',
                        'detail_discount_note',
                        'detail_content'
                    )
                    payment_policy_group['payment_policy_details'] = list(payment_policy_details)

                    if payment_policy_details:
                        for payment_policy_detail in payment_policy_details:

                            payment_policy_detail_values = SaleProjectPaymentPolicyGroupDetailValue.objects.filter(
                            deleted_flag=False,
                            project_payment_policy_group_detail_id=payment_policy_detail["detail_id"]
                            ).annotate(
                                detail_value_id=F('id')
                            ).values(
                                'detail_value_id',
                                'detail_value_payment_method',
                                'detail_value_payment_value',
                                'detail_value_payment_master_unit',
                                'detail_value_payment_progressive_percent'
                            )
                            
                            payment_policy_detail['detail_values'] = list(payment_policy_detail_values)
                            for payment_policy_detail_value in payment_policy_detail_values:
                                ppg_file = self.list_policy_group_detail_value_file(payment_policy_detail_value["detail_value_id"])
                                if int(len(ppg_file)) == 1:
                                    payment_policy_detail_value['detail_value_file'] = ppg_file[0]
                                if int(len(ppg_file)) > 1:
                                    payment_policy_detail_value['detail_value_file'] = ppg_file
            return self.response_success(payment_policy)
        else:
            return self.validate_exception('detail_value_id does not exist')

    def put(self, request, **kwargs):

        content = check_body(request.body)
        keys_payment_policy = list(content.keys())
        self.payment_policy_validate(content=content, payment_policy_list=keys_payment_policy, is_created=False)

        try:
            payment_policy = SaleProjectPaymentPolicy.objects.get(id=content['id'])
        except SaleProjectPaymentPolicy.DoesNotExist as ex:
            return self.validate_exception(str(ex))

        if 'payment_policy_name' in keys_payment_policy:
            payment_policy.payment_policy_name = content["payment_policy_name"]
        if 'payment_policy_date_from' in keys_payment_policy:
            payment_policy.payment_policy_date_from = content["payment_policy_date_from"]
        if 'payment_policy_date_to' in keys_payment_policy:
            payment_policy.payment_policy_date_to = content["payment_policy_date_to"]
        payment_policy.save()

        if 'payment_policy_groups' in keys_payment_policy:
            list_value_ppg = list(SaleProjectPaymentPolicyGroup.objects.filter(project_payment_policy_id=content['id']).values_list('id', flat=True))
            for index_ppg, payment_policy_group in enumerate(content['payment_policy_groups'], start=0):
                
                keys_group_list = list(payment_policy_group.keys())
                self.payment_policy_group_validate(content=payment_policy_group, group_list=keys_group_list, is_created=False)

                if payment_policy_group["id"] not in list_value_ppg:
                    return self.validate_exception('payment policy group not in payment policy')

                ppg = SaleProjectPaymentPolicyGroup.objects.get(id=payment_policy_group["id"])
                if 'group_type_id' in keys_group_list:
                    ppg.group_type_id = payment_policy_group["group_type_id"]
                
                if 'group_start_date' in keys_group_list:
                    ppg.group_start_date = payment_policy_group["group_start_date"]

                if 'group_end_date' in keys_group_list:
                    ppg.group_end_date = payment_policy_group["group_end_date"]
                
                if 'group_description' in keys_group_list:
                    ppg.group_description = payment_policy_group["group_description"]

                if 'group_active_flag' in keys_group_list:
                    ppg.group_active_flag = payment_policy_group["group_active_flag"]
                ppg.save()

        return self.response_success({
            'message': 'Update payment policy success'
        }, status_code=status.HTTP_201_CREATED)   


    def delete_payment_policy(self, request, **kwargs):
        params = request.query_params
        list_key_param = list(params.keys())
        if 'id' in list_key_param:
            try:
                payment_policy = SaleProjectPaymentPolicy.objects.get(id=int(params['id']))
            except SaleProjectPaymentPolicy.DoesNotExist as ex:
                return self.validate_exception(str(ex))
            payment_policy.payment_policy_deleted_flag = True
            payment_policy.save()
            payment_policy_file = SaleProjectPaymentPolicyFile.objects.filter(project_payment_policy_id=payment_policy)
            for pmt_plc_file in payment_policy_file:
                pmt_plc_file.deleted_flag = True
                pmt_plc_file.save()

            payment_policy_groups = SaleProjectPaymentPolicyGroup.objects.filter(project_payment_policy_id=payment_policy)
            for pmt_plc_grp in payment_policy_groups:
                pmt_plc_grp.deleted_flag = True
                pmt_plc_grp.save()

                group_file = SaleProjectPaymentPolicyGroupFile.objects.filter(project_payment_policy_group_id= pmt_plc_grp) 
                for grp_file in group_file:
                    grp_file.group_deleted_flag = True
                    grp_file.save()

            for pmt_plc_grp in payment_policy_groups:
                payment_policy_goup_details = SaleProjectPaymentPolicyGroupDetail.objects.filter(project_payment_policy_group_id=pmt_plc_grp)
                for group_detail in payment_policy_goup_details:
                    group_detail.deleted_flag = True
                    group_detail.save()

                    group_detail_value = SaleProjectPaymentPolicyGroupDetailValue.objects.filter(project_payment_policy_group_detail_id=group_detail)
                    for grp_dtl_vls in group_detail_value:
                        grp_dtl_vls.deleted_flag = True
                        grp_dtl_vls.save()

                        group_detail_value_file = SaleProjectPaymentPolicyGroupDetailValueFile.objects.filter(project_payment_policy_group_detail_value_id=grp_dtl_vls)
                        for grp_dtl_vls_file in group_detail_value_file:
                            grp_dtl_vls_file.deleted_flag = True
                            grp_dtl_vls_file.save()

            return Response({'message': 'Delete success'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return self.validate_exception('You have to input id param')


class PaymentPolicyFileView(BaseAPIView):
    def payment_policy_file_validate(self, content, payment_policy_file_list, is_created=True):
        if is_created:
            self.check_key_content(key_content_list=payment_policy_file_list,
                                   check_key_list=['file_url', 'file_size', 'file_name', 'file_content_type'])
        else:
            check_keys_list = ['id']
            self.check_key_content(key_content_list=payment_policy_file_list, check_key_list=check_keys_list)

            if len(payment_policy_file_list) == 1:
                return self.validate_exception('You do not change anything')
            
            if 'file_url' in payment_policy_file_list:
                file_url = content['file_url']
                if not isinstance(file_url, str):
                    return self.validate_exception('file_url must be a string')

            if 'file_size' in payment_policy_file_list:
                file_size = content['file_size']
                if not isinstance(file_size, int):
                    return self.validate_exception('file_size must be a integer')

            if 'file_name' in payment_policy_file_list:
                file_name = content['file_name']
                if not isinstance(file_name, str):
                    return self.validate_exception('file_name must be a string')

            if 'file_content_type' in payment_policy_file_list:
                file_content_type = content['file_content_type']
                if not isinstance(file_content_type, str):
                    return self.validate_exception('file_content_type must be a string')

    def payment_policy_group_file_validate(self, content, payment_policy_group_file_list, is_created=True):
        if is_created:
            self.check_key_content(key_content_list=payment_policy_group_file_list,
                                   check_key_list=['file_url', 'file_size', 'file_name', 'file_content_type'])
        else:
            check_keys_list = ['id']
            self.check_key_content(key_content_list=payment_policy_group_file_list, check_key_list=check_keys_list)

            if len(payment_policy_group_file_list) == 1:
                return self.validate_exception('You do not change anything')
            
            if 'file_url' in payment_policy_group_file_list:
                file_url = content['file_url']
                if not isinstance(file_url, str):
                    return self.validate_exception('file_url must be a string')

            if 'file_size' in payment_policy_group_file_list:
                file_size = content['file_size']
                if not isinstance(file_size, int):
                    return self.validate_exception('file_size must be a integer')

            if 'file_name' in payment_policy_group_file_list:
                file_name = content['file_name']
                if not isinstance(file_name, str):
                    return self.validate_exception('file_name must be a string')

            if 'group_file_content_type' in payment_policy_group_file_list:
                group_file_content_type = content['group_file_content_type']
                if not isinstance(group_file_content_type, str):
                    return self.validate_exception('group_file_content_type must be a string')

    def payment_policy_group_detail_value_file_validate(self, content, payment_policy_group_detail_value_file_list, is_created=True):
        if is_created:
            self.check_key_content(key_content_list=payment_policy_group_detail_value_file_list,
                                   check_key_list=['file_url', 'file_size', 'file_name', 'file_content_type'])
        else:
            check_keys_list = ['id']
            self.check_key_content(key_content_list=payment_policy_group_detail_value_file_list, check_key_list=check_keys_list)

            if len(payment_policy_group_detail_value_file_list) == 1:
                return self.validate_exception('You do not change anything')
            
            if 'file_url' in payment_policy_group_detail_value_file_list:
                file_url = content['file_url']
                if not isinstance(file_url, str):
                    return self.validate_exception('file_url must be a string')

            if 'file_size' in payment_policy_group_detail_value_file_list:
                file_size = content['file_size']
                if not isinstance(file_size, int):
                    return self.validate_exception('file_size must be a integer')

            if 'file_name' in payment_policy_group_detail_value_file_list:
                file_name = content['file_name']
                if not isinstance(file_name, str):
                    return self.validate_exception('file_name must be a string')

            if 'file_content_type' in payment_policy_group_detail_value_file_list:
                file_content_type = content['file_content_type']
                if not isinstance(file_content_type, str):
                    return self.validate_exception('file_content_type must be a string')

    def create_policy_file(self, request):

        try: 
            payment_policy_id = int(request.POST['payment_policy_id'])
        except ValueError:
            return self.validate_exception('You have to input payment_policy_id')
        if not isinstance(payment_policy_id, int):
            return self.validate_exception('payment_policy_id is not integer field')
        try:
            payment_policy = SaleProjectPaymentPolicy.objects.get(id=payment_policy_id)
        except SaleProjectPaymentPolicy.DoesNotExist as ex:
            return self.validate_exception(str(ex))
        
        file = request.FILES['file']
        file_url, file_size, file_name, file_content_type = save_upload_file(file=file, sub_folder='payment_policy')

        payment_policy = SaleProjectPaymentPolicyFile.objects.create(
            project_payment_policy_id=payment_policy,
            file_url=file_url,
            file_size=file_size,
            file_name=file_name,
            file_content_type=file_content_type,
            created_at=datetime.now(),
            updated_at=None,
        )
        return self.response_success({
            'message': 'Create new group detail value file success',
            'group_file_id': payment_policy.id,
            'created_at': payment_policy.created_at
        }, status_code=status.HTTP_201_CREATED)

        if request.body:
            try:
                content = decode_to_json(request.body)
            except Exception as ex:
                return self.validate_exception('Parsing body to json error')

            key_content_list = list(content.keys())

            self.payment_policy_file_validate(content=content, payment_policy_file_list=key_content_list, is_created=True) 
            try:
                project_payment_policy = SaleProjectPaymentPolicy.objects.get(id=content['project_payment_policy_id'])
            except SaleProjectPaymentPolicy.DoesNotExist as ex:
                return self.validate_exception(str (ex))

            SaleProjectPaymentPolicyFile.objects.create(
                project_payment_policy_id=project_payment_policy,
                file_url=content['file_url'],
                file_size=content['file_size'],
                file_name=content['file_name'],
                file_content_type=content['file_content_type']
            )
        else:
            return self.validate_exception('payment policy file must be valuable')
                                
        return self.response_success({
            'message': 'Create new payment policy file success'
        }, status_code=status.HTTP_201_CREATED)      

    def delete_policy_file(self, request, **kwargs):
        params = request.query_params
        list_key_param = list(params.keys())
        if 'id' in list_key_param:
            try:
                payment_policy = SaleProjectPaymentPolicyFile.objects.get(id=int(params['id']))
            except SaleProjectPaymentPolicyFile.DoesNotExist as ex:
                return self.validate_exception(str(ex))
                
            payment_policy.delete()
            return Response({'message': 'Delete success'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return self.validate_exception('You have to input id param')

    def create_policy_group_file(self, request):

        try: 
            group_id = int(request.POST['group_id'])
        except ValueError:
            return self.validate_exception('You have to input detail_value_id')
        if not isinstance(group_id, int):
            return self.validate_exception('group_id is not integer field')
        try:
            detail_group = SaleProjectPaymentPolicyGroup.objects.get(id=group_id)
        except SaleProjectPaymentPolicyGroup.DoesNotExist as ex:
            return self.validate_exception(str(ex))
        
        file = request.FILES['file']
        file_url, file_size, file_name, file_content_type = save_upload_file(file=file, sub_folder='group')

        payment_policy_group = SaleProjectPaymentPolicyGroupFile.objects.create(
            project_payment_policy_group_id=detail_group,
            group_file_url=file_url,
            group_file_size=file_size,
            group_file_name=file_name,
            group_file_content_type=file_content_type,
            created_at=datetime.now(),
            updated_at=None,
        )
        return self.response_success({
            'message': 'Create new group detail value file success',
            'group_file_id': payment_policy_group.id,
            'created_at': payment_policy_group.created_at
        }, status_code=status.HTTP_201_CREATED)


    def delete_policy_group_file(self, request, **kwargs):
        params = request.query_params
        list_key_param = list(params.keys())
        if 'id' in list_key_param:
            try:
                payment_policy_group = SaleProjectPaymentPolicyGroupFile.objects.get(id=int(params['id']))
            except SaleProjectPaymentPolicyGroupFile.DoesNotExist as ex:
                return self.validate_exception(str(ex))
                
            payment_policy_group.delete()
            return Response({'message': 'Delete success'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return self.validate_exception('You have to input id param')

    def create_policy_group_detail_value_file(self, request):
        try:
            detail_value_id = int(request.POST['detail_value_id'])
        except ValueError:
            return self.validate_exception('You have to input detail_value_id')
        if not isinstance(detail_value_id, int):
            return self.validate_exception('group_detail_value_id is not integer field')
        try:
            detail_value = SaleProjectPaymentPolicyGroupDetailValue.objects.get(id=detail_value_id)
        except SaleProjectPaymentPolicyGroupDetailValue.DoesNotExist as ex:
            return self.validate_exception(str(ex))
    
        file = request.FILES['file']
        file_url, file_size, file_name, file_content_type = save_upload_file(file=file, sub_folder='detail_values')

        group_detail_value_file = SaleProjectPaymentPolicyGroupDetailValueFile.objects.create(
            project_payment_policy_group_detail_value_id=detail_value,
            file_url=file_url,
            file_size=file_size,
            file_name=file_name,
            file_content_type=file_content_type,
            created_at=datetime.now(),
            updated_at=None,
        )
        return self.response_success({
            'message': 'Create new group detail value file success',
            'group_detail_file_id': group_detail_value_file.id,
            'created_at': group_detail_value_file.created_at
        }, status_code=status.HTTP_201_CREATED)
    

    def delete_policy_group_detail_value_file(self, request, **kwargs):
        params = request.query_params
        list_key_param = list(params.keys())
        if 'id' in list_key_param:
            try:
                payment_policy_group_detail_value = SaleProjectPaymentPolicyGroupDetailValueFile.objects.get(id=int(params['id']))
            except SaleProjectPaymentPolicyGroupDetailValueFile.DoesNotExist as ex:
                return self.validate_exception(str(ex))
            payment_policy_group_detail_value.delete()
            return Response({'message': 'Delete success'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return self.validate_exception('You have to input id param')

  
    

      
        

        

        