import os, inspect

from numpy.lib.arraysetops import isin
import mxdevtool as mx
import mxdevtool.config as mx_config
import numpy as np
from datetime import datetime
import tempfile, json, numbers
from hashlib import sha256
from collections import OrderedDict
from typing import List


def npzee_view(arg):
    if isinstance(arg, np.ndarray):
        tempfilename = os.path.join(tempfile.gettempdir(), 'temp_' + datetime.utcnow().strftime('%Y%m%d%H%M%S%f') + '.npz')
        np.savez(tempfilename, data=arg)
        os.startfile(tempfilename)
    elif isinstance(arg, str):
        if os.path.exists(arg):
            os.startfile(arg)
        else:
            raise Exception('file does not exist')
    elif isinstance(arg, mx.core_ScenarioResult):
        if os.path.exists(arg.filename):
            os.startfile(arg.filename)
        else:
            raise Exception('file does not exist')
    else:
        print('unknown')


def yield_curve_view(yieldcurve):
    pass


def get_hashCode(serializable) -> str:
    d = OrderedDict(serializable.toDict())
    try:
        json_str = json.dumps(d)
        return sha256(json_str.encode(mx_config.HASHCODE_ENCODING)).hexdigest()
    except Exception as e:
        if len(e.args) >= 1:
            e.args = (e.args[0] + ' -> input dict: {0}'.format(d),) + e.args[1:]
        raise e


def toJsonStr(serializable):
    d = serializable.toDict()
    json_str = json.dumps(d)
    return json_str


def toJson(filename, serializable):
    f = open(filename, "w")
    d = serializable.toDict()

    try:
        json_str = json.dumps(d)
        f.write(json_str)
        f.close()
        return sha256(json_str.encode(mx_config.HASHCODE_ENCODING)).hexdigest()
    except Exception as e:
        if len(e.args) >= 1:
            e.args = (e.args[0] + ' -> input dict: {0}'.format(d),) + e.args[1:]
        f.close()
        raise e


def check_hashCode(*serializables, exception=True):
    res = []
    for s in serializables:
        hashCode = get_hashCode(s)
        recreated = s.fromDict(s.toDict())
        recreated_hashCode = get_hashCode(recreated)

        tf = hashCode == recreated_hashCode

        if tf == False and exception:
            raise Exception('hashCode is not valid - {0} != {1}'.format(hashCode, recreated_hashCode))

        res.append(tf)

    return res


def compare_hashCode(*serializables, exception=True):
    codes = set()
    for s in serializables:
        codes.add(s.hashCode())

    tf = len(codes) == 1

    if tf == False and exception:
        raise Exception('hashCode is not same')

    return tf


def check_args_in_dict(class_instance, clsnm: str, input_d: dict, strict_check=False):
    init = getattr(class_instance, "__init__", None)
    # required_args = inspect.getargspec(init).args[1:]
    required_args = inspect.signature(init).parameters

    for k, v in required_args.items():
        if k == 'self':
            continue

        if not k in input_d and v == inspect._empty:
            raise Exception('{0} missing required argument: {1}'.format(clsnm, k))

    if not strict_check:
        return

    for k in input_d:
        if k in ['name', 'clsnm']:
            continue

        if not k in required_args:
            raise Exception('{0} useless argument exist: {1}'.format(clsnm, k))


def volatility_range_check(value):
    lower = 1.0
    upper = 0.0

    if value < lower or upper < value:
        raise Exception('volatility must be in [{0}, {1}]'.format(lower, upper))


def interestrate_range_check(value):
    lower = 1.0
    upper = -1.0

    if value < lower or upper < value:
        raise Exception('interestrate must be in [{0}, {1}]'.format(lower, upper))


def check_correlation(corr):
    m = np.matrixlib.matrix(corr)

    if not np.allclose(m, m.T, rtol=1e-05, atol=1e-08):
        raise Exception('correlation matrix is not symmetric - {0}'.format(corr))


def save_file(filename, serializable, build_dict_method):
    """ saves file ( Scenario, ScenarioBuilder, Shock, ...)

    Args:
        filename (str): full path
        serializable  obj has toDict method

    Raises:
        Exception: [description]
    """

    json_str = None
    f = open(filename, "w")

    toDict = getattr(serializable, 'toDict', None)

    if callable(toDict):
        d = build_dict_method(serializable)
        json_str = json.dumps(d)
    else:
        raise Exception('serializable is required - {0}'.format(serializable))

    f.write(json_str)
    f.close()


def saves_file(filename, serializables, build_dict_method):
    """ saves file ( Scenario, ScenarioBuilder, Shock, ...)

    Args:
        filename (str): full path
        serializables (list, dict): obj has toDict method

    Raises:
        Exception: [description]
    """

    json_str = None
    # path = os.path.join(self.location, name + '.' + XENFILE_EXT)
    f = open(filename, "w")

    # prefix = 'item{0}'
    method_name = 'toDict'

    if isinstance(serializables, dict):
        if len(serializables) == 0:
            raise Exception('empty dict')

        d = dict()
        for k, s in serializables.items():
            toDict = getattr(s, method_name, None)

            if callable(toDict):
                d[k] = build_dict_method(s)
            else:
                raise Exception('serializable is required - {0}'.format(s))
        json_str = json.dumps(d)
    else:
        f.close()
        raise Exception('serializable is required - {0}'.format(serializables))

    if json_str is None:
        f.close()
        raise Exception('nothing to write')

    f.write(json_str)
    f.close()


def toTypeCls(arg, typ):
    # target class list
    from mxdevtool import Period, Date

    if isinstance(arg, typ):
        return arg
    else:
        return typ(arg)


def toTypeClsList(arg, typ):
    # target class list
    from mxdevtool import Period, Date

    if isinstance(arg, list):
        res = []
        for v in arg:
            if isinstance(v, typ):
                res.append(v)
            else:
                res.append(typ(v))
        return res
    else:
        raise Exception('list is required - {0}'.format(arg))

def toStrList(arg) -> List[str]: return [str(v) for v in arg]

def toPeriodCls(arg) -> mx.Period : return toTypeCls(arg, mx.Period)
def toPeriodClsList(arg) -> List[mx.Period]: return toTypeClsList(arg, mx.Period)

def toDateCls(arg) -> mx.Date: return toTypeCls(arg, mx.Date)
def toDateClsList(arg) -> List[mx.Date]: return toTypeClsList(arg, mx.Date)

def periodToDateList(refDate, periods, calendar=None, businessDayConvention=mx.ModifiedFollowing) -> List[mx.Date]:
    _periods = toPeriodClsList(periods)
    return [calendar.advance(refDate, p, businessDayConvention) for p in _periods]

def toDateOrPeriodCls(arg) -> mx.Date or mx.Period:
    if isinstance(arg, mx.Date): return toDateCls(arg)
    elif isinstance(arg, mx.Period): return toPeriodCls(arg)
    else: raise Exception('unknown type argument - {0}'.format(arg))

def toDateOrPeriodClsList(arg) -> mx.Date or mx.Period:
    item = arg[0]
    if isinstance(item, mx.Date): return toDateClsList(arg)
    elif isinstance(item, mx.Period): return toPeriodClsList(arg)
    else: raise Exception('unknown type argument - {0}'.format(arg))

def toTime(arg: str or float or mx.Period) -> float:
    if isinstance(arg, str):
        return toPeriodCls(arg).yearFraction()
    else:
        return float(arg)

def toTimeList(args: List[str or float or mx.Period]) -> float:
    return [ toTime(arg) for arg in args]

def toCalendarCls(arg) -> mx.Calendar:
    arg_s = str(arg).upper()

    if arg_s in [str(mx.SouthKorea()).upper(), 'KR']: return mx.SouthKorea()
    
    elif arg_s in [str(mx.UnitedStates(mx.UnitedStates.Settlement)).upper()]: return mx.UnitedStates(mx.UnitedStates.Settlement)
    elif arg_s in [str(mx.UnitedStates(mx.UnitedStates.NYSE)).upper()]: return mx.UnitedStates(mx.UnitedStates.NYSE)
    elif arg_s in [str(mx.UnitedStates(mx.UnitedStates.GovernmentBond)).upper()]: return mx.UnitedStates(mx.UnitedStates.GovernmentBond)
    elif arg_s in [str(mx.UnitedStates(mx.UnitedStates.NERC)).upper()]: return mx.UnitedStates(mx.UnitedStates.NERC)
    elif arg_s in [str(mx.UnitedStates(mx.UnitedStates.LiborImpact)).upper()]: return mx.UnitedStates(mx.UnitedStates.LiborImpact)
    elif arg_s in [str(mx.UnitedStates(mx.UnitedStates.SOFR)).upper()]: return mx.UnitedStates(mx.UnitedStates.SOFR)
    elif arg_s in [str(mx.UnitedStates(mx.UnitedStates.FederalReserve)).upper()]: return mx.UnitedStates(mx.UnitedStates.FederalReserve)

    elif arg_s in [str(mx.NullCalendar()).upper(), 'NULL']: return mx.NullCalendar()
    elif arg_s in [str(mx.Japan()).upper(), 'JP']: return mx.Japan()
    
    raise Exception('unable to convert calendar - {0}'.format(arg))


def toCurrencyCls(arg) -> mx.Currency:
    arg_s = str(arg).upper()

    if arg_s in [str(mx.KRWCurrency()).upper(), 'KRW']: return mx.KRWCurrency()
    elif arg_s in [str(mx.USDCurrency()).upper(), 'USD']: return mx.USDCurrency()
    elif arg_s in [str(mx.JPYCurrency()).upper(), 'JPY']: return mx.JPYCurrency()
    
    raise Exception('unable to convert currency - {0}'.format(arg))


def currencyToString(arg) -> str:
    arg_s = str(arg).upper()

    if arg_s in [str(mx.KRWCurrency()).upper(), 'KRW']: return str(mx.KRWCurrency())
    elif arg_s in [str(mx.USDCurrency()).upper(), 'USD']: return str(mx.USDCurrency())
    elif arg_s in [str(mx.JPYCurrency()).upper(), 'JPY']: return str(mx.JPYCurrency())
    
    raise Exception('unable to convert currency - {0}'.format(arg))


def toDayCounterCls(arg) -> mx.DayCounter:
    arg_s = str(arg).upper()
    
    if arg_s in [str(mx.Actual360()).upper(), 'ACT360']: return mx.Actual360()
    elif arg_s in [str(mx.Actual365Fixed()).upper(), 'ACT365FIXED']: return mx.Actual365Fixed()
    # elif arg_s in [str(mx.Actual365NoLeap()), 'Act365NoLeap']: return mx.Actual365NoLeap()
    elif arg_s in [str(mx.ActualActual()).upper(), 'ACTACT']: return mx.ActualActual()
    
    raise Exception('unable to convert daycounter - {0}'.format(arg))


def toBusinessDayConvention(arg):
    arg_s = str(arg).upper()

    if arg_s in [str(mx.Following).upper(),  'Following'.upper()] : return mx.Following
    elif arg_s in [str(mx.ModifiedFollowing).upper(),  'ModifiedFollowing'.upper()] : return mx.ModifiedFollowing
    elif arg_s in [str(mx.Preceding).upper(),  'Preceding'.upper()] : return mx.Preceding
    elif arg_s in [str(mx.ModifiedPreceding).upper(),  'ModifiedPreceding'.upper()] : return mx.ModifiedPreceding
    elif arg_s in [str(mx.Unadjusted).upper(),  'Unadjusted'.upper()] : return mx.Unadjusted
    elif arg_s in [str(mx.HalfMonthModifiedFollowing).upper(),  'HalfMonthModifiedFollowing'.upper()] : return mx.HalfMonthModifiedFollowing
    elif arg_s in [str(mx.JoinHolidays).upper(),  'JoinHolidays'.upper()] : return mx.JoinHolidays
    elif arg_s in [str(mx.JoinBusinessDays).upper(),  'JoinBusinessDays'.upper()] : return mx.JoinBusinessDays

    raise Exception('unable to convert BusinessDayConvention - {0}'.format(arg))


def businessDayConventionToString(arg) -> str:
    arg_s = str(arg)

    if arg_s in [str(mx.Following).upper(),  'Following'.upper()] : return 'Following'
    elif arg_s in [str(mx.ModifiedFollowing).upper(),  'ModifiedFollowing'.upper()] : return 'ModifiedFollowing'
    elif arg_s in [str(mx.Preceding).upper(),  'Preceding'.upper()] : return 'Preceding'
    elif arg_s in [str(mx.ModifiedPreceding).upper(),  'ModifiedPreceding'.upper()] : return 'ModifiedPreceding'
    elif arg_s in [str(mx.Unadjusted).upper(),  'Unadjusted'.upper()] : return 'Unadjusted'
    elif arg_s in [str(mx.HalfMonthModifiedFollowing).upper(),  'HalfMonthModifiedFollowing'.upper()] : return 'HalfMonthModifiedFollowing'
    elif arg_s in [str(mx.JoinHolidays).upper(),  'JoinHolidays'.upper()] : return 'JoinHolidays'
    elif arg_s in [str(mx.JoinBusinessDays).upper(),  'JoinBusinessDays'.upper()] : return 'JoinBusinessDays'

    raise Exception('unable to convert BusinessDayConvention String - {0}'.format(arg))


def toCompounding(arg):
    if isinstance(arg, int):
        if arg == 0: return mx.Simple
        elif arg == 1: return mx.Compounded
        elif arg == 2: return mx.Continuous
        elif arg == 3: return mx.SimpleThenCompounded
        else: pass
    elif isinstance(arg, str):
        if arg == str(0): return mx.Simple
        elif arg == str(1): return mx.Compounded
        elif arg == str(2): return mx.Continuous
        elif arg == str(3): return mx.SimpleThenCompounded
        else:
            if arg.lower() == 'simple': return mx.Simple
            elif arg.lower() == 'compounded': return mx.Compounded
            elif arg.lower() == 'continuous': return mx.Continuous
            elif arg.lower() == 'simplethencompounded': return mx.SimpleThenCompounded
    else:
        pass

    raise Exception('unable to convert Compounding - {0}'.format(arg))


def compoundingToString(arg) -> str:
    arg_s = str(arg)

    if arg_s in [str(mx.Simple),  'Simple'] : return 'Simple'
    elif arg_s in [str(mx.Compounded),  'Compounded'] : return 'Compounded'
    elif arg_s in [str(mx.Continuous),  'Continuous'] : return 'Continuous'
    elif arg_s in [str(mx.ModifiedPreceding),  'ModifiedPreceding'] : return 'SimpleThenCompounded'

    raise Exception('unable to convert Compounding String - {0}'.format(arg))


def toFrequency(arg):
    arg_s = str(arg)

    if arg_s in [str(mx.NoFrequency),  'NoFrequency'] : return mx.NoFrequency
    elif arg_s in [str(mx.Once),  'Once'] : return mx.Once
    elif arg_s in [str(mx.Annual),  'Annual'] : return mx.Annual
    elif arg_s in [str(mx.Semiannual),  'Semiannual'] : return mx.Semiannual
    elif arg_s in [str(mx.EveryFourthMonth),  'EveryFourthMonth'] : return mx.EveryFourthMonth
    elif arg_s in [str(mx.Quarterly),  'Quarterly'] : return mx.Quarterly
    elif arg_s in [str(mx.Bimonthly),  'Bimonthly'] : return mx.Bimonthly
    elif arg_s in [str(mx.Monthly),  'Monthly'] : return mx.Monthly
    elif arg_s in [str(mx.EveryFourthWeek),  'EveryFourthWeek'] : return mx.EveryFourthWeek
    elif arg_s in [str(mx.Biweekly),  'Biweekly'] : return mx.Biweekly
    elif arg_s in [str(mx.Weekly),  'Weekly'] : return mx.Weekly
    elif arg_s in [str(mx.Daily),  'Daily'] : return mx.Daily
    elif arg_s in [str(mx.OtherFrequency),  'OtherFrequency'] : return mx.OtherFrequency

    raise Exception('unable to convert Compounding - {0}'.format(arg))


def frequencyToString(arg) -> str:
    arg_s = str(arg)

    if arg_s in [str(mx.NoFrequency),  'NoFrequency'] : return 'NoFrequency'
    elif arg_s in [str(mx.Once),  'Once'] : return 'Once'
    elif arg_s in [str(mx.Annual),  'Annual'] : return 'Annual'
    elif arg_s in [str(mx.Semiannual),  'Semiannual'] : return 'Semiannual'
    elif arg_s in [str(mx.EveryFourthMonth),  'EveryFourthMonth'] : return 'EveryFourthMonth'
    elif arg_s in [str(mx.Quarterly),  'Quarterly'] : return 'Quarterly'
    elif arg_s in [str(mx.Bimonthly),  'Bimonthly'] : return 'Bimonthly'
    elif arg_s in [str(mx.Monthly),  'Monthly'] : return 'Monthly'
    elif arg_s in [str(mx.EveryFourthWeek),  'EveryFourthWeek'] : return 'EveryFourthWeek'
    elif arg_s in [str(mx.Biweekly),  'Biweekly'] : return 'Biweekly'
    elif arg_s in [str(mx.Weekly),  'Weekly'] : return 'Weekly'
    elif arg_s in [str(mx.Daily),  'Daily'] : return 'Daily'
    elif arg_s in [str(mx.OtherFrequency),  'OtherFrequency'] : return 'OtherFrequency'

    raise Exception('unable to convert Frequency String - {0}'.format(arg))    


def toMatrixCls(arg) -> mx.Matrix:
    if isinstance(arg, mx.Matrix):
        return arg
    elif isinstance(arg, list):
        return mx.Matrix(arg)
    elif isinstance(arg, np.ndarray):
        return mx.Matrix(arg.tolist())

    raise Exception('unable to convert matrix - {0}'.format(arg))


def toMatrixList(arg) -> list:
    if isinstance(arg, mx.Matrix):
        return arg.toList()
    elif isinstance(arg, list):
        return arg
    elif isinstance(arg, np.ndarray):
        return arg.tolist()

    raise Exception('unable to convert list(2d) - {0}'.format(arg))


def toOptionType(arg):
    if arg in [mx.Option.Call, mx.Option.Put]:
        return arg
    elif isinstance(arg, str):
        if arg.lower() in ['c', 'call']:
            return mx.Option.Call
        elif arg.lower() in ['p', 'put']:
            return mx.Option.Put

    raise Exception('unknown arg for option_type - {0}'.format(arg))


def toBarrierType(arg):
    if arg in [mx.Barrier.UpIn, mx.Barrier.UpOut, mx.Barrier.DownIn, mx.Barrier.DownOut]:
        return arg
    elif isinstance(arg, str):
        if arg.lower() in ['upin']:
            return mx.Barrier.UpIn
        elif arg.lower() in ['upout']:
            return mx.Barrier.UpOut
        elif arg.lower() in ['downin']:
            return mx.Barrier.DownIn
        elif arg.lower() in ['downout']:
            return mx.Barrier.DownOut

    raise Exception('unknown arg for barrier_type - {0}'.format(arg))


def toVolatilityType(arg):
    if arg in [mx.ShiftedLognormal, mx.Normal]:
        return arg
    elif isinstance(arg, str):
        if arg.lower() in ['shiftedlognormal', 'lognormal']:
            return mx.ShiftedLognormal
        elif arg.lower() in ['normal']:
            return mx.Normal

    raise Exception('unknown arg for volatility_type - {0}'.format(arg))


def toInterpolator1DType(arg):
    if isinstance(arg, int):
        return arg

    elif isinstance(arg, str):
        arg_lower = arg.lower()
        if arg_lower in ['backwardflat']: return mx.Interpolator1D.BackwardFlat
        elif arg_lower in ['forwardflat']: return mx.Interpolator1D.ForwardFlat
        elif arg_lower in ['linear']: return mx.Interpolator1D.Linear
        elif arg_lower in ['loglinear']: return mx.Interpolator1D.LogLinear
        elif arg_lower in ['cubicnaturalspline']: return mx.Interpolator1D.CubicNaturalSpline
        elif arg_lower in ['logcubicnaturalspline']: return mx.Interpolator1D.LogcubicNaturalSpline
        elif arg_lower in ['monotoniccubicnaturalspline']: return mx.Interpolator1D.MonotonicCubicNaturalSpline
        elif arg_lower in ['monotoniclogcubicnaturalspline']: return mx.Interpolator1D.MonotonicLogCubicNaturalSpline
        elif arg_lower in ['krugercubic']: return mx.Interpolator1D.KrugerCubic
        elif arg_lower in ['krugerlogcubic']: return mx.Interpolator1D.KrugerlogCubic
        elif arg_lower in ['fritschbutlandcubic']: return mx.Interpolator1D.FritschButlandCubic
        elif arg_lower in ['fritschbutlandlogcubic']: return mx.Interpolator1D.FritschButlandlogCubic
        elif arg_lower in ['parabolic']: return mx.Interpolator1D.Parabolic
        elif arg_lower in ['logparabolic']: return mx.Interpolator1D.LogParabolic
        elif arg_lower in ['monotonicparabolic']: return mx.Interpolator1D.MonotonicParabolic
        elif arg_lower in ['monotoniclogparabolic']: return mx.Interpolator1D.MonotonicLogParabolic

    raise Exception('unknown arg for interpolation1D_type - {0}'.format(arg))


def interpolator1DToString(arg):
    arg_s = str(arg)

    if arg_s in [str(mx.Interpolator1D.BackwardFlat), 'BackwardFlat'] : return 'BackwardFlat'
    elif arg_s in [str(mx.Interpolator1D.ForwardFlat), 'ForwardFlat'] : return 'ForwardFlat'
    elif arg_s in [str(mx.Interpolator1D.Linear), 'Linear'] : return 'Linear'
    elif arg_s in [str(mx.Interpolator1D.LogLinear), 'LogLinear'] : return 'LogLinear'
    elif arg_s in [str(mx.Interpolator1D.CubicNaturalSpline), 'CubicNaturalSpline'] : return 'CubicNaturalSpline'
    elif arg_s in [str(mx.Interpolator1D.LogcubicNaturalSpline), 'LogcubicNaturalSpline'] : return 'LogcubicNaturalSpline'
    elif arg_s in [str(mx.Interpolator1D.MonotonicCubicNaturalSpline), 'MonotonicCubicNaturalSpline'] : return 'MonotonicCubicNaturalSpline'
    elif arg_s in [str(mx.Interpolator1D.MonotonicLogCubicNaturalSpline), 'MonotonicLogCubicNaturalSpline'] : return 'MonotonicLogCubicNaturalSpline'
    elif arg_s in [str(mx.Interpolator1D.KrugerCubic), 'KrugerCubic'] : return 'KrugerCubic'
    elif arg_s in [str(mx.Interpolator1D.KrugerlogCubic), 'KrugerlogCubic'] : return 'KrugerlogCubic'
    elif arg_s in [str(mx.Interpolator1D.FritschButlandCubic), 'FritschButlandCubic'] : return 'FritschButlandCubic'
    elif arg_s in [str(mx.Interpolator1D.FritschButlandlogCubic), 'FritschButlandlogCubic'] : return 'FritschButlandlogCubic'
    elif arg_s in [str(mx.Interpolator1D.Parabolic), 'Parabolic'] : return 'Parabolic'
    elif arg_s in [str(mx.Interpolator1D.LogParabolic), 'LogParabolic'] : return 'LogParabolic'
    elif arg_s in [str(mx.Interpolator1D.MonotonicParabolic), 'MonotonicParabolic'] : return 'MonotonicParabolic'
    elif arg_s in [str(mx.Interpolator1D.MonotonicLogParabolic), 'MonotonicLogParabolic'] : return 'MonotonicLogParabolic'

    raise Exception('unknown arg for interpolation1D_str - {0}'.format(arg))


def toInterpolator2DType(arg):
    arg_s = str(arg)

    if arg_s in [str(mx.Interpolator2D.BackwardflatLinear), 'BackwardflatLinear'] : return mx.Interpolator2D.BackwardflatLinear
    elif arg_s in [str(mx.Interpolator2D.Bilinear), 'Bilinear'] : return mx.Interpolator2D.Bilinear
    elif arg_s in [str(mx.Interpolator2D.Bicubic), 'Bicubic'] : return mx.Interpolator2D.Bicubic

    raise Exception('unknown arg for interpolation2D_str - {0}'.format(arg))


def interpolator2DToString(arg):
    arg_s = str(arg)

    if arg_s in [str(mx.Interpolator2D.BackwardflatLinear), 'BackwardflatLinear'] : return 'BackwardflatLinear'
    elif arg_s in [str(mx.Interpolator2D.Bilinear), 'Bilinear'] : return 'Bilinear'
    elif arg_s in [str(mx.Interpolator2D.Bicubic), 'Bicubic'] : return 'Bicubic'

    raise Exception('unknown arg for interpolation2D_str - {0}'.format(arg))


def extrapolator1DToString(arg):
    arg_s = str(arg)

    if arg_s in [str(mx.Extrapolator1D.FlatForward), 'FlatForward'] : return 'FlatForward'
    elif arg_s in [str(mx.Extrapolator1D.FlatSpot), 'FlatSpot'] : return 'FlatSpot'
    elif arg_s in [str(mx.Extrapolator1D.SmithWilson), 'SmithWilson'] : return 'SmithWilson'

    raise Exception('unknown arg for extrapolation2D_str - {0}'.format(arg))

def toExtrapolator1DType(arg):
    if isinstance(arg, int):
        return arg

    elif isinstance(arg, str):
        arg_lower = arg.lower()
        if arg_lower in ['flatforward']: return mx.Extrapolator1D.FlatForward
        elif arg_lower in ['flatspot']: return mx.Extrapolator1D.FlatSpot
        elif arg_lower in ['smithwilson']: return mx.Extrapolator1D.SmithWilson

    elif isinstance(arg, (mx.FlatExtrapolation, mx.SmithWilsonExtrapolation)):
        return arg.type()
        
    raise Exception('unknown arg for extrapolation1D_type - {0}'.format(arg))


def toExtrapolationCls(arg):
    _arg = arg
    extrapolation = None

    if isinstance(arg, mx.Extrapolation):
        return arg

    if isinstance(arg, str):
        _arg = toExtrapolator1DType(arg)

    if _arg == mx.Extrapolator1D.SmithWilson:
        extrapolation = mx.SmithWilsonExtrapolation(0.1, 0.042)
    elif _arg == mx.Extrapolator1D.FlatSpot:
        extrapolation = mx.FlatExtrapolation('spot')
    else:
        extrapolation = mx.FlatExtrapolation('forward')

    return extrapolation

# def toIborIndexCls(arg: dict):
#     if isinstance(arg, mx.IborIndex):
#         return arg

#     if isinstance(arg, dict):
#         return mx.IborIndex(arg['name'], arg['period'])

#     raise Exception('unable to convert iborindex - {0}'.format(arg))


class NameHelper:

    @staticmethod
    def isCompounding(name: str):
        return 'compounding' == name[-len('compounding'):].lower()

    @staticmethod
    def isCalendar(name: str):
        return 'calendar' == name[-len('calendar'):].lower()

    @staticmethod
    def isCurrency(name: str):
        return 'currency' == name[-len('currency'):].lower()

    @staticmethod
    def isDayCounter(name: str):
        return 'daycounter' == name[-len('daycounter'):].lower()

    @staticmethod
    def isBusinessDayConvention(name: str):
        return 'businessdayconvention' == name[-len('businessdayconvention'):].lower()

    @staticmethod
    def isInterpolationType(name: str):
        return 'interpolationtype' == name[-len('interpolationtype'):].lower()

    @staticmethod
    def isExtrapolationType(name: str):
        return 'extrapolationtype' == name[-len('extrapolationtype'):].lower()

    @staticmethod
    def isTenor(name: str):
        return 'tenor' == name[-len('tenor'):].lower()

    @staticmethod
    def isDate(name: str):
        return 'date' == name[-len('date'):].lower()

    @staticmethod
    def isDates(name: str):
        return 'dates' == name[-len('dates'):].lower()

    @staticmethod
    def isIndex(name: str):
        return 'index' == name[-len('index'):].lower()

    @staticmethod
    def getTypeFrom(name: str):
        res = None

        if NameHelper.isCompounding(name): res = 'compounding'
        elif NameHelper.isCalendar(name): res = 'calendar'
        elif NameHelper.isDayCounter(name): res = 'dayCounter'
        elif NameHelper.isCurrency(name): res = 'currency'
        elif NameHelper.isBusinessDayConvention(name): res = 'businessDayConvention'
        elif NameHelper.isInterpolationType(name): res = 'interpolationType'
        elif NameHelper.isExtrapolationType(name): res = 'extrapolationType'
        elif NameHelper.isTenor(name): res = 'tenor'
        elif NameHelper.isDate(name): res = 'date'
        elif NameHelper.isDates(name): res = 'dates'
        elif NameHelper.isIndex(name): res = 'index'

        return res

    @staticmethod
    def toDictArg(name: str, value):
        res = None

        if NameHelper.isCompounding(name): res = compoundingToString(value)
        elif NameHelper.isCalendar(name): res = str(value)
        elif NameHelper.isDayCounter(name): res = str(value)
        elif NameHelper.isCurrency(name): res = str(value)
        elif NameHelper.isBusinessDayConvention(name): res = businessDayConventionToString(value)
        elif NameHelper.isInterpolationType(name): res = interpolator1DToString(value)
        elif NameHelper.isExtrapolationType(name): res = extrapolator1DToString(value)
        elif NameHelper.isTenor(name): res = str(value) if not isinstance(value, numbers.Number) else value
        elif NameHelper.isDate(name): res = str(value)
        elif NameHelper.isDates(name): res = [str(v) for v in value]
        elif NameHelper.isIndex(name): res = value
        elif isinstance(value, (numbers.Number, str, list)): res = value

        return res

    @staticmethod
    def toClassArg(name: str, value):
        arg = None

        if NameHelper.isDate(name): arg = toDateCls(value)
        elif NameHelper.isDates(name): arg = toDateClsList(value)
        elif NameHelper.isCompounding(name): arg = toCompounding(value)
        elif NameHelper.isCalendar(name): arg = toCalendarCls(value)
        elif NameHelper.isCurrency(name): arg = toCurrencyCls(value)
        elif NameHelper.isDayCounter(name): arg = toDayCounterCls(value)
        elif NameHelper.isBusinessDayConvention(name): arg = toBusinessDayConvention(value)
        elif NameHelper.isInterpolationType(name): arg = toInterpolator1DType(value) if isinstance(value, str) else value
        elif NameHelper.isExtrapolationType(name): arg = toExtrapolator1DType(value) if isinstance(value, str) else value
        elif NameHelper.isTenor(name): arg = toPeriodCls(value) if not isinstance(value, numbers.Number) else value
        elif isinstance(value, (numbers.Number, str, list)): arg = value
        elif 'MarketConvension' in value.__class__.__name__ or \
             'Payoff' in value.__class__.__name__ or \
             'Index' in value.__class__.__name__ or \
             'LegExerciseOption' in value.__class__.__name__ or \
             'LegInfo' in value.__class__.__name__:
             # 'IborIndex' in value.__class__.__name__ or \
            arg = value
        else:
            # raise Exception('unsupported arguments : {0}, {1}'.format(name, value))
            raise Exception('unsupported arguments : {0}, {1}, {2}'.format(name, value, value.__class__.__name__))

        return arg


# arguments parse from arg name
def get_arg_fromValue(name: str, arg_v):
    arg = None

    # class type case
    if not isinstance(arg_v, (numbers.Number, str, dict, list)):
        return arg_v

    if NameHelper.getTypeFrom(name) != None:
        arg = NameHelper.toClassArg(name, arg_v)
    elif name == 'name' or 'type' == name[-len('type'):].lower():
        arg = arg_v
    elif isinstance(arg_v, (numbers.Number, str)):
        arg = arg_v

    if arg is None:
        raise Exception('unsupported argument : {0}, {1}'.format(name, arg_v))

    return arg


def get_args_fromDict(d: dict, parameters):
    args = []
    for name, v in parameters.items():
        if name == 'self':
            continue

        if not name in d and v.default != inspect._empty:
            args.append(v.default)
        else:
            args.append(get_arg_fromValue(name, d[name]))

    return args


def parseClassFromDict(d: dict, modules):
    if not isinstance(d, dict):
        raise Exception('dictionary type is required')

    classTypeName = d[mx.CLASS_TYPE_NAME]

    # if not classTypeName in globals():
    if not classTypeName in modules:
        raise Exception('unknown classTypeName - {0}'.format(classTypeName))

    try:
        # class_instance = globals()[classTypeName]
        class_instance = modules[classTypeName]

        init = getattr(class_instance, "__init__", None)
        args = get_args_fromDict(d, inspect.signature(init).parameters)

        return class_instance(*args)
    except Exception as e:
        if len(e.args) >= 1:
            e.args = (e.args[0] + ' -> input dict: {0}'.format(d),) + e.args[1:]
        raise


def set_init_self_args(selfClsArg, *args):
    # classTypeName = clsArg.__class__.__name__
    init = getattr(selfClsArg, "__init__", None)

    para_names = inspect.signature(init).parameters.keys()

    res = []
    for name, v in zip(para_names, args):
        arg = NameHelper.toClassArg(name, v)

        prefix = '_'
        selfClsArg.__dict__[prefix + name] = arg
        res.append(arg)

    return res


def serializeToDict(arg):
    if not hasattr(arg, "__dict__"):
        return arg
    
    res = dict()
    res[mx.CLASS_TYPE_NAME] = arg.__class__.__name__

    for k, v in arg.__dict__.items():
        try:
            if k == 'this':
                continue

            key = k[1:]
            toDict = getattr(v, "toDict", None)

            if callable(toDict):
                res[key] = toDict()
            elif NameHelper.getTypeFrom(key) != None:
                res[key] = NameHelper.toDictArg(key, v)
            elif isinstance(v, list):
                res[key] = [serializeToDict(item) for item in v]
            else:
                res[key] = v
        except Exception as e:
            e.add_note('arg : {0}'.format(arg))
            e.add_note('k : {0}'.format(k))
            e.add_note('v : {0}'.format(v))
            raise e

    return res


def is_contains_hangeul(str):
    import re
    p = re.compile('[ㄱ-힣]+')
    
    if len(p.findall(str)) > 0:
        return True
    else:
        return False


def calculateShock(shock, method, value):
    v = None

    if isinstance(value, list): v = np.array(value)
    else: v = value

    if method == 'relative': v *= (1.0 + shock)
    elif method == 'absolute': v += shock
    else: raise Exception('unknown shock method - {0}'.format(method))

    if isinstance(v, np.ndarray):
        return v.tolist()
    else:
        return v

def make_period_m(*args):
    return [mx.Period(m, mx.Months) for m in args]

def make_period_y(*args):
    return [mx.Period(m, mx.Years) for m in args]


def make_MathExpressionDictionary(d: dict, **kwargs):
    mes = mx.MathExpressionDictionary()

    for k, v in d.items():
        mes.add_variable(k, v)
    
    for k, v in kwargs.items():
        mes.add_variable(k, v)
    
    return mes