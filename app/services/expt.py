
class ServiceException(Exception):
    """Base exception for service layer"""
    pass

class TableNotFound(ServiceException):
    '''Table not found'''
    pass

class TableAlreadyReserv(ServiceException):
    '''Tavble already reserved'''
    pass
