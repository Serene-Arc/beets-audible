import random
import string
from copy import deepcopy
from pathlib import Path
from typing import Callable, Iterable, List, Optional, Sequence, Tuple
from unittest.mock import MagicMock, patch

import pytest
from beets.library import Item
from beets.util import bytestring_path

import beetsplug.audible as audible

random.seed(42)


def create_mock_item(item_name: str, item_index: int = 0, filename: Optional[str] = None) -> MagicMock:
    out = MagicMock()
    out.title = item_name
    out.track = item_index
    out.path = bytestring_path(str(Path(".", "test_audiobook", filename if filename else item_name + ".mp3").resolve()))
    out.__str__.return_value = f"{item_name} {out.path}"
    return out


def randomise_lists(lists: Tuple[List, ...], n: int = 5) -> Sequence[Tuple[List, List]]:
    out = []
    for l in lists:
        for i in range(1, n):
            copy = deepcopy(l)
            random.shuffle(copy)
            out.append((l, copy))
    return out


def generate_random_string(n: int) -> str:
    # Define the characters we want to use
    chars = string.ascii_letters + " "
    return "".join(random.choice(chars) for _ in range(n))


def generate_test_album_random_string_smaller_len(chapter_list):
    mock_4 = MagicMock()
    mock_4.tracks = [generate_random_string(20) for _ in range(1, (len(chapter_list) // 2) + 1)]
    return mock_4


def generate_test_album_random_string_greater_len(chapter_list):
    mock_3 = MagicMock()
    mock_3.tracks = [generate_random_string(20) for _ in range(1, len(chapter_list) + 10)]
    return mock_3


def generate_test_album_random_string_same_len(chapter_list):
    mock_2 = MagicMock()
    mock_2.tracks = [generate_random_string(20) for _ in chapter_list]
    return mock_2


def generate_test_album_same(chapter_list):
    mock_1 = MagicMock()
    mock_1.tracks = chapter_list
    return mock_1


def generate_fixture_albums(chapter_list: List[MagicMock]) -> List[MagicMock]:
    out = []

    # this mock just the chapters
    mock_1 = generate_test_album_same(chapter_list)
    out.append(mock_1)

    # this mock is a random set of strings of the same number of chapters
    mock_2 = generate_test_album_random_string_same_len(chapter_list)
    out.append(mock_2)

    # this mock is a random set of strings that is more than the given chapters
    mock_3 = generate_test_album_random_string_greater_len(chapter_list)
    out.append(mock_3)

    if len(chapter_list) > 1:
        # this mock is a random set of strings that is less than the given chapters
        mock_4 = generate_test_album_random_string_smaller_len(chapter_list)
        out.append(mock_4)

    return out


def pytest_generate_tests(metafunc: pytest.Metafunc):
    if "chapter_lists" in metafunc.fixturenames and "test_album" in metafunc.fixturenames:
        test_albums = []
        all_ids = []
        for i, c in enumerate(all_chapter_lists):
            for j, a in enumerate(generate_fixture_albums(c)):
                test_albums.append((c, a))
                all_ids.append(f"chapter_list{i}-album_fixture{j}")

        metafunc.parametrize("chapter_lists,test_album", test_albums, ids=all_ids)
    elif all(s in metafunc.fixturenames for s in ("randomised_items", "correct", "test_album")):
        test_albums = []
        all_ids = []
        for i, c in enumerate(all_chapter_lists):
            for j in range(1, 11):
                intermediate = random.sample(c, k=len(c))
                for k, a in enumerate(generate_fixture_albums(intermediate)):
                    test_albums.append((c, intermediate, a))
                    all_ids.append(f"chapter_list{i}-randomisation{j}-album_fixture{k}")

        metafunc.parametrize("correct,randomised_items,test_album", test_albums, ids=all_ids)

    elif "chapter_lists" in metafunc.fixturenames:
        metafunc.parametrize("chapter_lists", all_chapter_lists)


all_chapter_lists = (
    [  # 0
        create_mock_item("01", 0),
        create_mock_item("02", 0),
        create_mock_item("03", 0),
        create_mock_item("04", 0),
        create_mock_item("05", 0),
        create_mock_item("06", 0),
        create_mock_item("07", 0),
        create_mock_item("08", 0),
        create_mock_item("09", 0),
        create_mock_item("10", 0),
        create_mock_item("11", 0),
        create_mock_item("12", 0),
        create_mock_item("13", 0),
    ],
    [  # 1
        create_mock_item("Chapter 1", 0),
        create_mock_item("Chapter 2", 0),
        create_mock_item("Chapter 3", 0),
        create_mock_item("Chapter 4", 0),
        create_mock_item("Chapter 5", 0),
        create_mock_item("Chapter 6", 0),
        create_mock_item("Chapter 7", 0),
        create_mock_item("Chapter 8", 0),
        create_mock_item("Chapter 9", 0),
        create_mock_item("Chapter 10", 0),
    ],
    [  # 2
        create_mock_item("Chapter 01", 0),
        create_mock_item("Chapter 02", 0),
        create_mock_item("Chapter 03", 0),
        create_mock_item("Chapter 04", 0),
        create_mock_item("Chapter 05", 0),
        create_mock_item("Chapter 06", 0),
        create_mock_item("Chapter 07", 0),
        create_mock_item("Chapter 08", 0),
        create_mock_item("Chapter 09", 0),
        create_mock_item("Chapter 10", 0),
    ],
    [  # 3
        create_mock_item("Chapter - 01", 0),
        create_mock_item("Chapter - 02", 0),
        create_mock_item("Chapter - 03", 0),
        create_mock_item("Chapter - 04", 0),
        create_mock_item("Chapter - 05", 0),
        create_mock_item("Chapter - 06", 0),
        create_mock_item("Chapter - 07", 0),
        create_mock_item("Chapter - 08", 0),
        create_mock_item("Chapter - 09", 0),
        create_mock_item("Chapter - 10", 0),
        create_mock_item("Chapter - 11", 0),
        create_mock_item("Chapter - 12", 0),
        create_mock_item("Chapter - 13", 0),
    ],
    [  # 4
        create_mock_item("Chapter-01", 0),
        create_mock_item("Chapter-02", 0),
        create_mock_item("Chapter-03", 0),
        create_mock_item("Chapter-04", 0),
        create_mock_item("Chapter-05", 0),
        create_mock_item("Chapter-06", 0),
        create_mock_item("Chapter-07", 0),
        create_mock_item("Chapter-08", 0),
        create_mock_item("Chapter-09", 0),
        create_mock_item("Chapter-10", 0),
        create_mock_item("Chapter-11", 0),
        create_mock_item("Chapter-12", 0),
        create_mock_item("Chapter-13", 0),
    ],
    [  # 5
        create_mock_item("Mediocre-Part01", 0),
        create_mock_item("Mediocre-Part02", 0),
        create_mock_item("Mediocre-Part03", 0),
        create_mock_item("Mediocre-Part04", 0),
        create_mock_item("Mediocre-Part05", 0),
        create_mock_item("Mediocre-Part06", 0),
        create_mock_item("Mediocre-Part07", 0),
        create_mock_item("Mediocre-Part08", 0),
        create_mock_item("Mediocre-Part09", 0),
        create_mock_item("Mediocre-Part10", 0),
        create_mock_item("Mediocre-Part11", 0),
        create_mock_item("Mediocre-Part12", 0),
    ],
    [  # 6
        create_mock_item("Chapter 1 The DC Sniper The Untold Story of the DC Sniper Investigation - 1.m4b", 0),
        create_mock_item("Chapter 2 Terrorism The Untold Story of the DC Sniper Investigation - 1.m4b", 0),
        create_mock_item("Chapter 3 Brothers in the Arena The Untold Story of the DC Sniper Investigation - 1.m4b", 0),
        create_mock_item("Chapter 4 Call Me God The Untold Story of the DC Sniper Investigation - 1.m4b", 0),
        create_mock_item("Chapter 5 Close to Home The Untold Story of the DC Sniper Investigation - 1.m4b", 0),
        create_mock_item("Chapter 6 A Local Case The Untold Story of the DC Sniper Investigation - 1.m4b", 0),
        create_mock_item("Chapter 7 Demands The Untold Story of the DC Sniper Investigation - 1.m4b", 0),
        create_mock_item("Chapter 8 The Profile The Untold Story of the DC Sniper Investigation - 1.m4b", 0),
        create_mock_item("Chapter 9 Suspects The Untold Story of the DC Sniper Investigation - 1.m4b", 0),
        create_mock_item("Chapter 10 Prelude The Untold Story of the DC Sniper Investigation - 1.m4b", 0),
        create_mock_item("Chapter 11 The Arrest The Untold Story of the DC Sniper Investigation - 1.m4b", 0),
        create_mock_item("Chapter 12 Revenge The Untold Story of the DC Sniper Investigation - 1.m4b", 0),
        create_mock_item(
            "Chapter 13 The Trials of a Teenager The Untold Story of the DC Sniper Investigation - 1.m4b", 0
        ),
        create_mock_item("Chapter 14 Last Words The Untold Story of the DC Sniper Investigation - 1.m4b", 0),
    ],
    [  # 7
        create_mock_item("Prologue", 1),
        create_mock_item("Chapter 1", 2),
        create_mock_item("Chapter 2", 3),
        create_mock_item("Chapter 3", 4),
        create_mock_item("Chapter 4", 5),
        create_mock_item("Chapter 5", 6),
        create_mock_item("Chapter 6", 7),
        create_mock_item("Chapter 7", 8),
        create_mock_item("Chapter 8", 9),
        create_mock_item("Chapter 9", 10),
        create_mock_item("Chapter 10", 11),
        create_mock_item("End", 12),
        create_mock_item("Author's Note", 13),
    ],
    [  # 8
        create_mock_item("01 - Zg503IhGHXyRdZeVn838pZGhvO7uwM5C", 0),
        create_mock_item("02 - Hf7KcfUB8rsP2AzR8DlZgx3CRXN5ABKM", 0),
        create_mock_item("03 - nzCOIa8IGCZtInmoxa1M3zS5FmM9F8E7", 0),
        create_mock_item("04 - atijzxWA7 PZOI5aN mzNxyE1FU4hFGQ", 0),
        create_mock_item("05 - ucwzgmf4aA5YlHCvcYMdn2TCGz1Uxb6E", 0),
        create_mock_item("06 - k4yXBbaPPgtPOpI6nVnXM1ex Dg1Hgaw", 0),
        create_mock_item("07 - VtQIEznFhhWPvGLzljcL8vpHGITPv ey", 0),
        create_mock_item("08 - xe4fePnrboPoYKiiGTFC4LEOB8nP5NSt", 0),
        create_mock_item("09 - B8V 7YSwH02fjRFnkBpfvD8x iHNdUF2", 0),
        create_mock_item("10 - vPusDiJioUeF8j67IXBzcCoYuENxtjrU", 0),
        create_mock_item("11 - PHxgYdqZPcI6DwPIJXKy3AQvLzrdgzQD", 0),
        create_mock_item("12 - 7KCqFir8teX GEG Pa oi8S4K3t3leSI", 0),
        create_mock_item("13 - CvSesAAwUHbCIJbnI43aVdPlApEiUcIZ", 0),
        create_mock_item("14 - lvDZY0kn60eEmb3mkTC9vkCyDZSf1ifk", 0),
        create_mock_item("15 - dzlLiHkRm3FMd8Yad8Iigrm0qK8gIRib", 0),
        create_mock_item("16 - SKW2vzcx3mgjro3GjBu51qBSaMwiVFRB", 0),
        create_mock_item("17 - xGnYqQILdJVM3VcaqbqorbdiPMcieOzw", 0),
        create_mock_item("18 - XIvowcJjMMBjgTht8azQb3XIGQSb1s9e", 0),
        create_mock_item("19 - 97D0VmI9qgnRDPhwwkRwuL7atFCSKmNJ", 0),
        create_mock_item("20 - AEBmW2Dspf6czIMsF3l9u2IwmqUw826u", 0),
    ],
    [  # 9
        create_mock_item("Zg503IhGHXyRdZeVn838pZGhvO7uwM5C", 1),
        create_mock_item("Hf7KcfUB8rsP2AzR8DlZgx3CRXN5ABKM", 2),
        create_mock_item("nzCOIa8IGCZtInmoxa1M3zS5FmM9F8E7", 3),
        create_mock_item("atijzxWA7 PZOI5aN mzNxyE1FU4hFGQ", 4),
        create_mock_item("ucwzgmf4aA5YlHCvcYMdn2TCGz1Uxb6E", 5),
        create_mock_item("k4yXBbaPPgtPOpI6nVnXM1ex Dg1Hgaw", 6),
        create_mock_item("VtQIEznFhhWPvGLzljcL8vpHGITPv ey", 7),
        create_mock_item("xe4fePnrboPoYKiiGTFC4LEOB8nP5NSt", 8),
        create_mock_item("B8V 7YSwH02fjRFnkBpfvD8x iHNdUF2", 9),
        create_mock_item("vPusDiJioUeF8j67IXBzcCoYuENxtjrU", 10),
        create_mock_item("PHxgYdqZPcI6DwPIJXKy3AQvLzrdgzQD", 11),
        create_mock_item("7KCqFir8teX GEG Pa oi8S4K3t3leSI", 12),
        create_mock_item("CvSesAAwUHbCIJbnI43aVdPlApEiUcIZ", 13),
        create_mock_item("lvDZY0kn60eEmb3mkTC9vkCyDZSf1ifk", 14),
        create_mock_item("dzlLiHkRm3FMd8Yad8Iigrm0qK8gIRib", 15),
        create_mock_item("SKW2vzcx3mgjro3GjBu51qBSaMwiVFRB", 16),
        create_mock_item("xGnYqQILdJVM3VcaqbqorbdiPMcieOzw", 17),
        create_mock_item("XIvowcJjMMBjgTht8azQb3XIGQSb1s9e", 18),
        create_mock_item("97D0VmI9qgnRDPhwwkRwuL7atFCSKmNJ", 19),
        create_mock_item("AEBmW2Dspf6czIMsF3l9u2IwmqUw826u", 20),
    ],
    [  # 10
        create_mock_item("00 Part One.mp3"),
        create_mock_item("01.mp3"),
        create_mock_item("02.mp3"),
        create_mock_item("03.mp3"),
        create_mock_item("04.mp3"),
        create_mock_item("05.mp3"),
        create_mock_item("06 Part Two.mp3"),
        create_mock_item("07.mp3"),
        create_mock_item("08.mp3"),
        create_mock_item("09.mp3"),
        create_mock_item("10.mp3"),
        create_mock_item("11 Part Three.mp3"),
        create_mock_item("12.mp3"),
        create_mock_item("13.mp3"),
        create_mock_item("14.mp3"),
        create_mock_item("15.mp3"),
        create_mock_item("16 Part Four.mp3"),
        create_mock_item("17.mp3"),
        create_mock_item("18.mp3"),
        create_mock_item("19.mp3"),
        create_mock_item("20.mp3"),
        create_mock_item("21 Part Five.mp3"),
        create_mock_item("22.mp3"),
        create_mock_item("23.mp3"),
        create_mock_item("24.mp3"),
        create_mock_item("25.mp3"),
    ],
    # haven't thought of logic that would allow for this type of thing. honestly it might be impossible if there's no
    # online reference that exactly matches
    # [
    #     create_mock_item("Prologue", 0),
    #     create_mock_item("Chapter 1", 0),
    #     create_mock_item("Chapter 2", 0),
    #     create_mock_item("Chapter 3", 0),
    #     create_mock_item("Chapter 4", 0),
    #     create_mock_item("Chapter 5", 0),
    #     create_mock_item("Chapter 6", 0),
    #     create_mock_item("Chapter 7", 0),
    #     create_mock_item("Chapter 8", 0),
    #     create_mock_item("Chapter 9", 0),
    #     create_mock_item("Chapter 10", 0),
    #     create_mock_item("End", 0),
    #     create_mock_item("Author's Note", 0),
    # ],
)


def test_sort_items(chapter_lists: List[Item], mock_audible_plugin, test_album: List[MagicMock]):
    expected = deepcopy(chapter_lists)
    result = sort_tracks_for_test(chapter_lists, mock_audible_plugin, test_album)
    assert all([str(result[i]) == str(e) for i, e in enumerate(expected)])


def sort_tracks_for_test(chapter_lists, mock_audible_plugin, test_album):
    with patch("beetsplug.audible.get_common_data_attributes", return_value=dict()):
        with patch("beetsplug.audible.convert_items_to_trackinfo", lambda x, _: x):
            result = mock_audible_plugin.sort_tracks(mock_audible_plugin, test_album, chapter_lists)
    return result


def test_sort_items_reversed(chapter_lists: List[Item], mock_audible_plugin, test_album: List[MagicMock]):
    expected = deepcopy(chapter_lists)
    result = sort_tracks_for_test(chapter_lists, mock_audible_plugin, test_album)
    assert all([str(result[i]) == str(e) for i, e in enumerate(expected)])


def test_sort_items_randomised(
    correct: List[Item],
    randomised_items: List[Item],
    mock_audible_plugin,
    test_album: List[MagicMock],
):
    result = sort_tracks_for_test(randomised_items, mock_audible_plugin, test_album)
    assert all([str(result[i]) == str(e) for i, e in enumerate(correct)])


@pytest.mark.parametrize(
    ("test_chapter_list", "test_algorithm_choice", "album_generation_function"),
    (
        (all_chapter_lists[0], "starting_numbers", generate_test_album_same),
        (all_chapter_lists[0], "natural_sort", generate_test_album_same),
        (all_chapter_lists[0], "chapter_levenshtein", generate_test_album_same),
        (all_chapter_lists[0], "chapter_levenshtein", generate_test_album_same),
        (all_chapter_lists[7], "source_numbering", generate_test_album_same),
    ),
)
def test_sort_specific_method(
    mock_audible_plugin: MagicMock,
    test_chapter_list: List,
    test_algorithm_choice: str,
    album_generation_function: Callable,
):
    test_album = album_generation_function(deepcopy(test_chapter_list))
    correct = deepcopy(test_chapter_list)
    mock_audible_plugin.config["chapter_matching_algorithms"] = [
        test_algorithm_choice,
    ]
    result = sort_tracks_for_test(test_chapter_list, mock_audible_plugin, test_album)
    assert all([str(result[i]) == str(e) for i, e in enumerate(correct)])


@pytest.mark.online
@pytest.mark.parametrize(
    ("test_audiobook_id", "test_items", "expected_items"),
    (
        (
            "0063007711",
            (create_mock_item("Kleptopia: How Dirty Money Is Conquering the World"),),
            ("Kleptopia: How Dirty Money Is Conquering the World",),
        ),
        (
            "B07XTN4FTJ",
            (
                create_mock_item("Chapter 1 The DC Sniper The Untold Story of the DC Sniper Investigation - 1.m4b", 0),
                create_mock_item("Chapter 2 Terrorism The Untold Story of the DC Sniper Investigation - 1.m4b", 0),
                create_mock_item(
                    "Chapter 3 Brothers in the Arena The Untold Story of the DC Sniper Investigation - 1.m4b", 0
                ),
                create_mock_item("Chapter 4 Call Me God The Untold Story of the DC Sniper Investigation - 1.m4b", 0),
                create_mock_item("Chapter 5 Close to Home The Untold Story of the DC Sniper Investigation - 1.m4b", 0),
                create_mock_item("Chapter 6 A Local Case The Untold Story of the DC Sniper Investigation - 1.m4b", 0),
                create_mock_item("Chapter 7 Demands The Untold Story of the DC Sniper Investigation - 1.m4b", 0),
                create_mock_item("Chapter 8 The Profile The Untold Story of the DC Sniper Investigation - 1.m4b", 0),
                create_mock_item("Chapter 9 Suspects The Untold Story of the DC Sniper Investigation - 1.m4b", 0),
                create_mock_item("Chapter 10 Prelude The Untold Story of the DC Sniper Investigation - 1.m4b", 0),
                create_mock_item("Chapter 11 The Arrest The Untold Story of the DC Sniper Investigation - 1.m4b", 0),
                create_mock_item("Chapter 12 Revenge The Untold Story of the DC Sniper Investigation - 1.m4b", 0),
                create_mock_item(
                    "Chapter 13 The Trials of a Teenager The Untold Story of the DC Sniper Investigation - 1.m4b", 0
                ),
                create_mock_item("Chapter 14 Last Words The Untold Story of the DC Sniper Investigation - 1.m4b", 0),
            ),
            (
                "Chapter 1: The DC Sniper",
                "Chapter 2: Terrorism",
                "Chapter 3: Brothers in the Arena",
                "Chapter 4: Call Me God",
                "Chapter 5: Close to Home",
                "Chapter 6: A Local Case",
                "Chapter 7: Demands",
                "Chapter 8: The Profile",
                "Chapter 9: Suspects",
                "Chapter 10: Prelude",
                "Chapter 11: The Arrest",
                "Chapter 12: Revenge",
                "Chapter 13: The Trials of a Teenager",
                "Chapter 14: Last Words",
            ),
        ),
        (
            "B005CJAB5S",
            (
                create_mock_item("Cats-Eye-000.mp3", 0),
                create_mock_item("Cats-Eye-001.mp3", 0),
                create_mock_item("Cats-Eye-002.mp3", 0),
                create_mock_item("Cats-Eye-003.mp3", 0),
                create_mock_item("Cats-Eye-004.mp3", 0),
                create_mock_item("Cats-Eye-005.mp3", 0),
                create_mock_item("Cats-Eye-006.mp3", 0),
                create_mock_item("Cats-Eye-007.mp3", 0),
                create_mock_item("Cats-Eye-008.mp3", 0),
                create_mock_item("Cats-Eye-009.mp3", 0),
                create_mock_item("Cats-Eye-010.mp3", 0),
                create_mock_item("Cats-Eye-011.mp3", 0),
            ),
            (
                "Cats-Eye-000.mp3",
                "Cats-Eye-001.mp3",
                "Cats-Eye-002.mp3",
                "Cats-Eye-003.mp3",
                "Cats-Eye-004.mp3",
                "Cats-Eye-005.mp3",
                "Cats-Eye-006.mp3",
                "Cats-Eye-007.mp3",
                "Cats-Eye-008.mp3",
                "Cats-Eye-009.mp3",
                "Cats-Eye-010.mp3",
                "Cats-Eye-011.mp3",
            ),
        ),
        (
            "1250767547",
            (
                create_mock_item("01 - Paolini, C - To Sleep in a Sea of Stars — 01.mp3", 0),
                create_mock_item("02 - Paolini, C - To Sleep in a Sea of Stars — 02.mp3", 0),
                create_mock_item("03 - Paolini, C - To Sleep in a Sea of Stars — 03.mp3", 0),
                create_mock_item("04 - Paolini, C - To Sleep in a Sea of Stars — 04.mp3", 0),
                create_mock_item("05 - Paolini, C - To Sleep in a Sea of Stars — 05.mp3", 0),
                create_mock_item("06 - Paolini, C - To Sleep in a Sea of Stars — 06.mp3", 0),
                create_mock_item("07 - Paolini, C - To Sleep in a Sea of Stars — 07.mp3", 0),
                create_mock_item("08 - Paolini, C - To Sleep in a Sea of Stars — 08.mp3", 0),
                create_mock_item("09 - Paolini, C - To Sleep in a Sea of Stars — 09.mp3", 0),
                create_mock_item("10 - Paolini, C - To Sleep in a Sea of Stars — 10.mp3", 0),
                create_mock_item("11 - Paolini, C - To Sleep in a Sea of Stars — 11.mp3", 0),
                create_mock_item("12 - Paolini, C - To Sleep in a Sea of Stars — 12.mp3", 0),
                create_mock_item("13 - Paolini, C - To Sleep in a Sea of Stars — 13.mp3", 0),
                create_mock_item("14 - Paolini, C - To Sleep in a Sea of Stars — 14.mp3", 0),
                create_mock_item("15 - Paolini, C - To Sleep in a Sea of Stars — 15.mp3", 0),
                create_mock_item("16 - Paolini, C - To Sleep in a Sea of Stars — 16.mp3", 0),
                create_mock_item("17 - Paolini, C - To Sleep in a Sea of Stars — 17.mp3", 0),
                create_mock_item("18 - Paolini, C - To Sleep in a Sea of Stars — 18.mp3", 0),
                create_mock_item("19 - Paolini, C - To Sleep in a Sea of Stars — 19.mp3", 0),
                create_mock_item("20 - Paolini, C - To Sleep in a Sea of Stars — 20.mp3", 0),
                create_mock_item("21 - Paolini, C - To Sleep in a Sea of Stars — 21.mp3", 0),
                create_mock_item("22 - Paolini, C - To Sleep in a Sea of Stars — 22.mp3", 0),
                create_mock_item("23 - Paolini, C - To Sleep in a Sea of Stars — 23.mp3", 0),
                create_mock_item("24 - Paolini, C - To Sleep in a Sea of Stars — 24.mp3", 0),
                create_mock_item("25 - Paolini, C - To Sleep in a Sea of Stars — 25.mp3", 0),
                create_mock_item("26 - Paolini, C - To Sleep in a Sea of Stars — 26.mp3", 0),
                create_mock_item("27 - Paolini, C - To Sleep in a Sea of Stars — 27.mp3", 0),
                create_mock_item("28 - Paolini, C - To Sleep in a Sea of Stars — 28.mp3", 0),
                create_mock_item("29 - Paolini, C - To Sleep in a Sea of Stars — 29.mp3", 0),
                create_mock_item("30 - Paolini, C - To Sleep in a Sea of Stars — 30.mp3", 0),
                create_mock_item("31 - Paolini, C - To Sleep in a Sea of Stars — 31.mp3", 0),
                create_mock_item("32 - Paolini, C - To Sleep in a Sea of Stars — 32.mp3", 0),
                create_mock_item("33 - Paolini, C - To Sleep in a Sea of Stars — 33.mp3", 0),
                create_mock_item("34 - Paolini, C - To Sleep in a Sea of Stars — 34.mp3", 0),
                create_mock_item("35 - Paolini, C - To Sleep in a Sea of Stars — 35.mp3", 0),
                create_mock_item("36 - Paolini, C - To Sleep in a Sea of Stars — 36.mp3", 0),
                create_mock_item("37 - Paolini, C - To Sleep in a Sea of Stars — 37.mp3", 0),
                create_mock_item("38 - Paolini, C - To Sleep in a Sea of Stars — 38.mp3", 0),
                create_mock_item("39 - Paolini, C - To Sleep in a Sea of Stars — 39.mp3", 0),
                create_mock_item("40 - Paolini, C - To Sleep in a Sea of Stars — 40.mp3", 0),
                create_mock_item("41 - Paolini, C - To Sleep in a Sea of Stars — 41.mp3", 0),
                create_mock_item("42 - Paolini, C - To Sleep in a Sea of Stars — 42.mp3", 0),
                create_mock_item("43 - Paolini, C - To Sleep in a Sea of Stars — 43.mp3", 0),
                create_mock_item("44 - Paolini, C - To Sleep in a Sea of Stars — 44.mp3", 0),
                create_mock_item("45 - Paolini, C - To Sleep in a Sea of Stars — 45.mp3", 0),
                create_mock_item("46 - Paolini, C - To Sleep in a Sea of Stars — 46.mp3", 0),
                create_mock_item("47 - Paolini, C - To Sleep in a Sea of Stars — 47.mp3", 0),
                create_mock_item("48 - Paolini, C - To Sleep in a Sea of Stars — 48.mp3", 0),
                create_mock_item("49 - Paolini, C - To Sleep in a Sea of Stars — 49.mp3", 0),
                create_mock_item("50 - Paolini, C - To Sleep in a Sea of Stars — 50.mp3", 0),
                create_mock_item("51 - Paolini, C - To Sleep in a Sea of Stars — 51.mp3", 0),
                create_mock_item("52 - Paolini, C - To Sleep in a Sea of Stars — 52.mp3", 0),
                create_mock_item("53 - Paolini, C - To Sleep in a Sea of Stars — 53.mp3", 0),
                create_mock_item("54 - Paolini, C - To Sleep in a Sea of Stars — 54.mp3", 0),
                create_mock_item("55 - Paolini, C - To Sleep in a Sea of Stars — 55.mp3", 0),
                create_mock_item("56 - Paolini, C - To Sleep in a Sea of Stars — 56.mp3", 0),
                create_mock_item("57 - Paolini, C - To Sleep in a Sea of Stars — 57.mp3", 0),
                create_mock_item("58 - Paolini, C - To Sleep in a Sea of Stars — 58.mp3", 0),
                create_mock_item("59 - Paolini, C - To Sleep in a Sea of Stars — 59.mp3", 0),
                create_mock_item("60 - Paolini, C - To Sleep in a Sea of Stars — 60.mp3", 0),
            ),
            (
                "01 - Paolini, C - To Sleep in a Sea of Stars — 01.mp3",
                "02 - Paolini, C - To Sleep in a Sea of Stars — 02.mp3",
                "03 - Paolini, C - To Sleep in a Sea of Stars — 03.mp3",
                "04 - Paolini, C - To Sleep in a Sea of Stars — 04.mp3",
                "05 - Paolini, C - To Sleep in a Sea of Stars — 05.mp3",
                "06 - Paolini, C - To Sleep in a Sea of Stars — 06.mp3",
                "07 - Paolini, C - To Sleep in a Sea of Stars — 07.mp3",
                "08 - Paolini, C - To Sleep in a Sea of Stars — 08.mp3",
                "09 - Paolini, C - To Sleep in a Sea of Stars — 09.mp3",
                "10 - Paolini, C - To Sleep in a Sea of Stars — 10.mp3",
                "11 - Paolini, C - To Sleep in a Sea of Stars — 11.mp3",
                "12 - Paolini, C - To Sleep in a Sea of Stars — 12.mp3",
                "13 - Paolini, C - To Sleep in a Sea of Stars — 13.mp3",
                "14 - Paolini, C - To Sleep in a Sea of Stars — 14.mp3",
                "15 - Paolini, C - To Sleep in a Sea of Stars — 15.mp3",
                "16 - Paolini, C - To Sleep in a Sea of Stars — 16.mp3",
                "17 - Paolini, C - To Sleep in a Sea of Stars — 17.mp3",
                "18 - Paolini, C - To Sleep in a Sea of Stars — 18.mp3",
                "19 - Paolini, C - To Sleep in a Sea of Stars — 19.mp3",
                "20 - Paolini, C - To Sleep in a Sea of Stars — 20.mp3",
                "21 - Paolini, C - To Sleep in a Sea of Stars — 21.mp3",
                "22 - Paolini, C - To Sleep in a Sea of Stars — 22.mp3",
                "23 - Paolini, C - To Sleep in a Sea of Stars — 23.mp3",
                "24 - Paolini, C - To Sleep in a Sea of Stars — 24.mp3",
                "25 - Paolini, C - To Sleep in a Sea of Stars — 25.mp3",
                "26 - Paolini, C - To Sleep in a Sea of Stars — 26.mp3",
                "27 - Paolini, C - To Sleep in a Sea of Stars — 27.mp3",
                "28 - Paolini, C - To Sleep in a Sea of Stars — 28.mp3",
                "29 - Paolini, C - To Sleep in a Sea of Stars — 29.mp3",
                "30 - Paolini, C - To Sleep in a Sea of Stars — 30.mp3",
                "31 - Paolini, C - To Sleep in a Sea of Stars — 31.mp3",
                "32 - Paolini, C - To Sleep in a Sea of Stars — 32.mp3",
                "33 - Paolini, C - To Sleep in a Sea of Stars — 33.mp3",
                "34 - Paolini, C - To Sleep in a Sea of Stars — 34.mp3",
                "35 - Paolini, C - To Sleep in a Sea of Stars — 35.mp3",
                "36 - Paolini, C - To Sleep in a Sea of Stars — 36.mp3",
                "37 - Paolini, C - To Sleep in a Sea of Stars — 37.mp3",
                "38 - Paolini, C - To Sleep in a Sea of Stars — 38.mp3",
                "39 - Paolini, C - To Sleep in a Sea of Stars — 39.mp3",
                "40 - Paolini, C - To Sleep in a Sea of Stars — 40.mp3",
                "41 - Paolini, C - To Sleep in a Sea of Stars — 41.mp3",
                "42 - Paolini, C - To Sleep in a Sea of Stars — 42.mp3",
                "43 - Paolini, C - To Sleep in a Sea of Stars — 43.mp3",
                "44 - Paolini, C - To Sleep in a Sea of Stars — 44.mp3",
                "45 - Paolini, C - To Sleep in a Sea of Stars — 45.mp3",
                "46 - Paolini, C - To Sleep in a Sea of Stars — 46.mp3",
                "47 - Paolini, C - To Sleep in a Sea of Stars — 47.mp3",
                "48 - Paolini, C - To Sleep in a Sea of Stars — 48.mp3",
                "49 - Paolini, C - To Sleep in a Sea of Stars — 49.mp3",
                "50 - Paolini, C - To Sleep in a Sea of Stars — 50.mp3",
                "51 - Paolini, C - To Sleep in a Sea of Stars — 51.mp3",
                "52 - Paolini, C - To Sleep in a Sea of Stars — 52.mp3",
                "53 - Paolini, C - To Sleep in a Sea of Stars — 53.mp3",
                "54 - Paolini, C - To Sleep in a Sea of Stars — 54.mp3",
                "55 - Paolini, C - To Sleep in a Sea of Stars — 55.mp3",
                "56 - Paolini, C - To Sleep in a Sea of Stars — 56.mp3",
                "57 - Paolini, C - To Sleep in a Sea of Stars — 57.mp3",
                "58 - Paolini, C - To Sleep in a Sea of Stars — 58.mp3",
                "59 - Paolini, C - To Sleep in a Sea of Stars — 59.mp3",
                "60 - Paolini, C - To Sleep in a Sea of Stars — 60.mp3",
            ),
        ),
        (
            "B09VMXJP5W",
            (
                create_mock_item("1.mp3", 0),
                create_mock_item("2.mp3", 0),
                create_mock_item("3.mp3", 0),
                create_mock_item("4.mp3", 0),
                create_mock_item("5.mp3", 0),
                create_mock_item("6.mp3", 0),
                create_mock_item("7.mp3", 0),
                create_mock_item("8.mp3", 0),
                create_mock_item("9.mp3", 0),
            ),
            (
                "1.mp3",
                "2.mp3",
                "3.mp3",
                "4.mp3",
                "5.mp3",
                "6.mp3",
                "7.mp3",
                "8.mp3",
                "9.mp3",
            ),
        ),
    ),
)
def test_audiobook_chapter_matching(
    test_audiobook_id: str,
    test_items: List[Item],
    expected_items: List[Item],
    mock_audible_plugin: MagicMock,
):
    test_album = audible.Audible.get_album_info(mock_audible_plugin, test_audiobook_id)
    results = mock_audible_plugin.sort_tracks(mock_audible_plugin, test_album, test_items)
    assert results is not None
    assert all([results[i].title == e for i, e in enumerate(expected_items)])
    assert len(results) == len(expected_items)


@pytest.mark.parametrize(
    ("test_token1", "test_token2", "expected"),
    (
        ("example", "example", 0),
        ("exampl", "example", 1),
        ("example1", "example", 10),
        ("example1", "example2", 10),
        ("example1", "example12", 10),
        ("example21", "example12", 20),
        ("example1", "example1 test", 5),
    ),
)
def test_specialised_levenshtein(test_token1: str, test_token2: str, expected: int):
    result = audible.specialised_levenshtein(test_token1, test_token2)
    assert isinstance(result, int)
    assert result == expected


@pytest.mark.parametrize(
    ("test_tokens", "expected_prefix", "expected_suffix"),
    (
        ([], "", ""),
        (
            [
                "test",
            ],
            "",
            "",
        ),
        (["test", "test"], "test", "test"),
        (["test1", "test2"], "test", ""),
        (["testing", "test2"], "test", ""),
        (["testing", "test2"], "test", ""),
        (["prefix1suffix", "prefix2suffix"], "prefix", "suffix"),
        (["prologue", "chapter1", "chapter2", "chapter3"], "chapter", ""),
    ),
)
def test_find_regular_affixes(test_tokens: List[str], expected_prefix: str, expected_suffix: str):
    results = audible.find_regular_affixes(test_tokens)
    assert results[0] == expected_prefix
    assert results[1] == expected_suffix


@pytest.mark.parametrize(
    ("test_token", "test_affixes", "expected"),
    (
        ("example", ("", ""), "example"),
        ("test", ("test", ""), ""),
        ("test", ("", "test"), ""),
        ("testexampletest", ("test", ""), "exampletest"),
        ("testexampletest", ("", "test"), "testexample"),
        ("test.mp3", ("", ".mp3"), "test"),
        ("testxmp3", ("", ".mp3"), "testxmp3"),
    ),
)
def test_strip_affixes(test_token: str, test_affixes: Tuple[str, str], expected: str):
    result = audible.strip_affixes(test_token, test_affixes)
    assert result == expected


@pytest.mark.parametrize(
    ("test_numbers", "expected"),
    (
        ((1,), True),
        ((1, 2), True),
        ((0, 1, 2), True),
        ((0, None, 2), False),
        ((0, 1, None), False),
        ((10, 11, 12), True),
        ((10, 11, 13), False),
    ),
)
def test_is_continuous_number_series(test_numbers: Iterable[Optional[int]], expected: bool):
    result = audible.is_continuous_number_series(test_numbers)
    assert result == expected


@pytest.mark.parametrize(
    ("test_string", "expected"),
    (
        ("01 test", 1),
        ("01-test", 1),
        ("01_test", 1),
        ("100_test", 100),
        ("01 - test", 1),
        ("test", None),
        ("0t1 test", 0),
        ("01", 1),
        ("001", 1),
        ("012", 12),
    ),
)
def test_check_starts_with_number(test_string: str, expected: Optional[int]):
    result = audible.check_starts_with_number(test_string)
    assert result == expected
