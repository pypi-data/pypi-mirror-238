"""User facing template tags for htmx_datatables."""

from django import template

register = template.Library()


@register.inclusion_tag("htmx_datatables/data_table.html", takes_context=False)
def render_htmx_datatable(url: str, is_dark_mode: bool = False) -> dict:
    """Render HTML for data table with given url.

    Args:
        - url: Name of the URL for the corresponding data table view
        - is_dark_mode: wether to render in dark or light mode
    """
    return {"url_name": url, "is_dark_mode": int(is_dark_mode)}


@register.inclusion_tag("htmx_datatables/enable_htmx.html", takes_context=False)
def enable_htmx_js() -> dict:
    """Load htmx Javascript module and enable htmx for Django."""
    return {}
