from dataclasses import dataclass


@dataclass(frozen=True)
class Medium:
    media_url_https: str  # "https://pbs.twimg.com/media/GJhdoTjbkAAegbl.jpg"
    display_url: str  # "pic.twitter.com/qZXYi3fuEm"
    expanded_url: (
        str  # https://twitter.com/harajuku_tjpw/status/1772269440396333105/photo/1
    )
    ext_alt_text: str  # "たくさんのあい うけとれました🤍みんなにもとどいた？"
    # 以下は使わなくてもよさそう
    # id_str: str  # "1772269400395321344"
    # indices: list[int]  # [125, 148]
    # media_key: str  # "3_1772269400395321344"
    # type: str  # "photo"
    # url: str  # "https://t.co/qZXYi3fuEm"
    # ext_media_availability: dict[str, bool]  # {"status": "Available"}
    # features: dict[str, Features]
    # sizes: dict[str, Size]
    # original_info: OriginalInfo


# @dataclass(frozen=True)
# class Face:
#     x: int
#     y: int
#     h: int
#     w: int


# @dataclass(frozen=True)
# class Size:
#     h: int
#     w: int
#     resize: str


# @dataclass(frozen=True)
# class Features:
#     faces: list[Face]


# @dataclass(frozen=True)
# class OriginalInfo:
#     height: int
#     width: int
#     focus_rects: list[Face]
