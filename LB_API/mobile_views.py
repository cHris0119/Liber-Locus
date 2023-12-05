from rest_framework.decorators import api_view
from .models import PurchaseDetail, PurchaseDetailState
from rest_framework import status
from rest_framework.response import Response 


@api_view(['POST'])
def productReceived(request, id):
    try:
        data = request.data
        state = PurchaseDetailState.objects.get(id = 3)
        purchase = PurchaseDetail.objects.get(id = id)
        
        if not purchase:
            return Response({"error": "Pedido no encontrado"},status=status.HTTP_400_BAD_REQUEST)
        
        if not state:
            return Response({"error": "Estado no encontrado"},status=status.HTTP_400_BAD_REQUEST)
        
        if data['confirm_key'] == purchase.code_verify:
            purchase.purchase_detail_state = state
            purchase.save()
        return Response({'Ok': "El pedido fue confirmado correctamente"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"Error": e}, status=status.HTTP_400_BAD_REQUEST)
    

        
