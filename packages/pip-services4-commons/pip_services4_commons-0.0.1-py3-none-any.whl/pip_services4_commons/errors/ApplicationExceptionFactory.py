# -*- coding: utf-8 -*-
"""
    pip_services4_commons.errors.ApplicationExceptionFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Application error factory implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from .ApplicationException import ApplicationException
from .BadRequestException import BadRequestException
from .ConfigException import ConfigException
from .ConflictException import ConflictException
from .ConnectionException import ConnectionException
from .ErrorCategory import ErrorCategory
from .FileException import FileException
from .InternalException import InternalException
from .InvocationException import InvocationException
from .NotFoundException import NotFoundException
from .UnauthorizedException import UnauthorizedException
from .UnknownException import UnknownException
from .UnsupportedException import UnsupportedException
from ..errors.ErrorDescription import ErrorDescription


class ApplicationExceptionFactory:
    """
    Factory to recreate exceptions from :class:`ErrorDescription <pip_services4_commons.errors.ErrorDescription.ErrorDescription>` values passed through the wire.
    """

    @staticmethod
    def create(description: ErrorDescription) -> ApplicationException:
        """
        Recreates ApplicationException object from serialized ErrorDescription.

        It tries to restore original error type using type or error category fields.

        :param description: a serialized error description received as a result of remote call

        :return: ApplicationException object from serialized ErrorDescription.
        """
        if not description:
            raise Exception("Description cannot be null")

        error: ApplicationException

        # Create well-known error type based on error category
        if ErrorCategory.Unknown == description.category:
            error = UnknownException(description.trace_id, description.code, description.message)
        elif ErrorCategory.Internal == description.category:
            error = InternalException(description.trace_id, description.code, description.message)
        elif ErrorCategory.Misconfiguration == description.category:
            error = ConfigException(description.trace_id, description.code, description.message)
        elif ErrorCategory.NoResponse == description.category:
            error = ConnectionException(description.trace_id, description.code, description.message)
        elif ErrorCategory.FailedInvocation == description.category:
            error = InvocationException(description.trace_id, description.code, description.message)
        elif ErrorCategory.FileError == description.category:
            error = FileException(description.trace_id, description.code, description.message)
        elif ErrorCategory.BadRequest == description.category:
            error = BadRequestException(description.trace_id, description.code, description.message)
        elif ErrorCategory.Unauthorized == description.category:
            error = UnauthorizedException(description.trace_id, description.code, description.message)
        elif ErrorCategory.Conflict == description.category:
            error = ConflictException(description.trace_id, description.code, description.message)
        elif ErrorCategory.NotFound == description.category:
            error = NotFoundException(description.trace_id, description.code, description.message)
        elif ErrorCategory.Unsupported == description.category:
            error = UnsupportedException(description.trace_id, description.code, description.message)
        else:
            error = UnknownException()
            error.category = description.category
            error.status = description.status

        # Fill error with details
        error.details = description.details
        error.set_cause_string(description.cause)
        error.set_stack_trace_string(description.stack_trace)

        return error
