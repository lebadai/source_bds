from django.shortcuts import render

from django.views.generic import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from . models import (
    SaleProjectPaymentPolicy,
    SaleProjectPaymentPolicyFile
)

class PaymentPolicyView(View):
    def get(self, request, *args, **kwargs):
        payment_policies = list(SaleProjectPaymentPolicy.objects.values())
        if payment_policies:
            return JsonResponse(payment_policies, safe=False)
        return JsonResponse(({"payment policies": "empty list"}))
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentPolicyView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = request.body.decode('utf8')
        data = json.loads(data)
        try:
            new_payment_policy = SaleProjectPaymentPolicy(
                uniprime_project_id=data["uniprime_project_id"],
                name=data["name"],
                start_date=data["start_date"],
                end_date=data["end_date"],
                active_flag=data["active_flag"],
                project_sell_open_id=data["project_sell_open_id"],
                deleted_flag=data["deleted_flag"],
                project_sale_id=data["project_sale_id"],

            )
            new_payment_policy.save()
            return JsonResponse({"created": data}, safe=False)
        except Exception:
            return JsonResponse({"error": "not a valid data"}, safe=False)

class PaymentPolicylViewDetail(View):
    def get(self, request, pk):
        payment_policy = {"payment_policy": list(SaleProjectPaymentPolicy.objects.filter(pk=pk).values())}
        if payment_policy["payment_policy"]:
            return JsonResponse(payment_policy, safe=False)
        else:
            return JsonResponse({"error": "payment policy id does not exist"})
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentPolicylViewDetail, self).dispatch(request, *args, **kwargs)
    
    def put(self, request, pk):
        data = request.body.decode('utf8')
        data = json.loads(data)
        try:
            selected_payment_policy = SaleProjectPaymentPolicy.objects.get(pk=pk)
            data_key = list(data.keys())
            for key in data_key:
                if key == "uniprime_project_id":
                    selected_payment_policy.uniprime_project_id = data["uniprime_project_id"]
                if key == "name":
                    selected_payment_policy.name = data["name"]
                if key == "start_date":
                    selected_payment_policy.start_date = data["start_date"]
                if key == "end_date":
                    selected_payment_policy.end_date = data["end_date"]
                if key == "active_flag":
                    selected_payment_policy.active_flag = data["active_flag"]
                if key == "project_sell_open_id":
                    selected_payment_policy.project_sell_open_id = data["project_sell_open_id"]
                if key == "deleted_flag":
                    selected_payment_policy.deleted_flag = data["deleted_flag"]
                if key == "project_sale_id":
                    selected_payment_policy.project_sale_id = data["project_sale_id"]
                selected_payment_policy.save()
                return JsonResponse({"update": data})
        except SaleProjectPaymentPolicy.DoesNotExist:
            return JsonResponse({
                "payment_policy_id": pk,
                "error": "primary key does not exist"
            })
        except Exception:
            return JsonResponse({
                "payment_policy_id": pk,
                "error": "not a valid payment policy id"
            })
    def delete(self, request, pk):
        try:
            selected_payment_policy = SaleProjectPaymentPolicy.objects.get(pk=pk)
            selected_payment_policy.delete()
            return JsonResponse({"payment_policy_id": pk, "deleted": True})
        except PaymentPolicy.DoesNotExist:
            return JsonResponse({
                "payment_policy_id": pk,
                "error": "payment policy id does not exists"
            })
class PaymentPolicyFileView(View):
    def get(self, request, *args, **kwargs):
        payment_policy_files = list(SaleProjectPaymentPolicyFile.objects.values())
        if payment_policy_files:
            return JsonResponse(payment_policy_files, safe=False)
        return JsonResponse({"payment policy files": "empty list!"})

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentPolicyFileView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        data = request.body.decode('utf8')
        data = json.loads(data)
        print(data)
        try:
            new_payment_policy_detail = SaleProjectPaymentPolicyFile(
                project_payment_policy_id_id=data["project_payment_policy_id"],
                file_url=data["file_url"],
                file_size=data["file_size"],
                file_name=data["file_name"],
                file_content_type=data["file_content_type"],
                deleted_flag=data["deleted_flag"],
                file_type=data["file_type"],
            )
            new_payment_policy_detail.save()
            return JsonResponse({"created": data}, safe=False)

        except:
            return JsonResponse({"error": "not a valid data"}, safe=False)

class PaymentPolicyFileDetailView(View):
    def get(self, request, pk):
        payment_policy_files = {"payment_policy_files": list(SaleProjectPaymentPolicyFile.objects.filter(pk=pk).values())}
        if payment_policy_files["payment_policy_files"]:
            return JsonResponse(payment_policy_files, safe=False)
        else:
            return JsonResponse({"error": "payment policy id does not exist"})
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentPolicyFileDetailView, self).dispatch(request, *args, **kwargs)
    
    def put(self, request, pk):
        data = request.body.decode('utf8')
        data = json.loads(data)
 
        try:
            selected_payment_policy_file = SaleProjectPaymentPolicyFile.objects.get(pk=pk)
            data_key = list(data.keys())
            for key in data_key:
                if key == "project_payment_policy_detail_value_id":
                    selected_payment_policy_file.project_payment_policy_detail_value_id = data["project_payment_policy_detail_value_id"]
                if key == "file_url":
                    selected_payment_policy_file.file_url = data["file_url"]
                if key == "file_size":
                    selected_payment_policy_file.file_size = data["file_size"]
                if key == "file_name":
                    selected_payment_policy_file.file_name = data["file_name"]
                if key == "file_content_type":
                    selected_payment_policy_file.file_content_type = data["file_content_type"]
                if key == "deleted_flag":
                    selected_payment_policy_file.deleted_flag = data["deleted_flag"]
               
                selected_payment_policy_file.save()
                return JsonResponse({"update": data})
        except SaleProjectPaymentPolicyFile.DoesNotExist:
            return JsonResponse({
                "payment_policy_id": pk,
                "error": "primary key does not exist"
            })
        except Exception:
            return JsonResponse({
                "payment_policy_id": pk,
                "error": "not a valid payment policy id"
            })
    def delete(self, request, pk):
        try:
            selected_payment_policy_file = SaleProjectPaymentPolicyFile.objects.get(pk=pk)
            selected_payment_policy_file.delete()
            return JsonResponse({"payment_policy_id": pk, "deleted": True})
        except PaymentPolicy.DoesNotExist:
            return JsonResponse({
                "payment_policy_id": pk,
                "error": "payment policy id does not exists"
            })

class PaymentPolicyProjectView(View):
    def get(self, request, *args, **kwargs):
        payment_policies = list(PaymentPolicy.objects.values())
        if payment_policies:
            return JsonResponse(payment_policies, safe=False)
        return JsonResponse({"payment policies": "empty list"})