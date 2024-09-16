# SPDX-FileCopyrightText: 2024-present {{ copyright-holder }} <{{ copyright-holder-email }}>
#
# SPDX-License-Identifier: MIT

"""Stellarator Example."""

# %%
from __future__ import annotations

from typing import Any, Union

from bluemira.base.parameter_frame import EmptyFrame
from bluemira.base.reactor import Reactor
from bluemira.base.reactor_config import ReactorConfig

from stellarator_project.plasma.builder import PlasmaBuilder
from stellarator_project.plasma.designer import PlasmaDesigner
from stellarator_project.plasma.manager import Plasma
from stellarator_project.tf_coil.builder import TFCoilBuilder
from stellarator_project.tf_coil.designer import TFCoilDesigner
from stellarator_project.tf_coil.manager import TFCoil


class MyReactor(Reactor):
    """A simple reactor with two components."""

    plasma: Plasma
    tf_coil: TFCoil


def build_plasma(reactor_config):
    plasma_designer = PlasmaDesigner(
        reactor_config.params_for("Plasma", "designer"),
        reactor_config.config_for("Plasma", "designer"),
    )
    plasma_parameterisation = plasma_designer.execute()

    plasma_builder = PlasmaBuilder(
        plasma_parameterisation,
        reactor_config.config_for("Plasma"),
    )
    return Plasma(plasma_builder.build())


def build_tf(reactor_config):
    tf_coil_designer = TFCoilDesigner(
        None,
        reactor_config.config_for("TF Coil", "designer"),
    )
    tf_parameterisation = tf_coil_designer.execute()

    tf_coil_builder = TFCoilBuilder(
        reactor_config.params_for("TF Coil", "builder"),
        tf_parameterisation,
    )
    return TFCoil(tf_coil_builder.build())


def main(build_config: Union[str, Path, dict]) -> MyReactor:
    """Main reactor function."""
    reactor_config = ReactorConfig(build_config, EmptyFrame)

    reactor = MyReactor("Simple Example", n_sectors=1)

    reactor.plasma = build_plasma(reactor_config)
    reactor.tf_coil = build_tf(reactor_config)

    return reactor
