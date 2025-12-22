import re
from pathlib import Path
from base64 import b64decode
import urllib

# Путь к файлу с обфусцированным JS
JS_PATH = Path("input.js")

# Регулярка для вызовов вида:
# U('0x191', 'w1ba')
# U("0x191", "w1ba")
# U(0x194, 'SI&j')
pattern = re.compile(
    r"""
    U                      # имя функции
    \s*\(                  # открывающая скобка
    \s*
    (?:                    # первая группа: 0xNNN в кавычках ИЛИ без
       (?P<q1>['"])        # открывающая кавычка
       (?P<hex_quoted>0x[0-9a-fA-F]+)
       (?P=q1)             # та же кавычка
      |
       (?P<hex_raw>0x[0-9a-fA-F]+)
    )
    \s*,\s*
    (?P<q2>['"])           # кавычка для второго аргумента
    (?P<tag>[^'"]*)        # содержимое второго аргумента
    (?P=q2)                # та же кавычка
    \s*
    \)                     # закрывающая скобка
    """,
    re.VERBOSE,
)

def find_U_calls(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            for m in pattern.finditer(line):
                # берем hex-значение из той подгруппы, которая сработала
                hex_arg = m.group("hex_quoted") or m.group("hex_raw")
                tag = m.group("tag")
                yield {
                    "line": lineno,
                    "full_match": m.group(0),
                    "hex_arg": hex_arg,
                    "hex_int": int(hex_arg, 16),
                    "tag": tag,
                }

def base64(encoded: str) -> str:
    s = encoded.swapcase()
    s += "=" * (-len(s) % 4)
    return b64decode(s).decode("utf-8").encode("latin1")

def rc4(data: bytes, key: bytes) -> str:
    S = list(range(256))
    j = 0

    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) & 255
        S[i], S[j] = S[j], S[i]

    i = j = 0
    out = bytearray()

    for byte in data:
        i = (i + 1) & 255
        j = (j + S[i]) & 255
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) & 255]
        out.append(byte ^ K)

    return out #.decode('latin1')

cache = {}
array_b = ['Ac9khCkNygPAWOtdTSkbWQi', 'x8kNW5K9W7hdI8kb', 'aSo1CCoMa1VcKgvig8of', 'WRvZkJ0MgNNcISkF', 'W5qmAmo4W4tcHJL3xmoeywm', 'W6GEu2mVW5ZcU1ddJmotchHp', 'W4ZcU8kFWOzot8kyW5jsWQeBW54m', 'i8oUmKhdUSkTWQznw8obumobwG', 'EYnfWOpcIdlcU2xdOSoieSkauCo3', 'W6OwuMePW5RdH1RdVSoHafC', 'W5fuWOpdTCk5qbi', 'W77dRCo6g8kTW73dQ8kUd8ouvW', 'W5ldTmoZusrCW6baW5b8WOZdNW', 'aSo6E8oMba3dU3PKamocW5qQ', 'W61ip3XXWPrcWORdOCo4W5K8WPe', 'WQFcV8k1z2JcU0HDjSklW7xcHG4', 'awbogNaFiHxdJXRcIelcTSon', 'WPRdVCoj', 'DComW6FdQG', 'WO94BCkRW7va', 'W7BdSmo5mrldRX5EbSk1', 'WPRdSCoBW5y3gSocW4jvWOm', 'WPpdHmo3', 'WPjYymoVcCoDbdVcVq', 'bSkkiq', 'cCoPlq', 'Bmomk3xdUX1DWP3cLq', 'WP3dSmom', 'emoMlSks', 'gd9vzrGotIVdPG', 'WQlcK8kG', 'WRxdMCke', 'W5DHWRitnmo6s8k6EW', 'WRJdHSo0', 'DxOeW4m', 'WO9FcdXOFSkBW6ZcLq', 'edXh', 'hCk+WQVdLSogW4KJpeG', 'WRbipq', 'WRVcNmkJyW', 'W4NcTK9NmI8Cna', 'WODCgG', 'WRzabG', 'h3GG', 'W6tdQfhdRa', 'W4b2WQKHn8oHu8k+kmoJ', 'WPFdRSoj', 'WP1/zmk5W79gDJxcHG', 'DCoeW7ddTaNdGa', 'owCd', 'dY9MySoZzG', 'W6tcK3O', 'CmojW6VdVGi', 'W4hcTv0', 'WQdcVmkL', 'WOXFhWzLDq', 'WP7cRCkyW5hdSmo0', 'WRuEys4WW4W', 'WQZcSSkIwSozW7xdNmkhb8oO', 'W6hcIxy', 'iYbd', 'WPRcLmkL', 'txC5', 'WQNdI8kq', 'gSkEW4O', 'gMXQ', 'WPHwmq', 'zSk5EbVcOCoR', 'W5fYWQ8onCo6', 'qZ0Psszp', 'WR7cMmkvyaXzWP4', 'gN1tWP7cQW', 'eSkEnCkHWOCt', 'zCoRoa', 'W7aJBGerjq', 'h8klW4OhW6BdMq', 'WOVdUSoZySoZW4u', 'WO3cU8kD', 'W6jHeG', 'e8k8Eq', 'fG4uW4lcRmoh', 'lIXk', 'phidW5ZdLxi', 'WP0sDmkD', 'prJdVmo5W7JcHa', 'W6jJfG', 'AIbt', 'W4JdPq8', 'WP55Eq', 'hCk5WRFdIG', 'WPXalSkO', 'WPf4WPddJ8kUuG', 'W7dcH24oW4GG', 'rCkJoSk8wKG', 'WQ9heJLXWPK', 'emoUoCkmWRec', 'qZWttYy', 'W7S3tK0PWRy', 'C8kWAWdcJSoR', 'cmkAkCkVWP0p', 'W6SJza', 'WQpcV8kTt8oUW7i', 'W7/dRmo0jW', 'uMyLWPBcRSoW', 'oMeEW4hdLhldScldNG', 'hWWaCq', 'W4lcTLvjkdm', 'gCkyW5CAW6FdMCkryri', 'txyPWOlcRSoQW6KPBG', 'aCkPWQRdHCoDW5u', 'v24+WP0', 'ASoiW7FdSq', 'gIz1ECoEFxtdNLeX', 'WQhcKmkOCXLf', 'acVcRqW3WRS', 'WOSvAmkyfqJcS8k+tSoRC8kt', 'WRPoasjCWOldP2BdQmo0', 'gCkJWPFdLSoBW5q0kW', 'WP0iDW', 'xmo6W7hdRrxdKqNdTSo1WR4', 'g8kTWQJdL8om', 'i2aWW4FdIwFdSa', 'WOT8WOZdGCk0tG', 'WRTDDSoN', 'W5OEWQJcIG', 'hIVcTq4XWQaT', 'a8kJWRm', 'W68VAqq', 'WOfxcqu', 'mNinqa', 'cWFdN8oR', 'W4FcVK5c', 'qcujra', 'W7VdSNldSMDjxCkk', 'W73dIWKyW6ZcP8kTWPSb', 'wsm8rs1czeC', 'WOfjnqD1DCkiWRRdLq', 'WOfOzCkQW6rA', 'x8kNjSkYqfq', 'bCkpW5yjW7ZdHq', 'W5KgWOJcH0FdMG', 'WP5OqmkOW6K', 'twyaWPtcOW', 'WOJdVCoCW5S', 'WP/dSSoVBW', 'fmkqnW', 'WO8oACkr', 'WPtdQmohySoZW5GdW5C', 'WRbvkt5RWOJdPgBdMW', 'WPD2WPi', 'bGO1Cmk/ie7dUq', 'WRqsyq', 'W6ONCG8loq', 'emoUoCkw', 'umkTjSkMqgRcOLTY', 'W7hdRLRdQh12smkDzW', 'WP/dJCo/lbbcW6lcOHa', 'z3yhW53cN09Lmq3dL8omW7/cJCkm', 'oXBdVG', 'tNy4WPK', 'hXyd', 'oMycW50', 'fNtcKG', 'W67cH28OW5e6W44qA8k8mmoCWRhcVq', 'W6CNu0i', 'obxdP8oZW7m', 'WRBdMSkmBcPT', 'cIlcRaqX', 'W5ZcSLvkmZy', 'cN7cJc3dRCo/', 'WPJcTmkjnW', 'WOZdL8oInW', 'gCkFW4Sg', 'hchcSW', 'WR3cMSk2', 'C2ysW5W', 'WQLteZG', 'WQKuFW', 'eH/dMCoV', 'eaaw', 'WQLjea', 'WO3dRSoYyW', 'tMW7', 'WQRdISkryW', 'WPHvda', 'dZvr', 'csfK', 'C8oqW7hdTq', 'WPJcRSkk', 'WP14EmkL', 'W6tdVmo+pa', 'WPXAlq', 'WPHpdWe', 'WR/cTCkZ', 'W6tdJtmE', 'csfJ', 'WR3cGmk1Fa', 'W7yTBa', 'WPDSWPhdJG', 'ymk3EG', 'WOZdJCoH', 'WR/cR8kWqa', 'W6ldRKq', 'eGxdMG', 'W7y3BWa', 'WO3dTmoX', 'qd8k', 'oWZdVCo4', 'WPjVFW', 'C3Wr', 'W6ldTeFdSW', 'Bmorna', 'W7BcIwW', 'C8okW7i', 'oNWb', 'WRFcPCkk', 'gCkfW4G', 'fSo6omkn', 'W6tdPSo9', 'gw1RWPm', 'WPRcOSk2', 'W5D8WQ0', 'WOVcVCk2bwO', 'yMmrW5JcIa', 'CmoBkMBdOae', 'WOSoACkuoGZcQ8kfy8oGCSko', 'cGVdMCovCCopW5/dRLK', 'gI/cRX4M', 'WO5teGHTFmkwWPBdICo6W4zf', 'WO94WPhdTmkLuG7dOCou', 'w8kJo8khuuJcTLTV', 'fG4kW57cPW', 'W7JdNs4rW6ZcQG', 'd3f2WPRcVK/cKmoKW6ddSLhdRG', 'W7ZdQmo+fI/dRbLg', 'pXJdVmo3W7pcHa', 'hYD6ASoXFMNdSN4HWRZcQa', 'eZ9pvWui', 'W6aRCGKtpupcHSk2tmoRnq', 'WOvSEmkoW79CEYZcJvyj', 'WPn4WPddGCkLuG', 'DSkXzbpcO8oZW690CmoVxmoa', 'Bmoln2K', 'WQ8AFtO', 'fsT6BmoPEG', 'WQ1bA8oUlCoTCCkVtYpdSCkY', 'fSoQjCkbWRyyBgVcRSkVWQtdPSoDesCz', 'W5OoWRxcHKVdKmogp1qGpwycWOeInW', 'WOugDmkNmXtcP8k+yW', 'WPTSz8k4W7u', 'bXGas8k0pu/dRLK', 'WOVdUSoTFSo4', 'W7ZdMtm0W6RcP8kRWPu', 'WQnjDSonm8oKACkn', 'W7iJBG8Ajq', 'WOlcRmk1kNWhW5b8W5PSWQe', 'WObBdYPUFSkBWRBdICoRW4y', 'WONdUSoZBmo4W4u', 'hdVcSam', 'W57cVeS', 'WOlcVCkfW54', 'W5OeWQS', 'W5DMWQ4p', 'fM7cKsi', 'WRHveZL4WOm', 'q8kToa', 'WPj1FmoZ', 'WObqm8kNWOFdMW', 'ymkQzqBcOmoRW69nEW', 'hdZcRb8SWQCXsCk6', 'p3OErCo/mN5XWRZdP8kIWQRdP8ok', 'WQVcR8kuW7ZcK8oh', 'W7yWCXWqjupcV8k9', 'hWSCBCk+pupdRfi', 'WQ9ny8oMl8oKwmkutJFdSCk4Dvm', 'WO5LyCo8eSob', 'b2VcKIBdOa', 'WQDnA8oOnCoP', 'oM8iqmoO', 'WQNcKmkGFqniWQSlsCkwW5W/FSoH', 'qZuoFdfeze3dOHlcQvpcVmom', 'eb0jW5/cRCohqCknkG', 'W6CGt14YWQRcSCoMtG', 'W5KoWQ/cSLddKCovfvG6khm5WO4', 'WPr3iCkRmSo0Emkdu2pcSmkvxG', 'cSkPWRddSSoBW5iUi1NdMt8gWR4D', 'ax7cLHRdQ8o4w0RdNCoOW75rW6vu', 'WPRdVSo1rmoQW58NW4aSW5RcP8o/WQxcOt/cUmoggePJW6NdICo1W6K', 'a8kAmW', 'wwy/', 'dbGFDq', 'gYD6BW', 'W6tdLZa', 'WQdcR8koW4VcLCoaW5HFWQ7dOIaKDYC', 'gZ9hwr8fAMJcV8oCF8oQpmof', 'WRFcUmkvW6/cImoBW5vaWR8', 'xduusZDd', 'WR0EAsaQW4eMWO/dVCocW7ucWRpcIq', 'WPddH8o/obb8', 'W4RcTL1hmJ5/DaVcOcqWo8od', 'B3ypW5pcHui', 'WR7dMSkeyJbGDe/cPrGrW4/cObK', 'WQRdKmks', 'W7BdPfldSMDfECkDE8oxyIBdSu8', 'WPNdVSoNySoZW5qNW4aSW5RcP8o/WQxcOq', 'WPHieX1UzmkwWQ/dGG', 'wMyTWPJcTmo9W5a1zK/dHZnGxq', 'WOlcP8kg', 'WPJcS8kvk0zoWPC1yW', 'WOzLACoYcmomltNcT8oAvG0EW5u', 'W6iNEGerngRcVCk3wmoRp8kTjG', 'WP1IEW', 'hIPrxaG', 'WO9umCkS', 'WOfHy8o3', 'WOecACksiGG', 'W7hdOfJdTW', 'vduCrs1oqfddUrVcVetcH8ot', 'fSoGoW', 'aqxdHmo0ymojW5/dV0m', 'ebOvW4m', 'fILGqGmbqW', 'WQKjyd0RW5apWO3dTW', 'k2Olra', 'CCkOEH7cTG', 'WRFcV8kjW7m', 'WRThDq', 'WOZdRmovW6uAdCoF', 'gX0jt8kWo0K', 'W6ldMtif', 'W7aJBHS', 'WP1SECkOW75g', 'WPRcUmk1aq', 'W7dcH24u', 'WPhcP8kyW4xdSmokWQqnWQq', 'ymokW6ZdRHpdOGNdOmoz', 'eN/cMbZdUmoLxa', 'WRpcRSkaW43cHSoDW58', 'WRVcVSk5FSo7W6JdIW', 'W5JcSKLD', 'BmoFnMtdUH0', 'W6ddNdOGW7NcSmk5', 'W7iMzJ4Ei0K', 'WR1jD8o8', 'WQKAFsWQW5a', 'oNidW5ddLxi', 'WOBcRmkmW6ddPCoUWRy', 'WONdV8o7xCo8W4me', 'y8kOzHVcUW', 'WR9mF8ozimoZEW', 'WQ9heIm', 'WOJdP8oF', 'faVdMmo0', 'C8k3zahcU8ojW7DpBq', 'WOfVyCoOeSo/hdNcQW', 'WOr2WOZdLCk0CbRdOCoj', 'yhWpW4FcHxXumre', 'WONcOSkOgMC/W4vNW4C', 'fNRcKc/dT8oJ', 'WPZcPCkacuHiWP0', 'l3ScESoWjv0', 'WQ0FDr8LW5yf', 'ehRcKdK', 'kxWFW4BdJ1ddQcddIa', 'gIf6EmoPrhhdIwm', 'W6uTCHSlb1VcVCkR', 'W6BdPu7dJwHswG', 'WPrPWO7dJ8k0', 'W54pWQhcTepdJmos', 'dsPUxCo8ygm', 'WPSgDCkg', 'dSkJWQRdKCoDW6S7pL4', 'W4KeWRxcKvBdQmoacf8', 'WO5IzCk+W6rKBJFcKa', 'W5RcT0f4psLC', 'fCoJiSkgWRO', 'WQ7cLmkQEa', 'W6uJCaqAna', 'DSk3Ea', 'k3ai', 'WOLLDSoDcCoB', 'aXWDFSkLiq', 'WOr5BSk/W7fgydC', 'W7BcK28p', 'W7FdQmoHoa', 'WOL8WPRdKG', 'z8okW6ZdUa', 'gxDO', 'W4ikWQJcRvxdKmoXcemZpwqcWPe', 'W7JdRmoJmYNdOq', 'WPf0BSo4dCo6fdhcVq', 'oh4mt8o5hKbNWRBdRW', 'WPVdQCoBW5atnSocW4feWPm', 'WOr4WPBdHCkOBXxdT8oFfq', 'WQNcS8kTsCo2W7BdGCkRkmo4EXG', 'WRZdLSkmAJjPxxtcPaWrW4u', 'hXWDFCk4j13dMu9Veevzo8kLeW', 'WQ5gyCogl8oLBCkE', 'WOBcPmkckW', 'W7m9tK8', 'W6ldMsWdW70', 'WQhcV8k7xa', 'WQVcTCkTtq', 'WRhcQ8kwW67cGG', 'WO/dVSoYzmoXW4Cs', 'W6eZtf84', 'WQpcKmk+ya', 'l3Ckq8oM', 'ehRcJJ/dVa', 'WRVcSSkXr8oT', 'D3StW5VcHG', 'cSkAp8k8', 'WOBcOmkeW5NdSW', 'W7ddLY4t', 'h3L0WO7cTW', 'WQZdNSkoFJS', 'WP7cPCk0bMq', 'BCoaW7RdQq', 'W44eWRxcHW', 'WOT0ASoPb8oDeJK', 'agX9WONcS1FcHSoF', 'jrZdTSoK', 'p3awsq', 'WRNcU8kVxCo/', 'ctTnrrq', 'WPbLE8oUfmoh', 'WOhcTCkFluHoWOe3', 'hdTnxa', 'C8k5zH4', 'WOTBeaP0FmkoWQVdGSooW5fuDCoK', 'bCoUj8kj', 'cJZcRay', 'WOT2WOu']

def U(id, rc4_key):
    code = array_b[id]
    cache_key = f"{array_b[0]}{id}"
    try: return cache[cache_key]
    except KeyError: pass

    cache[cache_key] = decrypted = rc4(base64(code), rc4_key)
    return decrypted

letters = set("$0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz")
def format_bytes_as_safe_string(data: bytes) -> str:
    out = []
    yeah_all = True
    for b in data:
        ch = chr(b)
        # yeah = ch in letters
        yeah = ch.isalnum() or ch in "_$"
        yeah_all &= yeah
        out.append(ch if yeah else f"\\x{b:02X}")
    return f"'{''.join(out)}'", yeah_all

"""
if __name__ == "__main__":
    count = yeahs = 0
    not_yeah = []
    for item in find_U_calls(JS_PATH):
        print(
            f"line {item['line']}: {item['full_match']} -> hex={item['hex_arg']} ({item['hex_int']}), tag='{item['tag']}'"
        )
        decrypted = U(item['hex_int'], item['tag'].encode('latin1'))
        s, yeah = format_bytes_as_safe_string(decrypted)
        count += 1
        yeahs += yeah
        print(s)
        if not yeah: not_yeah.append(s)
    print("count:", count)
    print("yeahs:", yeahs)
    print("not_yeah:", not_yeah)
"""



U_CALL_RE = re.compile(
    r"""
    (?P<bracket>

\[)?                # возможная открывающая [
    U\s*\(\s*
        (?P<hex>0x[0-9a-fA-F]+|'0x[0-9a-fA-F]+'|\d+)   # hex или число
        \s*,\s*
        (?P<tag>'[^']*'|"[^"]*")    # строковый ключ
    \s*\)
    (?(bracket)\]

)                  # если была [, то требуем ]
    """,
    re.VERBOSE
)

def replace_U_call(match):
    hex_arg = match.group("hex")
    tag = match.group("tag")[1:-1]
    bracket = match.group("bracket")

    # нормализуем hex → int
    if hex_arg.startswith(("'", '"')):
        hex_arg = hex_arg[1:-1]
    idx = int(hex_arg, 16) if hex_arg.startswith("0x") else int(hex_arg)

    # дешифруем
    decrypted = U(idx, tag.encode("latin1"))
    s, yeah = format_bytes_as_safe_string(decrypted)

    # если строка полностью ['\w\w\w...']
    if yeah and bracket:
        name = decrypted.decode("latin1")
        return f".{name}"
    return s

with open(JS_PATH, "r", encoding="utf-8") as f:
    js = f.read()

new_js = U_CALL_RE.sub(replace_U_call, js)

with open("output.js", "w", encoding="utf-8") as f:
    f.write(new_js)
