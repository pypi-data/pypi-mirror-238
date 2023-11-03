from datetime import datetime
from typing import Annotated, Literal, Optional, Union

from pydantic import Field

from validio_sdk.scalars import JsonPointer, SourceId, WindowId

from .base_model import BaseModel
from .enums import WindowTimeUnit


class GetWindowByResourceName(BaseModel):
    window_by_resource_name: Optional[
        Annotated[
            Union[
                "GetWindowByResourceNameWindowByResourceNameWindow",
                "GetWindowByResourceNameWindowByResourceNameFileWindow",
                "GetWindowByResourceNameWindowByResourceNameFixedBatchWindow",
                "GetWindowByResourceNameWindowByResourceNameTumblingWindow",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="windowByResourceName")


class GetWindowByResourceNameWindowByResourceNameWindow(BaseModel):
    typename__: Literal["GlobalWindow", "Window"] = Field(alias="__typename")
    id: WindowId
    name: str
    source: "GetWindowByResourceNameWindowByResourceNameWindowSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetWindowByResourceNameWindowByResourceNameWindowSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetWindowByResourceNameWindowByResourceNameFileWindow(BaseModel):
    typename__: Literal["FileWindow"] = Field(alias="__typename")
    id: WindowId
    name: str
    source: "GetWindowByResourceNameWindowByResourceNameFileWindowSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    data_time_field: JsonPointer = Field(alias="dataTimeField")


class GetWindowByResourceNameWindowByResourceNameFileWindowSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetWindowByResourceNameWindowByResourceNameFixedBatchWindow(BaseModel):
    typename__: Literal["FixedBatchWindow"] = Field(alias="__typename")
    id: WindowId
    name: str
    source: "GetWindowByResourceNameWindowByResourceNameFixedBatchWindowSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetWindowByResourceNameWindowByResourceNameFixedBatchWindowConfig"
    data_time_field: JsonPointer = Field(alias="dataTimeField")


class GetWindowByResourceNameWindowByResourceNameFixedBatchWindowSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetWindowByResourceNameWindowByResourceNameFixedBatchWindowConfig(BaseModel):
    batch_size: int = Field(alias="batchSize")
    segmented_batching: bool = Field(alias="segmentedBatching")
    batch_timeout_secs: Optional[int] = Field(alias="batchTimeoutSecs")


class GetWindowByResourceNameWindowByResourceNameTumblingWindow(BaseModel):
    typename__: Literal["TumblingWindow"] = Field(alias="__typename")
    id: WindowId
    name: str
    source: "GetWindowByResourceNameWindowByResourceNameTumblingWindowSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetWindowByResourceNameWindowByResourceNameTumblingWindowConfig"
    data_time_field: JsonPointer = Field(alias="dataTimeField")


class GetWindowByResourceNameWindowByResourceNameTumblingWindowSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetWindowByResourceNameWindowByResourceNameTumblingWindowConfig(BaseModel):
    window_size: int = Field(alias="windowSize")
    time_unit: WindowTimeUnit = Field(alias="timeUnit")


GetWindowByResourceName.update_forward_refs()
GetWindowByResourceNameWindowByResourceNameWindow.update_forward_refs()
GetWindowByResourceNameWindowByResourceNameWindowSource.update_forward_refs()
GetWindowByResourceNameWindowByResourceNameFileWindow.update_forward_refs()
GetWindowByResourceNameWindowByResourceNameFileWindowSource.update_forward_refs()
GetWindowByResourceNameWindowByResourceNameFixedBatchWindow.update_forward_refs()
GetWindowByResourceNameWindowByResourceNameFixedBatchWindowSource.update_forward_refs()
GetWindowByResourceNameWindowByResourceNameFixedBatchWindowConfig.update_forward_refs()
GetWindowByResourceNameWindowByResourceNameTumblingWindow.update_forward_refs()
GetWindowByResourceNameWindowByResourceNameTumblingWindowSource.update_forward_refs()
GetWindowByResourceNameWindowByResourceNameTumblingWindowConfig.update_forward_refs()
