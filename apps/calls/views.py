from django.db import connection
from django.db.models import Q
from rest_framework.decorators import action, api_view
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from .models import CustomerDetail, CallRecord
from .serializers import CustomerSerializer, CallRecordSerializer


@api_view(['GET'])
def customer_total_costs(request):
    query = """
        SELECT name,
        (SUM(outgoing_bayar) + inner_customer.incoming_bayar) as bayar
         FROM (
            SELECT customer.id, customer.name,
            customer.phone,
            (CASE WHEN
                    customer.subscription_id IS NULL
                THEN
                    (500 + ((SUM(call_record.duration) - 120) * 2))
                ELSE
                    (CASE WHEN 
                            (500 + ((SUM(call_record.duration) - 120) * 2)) > subscription_plan.quota
                        THEN
                            (500 + ((SUM(call_record.duration) - 120) * 2)) - subscription_plan.quota
                        ELSE
                            0
                    END)
                END) as outgoing_bayar
            FROM call_record
            INNER JOIN customer_detail customer
            ON call_record.outgoing_number = customer.phone
            LEFT OUTER JOIN subscription_plan
            ON customer.subscription_id = subscription_plan.id
            GROUP BY MONTH(call_record.dialed_on), customer.id, customer.subscription_id
        ) AS outer_customer
        JOIN (
            SELECT customer_detail.id as icustomer_id, customer_detail.name as iname, 
                (CASE WHEN 
                    call_record.incoming_number IS NULL
                THEN
                    0
                ELSE
                    SUM(call_record.duration)
                END) as incoming_bayar
            FROM customer_detail
            LEFT JOIN call_record
            ON call_record.incoming_number = customer_detail.phone
            GROUP BY customer_detail.id
        ) as inner_customer
        ON outer_customer.name = inner_customer.iname
        GROUP BY outer_customer.id, inner_customer.icustomer_id
        ORDER BY outer_customer.name;
    """

    cursor = connection.cursor()
    cursor.execute(query)


class CustomerViewSet(ListModelMixin,
                      RetrieveModelMixin,
                      GenericViewSet):
    queryset = CustomerDetail.objects.all().order_by('name')
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'history':
            return CallRecordSerializer
        return super(CustomerViewSet, self).get_serializer_class()

    @action(methods=['GET'], detail=True)
    def history(self, request, *args, **kwargs):
        instance = self.get_object()
        queryset = CallRecord.objects.filter(
            Q(incoming_number=instance.phone) |
            Q(outgoing_number=instance.phone)
        ).order_by('-dialed_on')
        queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(instance=queryset, many=True)
        return self.get_paginated_response(serializer.data)
