# -*- coding: utf-8 -*-
"""
    pip_services4_commons.errors.ErrorDescription
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Error description implementation

    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
import json
from typing import Any, Optional, Dict


class ErrorDescription:
    """
    Serializeable error description. It is use to pass information about errors
    between microservices implemented in different languages. On the receiving side
    :class:`ErrorDescription <pip_services4_commons.errors.ErrorDescription.ErrorDescription>` is used to recreate error object close to its original type
    without missing additional details.
    """

    def __init__(self):
        self.type: Optional[str] = None
        self.category: Optional[str] = None
        self.status: Optional[int] = None
        self.code: Optional[str] = None
        self.message: Optional[str] = None
        self.details: Any = None
        self.trace_id: Optional[str] = None
        self.cause: Optional[str] = None
        self.stack_trace: Optional[str] = None

    def to_json(self) -> Dict[str, Any]:
        return {
            'type': self.type,
            'category': self.category,
            'status': self.status,
            'code': self.code,
            'message': self.message,
            'details': self.details,
            'trace_id': self.trace_id,
            'cause': self.cause,
            'stack_trace': self.stack_trace
        }

    @staticmethod
    def from_json(json_err: Dict[str, Any]) -> Any:
        if isinstance(json_err, str):
            json_err = json.loads(json_err)

        if not isinstance(json_err, dict):
            return json_err

        error = ErrorDescription()
        error.type = json_err.get('type')
        error.category = json_err.get('category')
        error.status = json_err.get('status')
        error.code = json_err.get('code')
        error.message = json_err.get('message')
        error.details = json_err.get('details')
        error.trace_id = json_err.get('trace_id')
        error.cause = json_err.get('cause')
        error.stack_trace = json_err['stack_trace']
        return error
