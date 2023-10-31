from typing import List
import mxdevtool as mx
import mxdevtool.xenarix as xen
import mxdevtool.termstructures as mx_t
import mxdevtool.marketconvension as mx_mc
import mxdevtool.utils as utils


# condition -----------------------------
class ANDCondition(mx.core_ANDConditionMC):
    def __init__(self, conditions: List[mx.ConditionMC]):
        self._conditions = conditions
        mx.core_ANDConditionMC.__init__(self, conditions)

    # @staticmethod
    # def fromDict(d: dict):
    #     mx.check_fromDict(d, mx.CLASS_TYPE_NAME, ANDCondition.__name__)
    #     conditions = toStructuredClsList(d['conditions'])
    #     return ANDCondition(conditions)

    # def toDict(self):
    #     res = dict()
    #     res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
    #     res['conditions'] = str(self._conditions)
    #     return res


class ORCondition(mx.core_ORConditionMC):
    def __init__(self, conditions: List[mx.ConditionMC]):
        self._conditions = conditions
        mx.core_ORConditionMC.__init__(self, conditions)

    # @staticmethod
    # def fromDict(d: dict):
    #     mx.check_fromDict(d, mx.CLASS_TYPE_NAME, ORCondition.__name__)
    #     conditions = toStructuredClsList(d['conditions'])
    #     return ORCondition(conditions)

    # def toDict(self):
    #     res = dict()
    #     res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
    #     res['conditions'] = str(self._conditions)
    #     return res
    

class XORCondition(mx.core_XORConditionMC):
    def __init__(self, condition1: mx.ConditionMC, condition2: mx.ConditionMC):
        self._condition1 = condition1
        self._condition2 = condition2
        mx.core_XORConditionMC.__init__(self, condition1, condition2)

    # @staticmethod
    # def fromDict(d: dict):
    #     mx.check_fromDict(d, mx.CLASS_TYPE_NAME, XORCondition.__name__)
    #     condition1 = toStructuredCls(d['condition1'])
    #     condition2 = toStructuredCls(d['condition2'])
    #     return XORCondition(condition1, condition2)

    # def toDict(self):
    #     res = dict()
    #     res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
    #     res['conditions'] = toDictList(self._conditions)
    #     return res
    

class NOTCondition(mx.core_NOTConditionMC):
    def __init__(self, condition: mx.ConditionMC):
        self._condition = condition
        mx.core_NOTConditionMC.__init__(self, condition)

    # @staticmethod
    # def fromDict(d: dict):
    #     mx.check_fromDict(d, mx.CLASS_TYPE_NAME, NOTCondition.__name__)
    #     condition = toStructuredCls(d['condition'])
    #     return NOTCondition(condition)

    # def toDict(self):
    #     res = dict()
    #     res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
    #     res['condition'] = self._condition.toDict()
    #     return res
    

class RangeCondition(mx.core_RangeConditionMC):
    def __init__(self, po: mx.PayoffMC, a: float, b: float):
        self._po = po
        self._a = a
        self._b = b
        mx.core_RangeConditionMC.__init__(self, po, a, b)

    # @staticmethod
    # def fromDict(d: dict):
    #     mx.check_fromDict(d, mx.CLASS_TYPE_NAME, RangeCondition.__name__)
    #     po = toStructuredCls(d['po'])
    #     a = float(d['a'])
    #     b = float(d['b'])
    #     return RangeCondition(po, a, b)

    # def toDict(self):
    #     res = dict()
    #     res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
    #     res['po'] = self._po.toDict()
    #     res['a'] = self._a
    #     res['b'] = self._b

    #     return res
    

class ANDDatesCondition(mx.core_DatesConditionMC):
    def __init__(self, po: mx.PayoffMC, dates: List[mx.Date]):
        self._po = po
        self._dates = dates
        mx.core_DatesConditionMC.__init__(self, po, dates, 'and')

    # @staticmethod
    # def fromDict(d: dict):
    #     mx.check_fromDict(d, mx.CLASS_TYPE_NAME, ANDDatesCondition.__name__)
    #     po = toStructuredCls(d['po'])
    #     dates = utils.toDateClsList(d['dates'])
    #     return ANDDatesCondition(po, dates)

    # def toDict(self):
    #     res = dict()
    #     res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
    #     res['po'] = self._po.toDict()
    #     res['dates'] = self._dates

    #     return res
    

class ORDatesCondition(mx.core_DatesConditionMC):
    def __init__(self, po: mx.PayoffMC, dates: List[mx.Date]):
        self._po = po
        self._dates = dates
        mx.core_DatesConditionMC.__init__(self, po, dates, 'or')

    # @staticmethod
    # def fromDict(d: dict):
    #     mx.check_fromDict(d, mx.CLASS_TYPE_NAME, ORDatesCondition.__name__)
    #     po = toStructuredCls(d['po'])
    #     dates = utils.toDateClsList(d['dates'])
    #     return ORDatesCondition(po, dates)

    # def toDict(self):
    #     res = dict()
    #     res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
    #     res['po'] = self._po.toDict()
    #     res['dates'] = self._dates

    #     return res
    

# class ANDBetweenDatesCondition(mx.core_BetweenDatesConditionMC):
#     def __init__(self, po, dates):
#         self._po = po
#         self._dates = dates
#         mx.core_BetweenDatesConditionMC.__init__(self, po, dates, 'and')


# class ORBetweenDatesCondition(mx.core_BetweenDatesConditionMC):
#     def __init__(self, po, dates):
#         self._po = po
#         self._dates = dates
#         mx.core_BetweenDatesConditionMC.__init__(self, po, dates, 'or')


class RelationalCondition(mx.core_RelationalConditionMC):
    def __init__(self, po1: mx.PayoffMC, operand: str, po2: mx.PayoffMC):
        self._po1 = po1
        self._operand = operand
        self._po2 = po2
        mx.core_RelationalConditionMC.__init__(self, po1, operand, po2)

    # @staticmethod
    # def fromDict(d: dict):
    #     mx.check_fromDict(d, mx.CLASS_TYPE_NAME, RelationalCondition.__name__)
    #     po1 = toStructuredCls(d['po1'])
    #     operand = d['operand']
    #     po2 = toStructuredCls(d['po2'])

    #     return RelationalCondition(po1, operand, po2)

    # def toDict(self):
    #     res = dict()
    #     res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
    #     res['po1'] = self._po1.toDict()
    #     res['operand'] = self._operand
    #     res['po2'] = self._po2.toDict()

    #     return res
    

# operators -----------------------------
class PlusPayoff(mx.core_PlusPayoffMC):
    def __init__(self, po: mx.PayoffMC):
        self._po = po
        mx.core_PlusPayoffMC.__init__(self, po)


class MinusPayoff(mx.core_MinusPayoffMC):
    def __init__(self, po: mx.PayoffMC):
        self._po = po
        mx.core_MinusPayoffMC.__init__(self, po)


class AdditionPayoff(mx.core_AdditionPayoffMC):
    def __init__(self, po1: mx.PayoffMC, po2: mx.PayoffMC):
        self._po1 = po1
        self._po2 = po2
        mx.core_AdditionPayoffMC.__init__(self, po1, po2)


class SubtractionPayoff(mx.core_SubtractionPayoffMC):
    def __init__(self, po1: mx.PayoffMC, po2: mx.PayoffMC):
        self._po1 = po1
        self._po2 = po2
        mx.core_SubtractionPayoffMC.__init__(self, po1, po2)


class MultiplicationPayoff(mx.core_MultiplicationPayoffMC):
    def __init__(self, po1: mx.PayoffMC, po2: mx.PayoffMC):
        self._po1 = po1
        self._po2 = po2
        mx.core_MultiplicationPayoffMC.__init__(self, po1, po2)


class DivisionPayoff(mx.core_DivisionPayoffMC):
    def __init__(self, po1: mx.PayoffMC, po2: mx.PayoffMC):
        self._po1 = po1
        self._po2 = po2
        mx.core_DivisionPayoffMC.__init__(self, po1, po2)


class IdentityPayoff(mx.core_IdentityPayoffMC):
    def __init__(self, po: mx.PayoffMC):
        self._po = po
        mx.core_IdentityPayoffMC.__init__(self, po)


class LinearPayoff(mx.core_LinearPayoffMC):
    def __init__(self, po: mx.PayoffMC, multiple: float, spread: float):
        self._po = po
        self._multiple = multiple
        self._spread = spread
        mx.core_LinearPayoffMC.__init__(self, po, multiple, spread)


class ConstantPayoff(mx.core_ConstantPayoffMC):
    def __init__(self, v: float):
        self._v = v
        mx.core_ConstantPayoffMC.__init__(self, v)


class ConditionPayoff(mx.core_ConditionPayoffMC):
    def __init__(self, condi: mx.ConditionMC, po_true: mx.PayoffMC, po_false: mx.PayoffMC):
        self._condi = condi
        self._po_true = po_true
        self._po_false = po_false
        mx.core_ConditionPayoffMC.__init__(self, condi, po_true, po_false)


class IndexPayoff(mx.core_IndexPayoffMC):
    def __init__(self, name: str):
        self._name = name
        mx.core_IndexPayoffMC.__init__(self, name)

    def index(self) -> mx.Index:
        return self._index()

    # parsing ex) krwirs10y
    # def as_iborIndex(self) -> mx_mc.IborIndex:
    #     mx_mc.get_iborIndex(self._name)

    def as_swapIndex(self) -> mx_mc.SwapIndex:
        mx_mc.get_swapIndex(self._name)

    @staticmethod
    def fromDict(d: dict):
        return utils.parseClassFromDict(d, globals())

    def toDict(self):
        return utils.serializeToDict(self)


class MinPayoff(mx.core_MinPayoffMC):
    def __init__(self, po1: mx.PayoffMC, po2: mx.PayoffMC):
        self._po1 = po1
        self._po2 = po2
        mx.core_MinPayoffMC.__init__(self, po1, po2, 'min')


class MaxPayoff(mx.core_MaxPayoffMC):
    def __init__(self, po1: mx.PayoffMC, po2: mx.PayoffMC):
        self._po1 = po1
        self._po2 = po2
        mx.core_MaxPayoffMC.__init__(self, po1, po2, 'max')


class MinimumBetweenDatesPayoff(mx.core_MinimumBetweenDatesPayoffMC):
    def __init__(self, po: mx.PayoffMC, startDate: mx.Date, endDate: mx.Date, hist_minimum=mx.nullDouble()):
        self._po = po
        self._startDate = startDate
        self._endDate = endDate
        mx.core_MinimumBetweenDatesPayoffMC.__init__(self, po, startDate, endDate, hist_minimum)


class MaximumBetweenDatesPayoff(mx.core_MaximumBetweenDatesPayoffMC):
    def __init__(self, po: mx.PayoffMC, startDate: mx.Date, endDate: mx.Date, hist_maximum=mx.nullDouble()):
        self._po = po
        self._startDate = startDate
        self._endDate = endDate
        mx.core_MaximumBetweenDatesPayoffMC.__init__(self, po, startDate, endDate, hist_maximum)


class AverageBetweenDatesPayoff(mx.core_AverageBetweenDatesPayoffMC):
    def __init__(self, po: mx.PayoffMC, startDate: mx.Date, endDate: mx.Date, hist_average=mx.nullDouble()):
        self._po = po
        self._startDate = startDate
        self._endDate = endDate
        mx.core_AverageBetweenDatesPayoffMC.__init__(self, po, startDate, endDate, hist_average)


class MinimumDatesPayoff(mx.core_MinimumDatesPayoffMC):
    def __init__(self, po: mx.PayoffMC, dates: List[mx.Date]):
        self._po = po
        self._dates = dates
        mx.core_MinimumDatesPayoffMC.__init__(self, po, dates)


class MaximumDatesPayoff(mx.core_MaximumDatesPayoffMC):
    def __init__(self, po: mx.PayoffMC, dates: List[mx.Date]):
        self._po = po
        self._dates = dates
        mx.core_MaximumDatesPayoffMC.__init__(self, po, dates)


class AverageDatesPayoff(mx.core_AverageDatesPayoffMC):
    def __init__(self, po: mx.PayoffMC, dates: List[mx.Date]):
        self._po = po
        self._dates = dates
        mx.core_AverageDatesPayoffMC.__init__(self, po, dates)


class MathExpressionPayoff(mx.core_MathExpressionPayoffMC):
    def __init__(self, expression: str, **kwargs):
        self._expression = expression
        self._kwargs = kwargs

        med = utils.make_MathExpressionDictionary(kwargs)

        mx.core_MathExpressionPayoffMC.__init__(self, expression, med)


# coupons -----------------------------

class RateAccrualCouponMC(mx.core_RateAccrualCouponMC):
    def __init__(self, paymentDate, nominal, payoffMC,
                 accrualStartDate, accrualEndDate, calendar, dayCounter):

        args = utils.set_init_self_args(self, paymentDate, nominal, payoffMC,
                accrualStartDate, accrualEndDate, calendar, dayCounter)

        super().__init__(*args)

    @staticmethod
    def makeLeg(schedule, payoffMC, notional=10000,
                calendar=mx.SouthKorea(), dayCounter=mx.Actual365Fixed()):

        cpns = []

        for i, d in enumerate(schedule):
            if i == 0: continue

            cpn = RateAccrualCouponMC(
                schedule[i],
                notional,
                payoffMC,
                schedule[i-1],
                schedule[i],
                calendar,
                dayCounter)

            cpns.append(cpn)

        return cpns

    def getResults(self) -> dict:
        res = {}

        # res = self.getCommonResults()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__

        res['npv'] = self._get_result_value('npv')
        res['amount'] = self._get_result_value('amount')
        res['discount'] = self._get_result_value('discount')
        res['time'] = self.accrualPeriod()

        return res


class FloatingRateCouponMC(mx.core_FloatingRateCouponMC):
    def __init__(self, paymentDate, nominal, fixingDays, indexPayoffMC, 
                accrualStartDate, accrualEndDate, calendar,
                dayCounter, gearing=1.0, spread=0.0):

        self._paymentDate = paymentDate
        self._nominal = nominal
        self._fixingDays = fixingDays
        self._indexPayoffMC = indexPayoffMC
        self._accrualStartDate = accrualStartDate
        self._accrualEndDate = accrualEndDate
        self._calendar = calendar
        self._dayCounter = dayCounter
        self._gearing = gearing
        self._spread = spread

        mx.core_FloatingRateCouponMC.__init__(self, self._paymentDate, self._nominal,
                    fixingDays, self._indexPayoffMC, self._accrualStartDate, self._accrualEndDate, self._calendar,
                    dayCounter, self._gearing, self._spread)

    @staticmethod
    def makeLeg(schedule, indexPayoffMC, notional=10000, fixingDays=1,
                calendar=mx.SouthKorea(), dayCounter=mx.Actual365Fixed(), gearing=1.0, spread=0.0):

        cpns = []

        for i, d in enumerate(schedule):
            if i == 0: continue

            cpn = FloatingRateCouponMC(
                schedule[i],
                notional,
                fixingDays,
                indexPayoffMC,
                schedule[i-1],
                schedule[i],
                calendar,
                dayCounter,
                gearing,
                spread)

            cpns.append(cpn)

        return cpns

    def getResults(self) -> dict:
        res = {}

        # res = self.getCommonResults()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__

        res['npv'] = self._get_result_value('npv')
        res['amount'] = self._get_result_value('amount')
        res['discount'] = self._get_result_value('discount')
        res['time'] = self.accrualPeriod()

        return res

    def getScenResults(self, scenCount):
        res = {}
        # res['indexPayoffMC'] = indexPayoffMC.getScenResults()
        return res



class ReturnCouponMC(mx.core_ReturnCouponMC):
    def __init__(self, paymentDate: mx.Date, notional: float, 
                 fixingDate: mx.Date, payoffMC: mx.PayoffMC, calendar: mx.Calendar, dayCounter: mx.DayCounter):
            
        self._paymentDate = paymentDate
        self._notional = notional
        self._fixingDate = fixingDate
        self._payoffMC = payoffMC
        self._calendar = calendar
        self._dayCounter = dayCounter

        mx.core_ReturnCouponMC.__init__(self, self._paymentDate, self._notional, self._fixingDate, self._payoffMC, 
                                        self._calendar, self._dayCounter)    


class SimpleCouponMC(ReturnCouponMC):
    def __init__(self, paymentDate: mx.Date, fixingDate: mx.Date, payoffMC: mx.PayoffMC, 
                 calendar: mx.Calendar, dayCounter: mx.DayCounter):
            
        self._paymentDate = paymentDate
        self._fixingDate = fixingDate
        self._payoffMC = payoffMC
        self._calendar = calendar
        self._dayCounter = dayCounter

        ReturnCouponMC.__init__(self, self._paymentDate, 1.0, self._fixingDate, self._payoffMC, 
                                        self._calendar, self._dayCounter)    


class RateCouponMC(mx.core_RateCouponMC):
    def __init__(self, paymentDate: mx.Date, notional: float, fixingDate: mx.Date, payoffMC: mx.PayoffMC, 
                 accrualStartDate: mx.Date, accrualEndDate: mx.Date, calendar: mx.Calendar, dayCounter: mx.DayCounter):
            
        self._paymentDate = paymentDate
        self._notional = notional
        self._fixingDate = fixingDate
        self._payoffMC = payoffMC
        self._accrualStartDate = accrualStartDate
        self._accrualEndDate = accrualEndDate
        self._calendar = calendar
        self._dayCounter = dayCounter

        mx.core_RateCouponMC.__init__(self, self._paymentDate, self._notional, self._fixingDate, 
                                      self._payoffMC, self._accrualStartDate, self._accrualEndDate, 
                                      self._calendar, self._dayCounter)


class ReturnAccrualCouponMC(mx.core_ReturnAccrualCouponMC):
    def __init__(self, paymentDate: mx.Date, notional: float, payoffMC: mx.PayoffMC, accrualStartDate: mx.Date, accrualEndDate: mx.Date, 
                 calendar: mx.Calendar, dayCounter: mx.DayCounter):
        
        self._paymentDate = paymentDate
        self._notional = notional
        self._payoffMC = payoffMC
        self._accrualStartDate = accrualStartDate
        self._accrualEndDate = accrualEndDate
        self._calendar = calendar
        self._dayCounter = dayCounter

        mx.core_ReturnAccrualCouponMC.__init__(self, self._paymentDate, self._notional, 
                                        self._payoffMC, self._accrualStartDate, self._accrualEndDate, 
                                        self._calendar, self._dayCounter)


class RateAccrualCouponMC(mx.core_RateAccrualCouponMC):
    def __init__(self, paymentDate: mx.Date, notional: float, payoffMC: mx.PayoffMC, accrualStartDate: mx.Date, accrualEndDate: mx.Date, 
                 calendar: mx.Calendar, dayCounter: mx.DayCounter):
        
        self._paymentDate = paymentDate
        self._notional = notional
        self._payoffMC = payoffMC
        self._accrualStartDate = accrualStartDate
        self._accrualEndDate = accrualEndDate
        self._calendar = calendar
        self._dayCounter = dayCounter

        mx.core_RateAccrualCouponMC.__init__(self, self._paymentDate, self._notional, 
                                        self._payoffMC, self._accrualStartDate, self._accrualEndDate, 
                                        self._calendar, self._dayCounter)



class MathExpressionCouponMC(mx.core_MathExpressionCouponMC):
    def __init__(self, paymentDate: mx.Date, notional: float, fixingDate: mx.Date, payoffMC: mx.PayoffMC, 
                 accrualStartDate: mx.Date, accrualEndDate: mx.Date, 
                 expr: str, calendar: mx.Calendar, dayCounter: mx.DayCounter):
            
        self._paymentDate = paymentDate
        self._notional = notional
        self._fixingDate = fixingDate
        self._payoffMC = payoffMC
        self._accrualStartDate = accrualStartDate
        self._accrualEndDate = accrualEndDate
        self._expr = expr
        self._calendar = calendar
        self._dayCounter = dayCounter

        mx.core_MathExpressionCouponMC.__init__(self, self._paymentDate, self._notional, self._fixingDate,
                 self._payoffMC, self._accrualStartDate, self._accrualEndDate, self._expr, self._calendar, self._dayCounter)


class AutoCallableCouponMC(mx.core_AutoCallableCouponMC):
    def __init__(self, paymentDate: mx.Date, condition: mx.ConditionMC, baseCoupon: mx.CouponMC) -> None:
        self._paymentDate = paymentDate
        self._condition = condition
        self._baseCoupon = baseCoupon

        mx.core_AutoCallableCouponMC.__init__(self, self._paymentDate, self._condition, self._baseCoupon)


# instruments ------------------------------------------------------------ 

class StructuredLegExerciseOption(mx.core_StructuredLegExerciseOption):
    def __init__(self, dates, settlementDates, amounts):
        args = utils.set_init_self_args(self, dates, settlementDates, amounts)

        super().__init__(*args)


class VanillaLegInfo(mx.core_VanillaLegInfo):
    def __init__(self, coupons: List[mx.CouponMC], currency=utils.toCurrencyCls('krw')):
        
        self._coupons = coupons
        self._currency = currency

        mx.core_VanillaLegInfo.__init__(self, self._coupons, self._currency)

    @staticmethod
    def fromDict(d: dict):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, StructuredSwap.__name__)
        coupons = toStructuredClsList(d['coupons'])
        currency = utils.toCurrencyCls(d['currency'])

        return VanillaLegInfo(coupons, currency)

    def toDict(self):
        res = dict()
        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['coupons'] = [cpn.toDict() for cpn in self._coupons]
        res['currency'] = str(self._currency)

        return res
    
    def getResults(self) -> dict:
        res = {}

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__

        coupons = []

        for cpn in self._coupons:
            d = cpn.getResults()
            coupons.append(d)

        res['coupons'] = coupons
        res['npv'] = self._get_result_value()
        res['leg_npv'] = self._get_result_value('leg_npv')

        return res


class StructuredLegInfo(mx.core_StructuredLegInfo):
    def __init__(self, coupons: List[mx.CouponMC], currency=utils.toCurrencyCls('krw'), option=None):
        self._coupons = coupons
        self._currency = currency
        self._option = option

        mx.core_StructuredLegInfo.__init__(self, self._coupons, self._currency)


    def getResults(self) -> dict:
        res = super().getResults()

        coupons = []

        for cpn in self._coupons:
            d = cpn.getResults()
            coupons.append(d)

        res['coupons'] = coupons
        res['option'] = 0.0

        return res

    def getScenResults(self):
        res = super().getResults()

        coupons = []

        for cpn in self._coupons:
            d = cpn.getScenResults()
            coupons.append(d)

        res['coupons'] = coupons
        res['option'] = 0.0

        return res


class StructuredSwap(mx.core_StructuredSwap):
    def __init__(self, payLegInfo: mx.LegInfo, recLegInfo: mx.LegInfo):
        self._payLegInfo = payLegInfo
        self._recLegInfo = recLegInfo

        mx.core_StructuredSwap.__init__(self, payLegInfo, recLegInfo)

    @staticmethod
    def fromDict(d: dict):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, StructuredSwap.__name__)
        payLegInfo = toStructuredCls(d['payLegInfo'])
        recLegInfo = toStructuredCls(d['recLegInfo'])

        return StructuredSwap(payLegInfo, recLegInfo)

    def toDict(self):
        res = dict()
        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['payLegInfo'] = self._payLegInfo.toDict()
        res['recLegInfo'] = self._recLegInfo.toDict()

        return res
    
    def payCpns(self) -> List[mx.CouponMC]:
        return self._payLegInfo._coupons

    def recCpns(self) -> List[mx.CouponMC]:
        return self._recLegInfo._coupons

    def setPricingParams_Scen(self, scen_filename: str, pay_discount: str, rec_discount: str, 
                              globalVariables = mx.MathExpressionGlobalDictionary(),
                              settingVariables = mx.SettingVariableDictionary()):
        self._setPricingParams_Scen(scen_filename, pay_discount, rec_discount, globalVariables, settingVariables)
        return self

    def getResults(self):
        res_d = super().getResults()

        res_d['payLegInfo'] = self._payLegInfo.getResults()
        res_d['recLegInfo'] = self._recLegInfo.getResults()

        return res_d

    def getScenResults(self, scenCount):
        return self.scenario_calculate(scenCount)
        
    

class StructuredBond(mx.core_StructuredBond):
    def __init__(self, legInfo: mx.LegInfo, option):
        self._legInfo = legInfo
        self._option = option

        mx.core_StructuredBond.__init__(self, legInfo)

    @staticmethod
    def fromDict(d: dict):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, StructuredSwap.__name__)
        legInfo = toStructuredCls(d['legInfo'])
        option = toStructuredCls(d['option'])

        return StructuredSwap(legInfo, option)

    def toDict(self):
        res = dict()
        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['legInfo'] = self._legInfo.toDict()
        res['option'] = self._option.toDict()

        return res
    
    def cpns(self) -> List[mx.CouponMC]:
        return self._legInfo._coupons

    def setPricingParams_Scen(self, discount: str or mx.YieldTermStructure, scen: xen.ScenarioResults or xen.Scenario, 
                              reg_index_names: str, global_variable_d: dict):
        mes = utils.make_MathExpressionDictionary(global_variable_d)
        self._setPricingParams_Scen(discount, reg_index_names, scen)
        return self
    

def toDictList(items):
    return [item.toDict() for item in items]


def toStructuredCls(d):
    return ANDCondition()


def toStructuredClsList(items: list) -> list:
    return [toStructuredCls(item) for item in items]

