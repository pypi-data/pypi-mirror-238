from urllib.parse import SplitResult
import mxdevtool as mx
import mxdevtool.utils as utils
import mxdevtool.marketconvension as mx_m
from typing import List


def setSmithWilsonParameter(curve: mx.YieldCurveExt, d):
    extrapolationType = utils.toExtrapolator1DType(d['extrapolationType'])

    if extrapolationType == mx.Extrapolator1D.SmithWilson:
        alpha = d['smithwilsonAlpha']
        ufr = d['smithwilsonUFR']
        curve.setSmithwilsonParameter(alpha, ufr)

    return curve


# termstructures
class FlatForward(mx.FlatForward):
    def __init__(self, refDate: mx.Date, forward: float,
                   dayCounter=mx.Actual365Fixed(),
                   compounding=mx.Compounded,
                   frequency=mx.Annual):

        self._refDate = utils.toDateCls(refDate)
        self._forward = forward
        self._dayCounter = utils.toDayCounterCls(dayCounter)
        self._compounding = utils.toCompounding(compounding)
        self._frequency = utils.toFrequency(frequency)

        mx.FlatForward.__init__(self, self._refDate, forward, dayCounter, compounding, frequency)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, FlatForward.__name__)

        refDate = utils.toDateCls(d['refDate'])
        forward = d['forward']
        dayCounter = utils.toDayCounterCls(d['dayCounter'])
        compounding = utils.toCompounding(d['compounding'])
        frequency = utils.toFrequency(d['frequency'])

        return FlatForward(refDate, forward, dayCounter, compounding, frequency)

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['refDate'] = str(self._refDate)
        res['forward'] = self._forward
        res['dayCounter'] = str(self._dayCounter)
        res['compounding'] = str(self._compounding)
        res['frequency'] = str(self._frequency)

        return res

    def shocked_clone(self, shock, method='absolute'):
        v = self._forward
        if method == 'relative': v *= (1.0 + shock)
        else: v += shock

        return FlatForward(self._refDate, v, self._dayCounter, self._compounding, self._frequency)

    def clone(self, **kwargs):
        refDate = kwargs['refDate'] if 'refDate' in kwargs else self._refDate
        forward = kwargs['forward'] if 'forward' in kwargs else self._forward
        dayCounter = kwargs['dayCounter'] if 'dayCounter' in kwargs else self._dayCounter
        compounding = kwargs['compounding'] if 'compounding' in kwargs else self._compounding
        frequency = kwargs['frequency'] if 'frequency' in kwargs else self._frequency

        return FlatForward(refDate, forward, dayCounter, compounding, frequency)

    def graph_view(self, typ=None, **kwargs):
        from mxdevtool.view import graph

        # period ( 1Y to 20Y )
        x =  [ v+1 for v in range(20) ]
        y1 = [ self.zeroRate(t, self._compounding).rate() for t in x]

        ydata_d = {'zeroRates': y1}
        return graph(name='FlatForward', xdata=x, ydata_d=ydata_d, **kwargs)


class DiscountCurve(mx.DiscountCurve):
    def __init__(self, dates, discounts, dayCounter, calendar=mx.default_calendar(), 
                 interpolationType=mx.Interpolator1D.Linear,
                 extrapolationType=mx.Extrapolator1D.FlatForward):
        
        self._dates = utils.toDateClsList(dates)
        self._discounts = discounts
        self._dayCounter = utils.toDayCounterCls(dayCounter)
        self._calendar = utils.toCalendarCls(calendar)
        self._interpolationType = utils.toInterpolator1DType(interpolationType)
        self._extrapolationType = utils.toExtrapolator1DType(extrapolationType)

        mx.DiscountCurve.__init__(self, self._dates, self._discounts, self._dayCounter, self._calendar)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, ZeroYieldCurve.__name__)

        dates = d['dates']
        discounts = d['discounts']
        dayCounter = d['dayCounter']
        calendar = d['calendar']
        interpolationType = utils.toInterpolator1DType(d['interpolationType'])
        extrapolationType = utils.toExtrapolator1DType(d['extrapolationType'])

        curve = DiscountCurve(dates, discounts, dayCounter, calendar, interpolationType, extrapolationType)

        # setSmithWilsonParameter(curve, d)

        return curve

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['dates'] = str(self._dates)
        res['discounts'] = self._discounts
        res['dayCounter'] = str(self._dayCounter)
        res['calendar'] = str(self._calendar)
        res['interpolationType'] = utils.interpolator1DToString(self._interpolationType)
        res['extrapolationType'] = utils.extrapolator1DToString(self._extrapolationType)

        return res

    def shocked_clone(self, shock, method='absolute'):
        # convert to zero ?
        shocked_value = utils.calculateShock(shock, method, self._discounts)

        return DiscountCurve(self._dates, shocked_value, self._dayCounter, self._calendar, self._interpolationType, self._extrapolationType)

    def clone(self, **kwargs):
        dates = kwargs['dates'] if 'dates' in kwargs else self._dates
        discounts = kwargs['discounts'] if 'discounts' in kwargs else self._discounts
        dayCounter = kwargs['dayCounter'] if 'dayCounter' in kwargs else self._dayCounter
        calendar = kwargs['calendar'] if 'calendar' in kwargs else self._calendar
        interpolationType = kwargs['interpolationType'] if 'interpolationType' in kwargs else self._interpolationType
        extrapolationType = kwargs['extrapolationType'] if 'extrapolationType' in kwargs else self._extrapolationType

        return DiscountCurve(dates, discounts, dayCounter, calendar, interpolationType, extrapolationType)

    def graph_view(self, **kwargs):
        from mxdevtool.view import graph
        return None
        # x = [ p.yearFraction() for p in utils.toda PeriodClsList(self._dates)]

        # y1 = self._discounts

        # ydata_d = {'zeroRates': y1}
        # return graph(name='DiscountCurve', xdata=x, ydata_d=ydata_d, **kwargs)


class ZeroCurve_Date(mx.ZeroCurve):
    def __init__(self, dates, yields, dayCounter, calendar=mx.default_calendar(), 
                 compounding=mx.Continuous, frequency=mx.Annual):

        self._dates = utils.toDateCls(dates)
        self._yields = yields
        self._dayCounter = utils.toDayCounterCls(dayCounter)
        self._calendar = utils.toCalendarCls(calendar)
        # interpolator=mx.Linear(), 
        self._compounding = utils.toCompounding(compounding)
        self._frequency = utils.toFrequency(frequency)

        mx.ZeroCurve.__init__(self, self._refDate, self._periods, zeroRates, interpolationType, extrapolationType,
                                    self._calendar, self._dayCounter, self._businessDayConvention, self._compounding)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, ZeroYieldCurve.__name__)

        refDate = d['refDate']
        periods = d['periods']
        zeroRates = d['zeroRates']
        interpolationType = utils.toInterpolator1DType(d['interpolationType'])
        extrapolationType = utils.toExtrapolation1DType(d['extrapolationType'])
        calendar = d['calendar']
        dayCounter = d['dayCounter']
        businessDayConvention = d['businessDayConvention']
        compounding = d['compounding']

        curve = ZeroYieldCurve(refDate, periods, zeroRates, interpolationType, extrapolationType,
                               calendar, dayCounter, businessDayConvention, compounding)

        setSmithWilsonParameter(curve, d)

        return curve

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['refDate'] = str(self._refDate)
        res['periods'] = self._periods
        res['zeroRates'] = self._zeroRates
        res['interpolationType'] = utils.interpolator1DToString(self._interpolationType)
        res['extrapolationType'] = utils.extrapolator1DToString(self._extrapolationType)
        res['calendar'] = str(self._calendar)
        res['dayCounter'] = str(self._dayCounter)
        res['businessDayConvention'] = utils.businessDayConventionToString(self._businessDayConvention)
        res['compounding'] = utils.compoundingToString(self._compounding)

        return res

    def shocked_clone(self, shock, method='absolute'):
        shocked_value = utils.calculateShock(shock, method, self._vol)

        return ZeroYieldCurve(self._refDate, shocked_value, self._calendar, self._dayCounter, self._businessDayConvention, self._compounding)

    def clone(self, **kwargs):
        refDate = kwargs['refDate'] if 'refDate' in kwargs else self._refDate
        periods = kwargs['periods'] if 'periods' in kwargs else self._periods
        zeroRates = kwargs['zeroRates'] if 'zeroRates' in kwargs else self._zeroRates
        interpolationType = kwargs['interpolationType'] if 'interpolationType' in kwargs else self._interpolationType
        extrapolationType = kwargs['extrapolationType'] if 'extrapolationType' in kwargs else self._extrapolationType
        calendar = kwargs['calendar'] if 'calendar' in kwargs else self._calendar
        dayCounter = kwargs['dayCounter'] if 'dayCounter' in kwargs else self._dayCounter
        businessDayConvention = kwargs['businessDayConvention'] if 'businessDayConvention' in kwargs else self._businessDayConvention
        compounding = kwargs['compounding'] if 'compounding' in kwargs else self._compounding

        return ZeroYieldCurve(refDate, periods, zeroRates, interpolationType, extrapolationType, calendar, dayCounter, businessDayConvention, compounding)


    def graph_view(self, **kwargs):
        from mxdevtool.view import graph

        x = [ p.yearFraction() for p in utils.toPeriodClsList(self._periods)]
        y1 = self._zeroRates

        ydata_d = {'zeroRates': y1}
        return graph(name='ZeroYieldCurve', xdata=x, ydata_d=ydata_d, **kwargs)


class ZeroCurve_Tenor(mx.ZeroCurve):
    def __init__(self, periods, yields, dayCounter=mx.Actual365Fixed(), calendar=mx.default_calendar(), 
                 compounding=mx.Continuous, frequency=mx.Annual, businessDayConvention=mx.ModifiedFollowing):

        self._periods = utils.toStrList(periods)
        self._yields = yields
        self._dayCounter = utils.toDayCounterCls(dayCounter)
        self._calendar = utils.toCalendarCls(calendar)
        # interpolator=mx.Linear(), 
        self._compounding = utils.toCompounding(compounding)
        self._frequency = utils.toFrequency(frequency)
        self._businessDayConvention = utils.toBusinessDayConvention(businessDayConvention)

        refDate = mx.Settings_instance().getEvaluationDate()
        
        dates = [ self._calendar.advance(refDate, p, self._businessDayConvention) for p in utils.toPeriodClsList(periods)]

        mx.ZeroCurve.__init__(self, dates, yields, self._dayCounter, self._calendar, mx.Linear(),
                              self._compounding, self._frequency)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, ZeroCurve_Tenor.__name__)

        periods = d['periods']
        yields = d['yields']
        dayCounter = d['dayCounter']
        calendar = d['calendar']
        compounding = d['compounding']
        frequency = d['frequency']
        businessDayConvention = d['businessDayConvention']

        curve = ZeroCurve_Tenor(periods, yields, dayCounter, calendar, compounding, frequency, businessDayConvention)

        return curve

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['periods'] = self._periods
        res['yields'] = self._yields
        res['dayCounter'] = str(self._dayCounter)
        res['calendar'] = str(self._calendar)
        res['compounding'] = utils.compoundingToString(self._compounding)
        res['frequency'] = utils.frequencyToString(self._frequency)
        res['businessDayConvention'] = utils.businessDayConventionToString(self._businessDayConvention)

        return res

    def shocked_clone(self, shock, method='absolute'):
        shocked_value = utils.calculateShock(shock, method, self._yields)

        return ZeroCurve_Tenor(self, self._periods, shocked_value, self._dayCounter, self._calendar, mx.Linear(), self._compounding, self._frequency)

    def clone(self, **kwargs):
        periods = kwargs['periods'] if 'periods' in kwargs else self._periods
        yields = kwargs['yields'] if 'yields' in kwargs else self._yields
        dayCounter = kwargs['dayCounter'] if 'dayCounter' in kwargs else self._dayCounter
        calendar = kwargs['calendar'] if 'calendar' in kwargs else self._calendar
        compounding = kwargs['compounding'] if 'compounding' in kwargs else self._compounding
        frequency = kwargs['frequency'] if 'frequency' in kwargs else self._frequency
        businessDayConvention = kwargs['businessDayConvention'] if 'businessDayConvention' in kwargs else self._businessDayConvention

        return ZeroCurve_Tenor(periods, yields, calendar, dayCounter, compounding, frequency, businessDayConvention)


    def graph_view(self, **kwargs):
        from mxdevtool.view import graph

        x = [ p.yearFraction() for p in utils.toPeriodClsList(self._periods)]
        y1 = self._yields

        ydata_d = {'yields': y1}
        return graph(name='ZeroCurve_Tenor', xdata=x, ydata_d=ydata_d, **kwargs)


class ZeroYieldCurve(mx.core_ZeroYieldCurveExt):
    def __init__(self, refDate: mx.Date, periods: List[str], zeroRates: List[float],
                   interpolationType=mx.Interpolator1D.Linear,
                   extrapolationType=mx.Extrapolator1D.FlatForward,
                   calendar=mx.NullCalendar(),
                   dayCounter=mx.Actual365Fixed(),
                   businessDayConvention=mx.ModifiedFollowing,
                   compounding=mx.Compounded):

        self._refDate = utils.toDateCls(refDate)
        self._periods = utils.toStrList(periods)
        self._zeroRates = zeroRates
        self._interpolationType = utils.toInterpolator1DType(interpolationType)
        self._extrapolationType = utils.toExtrapolator1DType(extrapolationType)
        self._calendar = utils.toCalendarCls(calendar)
        self._dayCounter = utils.toDayCounterCls(dayCounter)
        self._businessDayConvention = utils.toBusinessDayConvention(businessDayConvention)
        self._compounding = utils.toCompounding(compounding)

        mx.core_ZeroYieldCurveExt.__init__(self, self._refDate, self._periods, zeroRates, interpolationType, extrapolationType,
                                    self._calendar, self._dayCounter, self._businessDayConvention, self._compounding)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, ZeroYieldCurve.__name__)

        refDate = d['refDate']
        periods = d['periods']
        zeroRates = d['zeroRates']
        interpolationType = utils.toInterpolator1DType(d['interpolationType'])
        extrapolationType = utils.toExtrapolator1DType(d['extrapolationType'])
        calendar = d['calendar']
        dayCounter = d['dayCounter']
        businessDayConvention = d['businessDayConvention']
        compounding = d['compounding']

        curve = ZeroYieldCurve(refDate, periods, zeroRates, interpolationType, extrapolationType,
                               calendar, dayCounter, businessDayConvention, compounding)

        setSmithWilsonParameter(curve, d)

        return curve

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['refDate'] = str(self._refDate)
        res['periods'] = self._periods
        res['zeroRates'] = self._zeroRates
        res['interpolationType'] = utils.interpolator1DToString(self._interpolationType)
        res['extrapolationType'] = utils.extrapolator1DToString(self._extrapolationType)
        res['calendar'] = str(self._calendar)
        res['dayCounter'] = str(self._dayCounter)
        res['businessDayConvention'] = utils.businessDayConventionToString(self._businessDayConvention)
        res['compounding'] = utils.compoundingToString(self._compounding)

        return res

    def shocked_clone(self, shock, method='absolute'):
        shocked_value = utils.calculateShock(shock, method, self._vol)

        return ZeroYieldCurve(self._refDate, shocked_value, self._calendar, self._dayCounter, self._businessDayConvention, self._compounding)

    def clone(self, **kwargs):
        refDate = kwargs['refDate'] if 'refDate' in kwargs else self._refDate
        periods = kwargs['periods'] if 'periods' in kwargs else self._periods
        zeroRates = kwargs['zeroRates'] if 'zeroRates' in kwargs else self._zeroRates
        interpolationType = kwargs['interpolationType'] if 'interpolationType' in kwargs else self._interpolationType
        extrapolationType = kwargs['extrapolationType'] if 'extrapolationType' in kwargs else self._extrapolationType
        calendar = kwargs['calendar'] if 'calendar' in kwargs else self._calendar
        dayCounter = kwargs['dayCounter'] if 'dayCounter' in kwargs else self._dayCounter
        businessDayConvention = kwargs['businessDayConvention'] if 'businessDayConvention' in kwargs else self._businessDayConvention
        compounding = kwargs['compounding'] if 'compounding' in kwargs else self._compounding

        return ZeroYieldCurve(refDate, periods, zeroRates, interpolationType, extrapolationType, calendar, dayCounter, businessDayConvention, compounding)


    def graph_view(self, **kwargs):
        from mxdevtool.view import graph

        x = [ p.yearFraction() for p in utils.toPeriodClsList(self._periods)]
        y1 = self._zeroRates

        ydata_d = {'zeroRates': y1}
        return graph(name='ZeroYieldCurve', xdata=x, ydata_d=ydata_d, **kwargs)


# familyname : irskrw_krccp only now
class BootstapSwapCurveCCP(mx.core_BootstapSwapCurveCCP):
    def __init__(self, refDate, periods, rateTypes, quotes,
                interpolationType=mx.Interpolator1D.Linear,
                extrapolationType=mx.Extrapolator1D.FlatForward,
                familyname='irskrw_krccp',
                forSettlement=True):

        self._refDate = utils.toDateCls(refDate)
        self._periods = utils.toStrList(periods)
        self._rateTypes = rateTypes
        self._quotes = quotes
        self._interpolationType = utils.toInterpolator1DType(interpolationType)
        self._extrapolationType = utils.toExtrapolation1DType(extrapolationType)
        self._familyname = familyname
        self._forSettlement = forSettlement

        extrapolation = utils.toExtrapolationCls(extrapolationType)

        mx.core_BootstapSwapCurveCCP.__init__(self, self._refDate, self._periods, rateTypes, quotes,
                                              interpolationType, extrapolation,
                                              familyname, forSettlement)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, BootstapSwapCurveCCP.__name__)

        refDate = d['refDate']
        periods = d['periods']
        rateTypes = d['rateTypes']
        quotes = d['quotes']
        interpolationType = utils.toInterpolator1DType(d['interpolationType'])
        extrapolationType = utils.toExtrapolation1DType(d['extrapolationType'])
        familyname = d['familyname']
        forSettlement = d['forSettlement']

        curve = BootstapSwapCurveCCP(refDate, periods, rateTypes, quotes,
                                     interpolationType, extrapolationType,
                                     familyname, forSettlement)

        setSmithWilsonParameter(curve, d)

        return curve

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__

        res['refDate'] = str(self._refDate)
        res['periods'] = self._periods
        res['rateTypes'] = self._rateTypes
        res['quotes'] = self._quotes
        res['interpolationType'] = utils.interpolator1DToString(self._interpolationType)
        res['extrapolationType'] = utils.extrapolator1DToString(self._extrapolationType)

        if self._extrapolationType == mx.Extrapolator1D.SmithWilson:
            res['smithwilsonAlpha'] = self.smithwilsonAlpha()
            res['smithwilsonUFR'] = self.smithwilsonUFR()

        res['familyname'] = self._familyname
        res['forSettlement'] = self._forSettlement

        return res

    def shocked_clone(self, shock, method='absolute'):
        shocked_value = utils.calculateShock(shock, method, self._quotes)

        return BootstapSwapCurveCCP(self._refDate, self._periods, self._rateTypes, shocked_value, 
                                    self._interpolationType, self._extrapolationType, self._familyname, self._forSettlement)

    def clone(self, **kwargs):
        refDate = kwargs['refDate'] if 'refDate' in kwargs else self._refDate
        periods = kwargs['periods'] if 'periods' in kwargs else self._periods
        rateTypes = kwargs['rateTypes'] if 'rateTypes' in kwargs else self._rateTypes
        quotes = kwargs['quotes'] if 'quotes' in kwargs else self._quotes
        interpolationType = kwargs['interpolationType'] if 'interpolationType' in kwargs else self._interpolationType
        extrapolationType = kwargs['extrapolationType'] if 'extrapolationType' in kwargs else self._extrapolationType

        familyname = kwargs['familyname'] if 'familyname' in kwargs else self._familyname
        forSettlement = kwargs['forSettlement'] if 'forSettlement' in kwargs else self._forSettlement

        curve = BootstapSwapCurveCCP(refDate, periods, rateTypes, quotes, interpolationType, extrapolationType, familyname, forSettlement)

        smithwilsonAlpha = kwargs['smithwilsonAlpha'] if 'smithwilsonAlpha' in kwargs else self.smithwilsonAlpha()
        smithwilsonUFR = kwargs['smithwilsonUFR'] if 'smithwilsonUFR' in kwargs else self.smithwilsonUFR()
        curve.setSmithwilsonParameter(smithwilsonAlpha, smithwilsonUFR)

        return curve


    def graph_view(self, **kwargs):
        from mxdevtool.view import graph

        x = [ p.yearFraction() for p in utils.toPeriodClsList(self._periods)]
        y1 = self._quotes

        ydata_d = {'quotes': y1}

        return graph(name='BootstapSwapCurveCCP', xdata=x, ydata_d=ydata_d, **kwargs)


# generic(cash, bond, swap)
# class BootstrapCurve(mx.core_BootstrapCurve):
#     def __init__(self, refDate: mx.Date, periods: List[str or mx.Period], rateTypes: List[str], quotes: List[float],
#                 interpolationType=mx.Interpolator1D.Linear,
#                 extrapolationType=mx.Extrapolator1D.FlatForward,
#                 marketConvension=mx_m.get_marketConvension_vanillaswap('irskrw')):
#         '''
#         Args:
#             refDate (Date) : referenceDate
#             rateTypes (List[str]): Cash, Swap, Bond
#         '''
#         self._refDate = utils.toDateCls(refDate)
#         self._periods = utils.toStrList(periods)
#         self._rateTypes = rateTypes # 
#         self._quotes = quotes
#         self._interpolationType = utils.toInterpolator1DType(interpolationType)
#         self._extrapolationType = utils.toExtrapolation1DType(extrapolationType)
#         self._marketConvension = marketConvension

#         extrapolation = utils.toExtrapolationCls(extrapolationType)

#         mx.core_BootstrapCurve.__init__(self, self._refDate, self._periods, rateTypes, quotes,
#                                            interpolationType, extrapolation, marketConvension)

#     @staticmethod
#     def fromDict(d: dict, mrk=mx.MarketData()):
#         mx.check_fromDict(d, mx.CLASS_TYPE_NAME, BootstrapCurve.__name__)

#         refDate = d['refDate']
#         periods = d['periods']
#         rateTypes = d['rateTypes']
#         quotes = d['quotes']
#         interpolationType = utils.toInterpolator1DType(d['interpolationType'])
#         extrapolationType = utils.toExtrapolation1DType(d['extrapolationType'])
#         marketConvension = mx_m.marketConvensionFromDict(d['marketConvension'])

#         curve = BootstrapCurve(refDate, periods, rateTypes, quotes,
#                                     interpolationType, extrapolationType,
#                                     marketConvension)

#         setSmithWilsonParameter(curve, d)

#         return curve


#     def toDict(self):
#         res = dict()

#         res[mx.CLASS_TYPE_NAME] = self.__class__.__name__

#         res['refDate'] = str(self._refDate)
#         res['periods'] = self._periods
#         res['rateTypes'] = self._rateTypes
#         res['quotes'] = self._quotes
#         res['interpolationType'] = utils.interpolator1DToString(self._interpolationType)
#         res['extrapolationType'] = utils.extrapolator1DToString(self._extrapolationType)

#         if self._extrapolationType == mx.Extrapolator1D.SmithWilson:
#             res['smithwilsonAlpha'] = self.smithwilsonAlpha()
#             res['smithwilsonUFR'] = self.smithwilsonUFR()

#         res['marketConvension'] = self._marketConvension.toDict()
        
#         return res

#     def shocked_clone(self, shock, method='absolute'):
#         shocked_value = utils.calculateShock(shock, method, self._quotes)

#         return BootstrapCurve(self._refDate, self._periods, self._rateTypes, shocked_value, 
#                                     self._interpolationType, self._extrapolationType, self._marketConvension)

#     def clone(self, **kwargs):
#         refDate = kwargs['refDate'] if 'refDate' in kwargs else self._refDate
#         periods = kwargs['periods'] if 'periods' in kwargs else self._periods
#         rateTypes = kwargs['rateTypes'] if 'rateTypes' in kwargs else self._rateTypes
#         quotes = kwargs['quotes'] if 'quotes' in kwargs else self._quotes
#         interpolationType = kwargs['interpolationType'] if 'interpolationType' in kwargs else self._interpolationType
#         extrapolationType = kwargs['extrapolationType'] if 'extrapolationType' in kwargs else self._extrapolationType
#         marketConvension = kwargs['marketConvension'] if 'marketConvension' in kwargs else self._marketConvension

#         curve = BootstrapCurve(refDate, periods, rateTypes, quotes, interpolationType, extrapolationType, marketConvension)

#         smithwilsonAlpha = kwargs['smithwilsonAlpha'] if 'smithwilsonAlpha' in kwargs else self.smithwilsonAlpha()
#         smithwilsonUFR = kwargs['smithwilsonUFR'] if 'smithwilsonUFR' in kwargs else self.smithwilsonUFR()
#         curve.setSmithwilsonParameter(smithwilsonAlpha, smithwilsonUFR)

#         return curve

#     def graph_view(self, **kwargs):
#         from mxdevtool.view import graph

#         x = [ p.yearFraction() for p in utils.toPeriodClsList(self._periods)]
#         y1 = self._quotes

#         ydata_d = {'quotes': y1}

#         return graph(name='BootstrapCurve', xdata=x, ydata_d=ydata_d, **kwargs)



class ZeroSpreadedCurve(mx.ZeroSpreadedTermStructure):
    def __init__(self, baseCurve, spread, compounding=mx.Continuous, frequency=mx.Annual):

        self._baseCurve = baseCurve
        self._spread = spread
        self._compounding = compounding
        self._frequency = frequency

        mx.ZeroSpreadedTermStructure.__init__(self, baseCurve, spread, compounding, frequency)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, ZeroSpreadedCurve.__name__)

        baseCurve = mrk.get_yieldCurve_d(d['baseCurve'])
        spread = d['spread']
        compounding = utils.toCompounding(d['compounding'])
        frequency = utils.toFrequency(d['frequency'])
        
        return ZeroSpreadedCurve(baseCurve, spread, compounding, frequency)

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__

        res['baseCurve'] = self._baseCurve.toDict()
        res['spread'] = self._spread
        res['compounding'] = self._compounding
        res['frequency'] = self._frequency

        return res

    # shock to spread
    def shocked_clone(self, shock, method='absolute'):
        shocked_value = utils.calculateShock(shock, method, self._spread)

        return ZeroSpreadedCurve(self._baseCurve, shocked_value, self._compounding, self._frequency)

    def clone(self, **kwargs):
        baseCurve = kwargs['baseCurve'] if 'baseCurve' in kwargs else self._baseCurve
        spread = kwargs['spread'] if 'spread' in kwargs else self._spread
        compounding = kwargs['compounding'] if 'compounding' in kwargs else self._compounding
        frequency = kwargs['frequency'] if 'frequency' in kwargs else self._frequency

        return ZeroSpreadedCurve(baseCurve, spread, compounding, frequency)

    def graph_view(self, **kwargs):
        from mxdevtool.view import graph

        x = kwargs.get('x')

        # period ( 1Y to 20Y )
        x = [v+1 for v in range(20)] if x is None else x
        y1 = [self.zeroRate(t, self._compounding).rate() for t in x]
        ydata_d = {'zeroRates': y1}

        return graph(name='ZeroSpreadedCurve', xdata=x, ydata_d=ydata_d, **kwargs)


# class ForwardSpreadedCurve(mx.core_ForwardSpreadedTermStructure):
#     def __init__(self, curve, spread):
#         mx.core_ForwardSpreadedTermStructure.__init__(self, curve, spread)

