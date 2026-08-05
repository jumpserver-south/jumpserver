from rest_framework import serializers

from django.utils.translation import gettext_lazy as _
from tickets.models import ApplyLoginAssetTicket
from .ticket import TicketApplySerializer

__all__ = [
    'LoginAssetReviewSerializer'
]


class LoginAssetReviewSerializer(TicketApplySerializer):
    apply_reason = serializers.SerializerMethodField(label=_('Apply reason'))
    apply_operation_content = serializers.SerializerMethodField(label=_('Operation content'))
    apply_operation_duration = serializers.SerializerMethodField(label=_('Operation duration'))

    class Meta:
        model = ApplyLoginAssetTicket
        writeable_fields = ['apply_login_user', 'apply_login_asset', 'apply_login_account']
        fields = TicketApplySerializer.Meta.fields + writeable_fields + [
            'apply_reason', 'apply_operation_content', 'apply_operation_duration'
        ]

    def get_apply_reason(self, obj):
        return obj.meta.get('apply_reason', '')

    def get_apply_operation_content(self, obj):
        return obj.meta.get('apply_operation_content', '')

    def get_apply_operation_duration(self, obj):
        return obj.meta.get('apply_operation_duration', '')
