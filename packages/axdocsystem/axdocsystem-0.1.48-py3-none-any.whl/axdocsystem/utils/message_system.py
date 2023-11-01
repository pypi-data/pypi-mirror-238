import re
import os
import aiofiles
from typing import Tuple, Union
from .notification_system import NotificationSystem


DEFAULT_PATH = f"{os.path.dirname(__file__)}/message_templates" 


class MessageSystem:
    def __init__(self, notification_system: NotificationSystem, system_name = '[undefined]', templates_path = DEFAULT_PATH) -> None:
        self.system_name = system_name
        self._templates_path = templates_path
        self.notification_system = notification_system
        self.title_pattern = re.compile(r"<title>([\s\S]*?)</title>") 

    def _seperate_title_and_body(self, html: str) -> Tuple[str, str]:
        title = ''
        title_match = self.title_pattern.search(html)
        if title_match:
            title = title_match.group(1).strip()
            html = self.title_pattern.sub("", html)
        return title, html

    async def _send_template(self, template_name: str, receiver: str, data: dict, title: Union[str, None] = None, *, parse_mode = 'html'):
        data = {'system_name': self.system_name, **data}
        async with aiofiles.open(f"{self._templates_path}/{template_name}", "r") as f:
            temp = (await f.read()).format(**data)
            temp_title, content = self._seperate_title_and_body(temp)
            title = title or temp_title
            return await self.notification_system.send(
                content=content,
                receiver=receiver,
                title=title,
                parse_mode=parse_mode,
            )

    async def send_verification_code(self, receiver: str, code: str):
        return await self._send_template(
            template_name='email_verification.html',
            receiver=receiver,
            data={
                "code": code
            }
        )

    async def send_forgot_reset_passwd_code(self, receiver: str, name: str, code: str):
        return await self._send_template(
            template_name='forgot_passwd.html',
            receiver=receiver,
            data={
                'name': name,
                'code': code,
            }
        )

