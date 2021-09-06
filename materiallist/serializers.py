from rest_framework import serializers
from materiallist.models import Transactions

class Transactserializers(serializers.ModelSerializer):

    class Meta:
        model = Transactions
        fields = '__all__'