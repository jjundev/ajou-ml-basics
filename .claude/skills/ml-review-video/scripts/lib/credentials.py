"""Install a local credential file without overwriting another configuration."""
import os
from pathlib import Path


class CredentialError(ValueError):
    pass


def copy_env_file(source: Path, destination: Path) -> str:
    source, destination = Path(source), Path(destination)
    if source.is_symlink() or not source.is_file():
        raise CredentialError('source must be an existing regular file')
    if destination.is_symlink():
        raise CredentialError('destination symlink is not allowed')
    try:
        data = source.read_bytes()
        if destination.exists():
            if not destination.is_file() or destination.read_bytes() != data:
                raise CredentialError('destination conflict; existing file preserved')
            destination.chmod(0o600)
            return 'reused'
        fd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        try:
            with os.fdopen(fd, 'wb') as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            destination.chmod(0o600)
        except BaseException:
            destination.unlink(missing_ok=True)
            raise
        return 'copied'
    except OSError:
        raise CredentialError('credential file installation failed') from None
