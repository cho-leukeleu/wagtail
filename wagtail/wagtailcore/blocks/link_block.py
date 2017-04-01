import json

from django import forms

from wagtail.wagtailcore import blocks

from wagtail.wagtailadmin import widgets


class LinkBlock(blocks.FieldBlock):

    def __init__(self, required=True, help_text=None, max_length=None, min_length=None, **kwargs):
        self.field = forms.CharField(
            required=required,
            help_text=help_text,
            max_length=max_length,
            min_length=min_length,
            widget=widgets.AdminLinkChooser()
        )
        super(LinkBlock, self).__init__(**kwargs)

    def value_for_form(self, value):
        """
        Reverse of value_from_form; convert a value of this block's native value type
        to one that can be rendered by the form field
        """
        if value:
            return json.dumps(value)
        return value

    def clean(self, value):
        """
        Gets value in the form of a string
        Converts it to a list of name/value tuples
        Returns something in the structure of a StructBlock

        """
        cleaned_data = []
        if value and isinstance(json.loads(value), dict):
            for name, value in json.loads(value).items():  # child is a BoundBlock instance
                cleaned_data.append(
                    (name, value)
                )
        return blocks.StructValue(self, cleaned_data)

    class Meta:
        icon = "site"
