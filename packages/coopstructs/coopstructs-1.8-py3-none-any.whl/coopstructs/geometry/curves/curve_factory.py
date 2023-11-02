from coopstructs.geometry.curves.curves import CubicBezier, Arc, CircularArc, LineCurve, CatmullRom, Curve
from typing import Dict, Callable, List
from cooptools.typeProviders import StringProvider, resolve_string_provider, resolve
from cooptools.config import JsonConfigHandler


def curve_from_dict(curve_dict: Dict,
                    config_curve_type_header_provider: StringProvider = 'type') -> Curve:
    curve_type_header = resolve_string_provider(config_curve_type_header_provider)

    curve_type = curve_dict[curve_type_header]

    curve_gen_switch: Dict[str, Callable[[Dict], Curve]] = {
        CubicBezier.__name__: CubicBezier.from_dict,
        Arc.__name__: Arc.from_dict,
        CircularArc.__name__: CircularArc.from_dict,
        LineCurve.__name__: LineCurve.from_dict,
        CatmullRom.__name__: CatmullRom.from_dict,
    }
    gen_func = curve_gen_switch.get(curve_type, None)

    if gen_func is None:
        raise ValueError(f"Unsupported curve type: {curve_type}")

    return gen_func(curve_dict)

def curves_from_dict(curves_data: List[Dict],
                     ) -> Dict[str, Curve]:

    curves = {}
    for data in curves_data:
        curve = curve_from_dict(data)
        curves[curve.id] = curve

    return curves

def curves_from_json_file(curves_file: StringProvider,
                          config_curves_header_provider: StringProvider = 'curves') -> List[Curve]:
    json_config_file = JsonConfigHandler(file_path_provider=curves_file)
    curves_header = resolve_string_provider(config_curves_header_provider)

    curves_data = json_config_file.resolve(config=curves_header)

    return list(curves_from_dict(curves_data).values())


if __name__ == "__main__":
    import pprint
    curves = curves_from_json_file(r"C:\Users\tburns\PycharmProjects\coopstructs\tests\testData\curves.json")
    pprint.pprint(curves)