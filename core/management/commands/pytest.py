from django.core.management.base import BaseCommand
import pytest


class Command(BaseCommand):
    help = "Run pytest test suite (alias for `pytest`)."

    def add_arguments(self, parser):
        parser.add_argument("pytest_args", nargs="*", help="Arguments passed to pytest")

    def handle(self, *args, **options):
        pytest_args = options.get("pytest_args") or ["-q"]
        raise SystemExit(pytest.main(pytest_args))