from distutils.util import strtobool
import mxdevtool as mx
import mxdevtool.utils as utils


# equity vol

class BlackConstantVol(mx.BlackConstantVol):
    def __init__(self, refDate, vol, calendar=mx.default_calendar(), dayCounter=mx.Actual365Fixed()):

        self._refDate = utils.toDateCls(refDate)
        self._vol = vol
        self._calendar = utils.toCalendarCls(calendar)
        self._dayCounter = utils.toDayCounterCls(dayCounter)

        mx.BlackConstantVol.__init__(self, self._refDate, self._calendar, vol,  self._dayCounter)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, BlackConstantVol.__name__)

        refDate = mx.Date(d['refDate'])
        vol = d['vol']
        calendar = d['calendar']
        dayCounter = d['dayCounter']

        return BlackConstantVol(refDate, vol, calendar, dayCounter)

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['refDate'] = str(self._refDate)
        res['vol'] = self._vol
        res['calendar'] = str(self._calendar)
        res['dayCounter'] = str(self._dayCounter)

        return res

    def shocked_clone(self, shock, method='absolute'):
        shocked_value = utils.calculateShock(shock, method, self._vol)

        return BlackConstantVol(self._refDate, shocked_value, self._calendar, self._dayCounter)

    def clone(self, **kwargs):
        refDate = kwargs['refDate'] if 'refDate' in kwargs else self._refDate
        vol = kwargs['vol'] if 'vol' in kwargs else self._vol
        calendar = kwargs['calendar'] if 'calendar' in kwargs else self._calendar
        dayCounter = kwargs['dayCounter'] if 'dayCounter' in kwargs else self._dayCounter

        return BlackConstantVol(refDate, vol, calendar, dayCounter)


# dates direct inputs
class BlackVarianceCurve(mx.BlackVarianceCurve):
    def __init__(self, refDate, dates, volatilities,
                # interpolationType=mx.Interpolator1D.Linear, 
                dayCounter=mx.Actual365Fixed()):

        self._refDate = utils.toTypeCls(refDate, mx.Date)
        self._dates = utils.toTypeClsList(dates, mx.Date)
        self._volatilities = volatilities
        # self._interpolationType = interpolationType
        self._dayCounter = dayCounter

        mx.BlackVarianceCurve.__init__(self, self._refDate, self._dates, volatilities, dayCounter)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, BlackVarianceCurve.__name__)

        refDate = mx.Date(d['refDate'])
        dates = utils.toTypeClsList(d['dates'], mx.Date)
        volatilities = d['volatilities']
        # interpolationType = utils.toInterpolator1DType(d['interpolationType'])
        dayCounter = utils.toDayCounterCls(d['dayCounter'])

        return BlackVarianceCurve(refDate, dates, volatilities, dayCounter)

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['refDate'] = str(self._refDate)
        res['dates'] = utils.toStrList(self._dates)
        res['volatilities'] = self._volatilities
        # res['interpolationType'] = utils.interpolator1DToString(self._interpolationType)
        res['dayCounter'] = str(self._dayCounter)

        return res

    def shocked_clone(self, shock, method='absolute'):
        shocked_value = utils.calculateShock(shock, method, self._volatilities)

        return BlackVarianceCurve(self._refDate, self._dates, shocked_value, self._strike, self._dayCounter)

    def clone(self, **kwargs):
        refDate = kwargs['refDate'] if 'refDate' in kwargs else self._refDate
        dates = kwargs['dates'] if 'dates' in kwargs else self._dates
        volatilities = kwargs['volatilities'] if 'volatilities' in kwargs else self._volatilities
        # interpolationType = kwargs['interpolationType'] if 'interpolationType' in kwargs else self._interpolationType
        dayCounter = kwargs['dayCounter'] if 'dayCounter' in kwargs else self._dayCounter

        return BlackVarianceCurve(refDate, dates, volatilities, strike, dayCounter)


class BlackVarianceCurve2(BlackVarianceCurve):
    def __init__(self, refDate, periods, volatilities, strike=None,
                   interpolationType=mx.Interpolator1D.Linear, 
                   calendar=None,
                   dayCounter=mx.Actual365Fixed(), 
                   businessDayConvention=mx.ModifiedFollowing):
        _calendar = calendar

        if _calendar is None:
            _calendar = mx.default_calendar()

        #dates = [ _calendar.advance(refDate, p, businessDayConvention) for p in utils.toPeriodClsList(periods)]
        dates = utils.periodToDateList(refDate, periods, _calendar, businessDayConvention)

        self._calendar = utils.toCalendarCls(_calendar)
        self._businessDayConvention = utils.toBusinessDayConvention(businessDayConvention)
        self._periods = utils.toStrList(periods)

        BlackVarianceCurve.__init__(self, refDate, dates, volatilities, strike, interpolationType, dayCounter)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, BlackVarianceCurve2.__name__)

        refDate = d['refDate']
        periods = d['periods']
        volatilities = d['volatilities']
        strike = d['strike']
        interpolationType = d['interpolationType']
        calendar = d['calendar']
        dayCounter = d['dayCounter']
        businessDayConvention = d['businessDayConvention']

        return BlackVarianceCurve2(refDate, periods, volatilities, strike, interpolationType, 
                                calendar, dayCounter, businessDayConvention)

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['periods'] = self._periods
        res['calendar'] = str(self._calendar)
        res['businessDayConvention'] = utils.businessDayConventionToString(self._businessDayConvention)

        super_d = super().toDict()
        super_d.pop('dates')

        res = { **res, **super_d }

        return res


# dates direct inputs
class BlackVarianceSurface(mx.BlackVarianceSurface):
    def __init__(self, refDate, dates, strikes, blackVols,
                   dayCounter=mx.Actual365Fixed()):
        self._refDate = utils.toDateCls(refDate)
        self._dates = utils.toDateClsList(dates)
        self._strikes = strikes
        self._blackVols = utils.toMatrixList(blackVols)
        self._dayCounter = utils.toDayCounterCls(dayCounter)
        
        mx.BlackVarianceSurface.__init__(self, self._refDate, self._dates, strikes, self._blackVols, dayCounter)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, BlackVarianceSurface.__name__)

        refDate = d['refDate']
        dates = d['dates']
        strikes = d['strikes']
        blackVols = d['blackVols']
        dayCounter = d['dayCounter']

        return BlackVarianceSurface(refDate, dates, strikes, blackVols, dayCounter)

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        
        res['refDate'] = str(self._refDate)
        res['dates'] = utils.toStrList(self._dates)
        res['strikes'] = self._strikes
        res['blackVols'] = self._blackVols
        res['dayCounter'] = str(self._dayCounter)

        return res


class BlackVarianceSurface2(BlackVarianceSurface):
    def __init__(self, refDate, periods, strikes, blackVols,
                   calendar=None,
                   dayCounter=mx.Actual365Fixed(),
                   businessDayConvention=mx.ModifiedFollowing):
        self._refDate = utils.toDateCls(refDate)
        self._periods = utils.toStrList(periods)
        self._strikes = strikes
        self._blackVols = blackVols

        _calendar = calendar
        if _calendar is None: _calendar = mx.default_calendar()

        dates = [ _calendar.advance(refDate, p, businessDayConvention) for p in periods ]
        

        self._calendar = utils.toCalendarCls(_calendar)
        self._dayCounter = utils.toDayCounterCls(dayCounter)
        self._businessDayConvention = utils.toBusinessDayConvention(businessDayConvention)

        BlackVarianceSurface.__init__(self, self._refDate, dates, self._strikes, self._blackVols, self._dayCounter)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, BlackVarianceSurface2.__name__)

        refDate = mx.Date(d['refDate'])
        periods = d['periods']
        strikes = d['strikes']
        blackVols = d['blackVols']
        calendar = d['calendar']
        dayCounter = d['dayCounter']
        businessDayConvention = d['businessDayConvention']

        return BlackVarianceSurface2(refDate, periods, strikes, blackVols, 
                                     calendar, dayCounter, businessDayConvention)

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['periods'] = self._periods
        res['calendar'] = str(self._calendar)
        res['businessDayConvention'] = utils.businessDayConventionToString(self._businessDayConvention)
        
        super_d = super().toDict()
        super_d.pop('dates')

        res = { **res, **super_d }

        return res


# class CapHelper(mx.CapHelper):
#     def __init__(self, *args):
#         super().__init__(*args)

#         self.weight = 1.0


class SwaptionHelper(mx.SwaptionHelper):
    def __init__(self, optionDateOrTenor, swapTenor, volatility, index, fixedLegTenor,
                 fixedLegDayCounter, floatingLegDayCounter,
                 termStructure, errorType=mx.BlackCalibrationHelper.RelativePriceError,
                 strike=mx.nullDouble(), nominal=1.0, volatilityType=mx.ShiftedLognormal, weight=1.0):

        self._optionDateOrTenor = utils.toDateOrPeriodCls(optionDateOrTenor)
        self._swapTenor = utils.toPeriodCls(swapTenor)
        self._volatility = volatility
        
        self._index = index
        self._fixedLegTenor = utils.toPeriodCls(fixedLegTenor)
        self._fixedLegDayCounter = utils.toDayCounterCls(fixedLegDayCounter)
        self._floatingLegDayCounter = utils.toDayCounterCls(floatingLegDayCounter)
        self._termStructure = termStructure
        self._errorType = errorType
        self._strike = strike
        self._nominal = nominal
        self._volatilityType = utils.toVolatilityType(volatilityType)

        self._weight = weight
        
        mx.SwaptionHelper.__init__(self, self._optionDateOrTenor, self._swapTenor, 
                mx.QuoteHandle(mx.SimpleQuote(self._volatility)), self._index, self._fixedLegTenor, self._fixedLegDayCounter,
                self._floatingLegDayCounter, mx.YieldTermStructureHandle(self._termStructure),
                self._errorType, self._strike, self._nominal, self._volatilityType)

    def name(self):
        return "{0} {1} {2}".format(self._optionDateOrTenor, self._swapTenor, self._volatility, self._volatilityType)


# interest rate vol
class ConstantSwaptionVolatility(mx.ConstantSwaptionVolatility):
    def __init__(self, refDate, vol, calendar=mx.default_calendar(), 
                 businessDayConvention=mx.ModifiedFollowing, dayCounter=mx.Actual365Fixed(),
                 volatilityType= mx.ShiftedLognormal, familyname='krwcd'):

        self._refDate = utils.toDateCls(refDate)
        self._vol = vol
        self._calendar = utils.toCalendarCls(calendar)
        self._businessDayConvention = utils.toBusinessDayConvention(businessDayConvention)
        self._dayCounter = utils.toDayCounterCls(dayCounter)
        self._volatilityType = utils.toVolatilityType(volatilityType)
        self._familyname = familyname

        mx.ConstantSwaptionVolatility.__init__(self, self._refDate, self._calendar, 
                self._businessDayConvention, self._vol, self._dayCounter, self._volatilityType, 0.0)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, ConstantSwaptionVolatility.__name__)

        refDate = mx.Date(d['refDate'])
        vol = d['vol']
        calendar = d['calendar']
        businessDayConvention = d['businessDayConvention']
        dayCounter = d['dayCounter']
        volatilityType = d['volatilityType']
        familyname = d['familyname']

        return ConstantSwaptionVolatility(refDate, calendar, businessDayConvention, vol, dayCounter, volatilityType)

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['refDate'] = str(self._refDate)
        res['vol'] = self._vol
        res['calendar'] = str(self._calendar)
        res['dayCounter'] = str(self._dayCounter)
        res['businessDayConvention'] = str(self._businessDayConvention)
        res['volatilityType'] = str(self._volatilityType)
        res['familyname'] = self._familyname

        return res

    def shocked_clone(self, shock, method='absolute'):
        shocked_value = utils.calculateShock(shock, method, self._vol)

        return ConstantSwaptionVolatility(self._refDate, self._calendar, self._businessDayConvention, shocked_value, self._dayCounter, self._volatilityType, self._familyname)

    def clone(self, **kwargs):
        refDate = kwargs['refDate'] if 'refDate' in kwargs else self._refDate
        vol = kwargs['vol'] if 'vol' in kwargs else self._vol
        calendar = kwargs['calendar'] if 'calendar' in kwargs else self._calendar
        dayCounter = kwargs['dayCounter'] if 'dayCounter' in kwargs else self._dayCounter
        businessDayConvention = kwargs['businessDayConvention'] if 'businessDayConvention' in kwargs else self._businessDayConvention
        volatilityType = kwargs['volatilityType'] if 'volatilityType' in kwargs else self._volatilityType
        familyname = kwargs['familyname'] if 'familyname' in kwargs else self._familyname

        return ConstantSwaptionVolatility(refDate, calendar, businessDayConvention, vol, dayCounter, volatilityType, familyname)


# 
class SwaptionVolatilityMatrix(mx.SwaptionVolatilityMatrix):
    def __init__(self, refDate, optionDatesOrTenors, swapTenors, volatilities, calendar=mx.default_calendar(), 
                 businessDayConvention=mx.ModifiedFollowing, dayCounter=mx.Actual365Fixed(),
                 flatExtrapolation=False, volatilityType=mx.ShiftedLognormal, familyname='irskrw') -> None:

        self._refDate = utils.toDateCls(refDate)
        self._optionDatesOrTenors = utils.toDateOrPeriodClsList(optionDatesOrTenors)
        self._swapTenors = utils.toPeriodClsList(swapTenors)
        self._volatilities = volatilities # 2d array
        
        self._calendar = utils.toCalendarCls(calendar)
        self._businessDayConvention = utils.toBusinessDayConvention(businessDayConvention)
        self._dayCounter = utils.toDayCounterCls(dayCounter)
        self._flatExtrapolation = flatExtrapolation
        self._volatilityType = utils.toVolatilityType(volatilityType)
        self._familyname = familyname

        mx.SwaptionVolatilityMatrix.__init__(self, self._refDate, self._calendar, 
                self._businessDayConvention, self._optionDatesOrTenors, self._swapTenors, 
                self._volatilities, self._dayCounter, self._flatExtrapolation, volatilityType)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, SwaptionVolatilityMatrix.__name__)

        refDate = mx.Date(d['refDate'])
        optionDatesOrTenors = d['optionDatesOrTenors']
        swapTenors = d['swapTenors']
        volatilities = d['volatilities']
        calendar = d['calendar']
        businessDayConvention = d['businessDayConvention']
        dayCounter = d['dayCounter']
        flatExtrapolation = d['flatExtrapolation']
        volatilityType = d['volatilityType']
        familyname = d['familyname']
        
        return SwaptionVolatilityMatrix(refDate, optionDatesOrTenors, swapTenors, volatilities, 
                                        calendar, businessDayConvention, dayCounter, 
                                        flatExtrapolation, volatilityType, familyname)

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['refDate'] = str(self._refDate)

        res['optionDatesOrTenors'] = self._optionDatesOrTenors # !!?! ?��?�� ?��?��
        res['swapTenors'] = self._swapTenors # !!?! ?��?�� ?��?��
        res['volatilities'] = self._volatilities # !!?! ?��?�� ?��?��

        res['calendar'] = str(self._calendar)
        res['dayCounter'] = str(self._dayCounter)
        res['businessDayConvention'] = str(self._businessDayConvention)
        res['flatExtrapolation'] = self._flatExtrapolation
        res['volatilityType'] = self._volatilityType
        res['familyname'] = self._familyname

        return res

    def shocked_clone(self, shock, method='absolute'):
        shocked_value = utils.calculateShock(shock, method, self._volatilities)

        return SwaptionVolatilityMatrix(self._refDate, self._optionDatesOrTenors, self._swapTenors, shocked_value, 
                                        self._calendar, self._businessDayConvention, self._dayCounter, 
                                        self._flatExtrapolation, self._volatilityType, self._familyname)

    def clone(self, **kwargs):
        refDate = kwargs['refDate'] if 'refDate' in kwargs else self._refDate
        
        optionDatesOrTenors = kwargs['optionDatesOrTenors'] if 'optionDatesOrTenors' in kwargs else self._optionDatesOrTenors
        swapTenors = kwargs['swapTenors'] if 'swapTenors' in kwargs else self._swapTenors
        volatilities = kwargs['volatilities'] if 'volatilities' in kwargs else self._volatilities

        calendar = kwargs['calendar'] if 'calendar' in kwargs else self._calendar
        dayCounter = kwargs['dayCounter'] if 'dayCounter' in kwargs else self._dayCounter
        businessDayConvention = kwargs['businessDayConvention'] if 'businessDayConvention' in kwargs else self._businessDayConvention
        flatExtrapolation = kwargs['flatExtrapolation'] if 'flatExtrapolation' in kwargs else self._flatExtrapolation
        volatilityType = kwargs['volatilityType'] if 'volatilityType' in kwargs else self._volatilityType
        familyname = kwargs['familyname'] if 'familyname' in kwargs else self._familyname

        return SwaptionVolatilityMatrix(refDate, optionDatesOrTenors, swapTenors, volatilities, 
                                        calendar, businessDayConvention, dayCounter, 
                                        flatExtrapolation, volatilityType, familyname)

    def interpolate(self, start, lengh, extrapolate=False):
        _start = start
        _lengh = lengh

        if isinstance(start, str): _start = utils.toPeriodCls(start)
        if isinstance(lengh, str): _lengh = utils.toPeriodCls(lengh)
        
        return self.volatility(_start, _lengh, 0.0, extrapolate)
