class PoeExceptions(Exception):
    """Base exception class"""
    pass


class ResourceNotFoundException(PoeExceptions):
    """Server answer {'error': {'code': 1, 'message': 'Resource not found'}}"""
    def __str__(self):
        return 'Character not found'
