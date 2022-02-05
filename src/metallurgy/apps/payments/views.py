from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
import requests
import json

from django.urls import reverse

from .models import Payment
from ..projects.models import Factor

# Create your views here.

MERCHANT = settings.ZARINPAL_GATEWAY_SETTINGS['MERCHANT']
ZP_API_REQUEST = settings.ZARINPAL_GATEWAY_SETTINGS['ZP_API_REQUEST']
ZP_API_VERIFY = settings.ZARINPAL_GATEWAY_SETTINGS['ZP_API_VERIFY']
ZP_API_STARTPAY = settings.ZARINPAL_GATEWAY_SETTINGS['ZP_API_STARTPAY']
description = settings.ZARINPAL_GATEWAY_SETTINGS['description']
email = settings.ZARINPAL_GATEWAY_SETTINGS['email']
mobile = settings.ZARINPAL_GATEWAY_SETTINGS['mobile']
CallbackURL = settings.ZARINPAL_GATEWAY_SETTINGS['CallbackURL']


def zarinpal_send_request(request):
    factor_id = request.GET.get('f_id')
    if not factor_id:
        raise Http404

    factor = get_object_or_404(Factor, pk=factor_id)
    rial_amount = factor.get_total_factor_price() * 10
    for payment in factor.payments.all():
        if payment.status:
            raise Http404

    req_data = {
        "merchant_id": MERCHANT,
        "amount": rial_amount,
        "callback_url": CallbackURL,
        "description": description,
        "metadata": {"mobile": mobile, "email": email}
    }
    req_header = {"accept": "application/json",
                  "Content-Type": "application/json"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
        req_data), headers=req_header)
    authority = req.json()['data']['authority']
    pay = Payment.objects.create(
        factor=factor,
        user=request.user,
        amount=rial_amount,
        authority=req.json()['data']['authority'][::-1][:4],
        message=req.json()['data']['message']
    )

    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


def zarinpal_verify(request):
    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']

    payment = get_object_or_404(Payment, authority=t_authority[::-1][:4])

    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": payment.amount,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        print(req.json())
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                payment.ref_id = req.json()['data']['ref_id']
                payment.card_number = req.json()['data']['card_pan']
                payment.status = True
                payment.factor.is_paid = True
                payment.save()
                payment.factor.save()
                return HttpResponse(
                    f'تراکنش موفق.\nشماره مرجع: ' + str(
                        req.json()['data']['ref_id']
                    ) + f'</br> <a href="/projects/factor/{payment.factor.project.pk}/{payment.factor.pk}">بازگشت به صفحه فاکتور</a>')
            elif t_status == 101:
                return HttpResponse('Transaction submitted :  ' + str(
                    req.json()['data']['message']
                ) + f'</br> <a href="/projects/factor/{payment.factor.project.pk}/{payment.factor.pk}">بازگشت به صفحه فاکتور</a>')
            else:
                return HttpResponse('Transaction failed.\nStatus:  </br> <a href="/projects/factor/{payment.factor.project.pk}/{payment.factor.pk}">بازگشت به صفحه فاکتور</a>' + str(
                    req.json()['data']['message']
                ))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
    else:
        return HttpResponse('Transaction failed or canceled by user')
