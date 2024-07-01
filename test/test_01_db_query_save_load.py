from sfos.db import Select


def test_select_all_dict() -> None:
    # time.sleep(1)
    t_sel_8 = Select(from_table="tablename")

    t_dict_8 = t_sel_8.__dict__
    e_dict_8 = {
        "columns": None,
        "from_table": "tablename",
        "distinct": False,
        "where": [],
        "order": [],
        "group": [],
        "limit": None,
    }
    assert t_dict_8 == e_dict_8


def test_save_and_load() -> None:
    e_sql_9 = "SELECT colA, colB, colC FROM tablename WHERE colA is not ? AND colB = ?"
    e_params_9 = ["test value", "test value 2"]
    c_dict_9 = {
        "columns": ["colA", "colB", "colC"],
        "from_table": "tablename",
        "distinct": False,
        "where": [
            {
                "column": "colA",
                "operator": "is not",
                "criteria": "test value",
            },
            {
                "column": "colB",
                "operator": "=",
                "criteria": "test value 2",
            },
        ],
    }
    e_dict_9 = {
        "columns": ["colA", "colB", "colC"],
        "from_table": "tablename",
        "distinct": False,
        "where": [
            {
                "column": "colA",
                "operator": "is not",
                "criteria": "test value",
            },
            {
                "column": "colB",
                "operator": "=",
                "criteria": "test value 2",
            },
        ],
        "order": [],
        "group": [],
        "limit": None,
    }

    t_sel_9 = Select(from_dict=c_dict_9)
    t_dict_9 = t_sel_9.__dict__
    t_sql_9 = t_sel_9.__sql__
    t_params_9 = t_sel_9._params

    assert t_sql_9 == e_sql_9
    assert t_params_9 == e_params_9
    assert t_dict_9 == e_dict_9
