from rest_framework.renderers import BaseRenderer


class PDFRenderer(BaseRenderer):
    media_type = "application/pdf"
    format = "pdf"
    charset = None

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # A view devolve HttpResponse pronto; este render() nunca é chamado no sucesso.
        # Existe só para a negociação de conteúdo aceitar "Accept: application/pdf".
        return data if data is not None else b""
