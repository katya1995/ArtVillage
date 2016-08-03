import urllib2
import requests
url = "https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_notify-validate&protection_eligibility=Eligible&last_name=buyer&txn_id=2BV0182350041223Y&receiver_email=katq1995-2@gmail.com&paymen\
t_status=Completed&payment_gross=&tax=0.00&residence_country=US&address_state=&payer_status=verified&txn_type=web_accept&address_street=9 Elm Street\
Apt 5&handling_amount=0.00&payment_date=16:27:46 Aug 02, 2016 PDT&first_name=test&item_name=Teddy Bear&address_country=United Kingdom&charset=windows-1252&custom=kat1995&notify_versi\
on=3.8&address_name=John Doe&test_ipn=1&item_number=item id&receiver_id=FW8PVG7JS8LZY&transaction_subject=&business=katq1995-2@gmail.com&payer_id=XKAFW65VPKXJN&auth=AjtQyquVoKuysMOg.\
zrP1VyPhZ7HVQAC-K0k32Myenw-bWf4ywnjCHs1eMcjY58GXWt2UBjjzkWBE42vjxHRGPQ&verify_sign=AFcWxV21C7fd0v3bYYYRCpSSRl31AjzHPLU4k38wdPd-iJmd-4WOvAI8&address_zip=19312&payment_fee=&address_cou\
ntry_code=GB&address_city=Berwyn&address_status=confirmed&mc_fee=4.14&mc_currency=GBP&shipping=1.00&payer_email=anelyka-buyer@abv.bg&payment_type=instant&mc_gross=101.00&quantity=1"

print(requests.get(url=url))
