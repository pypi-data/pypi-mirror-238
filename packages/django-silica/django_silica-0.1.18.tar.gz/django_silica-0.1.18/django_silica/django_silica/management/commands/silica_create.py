import os
import random
from django_silica.utils import pascal_to_snake
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Creates a new Silica component'

    TEMPLATE_FOR_CLASS = """from django_silica.SilicaComponent import SilicaComponent

class {class_name}(SilicaComponent):
    # Your class implementation here
"""

    quotes = [
        'You are in control of your own destiny.',
        'Create something awesome.',
        'Carpe diem.',
    ]

    TEMPLATE_FOR_TEMPLATE = f"""
{{# {random.choice(quotes)} #}}
"""

    def add_arguments(self, parser):
        parser.add_argument('component_name', type=str)

    def handle(self, *args, **options):
        component_name: str = options['component_name']
        subfolders: list[str] = []

        if '.' in component_name:
            *subfolders, component_name = component_name.split(".") # list unpacking


        # Convert component name to snake_case for the template
        snake_component_name = pascal_to_snake(component_name)

        # Parse DJANGO_SETTINGS_MODULE to get the main app name
        settings_module = os.environ.get('DJANGO_SETTINGS_MODULE')
        if not settings_module:
            raise CommandError("DJANGO_SETTINGS_MODULE environment variable not set.")

        main_app_name = settings_module.split('.')[0]

        # Get the BASE_DIR from Django settings
        from django.conf import settings
        base_dir = getattr(settings, 'BASE_DIR')
        if not base_dir:
            raise CommandError("Unable to determine the BASE_DIR from Django settings.")

        component_path = os.path.join(base_dir, main_app_name, 'silica', *subfolders, f"{component_name}.py")
        template_path = os.path.join(base_dir, main_app_name, 'templates', 'silica', *subfolders, f"{snake_component_name}.html")

        # Check if files already exist
        if os.path.exists(component_path) or os.path.exists(template_path):
            raise CommandError(f"Component {component_name} already exists.")

        # Create component file
        os.makedirs(os.path.dirname(component_path), exist_ok=True)
        with open(component_path, 'w') as f:
            f.write(self.TEMPLATE_FOR_CLASS.format(class_name=component_name))

        # Create template file
        os.makedirs(os.path.dirname(template_path), exist_ok=True)
        with open(template_path, 'w') as f:
            f.write(self.TEMPLATE_FOR_TEMPLATE)

        # Print confirmation messages
        self.stdout.write(self.style.SUCCESS(f"Component created at {component_path}"))
        self.stdout.write(self.style.SUCCESS(f"Template created at {template_path}"))
