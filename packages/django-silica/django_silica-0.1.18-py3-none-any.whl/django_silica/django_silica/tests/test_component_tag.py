import os
from pathlib import Path
from django_silica.utils import pascal_to_snake
from django_silica.SilicaComponent import SilicaComponent
from django_silica.tests.SilicaTestCase import SilicaTestCase, SilicaTest
from django.test import TestCase, RequestFactory, Client, override_settings
from django.core.management import call_command
from django.conf import settings


class ComponentTagTestCase(SilicaTestCase):
    def test_short_tag_can_be_called(self):
        client = Client()
        response = client.get("/silica/tests/component-tag-test")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I'm component called with short name!")


    def test_components_in_subfolders_can_be_called(self):
        client = Client()
        response = client.get("/silica/tests/component-subfolder-test")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I'm component in subfolder!")

    def test_template_and_component_name_are_snake_case(self):
        call_command('silica_create', "TestUniqueSideBar")

        main_app_dir = Path(settings.BASE_DIR) / "example_project"

        # component
        pascal_component_path = main_app_dir / 'silica' / f"TestUniqueSideBar.py"
        snake_component_path = main_app_dir / 'silica' / f"test_unique_side_bar.py"

        # template
        pascal_template_path = main_app_dir / 'templates' / 'silica' / f"TestUniqueSideBar.html"
        snake_template_path = main_app_dir / 'templates' / 'silica' / f"test_unique_side_bar.html"

        try:
            # we want pascal components and snake templates
            self.assertTrue(pascal_component_path.exists(), f"{pascal_component_path} does not exist.")
            self.assertTrue(snake_template_path.exists(), f"{snake_template_path} does not exist.")
        finally:
            # Cleanup regardless of test outcome
            if pascal_component_path.exists():
                pascal_component_path.unlink()
            if pascal_template_path.exists():
                pascal_template_path.unlink()
            if snake_component_path.exists():
                snake_component_path.unlink()
            if snake_template_path.exists():
                snake_template_path.unlink()

    def test_silica_create_with_nested_subfolders(self):
        call_command('silica_create', "folder1.folder2.folder3.NewComponent")

        main_app_dir = Path(settings.BASE_DIR) / "example_project"

        # Component in nested subfolders
        component_path = main_app_dir / 'silica' / 'folder1' / 'folder2' / 'folder3' / "NewComponent.py"

        # Template in nested subfolders
        template_path = main_app_dir / 'templates' / 'silica' / 'folder1' / 'folder2' / 'folder3' / "new_component.html"

        # Incorrectly created component and template paths
        incorrect_component_path = main_app_dir / 'silica' / 'folder1.folder2.folder3' / 'NewComponent.py'
        incorrect_template_path = main_app_dir / 'templates' / 'silica' / 'folder1.folder2.folder3' / 'new_component.html'


        try:
            self.assertTrue(component_path.exists(), f"{component_path} does not exist.")
            self.assertTrue(template_path.exists(), f"{template_path} does not exist.")
        finally:
            # Cleanup regardless of test outcome
            if component_path.exists():
                component_path.unlink()
            if template_path.exists():
                template_path.unlink()
            if incorrect_component_path.exists():
                incorrect_component_path.unlink()
            if incorrect_template_path.exists():
                incorrect_template_path.unlink()