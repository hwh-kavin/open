# constants from panda/python/__init__.py
DLC_TO_LEN = [0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 16, 20, 24, 32, 48, 64]
LEN_TO_DLC = {length: dlc for (dlc, length) in enumerate(DLC_TO_LEN)}


class ALTERNATIVE_EXPERIENCE:
  DEFAULT = 0
  DISABLE_DISENGAGE_ON_GAS = 1
  DISABLE_STOCK_AEB = 2
  RAISE_LONGITUDINAL_LIMITS_TO_ISO_MAX = 8
  ALLOW_AEB = 16

  # sunnypilot
  ENABLE_MADS = 2 ** 10
  DISENGAGE_LATERAL_ON_BRAKE = 2 ** 11
