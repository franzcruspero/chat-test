import subprocess
from pathlib import Path
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Add a Git submodule using SSH and treat it as a Django app"

    def add_arguments(self, parser):
        parser.add_argument("repo_url", type=str, help="The SSH URL of the Git repository")
        parser.add_argument("app_name", type=str, help="The name of the Django app")

    def handle(self, *args, **options):
        repo_url = options["repo_url"]
        app_name = options["app_name"]

        root_dir = Path(__file__).resolve().parent.parent.parent.parent
        submodule_path = root_dir / app_name

        try:
            # Run the git submodule add command
            result = subprocess.run(
                ["git", "submodule", "add", repo_url, str(submodule_path)],
                cwd=root_dir,
                check=True,
                text=True,
                capture_output=True,
            )
            self.stdout.write(self.style.SUCCESS(result.stdout))

            # Initialize and update the submodule
            subprocess.run(
                ["git", "submodule", "update", "--init", "--recursive"],
                cwd=root_dir,
                check=True,
            )
            self.stdout.write(self.style.SUCCESS(f"Submodule added and initialized at {submodule_path}"))

        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR(f"Git command failed:\n{e.stderr}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Unexpected error: {e}"))
