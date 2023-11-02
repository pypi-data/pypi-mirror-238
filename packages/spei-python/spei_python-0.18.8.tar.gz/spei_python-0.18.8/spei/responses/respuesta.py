from lxml import etree

from spei.resources import Respuesta


class MensajeElement(object):
    def __new__(cls, respuesta, respuesta_cls: Respuesta = Respuesta):
        mensaje = etree.fromstring(  # noqa: S320
            bytes(respuesta.text, encoding='cp850'),
        )
        return respuesta_cls.parse_xml(mensaje)


class RespuestaElement(object):
    def __new__(cls, body):
        return body.find('{http://www.praxis.com.mx/}respuesta')


class BodyElement(object):
    def __new__(cls, mensaje):
        return mensaje.find(
            '{http://schemas.xmlsoap.org/soap/envelope/}Body',
        )


class RespuestaResponse(object):
    def __new__(cls, respuesta):
        mensaje = etree.fromstring(respuesta)  # noqa: S320
        return MensajeElement(RespuestaElement(BodyElement((mensaje))))
