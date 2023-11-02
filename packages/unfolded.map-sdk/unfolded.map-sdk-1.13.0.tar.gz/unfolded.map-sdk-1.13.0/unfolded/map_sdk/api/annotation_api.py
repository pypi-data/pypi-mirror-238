import sys
from typing import Any, List, Optional, Tuple, Union

from pydantic import StrictBool, StrictStr

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

from unfolded.map_sdk.api.base import Action, CamelCaseBaseModel
from unfolded.map_sdk.api.enums import ActionType
from unfolded.map_sdk.transport.base import (
    BaseInteractiveTransport,
    BaseNonInteractiveTransport,
    BaseTransport,
)
from unfolded.map_sdk.utils.validators import validate_kwargs


class Annotation(CamelCaseBaseModel):
    id: StrictStr
    kind: Literal["TEXT", "ARROW", "POINT", "CIRCLE"]
    is_visible: StrictBool
    auto_size: Optional[StrictBool]
    auto_size_y: Optional[StrictBool]
    anchor_point: Tuple[float, float]
    label: StrictStr
    editor_state: Optional[Any]
    map_index: Optional[int]
    line_color: StrictStr
    line_width: float
    text_width: float
    text_height: float
    text_vertical_align: Literal["top", "middle", "bottom"]
    arm_length: Optional[float]
    angle: Optional[float]
    radius_in_meters: Optional[float]


###########
# ACTIONS #
###########


class GetAnnotationsAction(Action):
    type: ActionType = ActionType.GET_ANNOTATIONS


class GetAnnotationByIdAction(Action):
    class Meta(Action.Meta):
        args = ["annotation_id"]

    type: ActionType = ActionType.GET_ANNOTATION_BY_ID
    annotation_id: StrictStr


class AddAnnotationAction(Action):
    class Meta(Action.Meta):
        args = ["annotation"]

    type: ActionType = ActionType.ADD_ANNOTATION
    annotation: Annotation


class UpdateAnnotationAction(Action):
    class Meta(Action.Meta):
        args = ["annotation_id", "values"]

    type: ActionType = ActionType.UPDATE_ANNOTATION
    annotation_id: StrictStr
    values: Annotation


class RemoveAnnotationAction(Action):
    class Meta(Action.Meta):
        args = ["annotation_id"]

    type: ActionType = ActionType.REMOVE_ANNOTATION
    annotation_id: StrictStr


###########
# METHODS #
###########


class BaseAnnotationApiMethods:
    transport: BaseTransport

    @validate_kwargs(positional_only=["annotation"])
    def add_annotation(
        self, annotation: Union[Annotation, dict, None] = None, **kwargs: Any
    ) -> Optional[Annotation]:
        """Adds a new annotation to the map.

        Args:
            annotation (Union[Annotation, dict, None], optional): The annotation to add. Defaults to None.

        Returns (widget map only):
            Annotation: The annotation that was added.
        """
        action = AddAnnotationAction(
            annotation=annotation if annotation is not None else kwargs
        )
        return self.transport.send_action_non_null(
            action=action, response_class=Annotation
        )

    @validate_kwargs(positional_only=["annotation_id", "values"])
    def update_annotation(
        self,
        annotation_id: str,
        values: Union[Annotation, dict, None] = None,
        **kwargs: Any
    ) -> Optional[Annotation]:
        """Updates an existing annotation with given values.

        Args:
            annotation_id (str): The id of the annotation to update.
            values (Union[Annotation, dict, None]): The values to update.

        Returns (widget map only)
            Annotation: The updated annotation.
        """
        action = UpdateAnnotationAction(
            annotation_id=annotation_id, values=values if values is not None else kwargs
        )
        return self.transport.send_action_non_null(
            action=action, response_class=Annotation
        )

    @validate_kwargs(positional_only=["annotation_id"])
    def remove_annotation(self, annotation_id: str) -> None:
        """Removes an annotation from the map.

        Args:
            annotation_id (str): The id of the annotation to remove

        Returns:
            None
        """
        action = RemoveAnnotationAction(annotation_id=annotation_id)
        self.transport.send_action(action=action, response_class=None)


class BaseInteractiveAnnotationApiMethods:
    transport: BaseInteractiveTransport

    def get_annotations(self) -> List[Annotation]:
        """Gets all the annotations currently available in the map.

        Returns:
            List[Annotation]: An array of annotations.
        """
        action = GetAnnotationsAction()
        return self.transport.send_action_non_null(
            action=action, response_class=List[Annotation]
        )

    @validate_kwargs(positional_only=["annotation_id"])
    def get_annotation_by_id(self, annotation_id: str) -> Optional[Annotation]:
        """Retrieves an annotation by its identifier if it exists.

        Args:
            annotation_id (str): Identifier of the annotation to get.

        Returns:
            Optional[Annotation]: Annotation with a given identifier, or null if one doesn't exist.
        """
        action = GetAnnotationByIdAction(annotation_id=annotation_id)
        return self.transport.send_action(action=action, response_class=Annotation)


class AnnotationApiNonInteractiveMixin(BaseAnnotationApiMethods):
    """Annotation methods that are supported in non-interactive (i.e. pure HTML) maps"""

    transport: BaseNonInteractiveTransport

    @validate_kwargs(positional_only=["annotation"])
    def add_annotation(
        self, annotation: Union[Annotation, dict, None] = None, **kwargs: Any
    ) -> None:
        super().add_annotation(annotation, **kwargs)
        return

    @validate_kwargs(positional_only=["annotation_id", "values"])
    def update_annotation(
        self,
        annotation_id: str,
        values: Union[Annotation, dict, None] = None,
        **kwargs: Any
    ) -> None:
        super().update_annotation(annotation_id, values, **kwargs)
        return

    @validate_kwargs(positional_only=["annotation_id"])
    def remove_annotation(self, annotation_id: str, **kwargs: Any) -> None:
        super().remove_annotation(annotation_id, **kwargs)
        return


class AnnotationApiInteractiveMixin(
    BaseAnnotationApiMethods, BaseInteractiveAnnotationApiMethods
):
    """Annotation methods that are supported in interactive (i.e. widget) maps"""

    transport: BaseInteractiveTransport

    @validate_kwargs(positional_only=["annotation"])
    def add_annotation(
        self, annotation: Union[Annotation, dict, None] = None, **kwargs: Any
    ) -> Annotation:
        return super().add_annotation(annotation, **kwargs)

    @validate_kwargs(positional_only=["annotation_id", "values"])
    def update_annotation(
        self,
        annotation_id: str,
        values: Union[Annotation, dict, None] = None,
        **kwargs: Any
    ) -> Annotation:
        return super().update_annotation(annotation_id, values, **kwargs)

    @validate_kwargs(positional_only=["annotation_id"])
    def remove_annotation(self, annotation_id: str, **kwargs) -> None:
        return super().remove_annotation(annotation_id, **kwargs)

    def get_annotations(self, **kwargs: Any) -> List[Annotation]:
        return super().get_annotations(**kwargs)

    @validate_kwargs(positional_only=["annotation_id"])
    def get_annotation_by_id(
        self, annotation_id: str, **kwargs: Any
    ) -> Optional[Annotation]:
        return super().get_annotation_by_id(annotation_id, **kwargs)
