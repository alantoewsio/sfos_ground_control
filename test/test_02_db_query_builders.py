import pytest

from sfos.db import Select


@pytest.fixture(scope="function")
def select_all() -> Select:
    return Select(from_table="tablename")


@pytest.fixture(scope="function")
def select_cols() -> Select:
    return Select("col1", "col2", "col3", from_table="tablename")


def test_select_all(select_all: Select) -> None:
    t_sel_1 = select_all
    t_sql_1 = t_sel_1.__sql__
    e_sql_1 = "SELECT * FROM tablename"

    assert t_sql_1 == e_sql_1


def test_select_cols(select_cols: Select) -> None:
    t_sel_2 = select_cols
    t_sql_2 = t_sel_2.__sql__
    e_sql_2 = "SELECT col1, col2, col3 FROM tablename"

    assert t_sql_2 == e_sql_2


def test_select_cols_where(select_cols: Select) -> None:
    e_sql_3 = "SELECT col1, col2, col3 FROM tablename WHERE col1 is not ?"
    e_params_3 = ["test value"]

    t_sel_3 = select_cols.where("col1", operator="is not", criteria="test value")
    t_sql_3 = t_sel_3.__sql__
    t_params_3 = t_sel_3._params
    assert t_sql_3 == e_sql_3
    assert t_params_3 == e_params_3


def test_select_cols_where_2(select_cols: Select) -> None:
    e_sql_4 = "SELECT col1, col2, col3 FROM tablename WHERE col1 is not ? AND col2 = ?"
    e_params_4 = ["test value", "test value 2"]

    t_sel4 = select_cols.where("col1", operator="is not", criteria="test value").where(
        "col2", operator="=", criteria="test value 2"
    )
    t_sql_4 = t_sel4.__sql__
    t_params_4 = t_sel4._params
    assert t_sql_4 == e_sql_4
    assert t_params_4 == e_params_4


def test_select_cols_order(select_cols: Select) -> None:
    cols = ["colQ", "colR", "colS"]
    act_col = cols[2]
    e_sql_5 = f"SELECT {", ".join(cols)} FROM tablename ORDER BY {act_col} ASC"
    select_cols._columns = cols
    t_sel_5 = select_cols.order_by(act_col)
    t_sql_5 = t_sel_5.__sql__
    assert t_sql_5 == e_sql_5


def test_select_cols_limit() -> None:
    cols = ["colQ", "colR", "colS"]
    e_sql_6 = f"SELECT {", ".join(cols)} FROM tablename LIMIT 100"

    t_sel_6 = Select(*cols, from_table="tablename", limit=100)
    t_sql_6 = t_sel_6.__sql__
    assert t_sql_6 == e_sql_6


def test_select_cols_group() -> None:
    cols = ["colT", "colU", "colV"]
    act_col = cols[2]

    e_sql_7 = f"SELECT {", ".join(cols)} FROM tablename GROUP BY {act_col}"

    t_sel_7 = Select(*cols, from_table="tablename").group_by(act_col)
    t_sql_7 = t_sel_7.__sql__
    assert t_sql_7 == e_sql_7
