# type: ignore

from __future__ import annotations

from typing import List, Optional, Union

from pydantic import BaseModel, Field, confloat


class Parameters(BaseModel):
    brightness: Optional[confloat(ge=-1.0, le=1.0)] = Field(
        0, description="The brightness of the effect"
    )
    contrast: Optional[confloat(ge=-1.0, le=1.0)] = Field(
        0, description="The contrast of the effect"
    )


class EffectItem(BaseModel):
    id: str = Field(..., description="The id of the effect")
    type: str = Field(
        "brightnessContrast", const=True, description="The type of the effect"
    )
    is_enabled: Optional[bool] = Field(
        True, alias="isEnabled", description="Whether the effect is enabled"
    )
    parameters: Parameters


class CenterItem(BaseModel):
    __root__: confloat(ge=0.0, le=1.0)


class Parameters1(BaseModel):
    center: Optional[List[CenterItem]] = Field(
        [0.5, 0.5],
        description="The center point of the effect",
        max_items=2,
        min_items=2,
    )
    angle: Optional[confloat(ge=0.0, le=1.5707963267948966)] = Field(
        1.1, description="The rotation angle of the grid"
    )
    size: Optional[confloat(ge=0.0, le=100.0)] = 4


class DeltaItem(CenterItem):
    pass


class Parameters3(BaseModel):
    radius: Optional[confloat(ge=0.0, le=100.0)] = Field(
        2, description="The radius of the blur"
    )
    delta: Optional[List[DeltaItem]] = Field(
        [1, 0], description="The direction of the blur", max_items=2, min_items=2
    )


class Parameters5(BaseModel):
    hue: Optional[confloat(ge=-1.0, le=1.0)] = Field(
        0, description="The hue of the effect"
    )
    saturation: Optional[confloat(ge=-1.0, le=1.0)] = Field(
        0, description="The saturation of the effect"
    )


class Parameters6(BaseModel):
    strength: Optional[confloat(ge=0.0, le=1.0)] = Field(
        0.5, description="The strength of the effect"
    )


class ShadowColorItem(BaseModel):
    __root__: confloat(ge=0.0, le=255.0)


class ScreenXyItem(CenterItem):
    pass


class Parameters8(BaseModel):
    amount: Optional[confloat(ge=0.0, le=1.0)] = Field(
        0.5, description="The amount of noise to apply."
    )


class Parameters9(BaseModel):
    amount: Optional[confloat(ge=0.0, le=1.0)] = Field(
        0.5, description="The amount of the effect"
    )


class StartItem(CenterItem):
    pass


class EndItem(CenterItem):
    pass


class Parameters10(BaseModel):
    blur_radius: Optional[confloat(ge=0.0, le=50.0)] = Field(
        20, alias="blurRadius", description="The radius of the blur"
    )
    gradient_radius: Optional[confloat(ge=0.0, le=400.0)] = Field(
        20, alias="gradientRadius", description="The radius of the gradient"
    )
    start: Optional[List[StartItem]] = Field(
        [0, 0], description="The start of the gradient", max_items=2, min_items=2
    )
    end: Optional[List[EndItem]] = Field(
        [1, 1], description="The end of the gradient", max_items=2, min_items=2
    )
    invert: Optional[bool] = Field(False, description="Whether to invert the gradient")


class Parameters11(BaseModel):
    radius: Optional[confloat(ge=0.0, le=100.0)] = Field(
        20, description="The radius of the blur"
    )
    delta: Optional[List[DeltaItem]] = Field(
        [1, 0], description="The direction of the blur", max_items=2, min_items=2
    )


class Parameters12(BaseModel):
    amount: Optional[confloat(ge=-1.0, le=1.0)] = Field(
        0, description="The amount of the effect"
    )


class Parameters13(BaseModel):
    radius: Optional[confloat(ge=0.0, le=1.0)] = Field(
        0.5, description="The radius of the vignette"
    )
    amount: Optional[confloat(ge=0.0, le=1.0)] = Field(
        0.5, description="The amount of vignette to apply"
    )


class Id(BaseModel):
    __root__: str = Field(..., description="The id of the effect")


class IsEnabled(BaseModel):
    __root__: bool = Field(..., description="Whether the effect is enabled")


class Center(BaseModel):
    __root__: List[CenterItem] = Field(
        ..., description="The center point of the effect", max_items=2, min_items=2
    )


class AmbientLightIntensity(BaseModel):
    __root__: float = Field(..., description="The intensity of the ambient light")


class Field0Item(ShadowColorItem):
    pass


class Field0(ShadowColorItem):
    pass


class Field1(BaseModel):
    __root__: List[Field0] = Field(..., max_items=4, min_items=4)


class ShadowIntensity(BaseModel):
    __root__: float = Field(..., description="The intensity of the shadow")


class SunLightIntensity(BaseModel):
    __root__: float = Field(..., description="The intensity of the sun light")


class EffectItem1(BaseModel):
    id: Id
    type: str = Field("colorHalftone", const=True, description="The type of the effect")
    is_enabled: Optional[IsEnabled] = Field(None, alias="isEnabled")
    parameters: Parameters1


class Parameters2(BaseModel):
    center: Optional[Center] = None
    angle: Optional[confloat(ge=0.0, le=1.5707963267948966)] = Field(
        1.1, description="The rotation angle of the grid"
    )
    size: Optional[confloat(ge=0.0, le=100.0)] = Field(
        3, description="The size of the dots."
    )


class EffectItem2(BaseModel):
    id: Id
    type: str = Field("dotScreen", const=True, description="The type of the effect")
    is_enabled: Optional[IsEnabled] = Field(None, alias="isEnabled")
    parameters: Parameters2


class EffectItem3(BaseModel):
    id: Id
    type: str = Field("edgeWork", const=True, description="The type of the effect")
    is_enabled: Optional[IsEnabled] = Field(None, alias="isEnabled")
    parameters: Parameters3


class Parameters4(BaseModel):
    center: Optional[Center] = None
    scale: Optional[confloat(ge=0.0, le=50.0)] = Field(
        10, description="The scale (size) of the hexagons"
    )


class EffectItem4(BaseModel):
    id: Id
    type: str = Field(
        "hexagonalPixelate", const=True, description="The type of the effect"
    )
    is_enabled: Optional[IsEnabled] = Field(None, alias="isEnabled")
    parameters: Parameters4


class EffectItem5(BaseModel):
    id: Id
    type: str = Field("hueSaturation", const=True, description="The type of the effect")
    is_enabled: Optional[IsEnabled] = Field(None, alias="isEnabled")
    parameters: Parameters5


class EffectItem6(BaseModel):
    id: Id
    type: str = Field("ink", const=True, description="The type of the effect")
    is_enabled: Optional[IsEnabled] = Field(None, alias="isEnabled")
    parameters: Parameters6


class EffectItem9(BaseModel):
    id: Id
    type: str = Field("noise", const=True, description="The type of the effect")
    is_enabled: Optional[IsEnabled] = Field(None, alias="isEnabled")
    parameters: Parameters8


class EffectItem10(BaseModel):
    id: Id
    type: str = Field("sepia", const=True, description="The type of the effect")
    is_enabled: Optional[IsEnabled] = Field(None, alias="isEnabled")
    parameters: Parameters9


class EffectItem11(BaseModel):
    id: Id
    type: str = Field("tiltShift", const=True, description="The type of the effect")
    is_enabled: Optional[IsEnabled] = Field(None, alias="isEnabled")
    parameters: Parameters10


class EffectItem12(BaseModel):
    id: Id
    type: str = Field("triangleBlur", const=True, description="The type of the effect")
    is_enabled: Optional[IsEnabled] = Field(None, alias="isEnabled")
    parameters: Parameters11


class EffectItem13(BaseModel):
    id: Id
    type: str = Field("vibrance", const=True, description="The type of the effect")
    is_enabled: Optional[IsEnabled] = Field(None, alias="isEnabled")
    parameters: Parameters12


class EffectItem14(BaseModel):
    id: Id
    type: str = Field("vignette", const=True, description="The type of the effect")
    is_enabled: Optional[IsEnabled] = Field(None, alias="isEnabled")
    parameters: Parameters13


class Parameters14(BaseModel):
    center: Optional[Center] = None
    strength: Optional[confloat(ge=0.0, le=1.0)] = Field(
        0.5, description="The strength of the effect"
    )


class EffectItem15(BaseModel):
    id: Id
    type: str = Field("zoomBlur", const=True, description="The type of the effect")
    is_enabled: Optional[IsEnabled] = Field(None, alias="isEnabled")
    parameters: Parameters14


class ShadowColor(BaseModel):
    __root__: Union[List[Union[ShadowColorItem, Field0]], List[Field0]] = Field(
        ..., description="The color of the shadow"
    )


class Field0Model(BaseModel):
    __root__: List[Union[Field0Item, Field0]] = Field(..., max_items=3, min_items=3)


class SunLightColor(BaseModel):
    __root__: Union[Field0Model, Field1] = Field(
        ..., description="The color of the sun light"
    )


class Parameter(BaseModel):
    shadow_intensity: float = Field(
        ..., alias="shadowIntensity", description="The intensity of the shadow"
    )
    shadow_color: Union[List[Union[ShadowColorItem, Field0]], List[Field0]] = Field(
        ..., alias="shadowColor", description="The color of the shadow"
    )
    sun_light_color: Union[Field0Model, Field1] = Field(
        ..., alias="sunLightColor", description="The color of the sun light"
    )
    sun_light_intensity: float = Field(
        ..., alias="sunLightIntensity", description="The intensity of the sun light"
    )
    ambient_light_color: Union[Field0Model, Field1] = Field(
        ..., alias="ambientLightColor", description="The color of the ambient light"
    )
    ambient_light_intensity: float = Field(
        ...,
        alias="ambientLightIntensity",
        description="The intensity of the ambient light",
    )
    time_mode: str = Field("pick", alias="timeMode", const=True)
    timestamp: float = Field(
        ..., description="The timestamp to use for the sun position"
    )
    timezone: Optional[str] = Field("UTC", description="The time zone to use")


class Parameters7(BaseModel):
    screen_xy: Optional[List[ScreenXyItem]] = Field(
        [0.5, 0.5],
        alias="screenXY",
        description="The screen position of the magnifier",
        max_items=2,
        min_items=2,
    )
    radius_pixels: Optional[confloat(ge=0.0, le=500.0)] = Field(
        200, alias="radiusPixels", description="The radius of the magnify effect"
    )
    zoom: Optional[confloat(ge=0.0, le=500.0)] = Field(
        2, description="The zoom level of the magnify effect"
    )
    border_width_pixels: Optional[confloat(ge=0.0)] = Field(
        0, alias="borderWidthPixels", description="The width of the border"
    )
    border_color: Optional[Union[Field0Model, Field1]] = Field(
        [255, 255, 255, 255], alias="borderColor", description="The color of the border"
    )


class EffectItem8(BaseModel):
    id: Id
    type: str = Field("magnify", const=True, description="The type of the effect")
    is_enabled: Optional[IsEnabled] = Field(None, alias="isEnabled")
    parameters: Parameters7


class AmbientLightColor(BaseModel):
    __root__: Union[Field0Model, Field1] = Field(
        ..., description="The color of the ambient light"
    )


class Parameter1(BaseModel):
    shadow_intensity: ShadowIntensity = Field(..., alias="shadowIntensity")
    shadow_color: ShadowColor = Field(..., alias="shadowColor")
    sun_light_color: SunLightColor = Field(..., alias="sunLightColor")
    sun_light_intensity: SunLightIntensity = Field(..., alias="sunLightIntensity")
    ambient_light_color: AmbientLightColor = Field(..., alias="ambientLightColor")
    ambient_light_intensity: AmbientLightIntensity = Field(
        ..., alias="ambientLightIntensity"
    )
    time_mode: str = Field("current", alias="timeMode", const=True)


class Parameter2(BaseModel):
    shadow_intensity: ShadowIntensity = Field(..., alias="shadowIntensity")
    shadow_color: ShadowColor = Field(..., alias="shadowColor")
    sun_light_color: SunLightColor = Field(..., alias="sunLightColor")
    sun_light_intensity: SunLightIntensity = Field(..., alias="sunLightIntensity")
    ambient_light_color: AmbientLightColor = Field(..., alias="ambientLightColor")
    ambient_light_intensity: AmbientLightIntensity = Field(
        ..., alias="ambientLightIntensity"
    )
    time_mode: str = Field("animation", alias="timeMode", const=True)


class EffectItem7(BaseModel):
    id: Id
    type: str = Field(
        "lightAndShadow", const=True, description="The type of the effect"
    )
    is_enabled: Optional[IsEnabled] = Field(None, alias="isEnabled")
    parameters: Union[Parameter, Parameter1, Parameter2]


class Effect(BaseModel):
    __root__: Union[
        EffectItem,
        EffectItem1,
        EffectItem2,
        EffectItem3,
        EffectItem4,
        EffectItem5,
        EffectItem6,
        EffectItem7,
        EffectItem8,
        EffectItem9,
        EffectItem10,
        EffectItem11,
        EffectItem12,
        EffectItem13,
        EffectItem14,
        EffectItem15,
    ] = Field(..., title="Effect")
