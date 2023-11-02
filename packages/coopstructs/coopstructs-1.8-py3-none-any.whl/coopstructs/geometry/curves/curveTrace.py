import time
from coopstructs.geometry.curves.curves import Curve
from coopstructs.geometry.polygonRegion import PolygonRegion
from coopstructs.geometry.vectors.vectorN import Vector2
import cooptools.geometry_utils.circle_utils as circ
from typing import Tuple, List, Dict, Sequence, Callable, Iterable, Union
import math
from dataclasses import dataclass
import cooptools.os_manip as osm
from coopstructs.geometry.curves.curve_factory import curves_from_dict, curves_from_json_file
from cooptools.plotting import plot_series
from cooptools.colors import Color
from cooptools.geometry_utils.vector_utils import FloatVec
import matplotlib.pyplot as plt
import logging
from cooptools.config import JsonConfigHandler
from cooptools.typeProviders import StringProvider, StringChoiceProvider, resolve_string_provider, resolve

logger = logging.getLogger(__name__)


@dataclass
class TraceIter:
    polygon: PolygonRegion
    anchor: Tuple[float, float]
    tangent: Tuple[float, float]


@dataclass
class TraceMeta:
    polygon: PolygonRegion
    traces: Dict[int, TraceIter]
    swimlane: PolygonRegion


TraceablePoly = Tuple[PolygonRegion, FloatVec]
TraceablePolyProvider = Union[TraceablePoly, Callable[[], TraceablePoly]]
CurvesProvider = Union[Iterable[Curve], Callable[[], Iterable[Curve]]]
DictProvider = Union[dict, Callable[[], dict]]
CurveTraceDict = Dict[Curve, TraceMeta]
CurveTraceBlockDict = Dict[Curve, Tuple[TraceMeta, Dict[Curve, TraceMeta]]]
CurveBlockDict = Dict[Curve, List[Curve]]

def resolve_traceable_poly(
        traceable_poly_provider: TraceablePolyProvider = None,
        traceable_poly_dict_provider: DictProvider = None,
) -> TraceablePoly:
    if traceable_poly_provider is not None:
        poly, pivot = resolve(traceable_poly_provider)
    elif traceable_poly_dict_provider is not None:
        poly_dict = resolve(traceable_poly_dict_provider)
        poly, pivot = traceable_poly_from_dict(poly_dict)
    else:
        raise ValueError(f"At least one of traceable_poly_provider or traceable_poly_dict_provider cannot be None")

    return poly, pivot


def trace_curves(
        curves_provider: CurvesProvider,
        traceable_poly_provider: TraceablePolyProvider = None,
        traceable_poly_dict_provider: DictProvider = None,
) -> Dict[Curve, TraceMeta]:
    poly, pivot = resolve_traceable_poly(
        traceable_poly_provider=traceable_poly_provider,
        traceable_poly_dict_provider=traceable_poly_dict_provider
    )
    curves = resolve(curves_provider)

    logger.info(f"Tracing Curves [{len(curves)}]")
    ret = {}
    for curve in curves:
        traced = trace_curve_with_polygon(curve=curve,
                                          polygon=poly,
                                          pivot=pivot)
        sl = create_swimlane([x.polygon for x in traced.values()], buffer=0.25)
        ret[curve] = TraceMeta(
            polygon=poly,
            traces=traced,
            swimlane=sl
        )

    logger.info(f"Done Tracing Curves")
    return ret


def trace_curve_with_polygon(curve: Curve,
                             polygon: PolygonRegion,
                             pivot: Iterable[float],
                             increment_fixed: float = None,
                             increment_p: float = None,
                             default_rads: float = None,
                             ) -> Dict[int, TraceIter]:
    if increment_p is None and increment_fixed is None:
        increment_p = 0.05

    if increment_p is None and increment_fixed is not None:
        increment_p = increment_fixed / curve.Length

    if increment_p is not None and increment_fixed is not None:
        increment_p = min(increment_p, increment_fixed / curve.Length)

    if default_rads is None:
        default_rads = math.pi / 2

    # move the poly so that its pivot is at 0, 0
    adjusted_poly = PolygonRegion(boundary_points=[pt - Vector2.from_tuple(pivot) for pt in polygon.boundary_points])

    # determine the convex hull of the adjusted poly
    ch = PolygonRegion.convex_hull(adjusted_poly.boundary_points)

    iter = {}
    t = 0
    ii = 0
    while t < 1:
        # get position and direction
        anchor = curve.point_at_t(t)
        tu = curve.tangent_at_t(t)

        rads = circ.rads_of_point_around_origin(tu.as_tuple()) - default_rads

        # translate ch to position and rotation
        pts = []
        for point in ch.boundary_points:
            rotated_point = circ.rotated_point(point=point.as_tuple(), center=(0, 0), rads=rads)
            adjusted_boundary_point = Vector2.from_tuple(rotated_point) + anchor
            pts.append(adjusted_boundary_point)
            iter[ii] = TraceIter(polygon=PolygonRegion(pts), anchor=anchor.as_tuple(), tangent=tu.as_tuple())

        # increment t
        t += increment_p
        ii += 1

    # convex hull of swim lane verts
    return iter


def create_swimlane(positions: Sequence[PolygonRegion], buffer: float = None) -> PolygonRegion:
    swimlane = None
    for ii, poly in enumerate(positions):
        if ii == 0:
            continue

        points = poly.boundary_points + positions[ii - 1].boundary_points
        hull = PolygonRegion.convex_hull(points)

        if swimlane is None:
            swimlane = hull
        else:
            swimlane = swimlane.union(hull)

    if buffer:
        swimlane = swimlane.buffer(buffer=buffer)

    return swimlane


def trace_from_files(poly_file: StringProvider,
                     curves_file: StringProvider) -> Dict[Curve, TraceMeta]:
    return trace_curves(
        traceable_poly_provider=lambda: traceable_poly_from_file(poly_file),
        curves_provider=lambda: curves_from_json_file(curves_file)
    )


def traceable_poly_from_dict(dict: DictProvider) -> TraceablePoly:
    dict = resolve(dict)
    poly = PolygonRegion.from_json(dict)
    pivot = Vector2.from_json(dict['pivotPoint'])
    return poly, pivot.as_tuple()


def traceable_poly_from_file(poly_file: StringProvider) -> TraceablePoly:
    poly_file = resolve(poly_file)
    content = osm.try_load_json_data_to_dict(poly_file)
    return traceable_poly_from_dict(content)


# def curves_from_file(curves_file: StringProvider) -> List[Curve]:
#     curves_file = resolve(curves_file)
#     content = osm.try_load_json_data_to_dict(curves_file)
#
#     return list(curves_from_dict(content).values())


def plot_traced_curve(traced_curve: Dict[int, TraceIter],
                      swim_lane: PolygonRegion,
                      ax,
                      fill_color: Color = None):
    plot_series(ax=ax, points=[x.as_tuple() for x in swim_lane.boundary_points], series_type='fill', color=fill_color)
    for ii, iter in traced_curve.items():
        plot_series(points=[x.as_tuple() for x in iter.polygon.boundary_points],
                    ax=ax,
                    series_type="scatter",
                    point_size=1
                    )
    plot_series(ax=ax, points=[traced.anchor for ii, traced in traced_curve.items()], series_type='line', color=Color.BLACK)


def plot_traced_curves(
        traces: Dict[Curve, TraceMeta],
        fill_color: Color = None,
        ax=None
):
    logger.info(f"Plotting Curves")

    if ax is None:
        fig, ax = plt.subplots(1, 1)

    for curve, meta in traces.items():
        plot_traced_curve(meta.traces, meta.swimlane, ax, fill_color=fill_color)

    logger.info(f"Done Plotting curves")
    plt.show()

def _get_traceable_poly_dict_from_config(
    config: JsonConfigHandler,
    traceable_poly_name_provider: StringChoiceProvider,
    config_signature_options_header_provider: StringProvider = 'signatures',
):
    signature_options_header =resolve_string_provider(config_signature_options_header_provider)
    signature_options = config.resolve(signature_options_header)
    choice = traceable_poly_name_provider(list(signature_options.keys()))
    if choice is None:
        return None
    return signature_options[choice]


def _get_curves_from_config(config: JsonConfigHandler) -> List[Curve]:
    curves_from_dict(
        curves_dict=config.resolve(),

    )

def _get_traceable_poly_from_config(
    config: JsonConfigHandler,
    traceable_poly_name_provider: StringChoiceProvider,
    config_signature_options_header_provider: StringProvider = 'signatures',
) -> TraceablePoly:
    poly_dict = _get_traceable_poly_dict_from_config(
        config=config,
        traceable_poly_name_provider=traceable_poly_name_provider,
        config_signature_options_header_provider=config_signature_options_header_provider
    )
    if poly_dict is None:
        return None
    return traceable_poly_from_dict(poly_dict)

def get_traces_from_config(
    config: JsonConfigHandler,
    curves: Iterable[Curve],
    traceable_poly_choice_provider: StringChoiceProvider,
    config_signature_options_header_provider: StringProvider = 'signatures',
    plot: bool = False
) -> Dict[Curve, TraceMeta]:

    traces = trace_curves(
         traceable_poly_provider=_get_traceable_poly_from_config(
             config=config,
             traceable_poly_name_provider=traceable_poly_choice_provider,
             config_signature_options_header_provider=config_signature_options_header_provider
         ),
         curves_provider=curves
    )

    if plot:
        plot_traced_curves(traces)

    return traces


def collision_naive_generator(
        traces: CurveTraceDict
):
    for curve, trace in traces.items():
        for curve2 in traces.keys():
            if curve == curve2:
                continue
            curve2_trace = traces[curve2]
            if trace.swimlane.intersects(curve2_trace.swimlane):
                yield curve, curve2

def collisions_naive_old(
    traces: CurveTraceDict,
) -> CurveBlockDict:
    ret = {}
    logger.info(f"Starting Naive Collision Analysis")

    for curve, trace in traces.items():
        intersects = []
        for curve2 in traces.keys():
            if curve == curve2:
                continue
            curve2_trace = traces[curve2]
            if trace.swimlane.intersects(curve2_trace.swimlane):
                intersects.append(curve2)
        ret[curve] = intersects

    logger.info(f"Naive Collision Analysis Completed!")
    return ret

def collisions_naive(
    traces: CurveTraceDict,
) -> CurveBlockDict:
    logger.info(f"Starting Naive Collision Analysis")

    curve_intersections = {}

    for c1, c2 in collision_naive_generator(traces=traces):
        curve_intersections.setdefault(c1, []).append(c2)

    logger.info(f"Naive Collision Analysis Completed!")
    return curve_intersections

def plot_collisions(
     curve_intersections: Dict[Curve, List[Curve]],
     traces: CurveTraceDict,
     ax
):
    logger.info(f"Plotting Collisions")

    for curve, blocked in curve_intersections.items():
        ax.clear()

        # curve_trace.plot_traced_curves(traces, fill_color=Color.GREY, ax=ax)

        plot_collision(traced_curve=traces[curve],
                       blocked_traces=[traces[x] for x in curve_intersections[curve]],
                       ax=ax)


        # drawing updated values
        ax.canvas.draw()

        # This will run the GUI event
        # loop until all UI events
        # currently waiting have been processed
        ax.canvas.flush_events()

        time.sleep(0.5)

    logger.info(f"Done Plotting Collisions")
    # plt.show()


def plot_collision(traced_curve: TraceMeta,
                   blocked_traces: List[TraceMeta],
                   ax,
                   blocked_trace_color: Color = None,
                   trace_color: Color = None):
    if blocked_trace_color is None: blocked_trace_color = Color.ORANGE
    if trace_color is None: trace_color = Color.BLUE
    for trace in blocked_traces:
        plot_traced_curve(
            traced_curve=trace.traces,
            swim_lane=trace.swimlane,
            ax=ax,
            fill_color=blocked_trace_color
        )

    plot_traced_curve(
        traced_curve=traced_curve.traces,
        swim_lane=traced_curve.swimlane,
        ax=ax,
        fill_color=trace_color
    )


if __name__ == "__main__":
    t0 = time.perf_counter()
    traces = trace_from_files(
        poly_file=r'C:\Users\tburns\PycharmProjects\coopstructs\tests\testData\traceable_poly_data.json',
        curves_file=r'C:\Users\tburns\PycharmProjects\coopstructs\tests\testData\curves.json'
    )
    print(time.perf_counter() - t0)

    plot_traced_curves(traces)




