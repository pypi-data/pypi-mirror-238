from dataclasses import dataclass

from atoti_core import keyword_only_dataclass


@keyword_only_dataclass
@dataclass(frozen=True)
class AwsClientSideEncryption:
    region: str
    """The AWS region to interact with."""
