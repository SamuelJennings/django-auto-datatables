from rest_framework import serializers


class AutoTableSerializerMixin:
    absolute_url_button = serializers.SerializerMethodField()

    def get_absolute_url_button(self, obj):
        template = self.button_template()
        return template.format(obj.get_absolute_url())

    def button_template(self):
        return "<a href='{}' class='btn btn-primary'>View</a>"


class AutoTableModelSerializer(serializers.ModelSerializer):
    pass
