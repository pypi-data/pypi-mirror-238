import os
from typing import Optional

import yaml

from ul_py_tool.utils.docker_compose import DockerComposeFile
from ul_py_tool.commands.cmd import Cmd
from ul_py_tool.utils.aseembly import AssemblyFile, AssemblyTarget
from ul_py_tool.utils.colors import FG_GREEN, NC
from ul_py_tool.utils.run_command import run_command
from ul_py_tool.utils.step import Stepper


class CmdReleaseDcfDev(Cmd):
    release_target: str
    assembly_file: AssemblyFile
    assembly_target: Optional[AssemblyTarget] = None
    '''
    Uses local files and values to generate test DCF
    '''
    def run(self) -> None:
        stepper = Stepper()
        cwd = os.getcwd()

        with stepper.step(f'{FG_GREEN}release{NC}'):
            run_command(
                [
                    'werf render --config=werf-release.yaml --values=.helm/dev-values.yaml  --values=.helm/charts.yaml --secret-values=.helm/dev-secret-values.yaml --loose-giterminism=True > kubernetes-objects.yaml',
                ],
                cwd=cwd,
                silent=True,
            )
            with open(os.path.join(cwd, "kubernetes-objects.yaml"), "r") as fr:
                dcf = DockerComposeFile.from_kubernetes(yaml.load_all(fr, yaml.FullLoader))
            final_file = dcf.to_json()
            with open("docker-compose.release.yaml", "w") as fw:
                yaml.dump(final_file, fw)
