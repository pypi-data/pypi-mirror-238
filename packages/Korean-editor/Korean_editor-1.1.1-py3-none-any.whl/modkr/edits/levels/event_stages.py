"""Handler for clearing event stages"""
from typing import Any

from ... import user_input_handler, helper
from ...edits.other import meow_medals


def set_stage_data(
    stage_data_edit: dict[str, Any],
    stage_id: int,
    stars: int,
    lengths: dict[str, int],
    unlock_next: bool,
) -> dict[str, Any]:
    """Set the stage data for a stage"""

    if stage_id >= len(stage_data_edit["Value"]["clear_progress"]):
        return stage_data_edit
    stage_data_edit = set_clear_progress(stage_data_edit, stage_id, stars, lengths)
    if unlock_next and stage_id + 1 < len(stage_data_edit["Value"]["clear_progress"]):
        stage_data_edit = set_unlock_next(stage_data_edit, stage_id, stars, lengths)
    stage_data_edit = set_clear_amount(stage_data_edit, stage_id, stars, lengths)
    return stage_data_edit


def set_clear_progress(
    stage_data: dict[str, Any], stage_id: int, stars: int, lengths: dict[str, int]
) -> dict[str, Any]:
    """Set the clear progress for a stage"""

    stage_data["Value"]["clear_progress"][stage_id] = ([lengths["stages"]] * stars) + (
        [0] * (lengths["stars"] - stars)
    )
    return stage_data


def set_unlock_next(
    stage_data: dict[str, Any], stage_id: int, stars: int, lengths: dict[str, int]
) -> dict[str, Any]:
    """Set the unlock next for a stage"""

    stage_data["Value"]["unlock_next"][stage_id + 1] = (
        [lengths["stars"] - 1] * stars
    ) + ([0] * (lengths["stars"] - stars))
    return stage_data


def set_clear_amount(
    stage_data: dict[str, Any], stage_id: int, stars: int, lengths: dict[str, int]
) -> dict[str, Any]:
    """Set the clear amount for a stage"""

    stage_data["Value"]["clear_amount"][stage_id] = (
        [[1] * lengths["stages"]] * stars
    ) + ([[0] * lengths["stages"]] * (lengths["stars"] - stars))
    return stage_data


def set_medals(
    stage_stats: dict[str, Any],
    medal_stats: dict[str, Any],
    valid_range: tuple[int, int],
    offset: int,
    is_jp: bool,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Set the medals for completed stages"""

    medal_data = meow_medals.get_medal_data(is_jp)
    if medal_data is None:
        return stage_stats, medal_stats

    unlock_next = stage_stats["Value"]["unlock_next"]

    for medal in medal_data.stages:
        if not medal.maps:
            continue
        completed = True
        for map_id in medal.maps:
            star = medal.star
            if map_id < 0:
                continue
            if map_id < valid_range[0] or map_id > valid_range[1]:
                completed = False
                break
            map_id += offset
            next_chapter = unlock_next[map_id + 1]
            if star is None:
                star = 0
            if next_chapter[star] == 0:
                completed = False
                break
        if completed:
            if medal.medal_id not in medal_stats["medal_data_1"]:
                medal_stats["medal_data_1"].append(medal.medal_id)
            medal_stats["medal_data_2"][medal.medal_id] = 1
    return stage_stats, medal_stats


def stage_handler(
    stage_data: dict[str, Any], ids: list[int], offset: int, unlock_next: bool = True
) -> dict[str, Any]:
    """Clear stages from a set of ids"""

    lengths = stage_data["Lengths"]

    individual = True
    if len(ids) > 1:
        individual = user_input_handler.ask_if_individual(
            "스테이지별 별/관"
        )
    first = True
    stars = 0
    stage_data_edit = stage_data
    for stage_id in ids:
        if not individual and first:
            stars = helper.check_int(
                user_input_handler.colored_input(
                    f"별/크라운의 수를 입력하십시오(최대 &{lengths['stars']}&):"
                )
            )
            if stars is None:
                print("유효한 숫자를 입력하세요.")
                break
            stars = helper.clamp(stars, 0, lengths["stars"])
            first = False
        elif individual:
            stars = helper.check_int(
                user_input_handler.colored_input(
                    f"하위 장에 대한 별/크라운의 수를 입력하십시오. &{stage_id}& (최대 &{lengths['stars']}&):"
                )
            )
            if stars is None:
                print("유효한 숫자를 입력하세요.")
                break
            stars = helper.clamp(stars, 0, lengths["stars"])
        stage_id += offset
        stage_data_edit = stage_data
        stage_data_edit = set_stage_data(
            stage_data_edit, stage_id, stars, lengths, unlock_next
        )

    print("성공적으로 하위 챕터 설정")

    return stage_data_edit


def stories_of_legend(save_stats: dict[str, Any]) -> dict[str, Any]:
    """Handler for clearing stories of legend"""

    stage_data = save_stats["event_stages"]

    ids = user_input_handler.get_range(
        user_input_handler.colored_input(
            "하위 챕터 ID 입력(예: &1& = 범례 시작, &2& = 열정의 땅)(모든 범위를 가져오려면 &all&을 입력할 수 있습니다. 예: &1&-&49& 또는 공백으로 구분된 ID(예: &5 4 7&):"
        ),
        50,
    )
    offset = -1
    save_stats["event_stages"] = stage_handler(stage_data, ids, offset)
    save_stats["event_stages"], save_stats["medals"] = set_medals(
        save_stats["event_stages"],
        save_stats["medals"],
        (0, 50),
        0,
        helper.check_data_is_jp(save_stats),
    )
    return save_stats


def event_stages(save_stats: dict[str, Any]) -> dict[str, Any]:
    """Handler for clearing event stages"""

    stage_data = save_stats["event_stages"]
    lengths = stage_data["Lengths"]

    ids = user_input_handler.get_range(
        user_input_handler.colored_input(
            "하위 챕터 ID를 입력하십시오(ID를 찾으려면 &이벤트 출시 순서 전투 고양이& 조회)(&all&을 입력하여 범위(예: &1&-&50&, 또는 공백으로 구분된 ID(예: &5 4 7&)를 얻을 수 있음):"
        ),
        lengths["total"] - 400,
    )
    offset = 400
    save_stats["event_stages"] = stage_handler(stage_data, ids, offset)
    save_stats["event_stages"], save_stats["medals"] = set_medals(
        save_stats["event_stages"],
        save_stats["medals"],
        (0, len(save_stats["event_stages"]["Value"]["unlock_next"])),
        -600,
        helper.check_data_is_jp(save_stats),
    )
    return save_stats
