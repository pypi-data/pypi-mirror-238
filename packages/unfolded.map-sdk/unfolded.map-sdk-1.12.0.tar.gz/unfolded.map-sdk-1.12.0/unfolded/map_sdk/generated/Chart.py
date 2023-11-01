# type: ignore

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, constr


class FieldItem(BaseModel):
    name: str = Field(..., description="The name of the field.")
    type: str = Field(..., description="The type of the field.")


class AggregationEnum(Enum):
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


class Axis(BaseModel):
    field: Optional[FieldItem] = Field(
        ..., description="The field to use for the axis."
    )
    aggregation: Optional[AggregationEnum] = Field(
        ...,
        description="The aggregation function for the axis. Must be one of: COUNT, SUM, MEAN, MAX, MIN, DEVIATION, VARIANCE, MEDIAN, P05, P25, P50, P75, P95, MODE, UNIQUE, MERGE",
    )
    title: Optional[str] = Field(..., description="The title of the axis.")
    benchmark: Optional[str] = Field(
        None, description="The field value to use as the benchmark for the axis."
    )
    enable_grid_line: Optional[bool] = Field(
        None,
        alias="enableGridLine",
        description="Whether to show grid lines for the axis.",
    )


class ChartDisplay(BaseModel):
    show_total: Optional[bool] = Field(
        None, alias="showTotal", description="Whether to show the total value."
    )
    format: Optional[str] = Field(None, description="The format to use for the value.")


class Metric(BaseModel):
    id: str = Field(..., description="The unique id of the metric.")
    label: str = Field(..., description="The label of the metric.")
    data_id: str = Field(
        ..., alias="dataId", description="The id of the dataset to use for the metric."
    )
    expression: str = Field(..., description="The expression to use for the metric.")
    sanitized_expression: str = Field(
        ...,
        alias="sanitizedExpression",
        description="The sanitized expression to use for the metric.",
    )
    window_function_id: str = Field(
        ...,
        alias="windowFunctionId",
        description="The window function id to use for the metric. Should be one of RECTANGLE, TRIANGLE, SIN, NORMAL.",
    )
    window_size: float = Field(
        ..., alias="windowSize", description="The window size to use for the metric."
    )


class ChartItem(BaseModel):
    id: str = Field(..., description="The unique id of the chart.")
    title: str = Field(..., description="The title of the chart.")
    data_id: Optional[str] = Field(
        ..., alias="dataId", description="The id of the dataset to use for the chart."
    )
    apply_filters: Optional[bool] = Field(
        False,
        alias="applyFilters",
        description="Whether to apply filters to the chart.",
    )
    type: str = Field(
        "bigNumber",
        const=True,
        description="The type of the chart. Must be one of: bigNumber, horizontalBar, lineChart, barChart, layerChart, heatmapChart",
    )
    axis: Optional[Axis] = Field(
        None, description="The axis configuration for the chart."
    )
    chart_display: Optional[ChartDisplay] = Field(
        {}, alias="chartDisplay", description="The display configuration for the chart."
    )
    metric: Optional[Metric] = Field(
        None, description="The metric to use for the chart."
    )
    use_metric: Optional[bool] = Field(
        None, alias="useMetric", description="Whether to use a metric for the chart."
    )


class AggregationEnum1(Enum):
    numeric_bin = "numericBin"
    time_bin = "timeBin"
    unique_bin = "uniqueBin"


class ColorBy(Enum):
    field_ = ""
    y_axis = "Y-Axis"
    group_by = "GroupBy"


class Sort(Enum):
    data_order = "dataOrder"
    ascending = "ascending"
    descending = "descending"
    alpha_asc = "alphaAsc"
    alpha_desc = "alphaDesc"
    manual = "manual"


class Type(Enum):
    sequential = "sequential"
    qualitative = "qualitative"
    diverging = "diverging"
    cyclical = "cyclical"
    custom = "custom"
    ordinal = "ordinal"
    custom_ordinal = "customOrdinal"


class ColorBy1(Enum):
    y_axis = "Y-Axis"
    group_by = "GroupBy"
    field_ = ""


class Tooltip(BaseModel):
    show_percentage_change: Optional[bool] = Field(
        None,
        alias="showPercentageChange",
        description="Whether to show the percentage change in the tooltip.",
    )


class ColorBy2(Enum):
    x_axis = "X-Axis"
    group_by = "GroupBy"
    field_ = ""


class ColorBy3(Enum):
    value = "value"
    field_ = ""


class ChartDisplay5(BaseModel):
    show_in_tooltip: Optional[bool] = Field(
        None,
        alias="showInTooltip",
        description="Whether to show the chart in the tooltip.",
    )
    id_field: Optional[str] = Field(
        None,
        alias="idField",
        description="The id field to filter the chart data by when hovering an element.",
    )
    format: Optional[str] = Field(None, description="The format to use for the chart.")
    interval: Optional[
        constr(regex=r"^([0-9]+)-(year|month|week|day|hour|minute|second|millisecond)$")
    ] = Field(
        None,
        description="Time interval to aggregate by. Should be in the form (number)-(interval), where interval is one of: year, month, week, day, hour, minute, second, millisecond, e.g 1-day, 2-week, 3-month, 4-year",
    )


class SortBy(Enum):
    natural = "NATURAL"
    category = "CATEGORY"
    value = "VALUE"


class ColorBy4(Enum):
    y_axis = "Y-Axis"
    field_ = ""


class ApplyFilters(BaseModel):
    __root__: bool = Field(..., description="Whether to apply filters to the chart.")


class Aggregation(BaseModel):
    __root__: Optional[AggregationEnum] = Field(
        ...,
        description="The aggregation function for the axis. Must be one of: COUNT, SUM, MEAN, MAX, MIN, DEVIATION, VARIANCE, MEDIAN, P05, P25, P50, P75, P95, MODE, UNIQUE, MERGE",
    )


class Benchmark(BaseModel):
    __root__: Optional[str] = Field(
        ..., description="The field value to use as the benchmark for the axis."
    )


class EnableGridLine(BaseModel):
    __root__: bool = Field(..., description="Whether to show grid lines for the axis.")


class FieldModel(BaseModel):
    __root__: Optional[FieldItem] = Field(
        ..., description="The field to use for the axis."
    )


class Field0(FieldItem):
    pass


class Title(BaseModel):
    __root__: Optional[str] = Field(..., description="The title of the axis.")


class DataId(BaseModel):
    __root__: Optional[str] = Field(
        ..., description="The id of the dataset to use for the chart."
    )


class Id(BaseModel):
    __root__: str = Field(..., description="The unique id of the chart.")


class TitleModel(BaseModel):
    __root__: str = Field(..., description="The title of the chart.")


class Items(BaseModel):
    __root__: str


class AggregationModel(BaseModel):
    __root__: Optional[AggregationEnum1] = Field(
        ...,
        description="The aggregation function for the axis. Must be one of: numericBin, timeBin, uniqueBin",
    )


class BenchmarkModel(BaseModel):
    __root__: str = Field(
        ..., description="The field value to use as the benchmark for the axis."
    )


class FieldModel1(BaseModel):
    __root__: Optional[Field0] = Field(
        ..., description="The field to use for the axis."
    )


class Interval(BaseModel):
    __root__: constr(
        regex=r"^([0-9]+)-(year|month|week|day|hour|minute|second|millisecond)$"
    ) = Field(
        ...,
        description="Time interval for the aggregation in case of a time axis. Should be in the form (number)-(interval), where interval is one of: year, month, week, day, hour, minute, second, millisecond, e.g 1-day, 2-week, 3-month, 4-year",
    )


class TitleModel1(Optional[Title]):
    pass


class Format(BaseModel):
    __root__: str = Field(..., description="The format to use for the chart.")


class IdField(BaseModel):
    __root__: str = Field(
        ...,
        description="The id field to filter the chart data by when hovering an element.",
    )


class ShowInTooltip(BaseModel):
    __root__: bool = Field(..., description="Whether to show the chart in the tooltip.")


class LayerId(BaseModel):
    __root__: str = Field(
        ..., description="The id of the layer which the charts are shown for."
    )


class TypeModel(BaseModel):
    __root__: str = Field(
        "layerChart",
        const=True,
        description="The type of the chart. Must be one of: bigNumber, horizontalBar, lineChart, barChart, layerChart, heatmapChart",
    )


class ApplyFiltersModel(BaseModel):
    __root__: bool = Field(
        ..., description="Whether to apply the filters to the chart."
    )


class ChartDisplayModel(BaseModel):
    show_in_tooltip: Optional[ShowInTooltip] = Field(None, alias="showInTooltip")
    id_field: Optional[IdField] = Field(None, alias="idField")
    format: Optional[Format] = None
    include_internal: Optional[bool] = Field(
        None, alias="includeInternal", description="Whether to include internal flows."
    )
    num_entries: Optional[float] = Field(
        None,
        alias="numEntries",
        description="The number of entries to show in the chart.",
    )


class XAxis(BaseModel):
    field: FieldModel
    aggregation: Aggregation
    title: Optional[Title]
    benchmark: Optional[Benchmark] = None
    enable_grid_line: Optional[EnableGridLine] = Field(None, alias="enableGridLine")


class YAxis(BaseModel):
    title: Optional[str] = Field(..., description="The title of the axis.")
    field: Optional[Field0] = Field(..., description="The field to use for the axis.")
    aggregation: Optional[AggregationEnum1] = Field(
        ...,
        description="The aggregation function for the axis. Must be one of: numericBin, timeBin, uniqueBin",
    )
    interval: Optional[
        constr(regex=r"^([0-9]+)-(year|month|week|day|hour|minute|second|millisecond)$")
    ] = Field(
        None,
        description="Time interval for the aggregation in case of a time axis. Should be in the form (number)-(interval), where interval is one of: year, month, week, day, hour, minute, second, millisecond, e.g 1-day, 2-week, 3-month, 4-year",
    )
    benchmark: Optional[str] = Field(
        None, description="The field value to use as the benchmark for the axis."
    )
    enable_grid_line: Optional[bool] = Field(
        None,
        alias="enableGridLine",
        description="Whether to show grid lines for the axis.",
    )


class GroupBy(BaseModel):
    title: Optional[TitleModel1]
    field: FieldModel1
    aggregation: AggregationModel
    interval: Optional[Interval] = None
    benchmark: Optional[BenchmarkModel] = None
    enable_grid_line: Optional[EnableGridLine] = Field(None, alias="enableGridLine")


class ColorRange(BaseModel):
    name: Optional[str] = Field("Unnamed", description="The name of the color range.")
    type: Optional[Type] = Field(
        "sequential",
        description="The type of the color range. Must be one of: sequential, qualitative, diverging, cyclical, custom, ordinal, customOrdinal",
    )
    category: Optional[str] = "Unnamed"
    colors: List[str]
    reversed: Optional[bool] = None
    color_map: Optional[
        List[List[Union[Optional[Union[str, float, List[str]]], Items]]]
    ] = Field(None, alias="colorMap")
    color_legends: Optional[Dict[str, str]] = Field(None, alias="colorLegends")


class ChartDisplay1(BaseModel):
    sort: Optional[Sort] = Field(None, description="The sort type for the chart.")
    sort_group_by: Optional[Sort] = Field(
        None, alias="sortGroupBy", description="The sort type for the group by axis."
    )
    number_shown: Optional[float] = Field(
        None,
        alias="numberShown",
        description="The number of bars to show in the chart.",
    )
    display_vertical: Optional[bool] = Field(
        None,
        alias="displayVertical",
        description="Whether to display the chart vertically.",
    )
    color_range: Optional[ColorRange] = Field(
        default_factory=lambda: ColorRange.parse_obj(
            {
                "name": "Uber Viz Qualitative",
                "type": "qualitative",
                "category": "Uber",
                "colors": [
                    "#12939A",
                    "#DDB27C",
                    "#88572C",
                    "#FF991F",
                    "#F15C17",
                    "#223F9A",
                    "#DA70BF",
                    "#125C77",
                    "#4DC19C",
                    "#776E57",
                ],
            }
        ),
        alias="colorRange",
        description="The color range for the chart.",
    )
    format: Optional[str] = Field(None, description="The format to use for the value.")


class ChartItem1(BaseModel):
    id: Id
    title: TitleModel
    data_id: Optional[DataId] = Field(..., alias="dataId")
    apply_filters: Optional[ApplyFilters] = Field(None, alias="applyFilters")
    type: str = Field(
        "horizontalBar",
        const=True,
        description="The type of the chart. Must be one of: bigNumber, horizontalBar, lineChart, barChart, layerChart, heatmapChart",
    )
    x_axis: XAxis = Field(
        ..., alias="xAxis", description="The x axis configuration for the chart."
    )
    y_axis: YAxis = Field(
        ..., alias="yAxis", description="The y axis configuration for the chart."
    )
    group_by: Optional[GroupBy] = Field(
        None,
        alias="groupBy",
        description="The group by axis configuration for the chart.",
    )
    color_by: Optional[ColorBy] = Field(
        "Y-Axis", alias="colorBy", description="The color by option for the chart."
    )
    num_groups: Optional[Union[float, str]] = Field(
        10,
        alias="numGroups",
        description="The number of groups to show in the chart. Use ALL to show all groups.",
    )
    chart_display: Optional[ChartDisplay1] = Field({}, alias="chartDisplay")


class XAxis1(GroupBy):
    pass


class YAxis1(XAxis):
    pass


class YAxis3(GroupBy):
    pass


class Value(XAxis):
    pass


class YAxis4(XAxis):
    pass


class ChartItem5(BaseModel):
    id: Id
    title: TitleModel
    type: str = Field(
        "layerChart",
        const=True,
        description="The type of the chart. Must be one of: bigNumber, horizontalBar, lineChart, barChart, layerChart, heatmapChart",
    )
    layer_chart_type: str = Field(
        "TIME_SERIES",
        alias="layerChartType",
        const=True,
        description="The tooltip chart type. Must be one of TIME_SERIES, HEXTILE_TIME_SERIES, BREAKDOWN_BY_CATEGORY, FLOW_TOP_ORIGINS, FLOW_TOP_DESTS",
    )
    layer_id: str = Field(
        ...,
        alias="layerId",
        description="The id of the layer which the charts are shown for.",
    )
    chart_display: Optional[ChartDisplay5] = Field(
        {}, alias="chartDisplay", description="The display configuration for the chart."
    )
    apply_filters: Optional[bool] = Field(
        None,
        alias="applyFilters",
        description="Whether to apply the filters to the chart.",
    )
    x_axis: XAxis1 = Field(
        ..., alias="xAxis", description="The x axis configuration for the chart."
    )
    y_axis: YAxis4 = Field(
        ..., alias="yAxis", description="The y axis configuration for the chart."
    )


class ChartDisplay6(BaseModel):
    show_in_tooltip: Optional[ShowInTooltip] = Field(None, alias="showInTooltip")
    id_field: Optional[IdField] = Field(None, alias="idField")
    format: Optional[Format] = None


class ChartItem6(BaseModel):
    id: Id
    title: TitleModel
    type: TypeModel
    layer_chart_type: str = Field(
        "HEXTILE_TIME_SERIES",
        alias="layerChartType",
        const=True,
        description="The tooltip chart type. Must be one of TIME_SERIES, HEXTILE_TIME_SERIES, BREAKDOWN_BY_CATEGORY, FLOW_TOP_ORIGINS, FLOW_TOP_DESTS",
    )
    layer_id: LayerId = Field(..., alias="layerId")
    chart_display: ChartDisplay6 = Field(
        ...,
        alias="chartDisplay",
        description="The display configuration for the chart.",
    )
    apply_filters: Optional[bool] = Field(
        None,
        alias="applyFilters",
        description="Whether to apply the filters to the chart.",
    )
    y_axis: YAxis4 = Field(
        ..., alias="yAxis", description="The y axis configuration for the chart."
    )


class Axis1(XAxis):
    pass


class ChartDisplay8(ChartDisplayModel):
    pass


class ChartItem8(BaseModel):
    id: Id
    title: TitleModel
    type: TypeModel
    layer_chart_type: str = Field(
        "FLOW_TOP_DESTS",
        alias="layerChartType",
        const=True,
        description="The tooltip chart type. Must be one of TIME_SERIES, HEXTILE_TIME_SERIES, BREAKDOWN_BY_CATEGORY, FLOW_TOP_ORIGINS, FLOW_TOP_DESTS",
    )
    layer_id: LayerId = Field(..., alias="layerId")
    chart_display: Optional[ChartDisplay8] = Field(
        {}, alias="chartDisplay", description="The display configuration for the chart."
    )
    apply_filters: Optional[ApplyFiltersModel] = Field(None, alias="applyFilters")


class ChartItem9(BaseModel):
    id: Id
    title: TitleModel
    type: TypeModel
    layer_chart_type: str = Field(
        "FLOW_TOP_ORIGINS",
        alias="layerChartType",
        const=True,
        description="The tooltip chart type. Must be one of TIME_SERIES, HEXTILE_TIME_SERIES, BREAKDOWN_BY_CATEGORY, FLOW_TOP_ORIGINS, FLOW_TOP_DESTS",
    )
    layer_id: LayerId = Field(..., alias="layerId")
    chart_display: Optional[ChartDisplayModel] = Field(None, alias="chartDisplay")
    apply_filters: Optional[ApplyFiltersModel] = Field(None, alias="applyFilters")


class ColorRangeModel(ColorRange):
    pass


class ChartDisplay2(BaseModel):
    color_range: Optional[ColorRangeModel] = Field(
        default_factory=lambda: ColorRangeModel.parse_obj(
            {
                "name": "Uber Viz Qualitative",
                "type": "qualitative",
                "category": "Uber",
                "colors": [
                    "#12939A",
                    "#DDB27C",
                    "#88572C",
                    "#FF991F",
                    "#F15C17",
                    "#223F9A",
                    "#DA70BF",
                    "#125C77",
                    "#4DC19C",
                    "#776E57",
                ],
            }
        ),
        alias="colorRange",
        description="The color range for the chart.",
    )
    sort: Optional[Sort] = Field(None, description="The sort type for the chart.")
    format_x_axis: Optional[str] = Field(
        None, alias="formatXAxis", description="The format to use for the x axis."
    )
    format_y_axis: Optional[str] = Field(
        None, alias="formatYAxis", description="The format to use for the y axis."
    )
    show_axis_line: Optional[bool] = Field(
        None, alias="showAxisLine", description="Whether to show the axis line."
    )
    show_legend: Optional[bool] = Field(
        None, alias="showLegend", description="Whether to show the legend."
    )


class ChartItem2(BaseModel):
    id: Id
    title: TitleModel
    data_id: Optional[DataId] = Field(..., alias="dataId")
    apply_filters: Optional[ApplyFilters] = Field(None, alias="applyFilters")
    type: str = Field(
        "lineChart",
        const=True,
        description="The type of the chart. Must be one of: bigNumber, horizontalBar, lineChart, barChart, layerChart, heatmapChart",
    )
    x_axis: XAxis1 = Field(
        ..., alias="xAxis", description="The x axis configuration for the chart."
    )
    y_axis: YAxis1 = Field(
        ..., alias="yAxis", description="The y axis configuration for the chart."
    )
    group_by: GroupBy = Field(
        ...,
        alias="groupBy",
        description="The group by axis configuration for the chart.",
    )
    num_groups: Optional[Union[float, str]] = Field(
        20,
        alias="numGroups",
        description="The number of groups to show in the chart. Use ALL to show all groups.",
    )
    group_others: Optional[bool] = Field(
        None,
        alias="groupOthers",
        description="Whether to group the other values into a single line.",
    )
    enable_area: Optional[bool] = Field(
        None,
        alias="enableArea",
        description="Whether to fill the area below the line chart.",
    )
    color_by: Optional[ColorBy1] = Field(
        None, alias="colorBy", description="The color by option for the chart."
    )
    chart_display: Optional[ChartDisplay2] = Field({}, alias="chartDisplay")
    tooltip: Optional[Tooltip] = Field(
        None, description="The tooltip configuration for the chart."
    )


class ChartDisplay3(BaseModel):
    color_range: Optional[ColorRangeModel] = Field(
        default_factory=lambda: ColorRangeModel.parse_obj(
            {
                "name": "Uber Viz Qualitative",
                "type": "qualitative",
                "category": "Uber",
                "colors": [
                    "#12939A",
                    "#DDB27C",
                    "#88572C",
                    "#FF991F",
                    "#F15C17",
                    "#223F9A",
                    "#DA70BF",
                    "#125C77",
                    "#4DC19C",
                    "#776E57",
                ],
            }
        ),
        alias="colorRange",
        description="The color range configuration for the chart.",
    )
    sort: Optional[Sort] = Field(None, description="The sort type for the chart.")
    format_x_axis: Optional[str] = Field(
        None, alias="formatXAxis", description="The format to use for the x axis."
    )
    format_y_axis: Optional[str] = Field(
        None, alias="formatYAxis", description="The format to use for the y axis."
    )
    show_values: Optional[bool] = Field(
        None, alias="showValues", description="Whether to show the values in the chart."
    )
    log_scale_values: Optional[bool] = Field(
        None,
        alias="logScaleValues",
        description="Whether to use a log scale for the values.",
    )
    rotate_x_ticks: Optional[Union[Any, bool]] = Field(
        None, alias="rotateXTicks", description="Whether to rotate the x ticks."
    )
    rotate_y_ticks: Optional[Union[Any, bool]] = Field(
        None, alias="rotateYTicks", description="Whether to rotate the y ticks."
    )
    less_x_ticks: Optional[bool] = Field(
        None, alias="lessXTicks", description="Whether to show less x ticks."
    )
    less_y_ticks: Optional[bool] = Field(
        None, alias="lessYTicks", description="Whether to show less y ticks."
    )
    more_space_x_axis: Optional[float] = Field(
        None,
        alias="moreSpaceXAxis",
        description="The amount of space to add to the x axis.",
    )
    more_space_y_axis: Optional[float] = Field(
        None,
        alias="moreSpaceYAxis",
        description="The amount of space to add to the y axis.",
    )
    sort_group_by: Optional[Sort] = Field(
        None, alias="sortGroupBy", description="The sort type for the group by axis."
    )
    is_horizontal: Optional[bool] = Field(
        None,
        alias="isHorizontal",
        description="Whether to display the chart horizontally.",
    )
    inner_padding: Optional[float] = Field(
        None, alias="innerPadding", description="The inner padding for the chart."
    )
    padding: Optional[float] = Field(None, description="The padding for the chart.")
    show_axis_line: Optional[bool] = Field(
        None, alias="showAxisLine", description="Whether to show the axis line."
    )
    show_legend: Optional[bool] = Field(
        None, alias="showLegend", description="Whether to show the legend."
    )
    x_axis_labels: Optional[List[Union[str, float]]] = Field(
        None,
        alias="xAxisLabels",
        description="Ordering of the labels to use for the x axis",
    )
    group_by_labels: Optional[List[str]] = Field(
        None,
        alias="groupByLabels",
        description='Ordering of the labels to use for "group by".',
    )
    hint: Optional[str] = Field(None, description="Add a hint for the chart.")


class ChartItem3(BaseModel):
    id: Id
    title: TitleModel
    data_id: Optional[DataId] = Field(..., alias="dataId")
    apply_filters: Optional[ApplyFilters] = Field(None, alias="applyFilters")
    type: str = Field(
        "barChart",
        const=True,
        description="The type of the chart. Must be one of: bigNumber, horizontalBar, lineChart, barChart, layerChart, heatmapChart",
    )
    x_axis: XAxis1 = Field(
        ..., alias="xAxis", description="The x axis configuration for the chart."
    )
    y_axis: YAxis1 = Field(
        ..., alias="yAxis", description="The y axis configuration for the chart."
    )
    group_by: Optional[GroupBy] = Field(
        None,
        alias="groupBy",
        description="The group by axis configuration for the chart.",
    )
    num_bins: float = Field(
        ..., alias="numBins", description="The number of bins to show in the chart."
    )
    bin_others: bool = Field(
        ...,
        alias="binOthers",
        description="Whether to bin the other values into a single bar.",
    )
    num_groups: Optional[Union[float, str]] = Field(
        10,
        alias="numGroups",
        description="The number of groups to show in the chart. Use ALL to show all groups.",
    )
    group_others: Optional[bool] = Field(
        None,
        alias="groupOthers",
        description="Whether to group the other values into a single bar.",
    )
    group_mode: str = Field(
        ...,
        alias="groupMode",
        description="The grouping mode for the chart. Must be one of: stacked, grouped",
    )
    color_by: Optional[ColorBy2] = Field(
        None,
        alias="colorBy",
        description="The color by option for the chart. Must be one of: X-Axis,GroupBy,",
    )
    chart_display: Optional[ChartDisplay3] = Field(
        {}, alias="chartDisplay", description="The display configuration for the chart."
    )


class ChartDisplay4(BaseModel):
    color_range: Optional[ColorRangeModel] = Field(
        default_factory=lambda: ColorRangeModel.parse_obj(
            {
                "name": "Uber Viz Qualitative",
                "type": "qualitative",
                "category": "Uber",
                "colors": [
                    "#12939A",
                    "#DDB27C",
                    "#88572C",
                    "#FF991F",
                    "#F15C17",
                    "#223F9A",
                    "#DA70BF",
                    "#125C77",
                    "#4DC19C",
                    "#776E57",
                ],
            }
        ),
        alias="colorRange",
        description="The color range configuration for the chart.",
    )
    show_values: Optional[bool] = Field(
        None, alias="showValues", description="Whether to show the values in the chart."
    )
    show_legend: Optional[bool] = Field(
        None, alias="showLegend", description="Whether to show the legend."
    )
    format: Optional[str] = Field(None, description="The format to use for the chart.")
    border_width: Optional[float] = Field(
        None, alias="borderWidth", description="The border width for the chart."
    )
    force_square: Optional[bool] = Field(
        None,
        alias="forceSquare",
        description="Whether to force the chart to be square.",
    )
    x_outer_padding: Optional[float] = Field(
        None, alias="xOuterPadding", description="The outer padding for the x axis."
    )
    x_inner_padding: Optional[float] = Field(
        None, alias="xInnerPadding", description="The inner padding for the x axis."
    )
    y_outer_padding: Optional[float] = Field(
        None, alias="yOuterPadding", description="The outer padding for the y axis."
    )
    y_inner_padding: Optional[float] = Field(
        None, alias="yInnerPadding", description="The inner padding for the y axis."
    )
    sort_x: Optional[Sort] = Field(
        "alphaAsc", alias="sortX", description="The sort type for the x axis."
    )
    sort_y: Optional[Sort] = Field(
        "alphaAsc", alias="sortY", description="The sort type for the y axis."
    )
    rotate_x_ticks: Optional[bool] = Field(
        None, alias="rotateXTicks", description="Whether to rotate ticks on x axis."
    )
    rotate_y_ticks: Optional[bool] = Field(
        None, alias="rotateYTicks", description="Whether to rotate ticks on y axis."
    )


class ChartItem4(BaseModel):
    id: Id
    title: TitleModel
    data_id: Optional[DataId] = Field(..., alias="dataId")
    apply_filters: Optional[ApplyFilters] = Field(None, alias="applyFilters")
    type: str = Field(
        "heatmapChart",
        const=True,
        description="The type of the chart. Must be one of: bigNumber, horizontalBar, lineChart, barChart, layerChart, heatmapChart",
    )
    x_axis: XAxis1 = Field(
        ..., alias="xAxis", description="The x axis configuration for the chart."
    )
    y_axis: YAxis3 = Field(
        ..., alias="yAxis", description="The y axis configuration for the chart."
    )
    value: Value = Field(..., description="The value axis configuration for the chart.")
    color_by: Optional[ColorBy3] = Field(
        None, alias="colorBy", description="The color by option for the chart."
    )
    num_of_col: Optional[float] = Field(
        None,
        alias="numOfCol",
        description="The maximum number of columns to show in the chart.",
    )
    num_of_row: Optional[float] = Field(
        None,
        alias="numOfRow",
        description="The maximum number of rows to show in the chart.",
    )
    chart_display: Optional[ChartDisplay4] = Field({}, alias="chartDisplay")


class ChartDisplay7(BaseModel):
    show_in_tooltip: Optional[ShowInTooltip] = Field(None, alias="showInTooltip")
    id_field: Optional[IdField] = Field(None, alias="idField")
    format: Optional[Format] = None
    color_range: Optional[ColorRangeModel] = Field(
        default_factory=lambda: ColorRangeModel.parse_obj(
            {
                "name": "Uber Viz Qualitative",
                "type": "qualitative",
                "category": "Uber",
                "colors": [
                    "#12939A",
                    "#DDB27C",
                    "#88572C",
                    "#FF991F",
                    "#F15C17",
                    "#223F9A",
                    "#DA70BF",
                    "#125C77",
                    "#4DC19C",
                    "#776E57",
                ],
            }
        ),
        alias="colorRange",
        description="The color range configuration for the chart.",
    )
    num_entries: Optional[Union[float, str]] = Field(
        None,
        alias="numEntries",
        description="The number of entries to show in the chart.",
    )
    sort_by: Optional[SortBy] = Field(
        None, alias="sortBy", description="The sort by configuration for the chart."
    )
    sort_order_reverse: Optional[bool] = Field(
        None, alias="sortOrderReverse", description="Whether to reverse the sort order."
    )


class ChartItem7(BaseModel):
    id: Id
    title: TitleModel
    type: TypeModel
    layer_chart_type: str = Field(
        "BREAKDOWN_BY_CATEGORY",
        alias="layerChartType",
        const=True,
        description="The tooltip chart type. Must be one of TIME_SERIES, HEXTILE_TIME_SERIES, BREAKDOWN_BY_CATEGORY, FLOW_TOP_ORIGINS, FLOW_TOP_DESTS",
    )
    layer_id: LayerId = Field(..., alias="layerId")
    chart_display: Optional[ChartDisplay7] = Field(
        {}, alias="chartDisplay", description="The display configuration for the chart."
    )
    apply_filters: Optional[ApplyFiltersModel] = Field(None, alias="applyFilters")
    axis: Optional[Axis1] = Field(
        None, description="The axis configuration for the chart."
    )
    color_by: Optional[ColorBy4] = Field(None, alias="colorBy")


class Chart(BaseModel):
    __root__: Union[
        Union[ChartItem, ChartItem1, ChartItem2, ChartItem3, ChartItem4],
        Union[ChartItem5, ChartItem6, ChartItem7, ChartItem8, ChartItem9],
    ] = Field(..., title="Chart")
