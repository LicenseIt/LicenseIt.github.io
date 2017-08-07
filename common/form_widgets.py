from itertools import chain

from django import forms
from django.forms.utils import flatatt
from django.utils.encoding import force_text
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe


class SelectWithTitles(forms.RadioSelect):
    def __init__(self, *args, **kwargs):
        super(SelectWithTitles, self).__init__(*args, **kwargs)
        # Ensure the titles dict exists
        self.titles = {}
        self.auto_num = 0

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        final_attrs = dict(attrs, name=name)
        output = [format_html('<select {}>', flatatt(final_attrs))]
        options = self.render_options(choices, value)
        if options:
            output.append(options)
        output.append('</select>')
        return mark_safe('\n'.join(output))

    def render_options(self, choices, selected_choices):
        selected_choices = set(force_text(v) for v in selected_choices)
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(format_html('<optgroup label="{}">', force_text(option_value)))
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))
                output.append('</optgroup>')
            else:
                output.append(self.render_option(selected_choices, option_value, option_label))
        return '\n'.join(output)

    def render_option(self, selected_choices, option_value, option_label):
        title_html = (option_label in self.titles) and \
            ' title="%s" ' % escape(self.titles[option_label]) or ''
        option_value = option_value
        selected_html = (option_value in selected_choices) and ' selected="selected"' or ''
        return '<option %s value="%s" %s class="col-sm-12">%s</option>' % (
            title_html, escape(option_value), selected_html, option_label)


class SelectMultipleWithTitles(forms.CheckboxSelectMultiple):
    def __init__(self, *args, **kwargs):
        super(SelectMultipleWithTitles, self).__init__(*args, **kwargs)
        # Ensure the titles dict exists
        self.titles = {}
        self.auto_num = 0

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        final_attrs = dict(attrs, name=name)
        output = [format_html('<div {}>', flatatt(final_attrs))]
        options = self.render_options(choices, value)
        if options:
            output.append(options)
        output.append('</div>')
        return mark_safe('\n'.join(output))

    def render_options(self, choices, selected_choices):
        selected_choices = set(force_text(v) for v in selected_choices)
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(format_html('<optgroup label="{}">', force_text(option_value)))
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))
                output.append('</optgroup>')
            else:
                output.append(self.render_option(selected_choices, option_value, option_label))
        return '\n'.join(output)

    def render_option(self, selected_choices, option_value, option_label):
        title_html = (option_label in self.titles) and \
            ' title="%s" ' % escape(self.titles[option_label]) or ''
        option_value = option_value
        selected_html = (option_value in selected_choices) and ' checked' or ''
        return '<div class=form-group><label class="col-sm-12" %s>'' \
        ''<span class="col-sm-1"><input type="checkbox" name="%s" value="%s" %s></span>%s</label></div>' % (
            title_html, 'distribution', escape(option_value), selected_html, option_label)


class ChoiceFieldWithTitles(forms.ModelMultipleChoiceField):
    widget = SelectWithTitles

    def __init__(self, queryset=(), *args, **kwargs):
        super(ChoiceFieldWithTitles, self).__init__(queryset, *args, **kwargs)
        self.widget.titles = dict([(c.name, c.explanation) for c in queryset.all()])


class MultipleChoiceFieldWithTitles(forms.ModelMultipleChoiceField):
    widget = SelectMultipleWithTitles

    def __init__(self, queryset=(), *args, **kwargs):
        super(MultipleChoiceFieldWithTitles, self).__init__(queryset, *args, **kwargs)
        self.widget.titles = dict([(c.name, c.explanation) for c in queryset.all()])
