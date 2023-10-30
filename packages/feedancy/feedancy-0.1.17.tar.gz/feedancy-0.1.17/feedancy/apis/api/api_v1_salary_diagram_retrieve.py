from __future__ import annotations

import datetime
import pydantic
import typing

from pydantic import BaseModel

from feedancy.lib.base import BaseApi
from feedancy.lib.request import ApiRequest
from feedancy.lib import json
class SalaryDiagram(BaseModel):
    count: int 
    salary: int 

def make_request(self: BaseApi,


) -> SalaryDiagram:
    

    
    body = None
    

    m = ApiRequest(
        method="GET",
        path="/api/v1/salary/diagram/".format(
            
        ),
        content_type=None,
        body=body,
        headers=self._only_provided({
        }),
        query_params=self._only_provided({
        }),
        cookies=self._only_provided({
        }),
    )
    return self.make_request({
    
        "200": {
            
                "application/json": SalaryDiagram,
            
        },
    
    }, m)