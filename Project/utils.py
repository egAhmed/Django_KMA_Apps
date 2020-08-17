# import cStringIO as StringIO
from io import BytesIO  
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
#################################
# import functools
# from django.conf import settings
# from .views import MyModelView
# from django_weasyprint import WeasyTemplateResponseMixin
# from django_weasyprint.views import CONTENT_TYPE_PNG

# class CustomWeasyTemplateResponse(WeasyTemplateResponse):
#     # customized response class to change the default URL fetcher
#     def get_url_fetcher(self):
#         # disable host and certificate check
#         context = ssl.create_default_context()
#         context.check_hostname = False
#         context.verify_mode = ssl.CERT_NONE
#         return functools.partial(django_url_fetcher, ssl_context=context)

# class MyModelPrintView(WeasyTemplateResponseMixin, MyModelView):
#     # output of MyModelView rendered as PDF with hardcoded CSS
#     pdf_stylesheets = [
#         settings.STATIC_ROOT + 'css/app.css',
#     ]
#     # show pdf in-line (default: True, show download dialog)
#     pdf_attachment = False
#     # custom response class to configure url-fetcher
#     response_class = CustomWeasyTemplateResponse

# class MyModelDownloadView(WeasyTemplateResponseMixin, MyModelView):
#     # suggested filename (is required for attachment/download!)
#     pdf_filename = 'foo.pdf'

# class MyModelImageView(WeasyTemplateResponseMixin, MyModelView):
#     # generate a PNG image instead
#     content_type = CONTENT_TYPE_PNG

    # dynamically generate filename
    # def get_pdf_filename(self):
    #     return 'foo-{at}.pdf'.format(
    #         at=timezone.now().strftime('%Y%m%d-%H%M'),
    #     )


