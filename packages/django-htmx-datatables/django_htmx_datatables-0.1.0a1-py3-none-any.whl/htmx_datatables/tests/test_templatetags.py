from django.template import RequestContext, Template
from django.test import RequestFactory, TestCase


class TestTemplateTags(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.factory = RequestFactory()

    def test_should_render_datatable(self):
        # given
        template = Template(
            '{% load htmx_datatables %}{% render_htmx_datatable url="admin:index" %}'
        )
        request = self.factory.get("/my-page")
        context = RequestContext(request, {})
        # when
        result = template.render(context)
        # then
        self.assertIn("Loading a data table via htmx", result)

    def test_should_render_with_js_tag(self):
        # given
        template = Template("{% load htmx_datatables %}{% enable_htmx_js %}")
        request = self.factory.get("/my-page")
        context = RequestContext(request, {})
        # when
        result = template.render(context)
        # then
        self.assertIn("<script>", result)
