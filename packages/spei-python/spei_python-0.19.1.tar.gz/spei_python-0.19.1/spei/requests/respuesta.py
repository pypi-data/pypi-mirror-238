from lxml import etree

from spei.resources import Respuesta

SOAP_NS = 'http://schemas.xmlsoap.org/soap/envelope/'
PRAXIS_NS = 'http://www.praxis.com.mx/'


class RespuestaElement(object):
    def __new__(cls, element):
        respuesta = etree.Element(
            etree.QName(PRAXIS_NS, 'respuesta'),
            nsmap={None: PRAXIS_NS},
        )
        mensaje = etree.tostring(element, xml_declaration=True, encoding='cp850')
        respuesta.text = mensaje
        return respuesta


class BodyElement(object):
    def __new__(cls, respuesta):
        body = etree.Element(etree.QName(SOAP_NS, 'Body'))
        body.append(respuesta)
        return body


class EnvelopeElement(object):
    def __new__(cls, body):
        etree.register_namespace('S', SOAP_NS)
        envelope = etree.Element(etree.QName(SOAP_NS, 'Envelope'))
        envelope.append(body)
        return envelope


class RespuestaRequest(object):
    def __new__(cls, mensaje: Respuesta, as_string=True):
        envelope = RespuestaElement(mensaje.build_xml())
        if not as_string:
            return envelope
        return etree.tostring(envelope, xml_declaration=True, encoding='utf-8')
