"""
Basic Lunar calendar
"""


# Source:
# Astronomical algorithms from the book "Astronomical Algorithms" by Jean Meeus, 1998
# https://www.informatik.uni-leipzig.de/~duc/amlich/AL.py


# Library
##############################################################
import math as __math

def __jdFromDate(dd, mm, yy):
    """
    Compute the (integral) Julian day number of day dd/mm/yyyy
    
    i.e., the number of days between 1/1/4713 BC (Julian calendar) and dd/mm/yyyy.
    """

    a = int((14 - mm) / 12.)
    y = yy + 4800 - a
    m = mm + 12*a - 3
    jd = dd + int((153*m + 2) / 5.) + 365*y + int(y/4.) - int(y/100.) + int(y/400.) - 32045
    if (jd < 2299161):
        jd = dd + int((153*m + 2)/5.) + 365*y + int(y/4.) - 32083
    return jd

def __jdToDate(jd: int):
    """
    Convert a Julian day number to day/month/year
    
    jd : integer.
    """
    if (jd > 2299160):
        ## After 5/10/1582, Gregorian calendar
        a = jd + 32044
        b = int((4*a + 3) / 146097.)
        c = a - int((b*146097) / 4.)
    else:
        b = 0
        c = jd + 32082
    d = int((4*c + 3) / 1461.)
    e = c - int((1461*d) / 4.)
    m = int((5*e + 2) / 153.)
    day = e - int((153*m + 2) / 5.) + 1
    month = m + 3 - 12*int(m / 10.)
    year = b*100 + d - 4800 + int(m / 10.)
    return [day, month, year]

def __NewMoon(k):
    """
    Compute the time of the k-th new moon after the new moon of 1/1/1900 13:52 UCT
    
    measured as the number of days since 1/1/4713 BC noon UCT, e.g., 2451545.125 is 1/1/2000 15:00 UTC.
    
    Returns a floating number
    
    e.g., 2415079.9758617813 for k=2 or 2414961.935157746 for k=-2."""
    ## Time in Julian centuries from 1900 January 0.5
    T = k / 1236.85
    T2 = T * T
    T3 = T2 * T
    dr = __math.pi / 180.
    Jd1 = 2415020.75933 + 29.53058868*k + 0.0001178*T2 - 0.000000155*T3
    Jd1 = Jd1 + 0.00033*__math.sin((166.56 + 132.87*T - 0.009173*T2)*dr)
    ## Mean new moon
    M = 359.2242 + 29.10535608*k - 0.0000333*T2 - 0.00000347*T3
    ## Sun's mean anomaly
    Mpr = 306.0253 + 385.81691806*k + 0.0107306*T2 + 0.00001236*T3
    ## Moon's mean anomaly
    F = 21.2964 + 390.67050646*k - 0.0016528*T2 - 0.00000239*T3
    ## Moon's argument of latitude
    C1 = (0.1734 - 0.000393*T)*__math.sin(M*dr) + 0.0021*__math.sin(2*dr*M)
    C1 = C1 - 0.4068*__math.sin(Mpr*dr) + 0.0161*__math.sin(dr*2*Mpr)
    C1 = C1 - 0.0004*__math.sin(dr*3*Mpr)
    C1 = C1 + 0.0104*__math.sin(dr*2*F) - 0.0051*__math.sin(dr*(M + Mpr))
    C1 = C1 - 0.0074*__math.sin(dr*(M - Mpr)) + 0.0004*__math.sin(dr*(2*F + M))
    C1 = C1 - 0.0004*__math.sin(dr*(2*F - M)) - 0.0006*__math.sin(dr*(2*F + Mpr))
    C1 = C1 + 0.0010*__math.sin(dr*(2*F - Mpr)) + 0.0005*__math.sin(dr*(2*Mpr + M))
    if (T < -11):
        deltat= 0.001 + 0.000839*T + 0.0002261*T2 - 0.00000845*T3 - 0.000000081*T*T3
    else:
        deltat= -0.000278 + 0.000265*T + 0.000262*T2
    JdNew = Jd1 + C1 - deltat
    return JdNew

def __SunLongitude(jdn):
    """
    Compute the longitude of the sun at any time.
    
    Parameter: floating number jdn, the number of days since 1/1/4713 BC noon.
    """
    T = (jdn - 2451545.0 ) / 36525.
    ## Time in Julian centuries
    ## from 2000-01-01 12:00:00 GMT
    T2 = T * T
    dr = __math.pi / 180.  ## degree to radian
    M = 357.52910 + 35999.05030*T - 0.0001559*T2 - 0.00000048*T*T2
    ## mean anomaly, degree
    L0 = 280.46645 + 36000.76983*T + 0.0003032*T2
    ## mean longitude, degree
    DL = (1.914600 - 0.004817*T - 0.000014*T2) * __math.sin(dr*M)
    DL += (0.019993 - 0.000101*T) *__math.sin(dr*2*M) + 0.000290*__math.sin(dr*3*M)
    L = L0 + DL  ## true longitude, degree
    L = L * dr
    L = L - __math.pi*2*(int(L / (__math.pi*2)))
    #### Normalize to (0, 2*math.pi)
    return L

def __getSunLongitude(dayNumber, timeZone):
    """
    Compute sun position at midnight of the day with the given Julian day number.
    
    The time zone if the time difference between local time and UTC: 7.0 for UTC+7:00.
    
    The function returns a number between 0 and 11. 
    
    From the day after March equinox and the 1st major term after March equinox, 0 is returned. After that, return 1, 2, 3 ...
    """
    return int(__SunLongitude(dayNumber - 0.5 - timeZone/24.) / __math.pi*6)

def __getNewMoonDay(k, timeZone):
    """
    Compute the day of the k-th new moon in the given time zone.
    
    The time zone if the time difference between local time and UTC: 7.0 for UTC+7:00."""
    return int(__NewMoon(k) + 0.5 + timeZone / 24.)

def __getLunarMonth11(yy, timeZone):
    """
    Find the day that starts the luner month 11of the given year for the given time zone.
    """
    # off = jdFromDate(31, 12, yy) \
    #            - 2415021.076998695
    off = __jdFromDate(31, 12, yy) - 2415021.
    k = int(off / 29.530588853)
    nm = __getNewMoonDay(k, timeZone)
    sunLong = __getSunLongitude(nm, timeZone)
    #### sun longitude at local midnight
    if (sunLong >= 9):
        nm = __getNewMoonDay(k - 1, timeZone)
    return nm

def __getLeapMonthOffset(a11, timeZone):
    """
    Find the index of the leap month after the month starting on the day a11.
    """
    k = int((a11 - 2415021.076998695) / 29.530588853 + 0.5)
    last = 0
    i = 1  ## start with month following lunar month 11
    arc = __getSunLongitude(__getNewMoonDay(k + i, timeZone), timeZone)
    while True:
        last = arc
        i += 1
        arc = __getSunLongitude(__getNewMoonDay(k + i, timeZone), timeZone)
        if  not (arc != last and i < 14):
            break
    return i - 1

def S2L(day: int, month: int, year: int, timeZone: int = 7):
    """
    Convert solar date to the corresponding lunar date.
    """
    dd = day
    mm = month
    yy = year
    dayNumber = __jdFromDate(dd, mm, yy)
    k = int((dayNumber - 2415021.076998695) / 29.530588853)
    monthStart = __getNewMoonDay(k + 1, timeZone)
    if (monthStart > dayNumber):
        monthStart = __getNewMoonDay(k, timeZone)
    # alert(dayNumber + " -> " + monthStart)
    a11 = __getLunarMonth11(yy, timeZone)
    b11 = a11
    if (a11 >= monthStart):
        lunarYear = yy
        a11 = __getLunarMonth11(yy - 1, timeZone)
    else:
        lunarYear = yy + 1
        b11 = __getLunarMonth11(yy + 1, timeZone)
    lunarDay = dayNumber - monthStart + 1
    diff = int((monthStart - a11) / 29.)
    lunarLeap = 0
    lunarMonth = diff + 11
    if (b11 - a11 > 365):
        leapMonthDiff = __getLeapMonthOffset(a11, timeZone)
        if (diff >= leapMonthDiff):
            lunarMonth = diff + 10
            if (diff == leapMonthDiff):
                lunarLeap = 1
    if (lunarMonth > 12):
        lunarMonth = lunarMonth - 12
    if (lunarMonth >= 11 and diff < 4):
        lunarYear -= 1
    return [lunarDay, lunarMonth, lunarYear, lunarLeap]

def L2S(day: int, month: int, year: int, lunarLeap, timezone: int = 7):
    """
    Convert a lunar date to the corresponding solar date.
    """
    lunarD = day
    lunarM = month
    lunarY = year
    tZ = timezone
    if (lunarM < 11):
        a11 = __getLunarMonth11(lunarY - 1, tZ)
        b11 = __getLunarMonth11(lunarY, tZ)
    else:
        a11 = __getLunarMonth11(lunarY, tZ)
        b11 = __getLunarMonth11(lunarY + 1, tZ)
    k = int(0.5 + (a11 - 2415021.076998695) / 29.530588853)
    off = lunarM - 11
    if (off < 0):
        off += 12
    if (b11 - a11 > 365):
        leapOff = __getLeapMonthOffset(a11, tZ)
        leapM = leapOff - 2
        if (leapM < 0):
            leapM += 12
        if (lunarLeap != 0 and lunarM != leapM):
            return [0, 0, 0]
        elif (lunarLeap != 0 or off >= leapOff):
            off += 1
    monthStart = __getNewMoonDay(k + off, tZ)
    return __jdToDate(monthStart + lunarD - 1)


# Run
##############################################################
if __name__ == "__main__":
    from datetime import datetime
    now = datetime.now()
    print(S2L(now.day, now.month, now.year))