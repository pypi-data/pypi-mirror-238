from lxml import etree

from spei.resources import Orden


class MensajeElement(object):
    def __new__(cls, ordenpago, orden_cls: Orden = Orden):
        mensaje = etree.fromstring(  # noqa: S320
            bytes(ordenpago.text, encoding='cp850'),
        )
        return orden_cls.parse_xml(mensaje)


class OrdenPagoElement(object):
    def __new__(cls, body):
        return body.find('{http://www.praxis.com.mx/}ordenpago')


class BodyElement(object):
    def __new__(cls, mensaje):
        return mensaje.find(
            '{http://schemas.xmlsoap.org/soap/envelope/}Body',
        )


class OrdenResponse(object):
    def __new__(cls, orden):
        mensaje = etree.fromstring(orden)  # noqa: S320
        return MensajeElement(OrdenPagoElement(BodyElement(mensaje)))
