class SimulatorError(Exception):
    pass
class NotImplementedInSimulatorError(SimulatorError):
    pass
class SimulatorNotRunningError(SimulatorError):
    pass
