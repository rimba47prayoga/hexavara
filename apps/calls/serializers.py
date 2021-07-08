from rest_framework import serializers
from .models import CustomerDetail, CallRecord


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerDetail
        fields = [
            'id', 'name', 'phone', 'total_duration',
            'total_outgoing', 'total_incoming'
        ]


class SimpleCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDetail
        fields = [
            'id', 'name', 'phone'
        ]


class CallRecordSerializer(serializers.ModelSerializer):
    incoming = serializers.SerializerMethodField()
    outgoing = serializers.SerializerMethodField()
    type_call = serializers.SerializerMethodField()

    class Meta:
        model = CallRecord
        fields = [
            'id', 'incoming', 'incoming_number',
            'outgoing', 'outgoing_number',
            'duration', 'dialed_on', 'type_call'
        ]

    def __init__(self, *args, **kwargs):
        super(CallRecordSerializer, self).__init__(*args, **kwargs)
        self.customer = self.context.get('view').get_object()

    def get_incoming(self, instance):
        if self.get_type_call(instance) == 'outgoing':
            user = CustomerDetail.objects.get(phone=instance.incoming_number)
            serializer = SimpleCustomerSerializer(instance=user)
            return serializer.data
        return None

    def get_outgoing(self, instance):
        if self.get_type_call(instance) == 'incoming':
            user = CustomerDetail.objects.get(phone=instance.outgoing_number)
            serializer = SimpleCustomerSerializer(instance=user)
            return serializer.data
        return None

    def get_type_call(self, instance):
        if instance.incoming_number == self.customer.phone:
            return 'incoming'
        return 'outgoing'
