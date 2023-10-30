from __future__ import annotations

import sys
import types
import typing
import warnings
from typing import TYPE_CHECKING, Any, Dict, FrozenSet, List, Optional, Set, Tuple, Type, TypeVar, Union, cast

from typing_extensions import Annotated, get_args, get_origin

from chalk.utils.cached_type_hints import cached_get_type_hints

if TYPE_CHECKING:
    from google.protobuf.message import Message as ProtobufMessage

    from chalk import Document, Windowed
    from chalk.features import DataFrame, Feature, Features, FeatureSetBase, FeatureWrapper, Vector
    from chalk.streams import Windowed


T = TypeVar("T")
U = TypeVar("U")
JsonValue = TypeVar("JsonValue")


class ParsedAnnotation:
    def __init__(
        self,
        features_cls: Optional[Type[Features]] = None,
        attribute_name: Optional[str] = None,
        *,
        underlying: Optional[Union[type, Annotated, Windowed]] = None,
    ) -> None:
        # Either pass in the underlying -- if it is already parsed -- or pass in the feature cls and attribute name
        self._features_cls = features_cls
        self._attribute_name = attribute_name
        self._is_nullable = False
        self._is_scalar = False
        self._is_feature_time = False
        self._is_primary = False
        self._is_document = False
        self._underlying: Optional[Union[type, Feature]] = None
        self._parsed_annotation: Optional[Union[Type, FeatureWrapper]] = None
        self._collection_type: Optional[Type] = None
        if underlying is not None:
            if features_cls is not None and attribute_name is not None:
                raise ValueError("If specifying the underlying, do not specify (features_cls, attribute_name)")
            self._parse_type(underlying)
        elif features_cls is None or attribute_name is None:
            raise ValueError(
                "If not specifying the underlying, then both the (features_cls, attribute_name) must be provided"
            )
        # Store the class and attribute name to later use typing.get_type_hints to
        # resolve any forward references in the type annotations
        # Resolution happens lazily -- after everything is imported -- to avoid circular imports

    @property
    def parsed_annotation(self) -> Union[Type, FeatureWrapper]:
        """The parsed type annotation. It will be parsed if needed.

        Unlike `.underlying`, parsed annotation contains any container or optional types, such as
        list, dataframe, or Optional.
        """
        if self._parsed_annotation is None:
            self._parse_annotation()
        assert self._parsed_annotation is not None
        return self._parsed_annotation

    def __str__(self):
        annotation = self._parsed_annotation
        if annotation is None:
            assert self._features_cls is not None
            assert self._attribute_name is not None
            annotation = self._features_cls.__annotations__[self._attribute_name]
        if isinstance(annotation, type):
            return annotation.__name__
        return str(annotation)

    def _get_globals_for_forward_references(self) -> Optional[Dict[str, Any]]:
        """
        If we're loading pickles from a notebook onto the branch server, we need special handling for forward references.
        By default, get_type_hints() looks at the feature class's module to find the references, but if a class was defined in a notebook that module doesn't exist.
        Instead, create a dummy namespace with Optional & DataFrame (commonly used in forward references for has-ones/has-manys) as well as any other feature class
         that was defined in a notebook.
        """
        # Probably redundant, just to be safe
        if self._features_cls.__module__ != "__main__":
            return None
        if not getattr(self._features_cls, "__chalk_is_loaded_from_notebook__", False):
            return None

        import typing

        import chalk
        from chalk.features import FeatureSetBase

        notebook_feature_classes = {}
        for feature_set in FeatureSetBase.registry.values():
            if not feature_set.__chalk_is_loaded_from_notebook__:
                continue
            notebook_feature_classes[feature_set.__name__] = feature_set

        return {
            # Support "typing.Optional[...]", "Optional[...]", etc."
            "typing": typing,
            **typing.__dict__,
            # Support "chalk.DataFrame[...]", "DataFrame[...]"
            "chalk": chalk,
            **chalk.__dict__,
            # Support forward references for cyclic has-one/has-many's
            **notebook_feature_classes,
        }

    def _parse_annotation(self):
        assert self._attribute_name is not None

        if self._features_cls.__chalk_is_loaded_from_notebook__:
            print("PARSED_ANNOTATIONS")
            print(self._features_cls.__module__)
            print("GLOBALS", getattr(sys.modules.get(self._features_cls.__module__, None), "__dict__", {}))
            print("LOCALS", dict(vars(self._features_cls)).keys())

        globalns = self._get_globals_for_forward_references()
        hints = cached_get_type_hints(self._features_cls, include_extras=True, globalns=globalns)
        parsed_annotation = hints[self._attribute_name]
        self._parse_type(parsed_annotation)

    def _parse_type(self, annotation: Union[type, Windowed, Annotated]):
        from chalk.features import DataFrame, Feature, Features, FeatureWrapper, unwrap_feature
        from chalk.streams import Windowed

        assert self._parsed_annotation is None, "The annotation was already parsed"
        if isinstance(annotation, Windowed):
            # If it's windowed, then unwrap it immediately, because Windowed annotations are really just a proxy to the underlying type
            annotation = annotation.kind
        self._parsed_annotation = annotation
        self._is_nullable = False
        self._is_primary = False
        self._is_feature_time = False
        if self._features_cls is not None and self._attribute_name is not None:
            # Return a more helpful error message, since we have context
            error_ctx = f" {self._features_cls.__name__}.{self._attribute_name}"
        else:
            error_ctx = ""
        origin = get_origin(annotation)

        if origin in (
            Union,
            getattr(types, "UnionType", Union),
        ):  # using getattr as UnionType was introduced in python 3.10
            args = get_args(annotation)
            # If it's a union, then the only supported union is for nullable features. Validate this
            if len(args) != 2 or (None not in args and type(None) not in args):
                raise TypeError(
                    f"Invalid annotation for feature{error_ctx}: Unions with non-None types are not allowed"
                )
            annotation = args[0] if args[1] in (None, type(None)) else args[1]
            origin = get_origin(annotation)
            self._is_nullable = True

        if origin in (Annotated, getattr(typing, "Annotated", Annotated)):
            args = get_args(annotation)
            annotation = args[0]
            if "__chalk_ts__" in args:
                self._is_feature_time = True
            if "__chalk_primary__" in args:
                self._is_primary = True
            if "__chalk_document__" in args:
                self._is_document = True
            origin = get_origin(annotation)

        # The only allowed collections here are Set, List, or DataFrame
        if origin in (set, Set):
            args = get_args(annotation)
            assert len(args) == 1, "typing.Set takes just one arg"
            annotation = args[0]
            self._collection_type = Set[cast(Type, annotation)]
        if origin in (frozenset, FrozenSet):
            args = get_args(annotation)
            assert len(args) == 1, "typing.FrozenSet takes just one arg"
            annotation = args[0]
            self._collection_type = FrozenSet[cast(Type, annotation)]
        if origin in (tuple, Tuple):
            args = get_args(annotation)
            assert len(args) == 2 and args[1] is ..., "typing.Tuple is only supported if it is homogenous"
            annotation = args[0]
            self._collection_type = Tuple[cast(Type, annotation)]
        if origin in (list, List):
            args = get_args(annotation)
            assert len(args) == 1, "typing.List takes just one arg"
            annotation = args[0]
            self._collection_type = List[cast(Type, annotation)]

        if isinstance(annotation, FeatureWrapper):
            # We never want FeatureWrappers; if this is the case, then unwrap it to the underlying feature
            annotation = unwrap_feature(annotation)

        self._is_scalar = isinstance(annotation, type) and not issubclass(annotation, (Features, DataFrame))

        if self._collection_type is not None and not self._is_scalar:
            raise TypeError(
                (
                    f"Invalid type annotation for feature {error_ctx}: "
                    f"{str(self._collection_type)} must be of scalar types, "
                    f"not {self._parsed_annotation}"
                )
            )
        assert isinstance(annotation, (type, Feature)), f"Type annotation {annotation} is unsupported"

        self._underlying = annotation

    def as_proto(self) -> Optional[Type[ProtobufMessage]]:
        from google.protobuf.message import Message as ProtobufMessage

        if self._parsed_annotation is None:
            self._parse_annotation()
        if not (isinstance(self._underlying, type) and issubclass(self._underlying, ProtobufMessage)):
            return None
        return self._underlying

    def as_document(self) -> Optional[Type[Document]]:
        if self._parsed_annotation is None:
            self._parse_annotation()
        if not self._is_document:
            return None
        return cast("Type[Document]", self._underlying)

    @property
    def is_nullable(self) -> bool:
        """Whether the type annotation is nullable."""
        if self._parsed_annotation is None:
            self._parse_annotation()
        assert self._is_nullable is not None
        return self._is_nullable

    @property
    def underlying(self) -> Union[Type, Windowed]:
        """The underlying type annotation from the annotation."""
        warnings.warn(
            DeprecationWarning(
                (
                    "`feature.typ.underlying` is deprecated. For scalar features, use `feature.converter.rich_type`. "
                    "For has-one features, use `feature.joined_class`."
                )
            )
        )
        if self._parsed_annotation is None:
            self._parse_annotation()
        if self._underlying is None:
            raise TypeError("There is no underlying type")
        return self._underlying

    def as_features_cls(self) -> Optional[Type[Features]]:
        from chalk.features import Features

        if self._parsed_annotation is None:
            self._parse_annotation()
        assert self._underlying is not None
        if not (isinstance(self._underlying, type) and issubclass(self._underlying, Features)):
            return None
        return self._underlying

    def as_dataframe(self) -> Optional[Type[DataFrame]]:
        from chalk.features import DataFrame

        if self._parsed_annotation is None:
            self._parse_annotation()
        if not (isinstance(self._underlying, type) and issubclass(self._underlying, DataFrame)):
            return None
        return self._underlying

    def as_vector(self) -> Optional[Type[Vector]]:
        from chalk.features._vector import Vector

        if self._parsed_annotation is None:
            self._parse_annotation()

        if not (isinstance(self._underlying, type) and issubclass(self._underlying, Vector)):
            return None
        return self._underlying

    def as_feature(self) -> Optional[Feature]:
        from chalk.features import Feature

        if not isinstance(self._underlying, Feature):
            return None
        return self._underlying

    @property
    def collection_type(self) -> Optional[type]:
        warnings.warn(
            DeprecationWarning(
                (
                    "`feature.typ.collection_type` is deprecated. "
                    "Instead, convert to rich types via `feature.converter.from_XXX_to_rich` is a list"
                )
            )
        )
        if self._parsed_annotation is None:
            self._parse_annotation()
        return self._collection_type

    @property
    def is_scalar(self) -> bool:
        """Whether the type annotation is a scalar type (i.e. not a Features type)."""
        warnings.warn(
            DeprecationWarning(
                (
                    "`feature.typ.is_scalar` is deprecated. "
                    "Instead, convert to rich types via `feature.converter.from_XXX_to_rich`"
                )
            )
        )
        if self._parsed_annotation is None:
            self._parse_annotation()
        return self._is_scalar

    def is_primary(self) -> bool:
        if self._parsed_annotation is None:
            self._parse_annotation()
        return self._is_primary

    def is_feature_time(self) -> bool:
        if self._parsed_annotation is None:
            self._parse_annotation()
        return self._is_feature_time
