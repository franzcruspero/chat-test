import os
import subprocess
from pathlib import Path
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Add a Git submodule using SSH and treat it as a Django app"

    def add_arguments(self, parser):
        parser.add_argument(
            "repo_url", type=str, help="The SSH URL of the Git repository"
        )
        parser.add_argument("app_name", type=str, help="The name of the Django app")

    def handle(self, *args, **options):
        repo_url = options["repo_url"]
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

            # Check if the submodule is already initialized
            try:
                result = subprocess.run(
                    ["git", "submodule", "status", app_name],
                    cwd=root_dir,
                    check=True,
                    capture_output=True,
                    text=True,
                )
                self.stdout.write(
                    self.style.WARNING(
                        f"Submodule '{app_name}' already exists. Updating instead of adding."
                    )
                )

                # Update the submodule
                subprocess.run(
                    ["git", "submodule", "update", "--init", "--recursive", app_name],
                    cwd=root_dir,
                    check=True,
                )
                self.stdout.write(
                    self.style.SUCCESS(f"Submodule '{app_name}' updated successfully.")
                )
            except subprocess.CalledProcessError:
                # Submodule does not exist, handle potential conflicts
                if submodule_path.exists():
                    self.stdout.write(
                        self.style.WARNING(
                            f"The path '{submodule_path}' already exists. Cleaning up..."
                        )
                    )
                    self.clean_submodule(app_name, root_dir)

                self.stdout.write(
                    self.style.SUCCESS(f"Adding submodule '{app_name}'...")
                )
                subprocess.run(
                    ["git", "submodule", "add", repo_url, app_name],
                    cwd=root_dir,
                    check=True,
                    text=True,
                )
                self.stdout.write(
                    self.style.SUCCESS(f"Submodule '{app_name}' added successfully.")
                )

                # Initialize and update the submodule
                subprocess.run(
                    ["git", "submodule", "update", "--init", "--recursive", app_name],
                    cwd=root_dir,
                    check=True,
                )
                self.stdout.write(
                    self.style.SUCCESS(f"Submodule initialized at {submodule_path}")
                )

        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR(f"Git command failed:\n{e.stderr}"))

            # Additional checks for .gitmodules file
            gitmodules_path = root_dir / ".gitmodules"
            if gitmodules_path.exists():
                with open(gitmodules_path, "r") as f:
                    content = f.read()
                    if app_name in content:
                        self.stderr.write(
                            self.style.WARNING(
                                f"The submodule '{app_name}' is mentioned in .gitmodules but might be misconfigured."
                            )
                        )
                        self.stderr.write(
                            self.style.WARNING(
                                "You may need to manually edit .gitmodules or remove and re-add the submodule."
                            )
                        )
            else:
                self.stderr.write(
                    self.style.WARNING(
                        "The .gitmodules file was not found. Ensure your Git repository is set up correctly."
                    )
                )

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Unexpected error: {e}"))

    def clean_submodule(self, app_name, root_dir):
        """
        Clean up any misconfigured or partially added submodule.
        """
        try:
            # Remove the submodule from Git index
            subprocess.run(
                ["git", "rm", "--cached", app_name],
                cwd=root_dir,
                check=True,
            )
            # Remove the directory
            submodule_path = root_dir / app_name
            if submodule_path.exists():
                subprocess.run(["rm", "-rf", str(submodule_path)], check=True)
            # Remove from .gitmodules
            subprocess.run(
                ["git", "config", "--file", ".gitmodules", "--remove-section", f"submodule.{app_name}"],
                cwd=root_dir,
                check=True,
            )
            # Remove from .git/config
            subprocess.run(
                ["git", "config", "--remove-section", f"submodule.{app_name}"],
                cwd=root_dir,
                check=True,
            )
            self.stdout.write(
                self.style.SUCCESS(f"Cleaned up existing submodule '{app_name}'.")
            )
        except subprocess.CalledProcessError as e:
            self.stderr.write(
                self.style.ERROR(
                    f"Failed to clean up submodule '{app_name}': {e.stderr}"
                )
            )
