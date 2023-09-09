import telethon.errors.rpcerrorlist
from django.shortcuts import render
from forms import GetUserPhone, GetUserCode
from .hossein_telegram_client import HosseinTelegramClient
import os
from django.http import HttpResponseRedirect
import shutil
import jwt
from .models import Users, Channels
from asgiref.sync import async_to_sync

async def get_phone_number(request):
    if request.method == 'POST':
        form = GetUserPhone(request.POST)
        phone = request.POST.get('phone_number')
        phone = '+' + phone
        parent_dir = "C:\\Users\\Admin\\PycharmProjects\\eitaa_sender\\eitaa_programms"
        path = os.path.join(parent_dir, phone)
        if not os.path.exists(path):
            api_id = 86576
            api_hash = "385886b58b21b7f3762e1cde2d651925"
            environment = 'Windows'
            if environment == 'Windows':
                client = HosseinTelegramClient(phone, api_id, api_hash, proxy=('socks5', '127.0.0.1', 10808))
            else:
                client = HosseinTelegramClient(phone, api_id, api_hash)
            await client.connect()
            try:
                phone_code_hash = await client.send_code_request(phone)
            except telethon.errors.rpcerrorlist.PhoneNumberInvalidError:
                await client.disconnect()
                os.remove(f"C:\\Users\\Admin\\PycharmProjects\\eitaa_sender\\{phone}.session")
                return render(request, 'eitaa/home.html', {'message': 'phone is invalid!', 'form': form})
            await client.disconnect()
            jwt_json = {'phone_number': phone, 'phone_code_hash': phone_code_hash.phone_code_hash}
            token = jwt.encode(jwt_json,'Ghased',algorithm="HS256")
            code_form = GetUserCode(initial={'jwt_code':token})
            return render(request, 'eitaa/code.html', {'form': code_form})
        else:
            return render(request, 'eitaa/home.html', {'message': 'this phone number is in use!', 'form': form})
    else:
        form = GetUserPhone()
    return render(request, "eitaa/home.html", {'form': form})


async def get_login_code(request):
    if request.method == 'POST':
        form = GetUserCode(request.POST)
        code = request.POST.get('code')
        token = request.POST.get('jwt_code')
        values = jwt.decode(token,'Ghased',algorithms=['HS256'])
        phone = values.get('phone_number')
        phone_code_hash = values.get('phone_code_hash')
        api_id = 86576
        api_hash = '385886b58b21b7f3762e1cde2d651925'
        client = HosseinTelegramClient(phone, api_id, api_hash, proxy=('socks5', '127.0.0.1', 10808))
        await client.connect()
        try:
            user = await client.sign_in(phone, code, phone_code_hash=phone_code_hash)
            me = await client.get_me()
            me_id = me.id
            await Users.objects.acreate(user_id=me_id, token=None)
        except telethon.errors.rpcerrorlist.PhoneCodeExpiredError:
            os.remove(f"C:\\Users\\Admin\\PycharmProjects\\eitaa_sender\\{phone}.session")
            return render(request, 'eitaa/code.html', {'message': 'code timeout!Go back to home page', 'form': form})
        except telethon.errors.rpcerrorlist.PhoneCodeInvalidError:
            return render(request, 'eitaa/code.html', {'message': 'code is invalid!', 'form': form})
        await client.disconnect()
        parent_dir = 'C:\\Users\\Admin\\PycharmProjects\\eitaa_sender\\eitaa_programms'
        src_dir = 'C:\\Users\\Admin\\PycharmProjects\\eitaa_sender\\Raw_programs'
        path = os.path.join(parent_dir, phone)
        os.mkdir(path)
        files = os.listdir(src_dir)
        for fname in files:
            # copying the files to the
            # destination directory
            shutil.copy2(os.path.join(src_dir, fname), path)
        return HttpResponseRedirect('/home/')
    else:
        form = GetUserCode()
    return render(request, "eitaa/code.html", {'form': form})
