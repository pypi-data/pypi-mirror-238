from keycloak_django.security import ValidatePermissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from ..utils.app_endpoints import get_endpoints
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, OpenApiExample


class GetEndpointsViewSet(APIView):
    # permission_classes = [IsAuthenticated, ValidatePermissions]
    permission_classes = []
    http_method_names = ['get']
    # validate_permissions = {'get': 'get_enpoints_allow_read'}
    
    """
        ViewSet con el metodo GET, que obtiene la lista de los endpoints pertenecientes a las aplicaciones del proyecto.

        Args:
            exclude (str): Los endpoints a excluir del resultado, separados por comas(,) y es un parametro que se debe pasar en la url.
                           Ejemplo: example.com/api/get-endpoints/?exclude=/api/auth_panel/end_point/create-endpoints-list/,/api/auth_panel/earp/create-earp-by-list/

        Returns:
        List[str] : La lista de los endpoints pertenecientes a las aplicaciones del proyecto.
    """
    
    @extend_schema(
        description="Devuelve una lista de los endpoints pertenecientes a las aplicaciones del proyecto:\n" +
        """
        [
            /api/app1/endpoint,
            /api/app1/endpoint2,
            /api/app1/endpoint3,
            /api/app2/endpoint,
            /api/app2/endpoint2,
            /api/app2/endpoint3,
            /api/app3/endpoint,
            /api/app3/endpoint2,
            /api/app3/endpoint3
        ]
        """,
        parameters=[
            OpenApiParameter(
                name="exclude",
                type=OpenApiTypes.STR,
                required=False,
                description="Excluir los endpoints del resultado, no es obligatorio este parametro",
                examples=[
                    OpenApiExample(
                        'Example:',
                        summary='Excluye los endpoints de la lista de Endpoints y Earps',
                        value='/api/auth_panel/end_point/create-endpoints-list/,/api/auth_panel/earp/create-earp-by-list/'
                    ),
                    OpenApiExample(
                        'Example2:',
                        summary='Sin excluir ningún endpoint',
                        value=''
                    )
                ]
            ),
        ],
    )

    def get(self, request, format=None):
        match = 'exclude' in request.query_params
        exclude = request.query_params['exclude'].split(',') if match else []
        data = get_endpoints(exclude=exclude)
        return Response(data, status=status.HTTP_200_OK)