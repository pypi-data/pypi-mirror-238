from dataclasses import dataclass

import atoti as tt
from atoti_core import keyword_only_dataclass

from ._client_side_encryption import AwsClientSideEncryption


@keyword_only_dataclass
@dataclass(frozen=True)
class AwsKeyPair(tt.KeyPair, AwsClientSideEncryption, tt.ClientSideEncryptionConfig):
    """Key pair to use for `client side encryption <https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingClientSideEncryption.html>`__.

    Example:
        >>> from atoti_aws import AwsKeyPair
        >>> client_side_encryption_config = (
        ...     AwsKeyPair(
        ...         region="eu-west-3",
        ...         private_key="private_key",
        ...         public_key="public_key",
        ...     ),
        ... )
    """
