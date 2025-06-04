from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from common.utils import CommonUtils

class HealthView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        """
        @description: This API used to check if server is active or not
        @param request:
        @return: "SUCCESS"
        """
        try:
            return CommonUtils.dispatch_success("SUCCESS")
        except Exception as e:
            # Fallback simple response if CommonUtils fails
            return Response({
                'status': 'success', 
                'data': 'BASIC_SUCCESS',
                'error': str(e) if str(e) else None
            }, status=status.HTTP_200_OK)

class SimpleHealthView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        """
        Simple health check without dependencies
        """
        return Response({
            'status': 'success',
            'message': 'Server is running',
            'environment': 'Railway Production'
        }, status=status.HTTP_200_OK)