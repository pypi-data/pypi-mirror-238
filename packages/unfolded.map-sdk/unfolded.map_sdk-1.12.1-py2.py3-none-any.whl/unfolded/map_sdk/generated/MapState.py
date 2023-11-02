# type: ignore

from __future__ import annotations

from typing import List, Optional, Union

import MapStateItem1 as MapStateItem1_1
from pydantic import BaseModel, Field, confloat


class MapStateItem(BaseModel):
    map_view_mode: str = Field("MODE_2D", alias="mapViewMode", const=True)


class MapStateItem1(BaseModel):
    latitude: Latitude
    longitude: Longitude
    zoom: Optional[Zoom] = None
    bearing: Optional[Bearing] = None
    pitch: Pitch
    drag_rotate: Optional[DragRotate] = Field(None, alias="dragRotate")
    map_split_mode: str = Field("SWIPE_COMPARE", alias="mapSplitMode", const=True)
    is_split: bool = Field(True, alias="isSplit", const=True)


class LabelsColorItem(BaseModel):
    __root__: confloat(ge=0.0, le=255.0)


class MapState1(BaseModel):
    pass


class MapState2(MapStateItem, MapState1):
    pass


class MapState3(MapStateItem1, MapState1):
    pass


class MapState6(MapState2):
    pass


class MapState7(MapState3):
    pass


class Bearing(BaseModel):
    __root__: float


class DragRotate(BaseModel):
    __root__: bool


class Latitude(BaseModel):
    __root__: confloat(ge=-90.0, le=90.0)


class Longitude(BaseModel):
    __root__: confloat(ge=-180.0, le=180.0)


class Pitch(BaseModel):
    __root__: confloat(ge=0.0, lt=90.0)


class Zoom(BaseModel):
    __root__: confloat(ge=0.0, le=25.0)


class Field0(LabelsColorItem):
    pass


class MapStateItem2(BaseModel):
    map_view_mode: str = Field("MODE_GLOBE", alias="mapViewMode", const=True)
    globe: Globe


class SplitMapViewport(BaseModel):
    latitude: Latitude
    longitude: Longitude
    zoom: Optional[Zoom] = None
    bearing: Optional[Bearing] = None
    pitch: Pitch
    drag_rotate: Optional[DragRotate] = Field(None, alias="dragRotate")


class MapStateItem3(BaseModel):
    latitude: Latitude
    longitude: Longitude
    zoom: Optional[Zoom] = None
    bearing: Optional[Bearing] = None
    pitch: Pitch
    drag_rotate: Optional[DragRotate] = Field(None, alias="dragRotate")
    map_split_mode: str = Field("DUAL_MAP", alias="mapSplitMode", const=True)
    is_split: bool = Field(True, alias="isSplit", const=True)
    is_viewport_synced: bool = Field(False, alias="isViewportSynced", const=True)
    is_zoom_locked: Optional[bool] = Field(False, alias="isZoomLocked")
    split_map_viewports: List[SplitMapViewport] = Field(..., alias="splitMapViewports")


class MapState4(MapStateItem2, MapState1):
    pass


class MapState5(MapStateItem3, MapState1):
    pass


class MapState8(MapState4):
    pass


class MapState(BaseModel):
    __root__: Union[
        MapState2, MapState3, MapState4, MapState5, MapState6, MapState7, MapState8
    ] = Field(..., title="MapState")


class LabelsColor(BaseModel):
    __root__: Union[List[Union[LabelsColorItem, Field0]], List[Field0]]


class Config(BaseModel):
    atmosphere: bool
    azimuth: bool
    azimuth_angle: float = Field(..., alias="azimuthAngle")
    terminator: bool
    terminator_opacity: confloat(ge=0.0, le=1.0) = Field(..., alias="terminatorOpacity")
    basemap: bool
    labels: Optional[bool] = False
    labels_color: Optional[
        Union[List[Union[LabelsColorItem, Field0]], List[Field0]]
    ] = Field([114.75, 114.75, 114.75], alias="labelsColor")
    admin_lines: Optional[bool] = Field(True, alias="adminLines")
    admin_lines_color: Optional[LabelsColor] = Field(
        default_factory=lambda: LabelsColor.parse_obj([40, 63, 93]),
        alias="adminLinesColor",
    )
    water: Optional[bool] = True
    water_color: Optional[LabelsColor] = Field(
        default_factory=lambda: LabelsColor.parse_obj([17, 35, 48]), alias="waterColor"
    )
    surface: Optional[bool] = True
    surface_color: Optional[LabelsColor] = Field(
        default_factory=lambda: LabelsColor.parse_obj([9, 16, 29]), alias="surfaceColor"
    )


class Globe(BaseModel):
    enabled: bool
    config: Config
