# [[[fill git_describe()]]]
__version__ = '2023.10.29+parent.75d8f6d6'
# [[[end]]] (checksum: e490d5e79e956f80533629ca467bfdfc)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)
