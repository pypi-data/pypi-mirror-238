# type: ignore

from __future__ import annotations

from enum import Enum
from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field, constr


class FilterItem(BaseModel):
    id: str = Field(..., description="Unique id for this filter")
    name: List[str] = Field(
        ...,
        description="Names of the fields that this filter applies to (respectively to dataIds)",
    )
    type: str = Field(
        "range",
        const=True,
        description="Range filter specifies sets min and max values for a numeric field",
    )
    data_id: List[str] = Field(
        ..., alias="dataId", description="Dataset ids that this filter applies to"
    )
    view: str = Field(
        "side",
        const=True,
        description="Where the filter should be displayed: has to be side for non-timeRange filters",
    )
    value: Optional[List[float]] = Field(..., description="Range of the filter")


class View(Enum):
    side = "side"
    enlarged = "enlarged"
    minified = "minified"


class AnimationWindow(Enum):
    free = "free"
    incremental = "incremental"
    point = "point"
    interval = "interval"


class Type(Enum):
    integer = "integer"
    real = "real"
    string = "string"
    boolean = "boolean"
    date = "date"


class YAxi(BaseModel):
    name: str = Field(..., description="Name of the field")
    type: Type = Field(..., description="Type of the field")


class SyncTimelineMode(Enum):
    number_0 = 0
    number_1 = 1


class Type1(Enum):
    histogram = "histogram"
    line_chart = "lineChart"


class Aggregation(Enum):
    count = "COUNT"
    sum = "SUM"
    mean = "MEAN"
    max = "MAX"
    min = "MIN"
    deviation = "DEVIATION"
    variance = "VARIANCE"
    median = "MEDIAN"
    p05 = "P05"
    p25 = "P25"
    p50 = "P50"
    p75 = "P75"
    p95 = "P95"
    mode = "MODE"
    unique = "UNIQUE"
    merge = "MERGE"


class PlotType(BaseModel):
    type: Optional[Type1] = "histogram"
    interval: Optional[
        constr(regex=r"^([0-9]+)-(year|month|week|day|hour|minute|second|millisecond)$")
    ] = Field(
        None,
        description="Time interval for the time axis aggregation. Should be in the form (number)-(interval), where interval is one of: year, month, week, day, hour, minute, second, millisecond, e.g 1-day, 2-week, 3-month, 4-year",
    )
    aggregation: Optional[Aggregation] = Field(
        "SUM", description="Aggregation function for the time axis"
    )
    default_time_format: Optional[str] = Field(
        None,
        alias="defaultTimeFormat",
        description="Default time format for the time axis. For the syntax check these docs: https://momentjs.com/docs/#/displaying/format/",
    )


class GeometryItem(BaseModel):
    type: str = Field("Polygon", const=True)
    coordinates: List[List[List[float]]]


class GeometryItem1(BaseModel):
    type: str = Field("MultiPolygon", const=True)
    coordinates: List[List[List[List[float]]]]


class ValueItem(BaseModel):
    type: str = Field("Feature", const=True)
    properties: Optional[Any] = None
    geometry: Union[GeometryItem, GeometryItem1]
    id: Optional[str] = Field(None, description="Unique id of the polygon")


class DataId(BaseModel):
    __root__: List[str] = Field(
        ..., description="Dataset ids that this filter applies to"
    )


class Id(BaseModel):
    __root__: str = Field(..., description="Unique id for this filter")


class Name(BaseModel):
    __root__: List[str] = Field(
        ...,
        description="Names of the fields that this filter applies to (respectively to dataIds)",
    )


class ViewModel(BaseModel):
    __root__: str = Field(
        "side",
        const=True,
        description="Where the filter should be displayed: has to be side for non-timeRange filters",
    )


class FilterItem1(BaseModel):
    id: Id
    name: Name
    type: str = Field(
        "timeRange",
        const=True,
        description="Time range filter specifies sets min and max values",
    )
    data_id: DataId = Field(..., alias="dataId")
    view: Optional[View] = Field(
        "side",
        description="Where the filter should be displayed: side, enlarged or minified",
    )
    value: Optional[List[float]] = Field(..., description="Range of the filter")
    animation_window: Optional[AnimationWindow] = Field(
        "free", alias="animationWindow", description="Animation window type"
    )
    y_axis: Optional[Union[Any, YAxi]] = Field(
        None, alias="yAxis", description="Dimension field for the y axis"
    )
    speed: Optional[float] = Field(1, description="Speed of the animation")
    synced_with_layer_timeline: Optional[bool] = Field(
        None,
        alias="syncedWithLayerTimeline",
        description="Whether the filter should be synced with the layer timeline",
    )
    sync_timeline_mode: Optional[SyncTimelineMode] = Field(
        None,
        alias="syncTimelineMode",
        description="Sync timeline mode: 0 (sync with range start) or 1 (sync with range end)",
    )
    invert_trend_color: Optional[bool] = Field(
        None,
        alias="invertTrendColor",
        description="Whether the trend color should be inverted",
    )
    timezone: Optional[str] = Field(
        None,
        description="Timezone (TZ identifier) for displaying time, e.g. America/New_York",
    )
    plot_type: Optional[PlotType] = Field(
        default_factory=lambda: PlotType.parse_obj("histogram"),
        alias="plotType",
        description="Type of plot to show in the enlarged panel",
    )


class FilterItem2(BaseModel):
    id: Id
    name: Name
    type: str = Field(
        "select", const=True, description="Select filter with a single boolean value"
    )
    data_id: DataId = Field(..., alias="dataId")
    view: Optional[ViewModel] = None
    value: Optional[bool] = Field(..., description="Selected or not")


class FilterItem3(BaseModel):
    id: Id
    name: Name
    type: str = Field(
        "multiSelect",
        const=True,
        description="Multi select filter with a list of values",
    )
    data_id: DataId = Field(..., alias="dataId")
    view: Optional[ViewModel] = None
    value: Optional[List[str]] = Field(..., description="List of selected values")


class FilterItem4(BaseModel):
    id: Id
    name: Name
    type: str = Field("polygon", const=True, description="Polygon selection on the map")
    data_id: DataId = Field(..., alias="dataId")
    view: Optional[ViewModel] = None
    value: Optional[ValueItem] = Field(
        ..., description="Polygon selection on a map (GeoJSON format)"
    )
    layer_id: Optional[List[str]] = Field(
        None, alias="layerId", description="Layer ids that this filter applies to"
    )


class Filter(BaseModel):
    __root__: Union[
        FilterItem, FilterItem1, FilterItem2, FilterItem3, FilterItem4
    ] = Field(..., title="Filter")
