import mxdevtool as mx
import mxdevtool.utils as utils
import inspect, numbers
from typing import List


class DeterministicParameter(mx.PiecewiseConstantParameter2):
    def __init__(self, times: List[float], values: List[float]):
        self._times = times
        self._values = values
        
        times_conv = utils.toTimeList(times)
        
        mx.PiecewiseConstantParameter2.__init__(self, times_conv)

        for i, v in enumerate(values):
            self.setParam(i, v)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        if isinstance(d, numbers.Number):
            return DeterministicParameter(['1Y', '100Y'], [d, d])

        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, DeterministicParameter.__name__)

        times = d['times']
        values = d['values']

        return DeterministicParameter(times, values)

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['times'] = self._times
        res['values'] = self._values

        return res

    def clone(self, **kwargs):
        args = []

        for arg in ['times', 'values']:
            args.append(kwargs.get(arg, getattr(self, '_{0}'.format(arg))))

        return DeterministicParameter(*args)

# models ----------------------------

class GBMConst(mx.core_GBMConstModel):
    # compounded rate is required
    def __init__(self, name: str, x0: float, rf: float, div: float, vol: float):
        self._x0 = x0
        self._rf = rf
        self._div = div
        self._vol = vol

        mx.core_GBMConstModel.__init__(self, name, x0, rf, div, vol)

    def clone(self, **kwargs):
        name = kwargs.get('name', self.name)
        args = []

        for arg in ['x0', 'rf', 'div', 'vol']:
            args.append(kwargs.get(arg, getattr(self, '_{0}'.format(arg))))

        return GBMConst(name, *args)
    
    def shocked_clone(self, amount):
        shocked_v = self._x0 + amount
        return self.clone(x0=shocked_v)


class GBM(mx.core_GBMModel):
    def __init__(self, name: str, x0, rfCurve: mx.YieldTermStructure, divCurve: mx.YieldTermStructure, volTs: mx.BlackVolTermStructure):

        self._x0 = x0
        self._rfCurve = rfCurve
        self._divCurve = divCurve
        self._volTs = volTs

        mx.core_GBMModel.__init__(self, name, x0, rfCurve, divCurve, volTs)

    def clone(self, **kwargs):
        name = kwargs.get('name', self.name)
        args = []

        for arg in ['x0', 'rfCurve', 'divCurve', 'volTs']:
            args.append(kwargs.get(arg, getattr(self, '_{0}'.format(arg))))

        return GBM(name, *args)

    def shocked_clone(self, amount):
        shocked_v = self._x0 + amount
        return self.clone(x0=shocked_v)


class Heston(mx.core_HestonModel):
    def __init__(self, name: str, x0: float, rfCurve: mx.YieldTermStructure, divCurve: mx.YieldTermStructure, 
                 v0: float, volRevertingSpeed: float, longTermVol: float, volOfVol: float, rho: float):

        self._x0 = x0
        self._rfCurve = rfCurve
        self._divCurve = divCurve
        self._v0 = v0
        self._volRevertingSpeed = volRevertingSpeed
        self._longTermVol = longTermVol
        self._volOfVol = volOfVol
        self._rho = rho

        mx.core_HestonModel.__init__(self, name, x0, rfCurve, divCurve, v0, volRevertingSpeed, longTermVol, volOfVol, rho)

    def clone(self, **kwargs):
        name = kwargs.get('name', self.name)
        args = []

        for arg in ['x0', 'rfCurve', 'divCurve', 'v0', 'volRevertingSpeed', 'longTermVol', 'volOfVol', 'rho']:
            args.append(kwargs.get(arg, getattr(self, '_{0}'.format(arg))))

        return Heston(name, *args)

    def shocked_clone(self, amount):
        shocked_v = self._x0 + amount
        return self.clone(x0=shocked_v)


class CIR1F(mx.core_CIR1FModel):
    def __init__(self, name: str, r0: float, alpha: float, longterm: float, sigma: float):
        self._r0 = r0
        self._alpha = alpha
        self._longterm = longterm
        self._sigma = sigma

        self.fixParameters = [False] * 4 # this for calibration

        mx.core_CIR1FModel.__init__(self, name, r0, alpha, longterm, sigma)

    def clone(self, **kwargs):
        name = kwargs.get('name', self.name)
        r0 = kwargs.get('r0', self._r0)
        alpha = kwargs.get('alpha', self._alpha)
        longterm = kwargs.get('longterm', self._longterm)
        sigma = kwargs.get('sigma', self._sigma) 
        fixParameters = kwargs.get('fixParameters', self.fixParameters)

        if 'calibrated_parameters' in kwargs:
            calibrated_parameters = kwargs['calibrated_parameters']

            r0 = calibrated_parameters[0]
            alpha = calibrated_parameters[1]
            longterm = calibrated_parameters[2]
            sigma = calibrated_parameters[3]
        
        model = CIR1F(name, r0, alpha, longterm, sigma)
        model.fixParameters = fixParameters

        return model

    def shocked_clone(self, amount):
        shocked_v = self._r0 + amount
        return self.clone(r0=shocked_v)


class Vasicek1F(mx.core_Vasicek1FModel):
    def __init__(self, name: str, r0: float, alpha: float, longterm: float, sigma: float):

        self._r0 = r0
        self._alpha = alpha
        self._longterm = longterm
        self._sigma = sigma

        self.fixParameters = [False] * 4 # this for calibration

        mx.core_Vasicek1FModel.__init__(self, name, r0, alpha, longterm, sigma)

    def clone(self, **kwargs):
        name = kwargs.get('name', self.name)
        r0 = kwargs.get('r0', self._r0)
        alpha = kwargs.get('alpha', self._alpha)
        longterm = kwargs.get('longterm', self._longterm)
        sigma = kwargs.get('sigma', self._sigma) 
        fixParameters = kwargs.get('fixParameters', self.fixParameters)

        if 'calibrated_parameters' in kwargs:
            calibrated_parameters = kwargs['calibrated_parameters']
            r0 = calibrated_parameters[0]
            alpha = calibrated_parameters[1]
            longterm = calibrated_parameters[2]
            sigma = calibrated_parameters[3]
            
        model = Vasicek1F(name, r0, alpha, longterm, sigma)
        model.fixParameters = fixParameters
        
        return model

    def shocked_clone(self, amount):
        shocked_v = self._r0 + amount
        return self.clone(r0=shocked_v)


class HullWhite1F(mx.core_HullWhite1FModel):
    def __init__(self, name: str, fittingCurve: mx.YieldTermStructure, alphaPara: DeterministicParameter, sigmaPara: DeterministicParameter):

        self._fittingCurve = fittingCurve
        self._alphaPara = alphaPara
        self._sigmaPara = sigmaPara
        
        self.fixParameters = [False] * (len(alphaPara._values) + len(sigmaPara._values)) # this for calibration

        mx.core_HullWhite1FModel.__init__(self, name, fittingCurve, alphaPara, sigmaPara)

    def clone(self, **kwargs):
        name = kwargs.get('name', self.name)
        fittingCurve = kwargs.get('fittingCurve', self._fittingCurve)
        alphaPara = kwargs.get('alphaPara', self._alphaPara)
        sigmaPara = kwargs.get('sigmaPara', self._sigmaPara)
        fixParameters = kwargs.get('fixParameters', self.fixParameters)

        if 'calibrated_parameters' in kwargs:
            calibrated_parameters = kwargs['calibrated_parameters']
            alphaPara = DeterministicParameter(self._alphaPara._times, calibrated_parameters[:len(self._alphaPara._values)])
            sigmaPara = DeterministicParameter(self._sigmaPara._times, calibrated_parameters[len(self._alphaPara._values):])
            
        model = HullWhite1F(name, fittingCurve, alphaPara, sigmaPara)
        model.fixParameters = fixParameters
        
        return model

    def shocked_clone(self, amount):
        shocked_curve = self._fittingCurve.shocked_clone(amount)
        return self.clone(fittingCurve=shocked_curve)


class BK1F(mx.core_BK1FModel):
    def __init__(self, name: str, fittingCurve: mx.YieldTermStructure, alphaPara: DeterministicParameter, sigmaPara: DeterministicParameter):

        self._fittingCurve = fittingCurve
        self._alphaPara = alphaPara
        self._sigmaPara = sigmaPara

        self.fixParameters = [False] * (len(alphaPara._values) + len(sigmaPara._values)) # this for calibration

        mx.core_BK1FModel.__init__(self, name, fittingCurve, alphaPara, sigmaPara)

    def clone(self, **kwargs):
        name = kwargs.get('name', self.name)
        fittingCurve = kwargs.get('fittingCurve', self._fittingCurve)
        alphaPara = kwargs.get('alphaPara', self._alphaPara)
        sigmaPara = kwargs.get('sigmaPara', self._sigmaPara)
        fixParameters = kwargs.get('fixParameters', self.fixParameters)

        if 'calibrated_parameters' in kwargs:
            calibrated_parameters = kwargs['calibrated_parameters']
            alphaPara = DeterministicParameter(self._alphaPara._times, calibrated_parameters[:len(self._alphaPara._values)])
            sigmaPara = DeterministicParameter(self._sigmaPara._times, calibrated_parameters[len(self._alphaPara._values):])

        model = BK1F(name, fittingCurve, alphaPara, sigmaPara)
        model.fixParameters = fixParameters
        
        return model            

    def shocked_clone(self, amount):
        shocked_curve = self._fittingCurve.shocked_clone(amount)
        return self.clone(fittingCurve=shocked_curve)


class G2Ext(mx.core_GTwoExtModel):
    def __init__(self, name: str, fittingCurve: mx.YieldTermStructure, 
                 alpha1: float, sigma1: float, alpha2: float, sigma2: float, corr: float):

        self._fittingCurve = fittingCurve
        self._alpha1 = alpha1
        self._sigma1 = sigma1
        self._alpha2 = alpha2
        self._sigma2 = sigma2
        self._corr = corr

        self.fixParameters = [False] * 5 # this for calibration

        mx.core_GTwoExtModel.__init__(self, name, fittingCurve, alpha1, sigma1, alpha2, sigma2, corr)

    def clone(self, **kwargs):
        name = kwargs.get('name', self.name)
        fittingCurve = kwargs.get('fittingCurve', self._fittingCurve)
        alpha1 = kwargs.get('alpha1', self._alpha1)
        sigma1 = kwargs.get('sigma1', self._sigma1)
        alpha2 = kwargs.get('alpha2', self._alpha2)
        sigma2 = kwargs.get('sigma2', self._sigma2)
        corr = kwargs.get('corr', self._corr)
        fixParameters = kwargs.get('fixParameters', self.fixParameters)
        
        if 'calibrated_parameters' in kwargs:
            calibrated_parameters = kwargs['calibrated_parameters']
            alpha1 = calibrated_parameters[0]
            sigma1 = calibrated_parameters[1]
            alpha2 = calibrated_parameters[2]
            sigma2 = calibrated_parameters[3]
            corr = calibrated_parameters[4]

        model = G2Ext(name, fittingCurve, alpha1, sigma1, alpha2, sigma2, corr)
        model.fixParameters = fixParameters
        
        return model                 

    def shocked_clone(self, amount):
        shocked_curve = self._fittingCurve.shocked_clone(amount)
        return self.clone(fittingCurve=shocked_curve)
        

# operators -----------------------------
class PlusOper(mx.core_PlusOperCalc):
    def __init__(self, pv: mx.ProcessValue):
        self._pv = pv
        mx.core_PlusOperCalc.__init__(self, pv)


class MinusOper(mx.core_MinusOperCalc):
    def __init__(self, pv: mx.ProcessValue):
        self._pv = pv
        mx.core_MinusOperCalc.__init__(self, pv)


class AdditionOper(mx.core_AdditionOperCalc):
    def __init__(self, pv1: mx.ProcessValue, pv2: mx.ProcessValue):
        self._pv1 = pv1
        self._pv2 = pv2
        mx.core_AdditionOperCalc.__init__(self, pv1, pv2)


class AdditionConstOper(mx.core_AdditionConstOperCalc):
    def __init__(self, pv1: mx.ProcessValue, v: float):
        self._pv1 = pv1
        self._v = v
        mx.core_AdditionConstOperCalc.__init__(self, pv1, v)


class AdditionConstReverseOper(mx.core_AdditionConstReverseOperCalc):
    def __init__(self, v: float, pv2: mx.ProcessValue):
        self._v = v
        self._pv2 = pv2
        mx.core_AdditionConstReverseOperCalc.__init__(self, v, pv2)


class SubtractionOper(mx.core_SubtractionOperCalc):
    def __init__(self, pv1: mx.ProcessValue, pv2: mx.ProcessValue):
        self._pv1 = pv1
        self._pv2 = pv2
        mx.core_SubtractionOperCalc.__init__(self, pv1, pv2)


class SubtractionConstOper(mx.core_SubtractionConstOperCalc):
    def __init__(self, pv1: mx.ProcessValue, v: float):
        self._pv1 = pv1
        self._v = v
        mx.core_SubtractionConstOperCalc.__init__(self, pv1, v)


class SubtractionConstReverseOper(mx.core_SubtractionConstReverseOperCalc):
    def __init__(self, v: float, pv2: mx.ProcessValue):
        self._v = v
        self._pv2 = pv2
        mx.core_SubtractionConstReverseOperCalc.__init__(self, v, pv2)


class MultiplicationOper(mx.core_MultiplicationOperCalc):
    def __init__(self, pv1: mx.ProcessValue, pv2: mx.ProcessValue):
        self._pv1 = pv1
        self._pv2 = pv2
        mx.core_MultiplicationOperCalc.__init__(self, pv1, pv2)


class MultiplicationConstOper(mx.core_MultiplicationConstOperCalc):
    def __init__(self, pv1: mx.ProcessValue, v: float):
        self._pv1 = pv1
        self._v = v
        mx.core_MultiplicationConstOperCalc.__init__(self, pv1, v)


class MultiplicationConstReverseOper(mx.core_MultiplicationConstReverseOperCalc):
    def __init__(self, v: float, pv2: mx.ProcessValue):
        self._v = v
        self._pv2 = pv2
        mx.core_MultiplicationConstReverseOperCalc.__init__(self, v, pv2)


class DivisionOper(mx.core_DivisionOperCalc):
    def __init__(self, pv1: mx.ProcessValue, pv2: mx.ProcessValue):
        self._pv1 = pv1
        self._pv2 = pv2
        mx.core_DivisionOperCalc.__init__(self, pv1, pv2)


class DivisionConstOper(mx.core_DivisionConstOperCalc):
    def __init__(self, pv1: mx.ProcessValue, v: float):
        self._pv1 = pv1
        self._v = v
        mx.core_DivisionConstOperCalc.__init__(self, pv1, v)


class DivisionConstReverseOper(mx.core_DivisionConstReverseOperCalc):
    def __init__(self, v: float, pv2: mx.ProcessValue):
        self._v = v
        self._pv2 = pv2
        mx.core_DivisionConstReverseOperCalc.__init__(self, v, pv2)


def get_operator(pv1, pv2, operand):
    if isinstance(pv1, (float, int)):
        
        if operand == '+': return AdditionConstReverseOper(pv1, pv2)
        elif operand == '-': return SubtractionConstReverseOper(pv1, pv2)
        elif operand == '*': return  MultiplicationConstReverseOper(pv1, pv2)
        elif operand == '/': return DivisionConstReverseOper(pv1, pv2)
    elif isinstance(pv2, (float, int)):
        if operand == '+': return AdditionConstOper(pv1, pv2)
        elif operand == '-': return SubtractionConstOper(pv1, pv2)
        elif operand == '*': return MultiplicationConstOper(pv1, pv2)
        elif operand == '/': return DivisionConstOper(pv1, pv2)
    else:
        if operand == '+': return AdditionOper(pv1, pv2)
        elif operand == '-': return SubtractionOper(pv1, pv2)
        elif operand == '*': return MultiplicationOper(pv1, pv2)
        elif operand == '/': return DivisionOper(pv1, pv2)
    
    raise Exception('unknown operator for ProcessValue - {0}, {1}, {2}'.format(pv1, pv2, operand))


# calcs -----------------------------

class Identity(mx.core_IdentityWrapperCalc):
    def __init__(self, name: str, pv: mx.ProcessValue):
        self._pv = pv

        mx.core_IdentityWrapperCalc.__init__(self, name, pv)

    def toDict(self):
        return self._pv.toDict()


class YieldCurve(mx.core_YieldCurveValueCalc):
    def __init__(self, name: str, yieldCurve: mx.YieldTermStructure, output_type='spot', compounding=mx.Compounded):

        self._yieldCurve = yieldCurve
        self._output_type = output_type
        self._compounding = compounding

        mx.core_YieldCurveValueCalc.__init__(self, name, yieldCurve, output_type, compounding)


class FixedRateBond(mx.core_FixedRateCMBondPositionCalc):
    def __init__(self, name: str, ir_pv: mx.ProcessValue,
                 notional=10000,
                 fixedRate=0.0,
                 couponTenor=mx.Period(3, mx.Months),
                 maturityTenor=mx.Period(3, mx.Years),
                 discountCurve=None):
        if discountCurve is None:
            raise Exception('discount curve is required')

        self._ir_pv = ir_pv
        self._notional = notional
        self._fixedRate = fixedRate
        self._couponTenor = couponTenor
        self._maturityTenor = maturityTenor
        self._discountCurve = discountCurve

        mx.core_FixedRateCMBondPositionCalc.__init__(self, name, ir_pv, notional, fixedRate, couponTenor, maturityTenor, discountCurve)



class Returns(mx.core_ReturnWrapperCalc):
    def __init__(self, name: str, pv: mx.ProcessValue, return_type='return'):
        self._pv = pv
        self._return_type = return_type

        mx.core_ReturnWrapperCalc.__init__(self, name, pv, return_type)


class Shift(mx.core_ShiftWrapperCalc):
    def __init__(self, name: str, pv: mx.ProcessValue, 
                 shift: int, fill_value=0.0):
        self._pv = pv
        self._shift = shift
        self._fill_value = fill_value

        mx.core_ShiftWrapperCalc.__init__(self, name, pv, shift, fill_value)


class ConstantValue(mx.core_ConstantValueCalc):
    def __init__(self, name: str, v: float):
        self._v = v
        mx.core_ConstantValueCalc.__init__(self, name, v)


class ConstantArray(mx.core_ConstantArrayCalc):
    def __init__(self, name: str, arr: List[float]):
        self._arr = arr
        mx.core_ConstantArrayCalc.__init__(self, name, arr)


class LinearOper(mx.core_LinearOperWrapperCalc):
    def __init__(self, name: str, pv: mx.ProcessValue, multiple=1.0, spread=0.0):
        self._pv = pv
        self._multiple = multiple
        self._spread = spread
        mx.core_LinearOperWrapperCalc.__init__(self, name, pv, multiple, spread)


class UnaryFunction(mx.core_UnaryFunctionWrapperCalc):
    def __init__(self, name: str, pv: mx.ProcessValue, func_type: str):
        self._pv = pv
        self._func_type = func_type
        mx.core_UnaryFunctionWrapperCalc.__init__(self, name, pv, func_type)


class BinaryFunction(mx.core_BinaryFunctionWrapperCalc):
    def __init__(self, name: str, pv1: mx.ProcessValue, pv2: mx.ProcessValue, func_type: str):
        self._pv1 = pv1
        self._pv2 = pv2
        self._func_type = func_type
        mx.core_BinaryFunctionWrapperCalc.__init__(self, name, pv1, pv2, func_type)


class MultaryFunction(mx.core_MultaryFunctionWrapperCalc):
    def __init__(self, name: str, pv_list: List[mx.ProcessValue], func_type: str):
        self._pv_list = pv_list
        self._func_type = func_type
        mx.core_MultaryFunctionWrapperCalc.__init__(self, name, pv_list, func_type)


class Overwrite(mx.core_OverwriteWrapperCalc):
    def __init__(self, name: str, pv: mx.ProcessValue, start_pos: int, arr: List[float]):
        self._pv = pv
        self._arr = arr
        mx.core_OverwriteWrapperCalc.__init__(self, name, pv, start_pos, arr)


class Fund(mx.core_FundWrapperCalc):
    def __init__(self, name: str, weights: float, pv_list: List[mx.ProcessValue]):
        self._weights = weights
        self._pv_list = pv_list
        mx.core_FundWrapperCalc.__init__(self, name, weights, pv_list)

# model
class SpotRate(mx.core_SpotRateCalc):
    def __init__(self, name: str, ir_pv: mx.ProcessValue, 
                 maturityTenor: mx.Period, compounding=mx.Compounded):
        self._ir_pv = ir_pv
        self._maturityTenor = maturityTenor
        self._compounding = utils.toCompounding(compounding)
        mx.core_SpotRateCalc.__init__(self, name, ir_pv, maturityTenor, compounding)


class ForwardRate(mx.core_ForwardRateCalc):
    def __init__(self, name: str, ir_pv: mx.ProcessValue, 
                 startTenor: mx.Period, maturityTenor: mx.Period, compounding=mx.Compounded):
        self._ir_pv = ir_pv
        self._startTenor = startTenor
        self._maturityTenor = maturityTenor
        self._compounding = utils.toCompounding(compounding)
        mx.core_ForwardRateCalc.__init__(self, name, ir_pv, startTenor, maturityTenor, compounding)


class DiscountFactor(mx.core_DiscountFactorCalc):
    def __init__(self, name: str, ir_pv: mx.ProcessValue):
        self._ir_pv = ir_pv
        mx.core_DiscountFactorCalc.__init__(self, name, ir_pv)


class DiscountBond(mx.core_DiscountBondCalc):
    def __init__(self, name: str, ir_pv: mx.ProcessValue, maturityTenor: mx.Period):
        self._ir_pv = ir_pv
        self._maturityTenor = maturityTenor
        mx.core_DiscountBondCalc.__init__(self, name, ir_pv, maturityTenor)


# Bond Price Dynamics
class DiscountBondReturn(mx.core_DiscountBondReturnCalc):
    def __init__(self, name: str, ir_pv: mx.ProcessValue, 
                 maturityTenor: mx.Period, isConstantMaturity=True):
        self._ir_pv = ir_pv
        self._maturityTenor = maturityTenor
        self._isConstantMaturity = isConstantMaturity
        
        mx.core_DiscountBondReturnCalc.__init__(self, name, ir_pv, maturityTenor, isConstantMaturity)


class Overnight(mx.core_OvernightCalc):
    def __init__(self, name: str, ir_pv: mx.ProcessValue, overnightIndex: mx.OvernightIndex):
        self._ir_pv = ir_pv
        self._overnightIndex = overnightIndex

        mx.core_OvernightCalc.__init__(self, name, ir_pv, overnightIndex)


class Ibor(mx.core_IborCalc):
    def __init__(self, name: str, ir_pv: mx.ProcessValue, iborIndex: mx.IborIndex):
        self._ir_pv = ir_pv
        self._iborIndex = iborIndex

        mx.core_IborCalc.__init__(self, name, ir_pv, iborIndex)


class SwapRate(mx.core_SwapRateCalc):
    def __init__(self, name: str, ir_pv: mx.ProcessValue, swapIndex: mx.SwapIndex):
        self._ir_pv = ir_pv
        self._swapIndex = swapIndex

        mx.core_SwapRateCalc.__init__(self, name, ir_pv, swapIndex)


class BondRate(mx.core_BondRateCalc):
    def __init__(self, name: str, ir_pv: mx.ProcessValue, bondIndex: mx.BondIndex):
        self._ir_pv = ir_pv
        self._bondIndex = bondIndex

        mx.core_BondRateCalc.__init__(self, name, ir_pv, bondIndex)


# Fx model is reqired
# class FxRate(mx.core_FxRateCalc):
#     def __init__(self, name: str, fx_pv: mx.ProcessValue, fixing=None):
#         self._fx_pv = fx_pv
#         self._fixing = fixing

#         fixing_conv = mx.nullDouble() if fixing is None else fixing

#         mx.core_FxRateCalc.__init__(self, name, fx_pv, fixing_conv)


# math functions ---------------------

def min(pv_list: List[mx.ProcessValue], name=None):
    if name is None:
        name = '_'.join([pv.name() for pv in pv_list]) + 'min'
    return mx.core_MultaryFunctionWrapperCalc(name, pv_list, 'min')


def max(pv_list: List[mx.ProcessValue], name=None):
    if name is None:
        name = '_'.join([pv.name() for pv in pv_list]) + 'max'
    return mx.core_MultaryFunctionWrapperCalc(name, pv_list, 'max')



