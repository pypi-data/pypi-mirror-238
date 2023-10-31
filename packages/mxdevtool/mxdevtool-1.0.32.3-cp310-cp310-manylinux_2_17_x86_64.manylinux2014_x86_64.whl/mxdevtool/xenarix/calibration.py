import mxdevtool as mx


# for setting...? -> 이럴거면 그냥 setting 에서 dict로 하는게 낫지않나...?
class ModelCalibrator:
    def __init__(self, method='levenberg'):
        self._method = method

    def calibrate(self, model, helpers, fix_parameters):
        _method = self._method
        _endcriteria = self._endcriteria
        _constraint = self._constraint
        weights = [h.weight for h in helpers]

        parameters = model.calibrate(helpers, _method, _endcriteria, _constraint, weights, fix_parameters)
        
        return parameters


