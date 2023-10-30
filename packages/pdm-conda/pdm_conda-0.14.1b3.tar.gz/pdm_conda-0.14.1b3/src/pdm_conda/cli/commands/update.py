from __future__ import annotations

from typing import TYPE_CHECKING, cast

from pdm.cli.commands.update import Command as BaseCommand
from pdm.models.specifiers import get_specifier

from pdm_conda.project import CondaProject

if TYPE_CHECKING:
    import argparse

    from pdm_conda.project import Project


class Command(BaseCommand):
    description = BaseCommand.__doc__
    name = "update"

    def handle(self, project: Project, options: argparse.Namespace) -> None:
        super().handle(project=project, options=options)
        project = cast(CondaProject, project)
        if project.conda_config.custom_behavior:
            if not options.dry_run and options.save_strategy:
                groups = set(project.iter_groups(dev=False))
                dev_groups = set(project.iter_groups(dev=True)) - groups
                num_groups = len(groups) + len(dev_groups)
                candidates = project.locked_repository.all_candidates
                for i, group in enumerate(groups | dev_groups):
                    requirements = dict()
                    for identifier, _ in project.get_dependencies(group).items():
                        req = candidates.get(identifier).req

                        if req.is_named:
                            version = str(req.specifier).removeprefix("==")
                            if options.save_strategy == "minimum":
                                req.specifier = get_specifier(f">={version}")
                            elif options.save_strategy == "compatible":
                                req.specifier = get_specifier(f"~={version}")
                        requirements[identifier] = req
                    project.add_dependencies(requirements, to_group=group, dev=i >= len(groups), show_message=i == num_groups - 1)
