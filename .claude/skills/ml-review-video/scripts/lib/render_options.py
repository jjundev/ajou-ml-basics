"""Read-only render policy, deliberately independent of voice configuration."""
from pathlib import Path
import subprocess
import sys
import json

InputError = ValueError

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def detect_hardware() -> dict[str, object]:
    hardware = dict(platform=sys.platform, chip=None, cpu_cores=None, memory_bytes=None)
    if sys.platform == 'darwin':
        for key, field, convert in [('chip', 'machdep.cpu.brand_string', str),
                                    ('cpu_cores', 'hw.physicalcpu', int),
                                    ('memory_bytes', 'hw.memsize', int)]:
            try:
                result = subprocess.run(['/usr/sbin/sysctl', '-n', field], capture_output=True,
                                        text=True, timeout=2, check=True)
                hardware[key] = convert(result.stdout.strip())
            except (OSError, subprocess.SubprocessError, ValueError):
                pass
    return hardware


def worker_capacity(hardware: dict[str, object] | None = None) -> int:
    host = detect_hardware() if hardware is None else hardware
    verified = (host.get('platform') == 'darwin' and host.get('chip') == 'Apple M5'
                and type(host.get('cpu_cores')) is int and host['cpu_cores'] == 10
                and type(host.get('memory_bytes')) is int and host['memory_bytes'] >= 16 * 1024**3)
    return 6 if verified else 2


def default_render_options(hardware: dict[str, object] | None = None) -> dict[str, object]:
    return dict(schema_version=2,workers='auto',encoder='cpu',browser_gpu='auto',fast_capture=False)


def resolve_scene_workers(run,part,options,*,hardware=None):
    from .workload import scene_motion_profile
    options=validate_render_options(options)
    if options['workers']!='auto':
        return dict(mode='fixed',workers=options['workers'],reason='explicit_setting')
    profile=scene_motion_profile(run,part)
    capacity=worker_capacity(hardware)
    if capacity<6:workers,reason=2,'unverified_hardware'
    elif profile['status']=='unknown':workers,reason=2,'missing_motion_metadata'
    elif profile['scene_frames']<900:workers,reason=2,'short_scene'
    elif profile['motion_ratio']>.5:workers,reason=6,'motion_majority'
    else:workers,reason=2,'static_majority'
    return dict(mode='auto',workers=workers,reason=reason,policy_version=1,
                threshold_ratio=.5,min_scene_frames=900,capacity=capacity,**profile)


def validate_render_options(options: dict[str, object]) -> dict[str, object]:
    keys = {'schema_version', 'workers', 'encoder', 'browser_gpu', 'fast_capture'}
    if not isinstance(options, dict) or set(options) != keys:
        raise InputError('render options require exactly: ' + ', '.join(sorted(keys)))
    if type(options['schema_version']) is not int or options['schema_version'] not in (1,2):
        raise InputError('render options schema_version must be integer 1 or 2')
    fixed=type(options['workers']) is int and 1<=options['workers']<=6
    automatic=options['schema_version']==2 and options['workers']=='auto'
    if not (fixed or automatic):raise InputError('render workers must be auto or an integer from 1 to 6')
    if (options['encoder'] != 'cpu' or options['browser_gpu'] != 'auto'
            or type(options['fast_capture']) is not bool or options['fast_capture']):
        raise InputError('render requires CPU encoding, browser GPU auto, fast_capture=false')
    return dict(options)


def load_render_options(run: Path, workers: int | str | None = None, *,
                        hardware: dict[str, object] | None = None) -> dict[str, object]:
    path = Path(run) / 'source/render-options.json'
    if path.exists():
        try:
            options = validate_render_options(read(path))
        except (OSError, ValueError) as ex:
            raise InputError('invalid saved render options: ' + str(ex)) from ex
    else:
        options = default_render_options(hardware)
    if workers is not None:
        options['workers'] = workers
        if workers == 'auto': options['schema_version'] = 2
    return validate_render_options(options)
