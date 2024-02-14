from datetime import datetime
from unittest.mock import patch
from clfill.tracker import ready_for_followup


def test_ready_for_followup():
    # write test cases
    row_pass = ["", "", "1/21", "No", "Yes", "", "email@email"]
    row_not_ready = ["", "", "11/21", "No", "Yes", "", "email@email"]
    row_not_full = ["", "", "11/21", "No", "Yes", ""]
    with patch('clfill.tracker.datetime') as mock_datetime:
        # fill mock obj with datetime's methods
        mock_datetime.side_effect = lambda y, m, d: datetime(y, m, d)
        mock_datetime.strptime.side_effect = lambda x, y: datetime.strptime(x, y)
        mock_datetime.now.return_value = datetime(2024, 7, 21)
        # call test cases
        row_pass_result = ready_for_followup(row_pass)
        row_not_ready_result = ready_for_followup(row_not_ready)
        row_not_full_result = ready_for_followup(row_not_full)

    assert row_pass_result is True
    assert row_not_ready_result is False
    assert row_not_full_result is False
