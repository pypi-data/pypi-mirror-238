# Exceptions

class XangoError(Exception): pass
class AdapterError(XangoError): pass
class CollectionNotFoundError(XangoError): pass
class CollectionExistsError(XangoError): pass
class ItemNotFoundError(XangoError):pass
class ItemExistsError(XangoError):pass
class NoResultsError(XangoError): pass
class ConstraintError(XangoError): pass
class UndeletableError(XangoError): pass
class MissingCommitterCallbackError(XangoError): pass
class MissingItemKeyError(XangoError): pass
class InvalidItemPathError(XangoError): pass 
class MutationTypeError(XangoError): pass
