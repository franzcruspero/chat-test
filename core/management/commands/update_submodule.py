import subprocess
from pathlib import Path
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Update the submodule to the latest version from the remote repository"

    def add_arguments(self, parser):
        parser.add_argument("app_name", type=str, help="The name of the submodule (Django app)")

    def handle(self, *args, **options):
        app_name = options["app_name"]

        # Define the root directory and submodule path
        root_dir = Path(__file__).resolve().parent.parent.parent.parent
        submodule_path = root_dir / app_name

        self.stdout.write(self.style.SUCCESS(f"Root directory: {root_dir}"))

        try:
            # Ensure the directory is a Git repository
            subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                cwd=root_dir,
                check=True,
                capture_output=True,
                text=True,
            )

            # Check if the submodule exists
            try:
                subprocess.run(
                    ["git", "submodule", "status", app_name],
                    cwd=root_dir,
                    check=True,
                    capture_output=True,
                    text=True,
                )

                self.stdout.write(self.style.SUCCESS(f"Updating submodule '{app_name}'..."))

                # Update the submodule to the latest commit from the remote repository
                subprocess.run(
                    ["git", "submodule", "update", "--remote", "--recursive", app_name],
                    cwd=root_dir,
                    check=True,
                    text=True,
                )

                self.stdout.write(self.style.SUCCESS(f"Submodule '{app_name}' updated successfully."))

            except subprocess.CalledProcessError:
                self.stderr.write(self.style.ERROR(f"Submodule '{app_name}' does not exist."))
                return

        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR(f"Git command failed:\n{e.stderr}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Unexpected error: {e}"))
