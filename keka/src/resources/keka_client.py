from typing import Union

from .HR import Employee
from .Helpdesk import TicketManagement
from .Auth.auth import KekaAuth


class KekaClient:

    __slots__ = ('instance_url', 'hr', 'helpdesk')

    def __init__(self, auth: Union[str, KekaAuth], instance_url: str):
        self.instance_url = instance_url

        # Pass authenticated client and token to child classes
        self.hr = Employee(instance_url, auth)
        self.helpdesk = TicketManagement(instance_url, auth)
    
