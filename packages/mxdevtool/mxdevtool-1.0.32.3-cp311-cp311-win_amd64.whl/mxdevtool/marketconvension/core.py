import mxdevtool as mx
import mxdevtool.utils as utils


class OvernightIndex(mx.OvernightIndex):
    def __init__(self, familyName, settlementDays,
                 currency, calendar, dayCounter):

        args = utils.set_init_self_args(self, familyName, settlementDays,
                 currency, calendar, dayCounter)

        super().__init__(*args)

    
    @staticmethod
    def fromDict(d: dict):
        return utils.parseClassFromDict(d, globals())

    def toDict(self):
        return utils.serializeToDict(self)

    def getCalc(self, name, ir_model):
        from mxdevtool.xenarix.pathcalc import Overnight
        return Overnight(name, ir_model, self)
    

class IborIndex(mx.IborIndex):
    def __init__(self, familyName, tenor, settlementDays,
                 currency, calendar, convention,
                 endOfMonth, dayCounter):

        args = utils.set_init_self_args(self, familyName, tenor, settlementDays,
                 currency, calendar, convention, endOfMonth, dayCounter)

        super().__init__(*args)

    @staticmethod
    def fromDict(d: dict):
        return utils.parseClassFromDict(d, globals())

    def toDict(self):
        return utils.serializeToDict(self)

    def getCalc(self, name, ir_model):
        from mxdevtool.xenarix.pathcalc import Ibor
        return Ibor(name, ir_model, self)


class SwapIndex(mx.SwapIndex):
    def __init__(self, familyName, tenor, settlementDays,
                 currency, calendar, fixedLegTenor, fixedLegConvention,
                 fixedLegDayCounter, iborIndex):

        args = utils.set_init_self_args(self, familyName, tenor, settlementDays,
                 currency, calendar, fixedLegTenor, fixedLegConvention, fixedLegDayCounter, iborIndex)

        super().__init__(*args)

    @staticmethod
    def fromDict(d: dict):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, SwapIndex.__name__)

        familyName = d['familyName']
        tenor = utils.toPeriodCls(d['tenor'])
        settlementDays = d['settlementDays']
        currency = utils.toCurrencyCls(d['currency'])
        calendar = utils.toCalendarCls(d['calendar'])
        fixedLegTenor = utils.toPeriodCls(d['fixedLegTenor'])
        fixedLegConvention = utils.toBusinessDayConvention(d['fixedLegConvention'])
        fixedLegDayCounter = utils.toDayCounterCls(d['fixedLegDayCounter'])
        iborIndex = IborIndex.fromDict(d['iborIndex'])

        return SwapIndex(familyName, tenor, settlementDays,
                 currency, calendar, fixedLegTenor, fixedLegConvention,
                 fixedLegDayCounter, iborIndex)


    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['familyName'] = str(self._familyName)
        res['tenor'] = str(self._tenor)
        res['settlementDays'] = self._settlementDays
        res['currency'] = str(self._currency)
        res['calendar'] = str(self._calendar)
        res['fixedLegTenor'] = str(self._fixedLegTenor)
        res['fixedLegConvention'] = self._fixedLegConvention
        res['fixedLegDayCounter'] = str(self._fixedLegDayCounter)
        res['iborIndex'] = self._iborIndex.toDict()

        return res

    def getCalc(self, name, ir_model):
        from mxdevtool.xenarix.pathcalc import SwapRate
        return SwapRate(name, ir_model, self)


# fixed only
class BondIndex(mx.BondIndex):
    def __init__(self, familyName, tenor, settlementDays,
                 currency, calendar, fixedLegTenor, fixedLegConvention,
                 fixedLegDayCounter):

        args = utils.set_init_self_args(self, familyName, tenor, settlementDays,
                 currency, calendar, fixedLegTenor, fixedLegConvention, fixedLegDayCounter)

        super().__init__(*args)

    @staticmethod
    def fromDict(d: dict):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, BondIndex.__name__)

        familyName = d['familyName']
        tenor = utils.toPeriodCls(d['tenor'])
        settlementDays = d['settlementDays']
        currency = utils.toCurrencyCls(d['currency'])
        calendar = utils.toCalendarCls(d['calendar'])
        fixedLegTenor = utils.toPeriodCls(d['fixedLegTenor'])
        fixedLegConvention = utils.toBusinessDayConvention(d['fixedLegConvention'])
        fixedLegDayCounter = utils.toDayCounterCls(d['fixedLegDayCounter'])

        return BondIndex(familyName, tenor, settlementDays,
                 currency, calendar, fixedLegTenor, fixedLegConvention,
                 fixedLegDayCounter)


    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['familyName'] = str(self._familyName)
        res['tenor'] = str(self._tenor)
        res['settlementDays'] = self._settlementDays
        res['currency'] = str(self._currency)
        res['calendar'] = str(self._calendar)
        res['fixedLegTenor'] = str(self._fixedLegTenor)
        res['fixedLegConvention'] = self._fixedLegConvention
        res['fixedLegDayCounter'] = str(self._fixedLegDayCounter)

        return res

    def getCalc(self, name, ir_model):
        from mxdevtool.xenarix.pathcalc import BondRate
        return BondRate(name, ir_model, self)


# spot, forward
# class FxIndex(mx.FxIndex):
#     def __init__(self, familyName, tenor, settlementDays,
#                  domesticCurrency, foreignCurrency, domesticCalendar, foreignCalendar):

#         args = utils.set_init_self_args(self, familyName, tenor, settlementDays,
#                  domesticCurrency, foreignCurrency, domesticCalendar, foreignCalendar)

#         super().__init__(*args)

#     @staticmethod
#     def fromDict(d: dict):
#         mx.check_fromDict(d, mx.CLASS_TYPE_NAME, FxIndex.__name__)

#         familyName = d['familyName']
#         tenor = utils.toPeriodCls(d['tenor'])
#         settlementDays = d['settlementDays']
#         domesticCurrency = utils.toCurrencyCls(d['domesticCurrency'])
#         domesticCalendar = utils.toCalendarCls(d['domesticCalendar'])
#         foreignCurrency = utils.toCurrencyCls(d['foreignCurrency'])
#         foreignCalendar = utils.toCalendarCls(d['foreignCalendar'])        

#         return FxIndex(familyName, tenor, settlementDays,
#                  domesticCurrency, domesticCalendar, foreignCurrency, foreignCalendar)


#     def toDict(self):
#         res = dict()

#         res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
#         res['familyName'] = str(self._familyName)
#         res['tenor'] = str(self._tenor)
#         res['settlementDays'] = self._settlementDays
#         res['domesticCurrency'] = str(self._domesticCurrency)
#         res['domesticCalendar'] = str(self._domesticCalendar)
#         res['foreignCurrency'] = str(self._foreignCurrency)
#         res['foreignCalendar'] = str(self._foreignCalendar)
        
#         return res

#     def getCalc(self, name, fx_model):
#         from mxdevtool.xenarix.pathcalc import FXRate
#         return FXRate(name, fx_model, self)


class FixedBondMarketConvension(mx.core_FixedBondMarketConvension):
    def __init__(self, calendar, dayCounter, businessDayConvention,
                 settlementDays, couponTenor, compounding, familyname):

        args = utils.set_init_self_args(self, calendar, dayCounter, businessDayConvention,
                 settlementDays, couponTenor, compounding, familyname)

        # this for intellisense
        self._calendar: mx.Calendar = self._calendar
        self._dayCounter: mx.DayCounter = self._dayCounter
        self._businessDayConvention: int = self._businessDayConvention
        self._settlementDays: int = self._settlementDays
        self._couponTenor: mx.Period = self._couponTenor
        self._compounding: int = self._compounding
        self._familyname: str = self._familyname

        super().__init__(*args)

    @staticmethod
    def fromDict(d: dict):
        return utils.parseClassFromDict(d, globals())

    def toDict(self):
        return utils.serializeToDict(self)


class VanillaSwapMarketConvension(mx.core_VanillaSwapMarketConvension):
    def __init__(self, calendar, dayCounter, businessDayConvention,
                 settlementDays, couponTenor, iborIndex, familyname):

        args = utils.set_init_self_args(self, calendar, dayCounter, businessDayConvention,
                 settlementDays, couponTenor, iborIndex, familyname)

        # this for intellisense
        self._calendar: mx.Calendar = self._calendar
        self._dayCounter: mx.DayCounter = self._dayCounter
        self._businessDayConvention: int = self._businessDayConvention
        self._settlementDays: int = self._settlementDays
        self._couponTenor: mx.Period = self._couponTenor
        self._iborIndex: IborIndex = self._iborIndex
        self._familyname: str = self._familyname

        super().__init__(*args)

    @staticmethod
    def fromDict(d: dict):
        return utils.parseClassFromDict(d, globals())

    def toDict(self):
        return utils.serializeToDict(self)



class IndexFactory:
    def __init__(self) -> None:
        pass
        
    def get_overnightIndex(self, name: str) -> OvernightIndex:
        index = None
        if name == 'sofr': index = mx.Sofr()
        elif name == 'estr': index = mx.Estr()
        elif name == 'aonia': index = mx.Aonia()
        elif name == 'eonia': index = mx.Eonia()
        elif name == 'sonia': index = mx.Sonia()
        elif name == 'fedfunds': index = mx.FedFunds()
        # elif name == 'tona': index = mx.Tona()
        else:
            raise Exception('unknown iborIndex - {0}'.format(name))

        return OvernightIndex(index.familyName(), index.fixingDays(), index.currency(), index.fixingCalendar(), index.dayCounter())

    def get_iborIndex(self, name: str, tenor: mx.Period) -> IborIndex:
        if name in ['krwcd']: return IborIndex("KrwCD", tenor, 1, mx.KRWCurrency(), mx.SouthKorea(), mx.ModifiedFollowing, True, mx.Actual365Fixed())
        elif name in ['libor']: return IborIndex("libor", tenor, 1, mx.USDCurrency(), mx.UnitedStates(mx.UnitedStates.GovernmentBond), mx.ModifiedFollowing, True, mx.Actual360())
        else:
            pass

        raise Exception('unknown iborIndex - {0}'.format(name))
    
    def get_bondIndex(self, name: str, tenor: mx.Period, fixedLegTenor: mx.Period) -> BondIndex:
        if name in ['ktb']:
            return BondIndex("ktb", tenor, 1, mx.KRWCurrency(), mx.SouthKorea(), fixedLegTenor, mx.ModifiedFollowing, mx.Actual365Fixed())
        else:
            pass

        raise Exception('unknown iborIndex - {0}'.format(name))
    
    def get_swapIndex(self, name: str, tenor: mx.Period, fixedLegTenor: mx.Period) -> SwapIndex:
        if name in ['krwirs']:
            return SwapIndex("Krwirs", tenor, 1, mx.KRWCurrency(), mx.SouthKorea(), 
                             fixedLegTenor,  mx.ModifiedFollowing, mx.Actual365Fixed(), self.get_iborIndex('krwcd', mx.Period('3m')))
        elif name == 'libor':
            return SwapIndex('libor', tenor, 1, mx.USDCurrency(), mx.UnitedStates(mx.UnitedStates.GovernmentBond), 
                             fixedLegTenor, mx.ModifiedFollowing, mx.Actual360(), self.get_iborIndex('libor', mx.Period('3m')))
        else:
            pass

        raise Exception('unknown iborIndex - {0}'.format(name))

    def createByName(self, name):
        index = None
        if name == 'sofr':
            index = mx.Sofr()
        else:
            return index
        
        return OvernightIndex(index.familyName())


def marketConvensionFromDict(d: dict):
    if not isinstance(d, dict):
        raise Exception('dictionary is required - {0}'.format(d))

    clsnm = d[mx.CLASS_TYPE_NAME]
    if clsnm == FixedBondMarketConvension.__name__:
        return FixedBondMarketConvension.fromDict(d)
    elif clsnm == VanillaSwapMarketConvension.__name__:
        return VanillaSwapMarketConvension.fromDict(d)

    raise Exception('unknown marketConvension - {0}'.format(clsnm))


def get_marketConvension_fixedbond(name) -> FixedBondMarketConvension:
    if name == 'ktb1':
        return FixedBondMarketConvension(
            mx.SouthKorea(), mx.Actual365Fixed(), mx.ModifiedFollowing, 1, mx.Period('3m'), mx.Compounded, name)
    elif name == 'ktb2':
        return FixedBondMarketConvension(
            mx.SouthKorea(), mx.Actual365Fixed(), mx.ModifiedFollowing, 1, mx.Period('6m'), mx.Compounded, name)

    return None


def get_marketConvension_vanillaswap(name) -> VanillaSwapMarketConvension:
    if name in ('irskrw', 'irskrw_krccp'):
        iborIndex = get_iborIndex('krwcd', '3m')
        return VanillaSwapMarketConvension(
            mx.SouthKorea(), mx.Actual365Fixed(), mx.ModifiedFollowing, 1, mx.Period('3m'), iborIndex, name)

    return None


def get_marketConvension(name):
    fb = get_marketConvension_fixedbond(name)
    if fb != None: return fb

    vs = get_marketConvension_vanillaswap(name)
    if vs != None: return vs

    raise Exception('unknown marketConvension - {0}'.format(name))


