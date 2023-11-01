from django.core.management import BaseCommand
from ...utils.app_endpoints import get_endpoints


class Command(BaseCommand):
    """
        Comando que obtiene la lista de los endpoints pertenecientes a las aplicaciones del proyecto.

        Args:
            --with_line_break (bool): True si quiere desplegar el resultado con salto de línea.
            --exclude (str): Los endpoints a excluir del resultado, entre comillas simple(') o dobles(") y separados por comas(,).

        Returns:
        List[str] : La lista de los endpoints pertenecientes a las aplicaciones del proyecto.
    """
    
    def add_arguments(self, parser):
        parser.add_argument('--with_line_break', type=bool, help='Print endpoints with line break')
        parser.add_argument('--exclude', type=str, help="The endpoints you don't want to take into account. Example: '/api/commons/example/,/api/commons/example2/'")


    def handle(self, *args, **options):
        endpoints_exclude = options['exclude']
        exclude = endpoints_exclude.split(',') if endpoints_exclude else []
        endpoints_list = get_endpoints(exclude=exclude)
        if options["with_line_break"]:
            for endpoint in endpoints_list:
                self.stdout.write(f'"{endpoint}"')
        else:
            endpoints = ', '.join([f'"{endpoint}"' for endpoint in endpoints_list])
            self.stdout.write(endpoints)