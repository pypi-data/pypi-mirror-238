""" Filters for finetuning runs """
import fnmatch
from typing import Dict, List, Optional

from mcli.api.finetuning_runs import get_finetuning_runs
from mcli.api.model.finetune import Finetune
from mcli.cli.common.run_filters import _split_glob_filters
from mcli.utils.utils_run_status import RunStatus
from mcli.utils.utils_spinner import console_status


def get_finetuning_runs_with_filters(
    name_filter: Optional[List[str]] = None,
    before_filter: Optional[str] = None,
    after_filter: Optional[str] = None,
    status_filter: Optional[List[RunStatus]] = None,
    latest: bool = False,
    user_filter: Optional[List[str]] = None,
    limit: Optional[int] = None,
    include_details: bool = False,
) -> List[Finetune]:
    finetuning_runs = []
    if not name_filter:
        # Accept all that pass other filters
        name_filter = []

    # Use get_runs only for the non-glob names provided
    glob_filters, run_names = _split_glob_filters(name_filter)

    # If we're getting the latest run, we only need to get one
    if latest:
        limit = 1

    with console_status('Retrieving requested finetuning runs...'):
        filters = {
            'user_emails': user_filter,
            'before': before_filter,
            'after': after_filter,
            'statuses': status_filter,
            'include_details': include_details,
            'limit': limit,
            'timeout': None,
        }
        finetuning_runs = get_finetuning_runs(
            finetuning_runs=(run_names or None) if not glob_filters else None,
            **filters,
        )

    if glob_filters:
        found_runs: Dict[str, Finetune] = {r.name: r for r in finetuning_runs}

        # Any globs will be handled by additional client-side filtering
        filtered = set()
        for pattern in glob_filters:
            for match in fnmatch.filter(found_runs, pattern):
                filtered.add(match)

        expected_names = set(run_names)
        for run_name in found_runs:
            if run_name in expected_names:
                filtered.add(run_name)

        finetuning_runs = list(found_runs[r] for r in filtered)

    return finetuning_runs
