"""
Copyright (c) 2021-, Haibin Wen, sunnypilot, and a number of other contributors.

This file is part of sunnypilot and is licensed under the MIT License.
See the LICENSE.md file in the root directory for more details.
"""

from dataclasses import dataclass

from opendbc.car import structs
from opendbc.car.interfaces import CarStateBase
from opendbc.sunnypilot.car.hyundai.longitudinal.tuning_controller import LongitudinalTuningController

LongCtrlState = structs.CarControl.Actuators.LongControlState


@dataclass
class LongitudinalState:
  desired_accel: float = 0.0
  actual_accel: float = 0.0
  jerk_upper: float = 0.0
  jerk_lower: float = 0.0


class LongitudinalController:
  """Longitudinal controller which gets injected into CarControllerParams."""

  def __init__(self, CP: structs.CarParams, CP_SP: structs.CarParamsSP) -> None:
    self.tuning = LongitudinalTuningController(CP, CP_SP)
    self.long_state = LongitudinalState()

  def calculate_and_get_jerk(self, CC: structs.CarControl, CS: CarStateBase,
                             long_control_state: LongCtrlState) -> None:
    """Calculate jerk based on tuning."""
    self.tuning.make_jerk(CC, CS, long_control_state)

    if not CC.longActive:
      self.long_state.jerk_upper = 0.0
      self.long_state.jerk_lower = 0.0
      return

    self.long_state.jerk_upper = self.tuning.jerk_upper
    self.long_state.jerk_lower = self.tuning.jerk_lower

  def calculate_a_value(self, CC: structs.CarControl) -> None:
    """Calculate aReqValue."""
    self.tuning.calculate_a_value(CC)

    self.long_state.desired_accel = self.tuning.desired_accel
    self.long_state.actual_accel = self.tuning.actual_accel

  def update(self, CC: structs.CarControl, CS: CarStateBase) -> None:
    """Inject Longitudinal Controls for HKG Vehicles."""
    actuators = CC.actuators
    long_control_state = actuators.longControlState

    self.calculate_and_get_jerk(CC, CS, long_control_state)
    self.calculate_a_value(CC)
