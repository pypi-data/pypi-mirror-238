"""Handler for selecting story levels"""
from typing import Optional

from ... import user_input_handler, helper
from . import main_story


def select_specific_chapters() -> list[int]:
    """Select specific levels"""

    print("어떤 챕터를 선택하시겠습니까?")
    ids = user_input_handler.select_not_inc(main_story.CHAPTERS, "clear")
    return ids


def get_option():
    """Get option"""

    options = [
        "단계 ID로 특정 수준 선택",
        "특정 단계까지의 모든 레벨 선택",
        "모든 레벨 선택",
    ]
    return user_input_handler.select_single(options)


def select_levels(
    chapter_id: Optional[int], forced_option: Optional[int] = None, total: int = 48
) -> list[int]:
    """Select levels"""

    if forced_option is None:
        choice = get_option()
    else:
        choice = forced_option
    if choice == 1:
        return select_specific_levels(chapter_id, total)
    if choice == 2:
        return select_levels_up_to(chapter_id, total)
    if choice == 3:
        return select_all(total)
    return []


def select_specific_levels(chapter_id: Optional[int], total: int) -> list[int]:
    """Select specific levels"""

    print("어떤 수준을 선택하시겠습니까?")
    if chapter_id is not None:
        helper.colored_text(
            f"Chapter: &{chapter_id+1}& : &{main_story.CHAPTERS[chapter_id]}&"
        )
    ids = user_input_handler.get_range_ids(
        "레벨 ID(예: &1&=한국, &2&=몽골)", total
    )
    ids = helper.check_clamp(ids, total, 1, -1)
    return ids


def select_levels_up_to(chapter_id: Optional[int], total: int) -> list[int]:
    """Select levels up to a certain level"""

    print("어떤 수준을 선택하시겠습니까?")
    if chapter_id is not None:
        helper.colored_text(
            f"Chapter: &{chapter_id+1}& : &{main_story.CHAPTERS[chapter_id]}&"
        )
    stage_id = user_input_handler.get_int(
        f"원하는단계 단계 ID를 최대(및 포함)까지 입력하세요(예: &1&=한국 클리어, &2&=한국 &또는& 몽골 클리어, &{total}&=all)?:"
    )
    stage_id = helper.clamp(stage_id, 1, total)
    return list(range(0, stage_id))


def select_all(total: int) -> list[int]:
    """Select all levels"""

    return list(range(0, total))


def select_level_progress(
    chapter_id: Optional[int], total: int, examples: Optional[list[str]] = None
) -> int:
    """Select level progress"""

    if examples is None:
        examples = [
            "한국",
            "몽골",
        ]

    print("어떤 레벨까지 클리어하고 싶나요?")
    if chapter_id is not None:
        helper.colored_text(
            f"챕터: &{chapter_id+1}& : &{main_story.CHAPTERS[chapter_id]}&"
        )
    progress = user_input_handler.get_int(
        f"원하는 단계 ID를 입력하세요.클리어/언클리어 (e.g &1&={examples[0]} 클리어, &2&={examples[0]} &또는& {examples[1]} 클리어, &{total}&=all, &0&=언클리어 all)?:"
    )
    progress = helper.clamp(progress, 0, total)
    return progress
