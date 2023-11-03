from duckdb_kernel.parser import DCParser
from . import Connection


def test_simple_queries():
    with Connection() as con:
        for query in [
            '{ id | users(id, _) }',
            '{ id | users (id, _) }',
            '{ id | users id,_ }',
            '{id|users(id,_)}',
            'id | users (id ,_)',
        ]:
            root = DCParser.parse_query(query)
            assert con.execute_dc(root) == [
                (1,),
                (2,),
                (3,)
            ]

        for query in [
            '{ id, name | users(id, name) }',
            '{ id,name | users(id, name) }'
        ]:
            root = DCParser.parse_query(query)
            assert con.execute_dc(root) == [
                (1, 'Alice'),
                (2, 'Bob'),
                (3, 'Charlie')
            ]


def test_conditions():
    with Connection() as con:
        for query in [
            '{ name | users(id, name) ∧ id > 1 }',
            '{ name | users(id, name) ∧ id ≠ 1 }',
            '{ name | users(id, name) ∧ (id = 2 ∨ id = 3) }'
        ]:
            root = DCParser.parse_query(query)
            assert con.execute_dc(root) == [
                ('Bob',),
                ('Charlie',)
            ]

        for query in [
            '{ id | users(id, name) ∧ name > "B" ∧ name < "C" }'
        ]:
            root = DCParser.parse_query(query)
            assert con.execute_dc(root) == [
                (2,)
            ]


def test_shortcut_conditions():
    with Connection() as con:
        # single shortcut conditions
        for query in [
            '{ name | users(1, name) }'
        ]:
            root = DCParser.parse_query(query)
            assert con.execute_dc(root) == [
                ('Alice',)
            ]

        for query in [
            '{ season_name | seasons(1, 1, season_name) }'
        ]:
            root = DCParser.parse_query(query)
            assert con.execute_dc(root) == [
                ('Show 1 / Season 1',)
            ]

        # multiple shortcut conditions
        for query in [
            '{ sname, ename | seasons(snum, 2, sname) ∧ episodes(enum, snum, 2, ename) }'
        ]:
            root = DCParser.parse_query(query)
            assert con.execute_dc(root) == [
                ('Show 2 / Season 1', 'Show 2 / Season 1 / Episode 1'),
                ('Show 2 / Season 1', 'Show 2 / Season 1 / Episode 2'),
                ('Show 2 / Season 1', 'Show 2 / Season 1 / Episode 3'),
                ('Show 2 / Season 2', 'Show 2 / Season 2 / Episode 1'),
                ('Show 2 / Season 2', 'Show 2 / Season 2 / Episode 2'),
                ('Show 2 / Season 2', 'Show 2 / Season 2 / Episode 3'),
                ('Show 2 / Season 2', 'Show 2 / Season 2 / Episode 4')
            ]


def test_joins():
    with Connection() as con:
        # with one attribute
        for query in [
            '{ sename | shows(shid, shname) ∧ seasons(senum, shid, sename) }'
        ]:
            root = DCParser.parse_query(query)
            assert con.execute_dc(root) == [
                ('Show 1 / Season 1',),
                ('Show 1 / Season 2',),
                ('Show 2 / Season 1',),
                ('Show 2 / Season 2',)
            ]

        for query in [
            '{ sename | shows(shid, shname) ∧ seasons(senum, shid, sename) ∧ shname = "Show 1" }',
            '{ sename | seasons(senum, shid, sename) ∧ shows(shid, "Show 1") }'
        ]:
            root = DCParser.parse_query(query)
            assert con.execute_dc(root) == [
                ('Show 1 / Season 1',),
                ('Show 1 / Season 2',)
            ]

        # with multiple attributes
        for query in [
            '{ sname, ename | seasons(snum, shid, sname) ∧ episodes(enum, snum, shid, ename) ∧ shid = 2 }'
        ]:
            root = DCParser.parse_query(query)
            assert con.execute_dc(root) == [
                ('Show 2 / Season 1', 'Show 2 / Season 1 / Episode 1'),
                ('Show 2 / Season 1', 'Show 2 / Season 1 / Episode 2'),
                ('Show 2 / Season 1', 'Show 2 / Season 1 / Episode 3'),
                ('Show 2 / Season 2', 'Show 2 / Season 2 / Episode 1'),
                ('Show 2 / Season 2', 'Show 2 / Season 2 / Episode 2'),
                ('Show 2 / Season 2', 'Show 2 / Season 2 / Episode 3'),
                ('Show 2 / Season 2', 'Show 2 / Season 2 / Episode 4')
            ]

        # join three relations
        for query in [
            '{ s2,c5 | shows(s1,s2) ∧ episodes(e1,e2,s1,e4) ∧ characters(c1,e1,c3,s1,c5) ∧ s1=2 ∧ e4="Show 2 / Season 1 / Episode 2" }'
        ]:
            root = DCParser.parse_query(query)
            assert con.execute_dc(root) == [
                ('Show 2', 'Actor F')
            ]


def test_underscores():
    with Connection() as con:
        # distinct underscores
        for query in [
            '{ ename | seasons(snum, shid, sname) ∧ episodes(_, snum, shid, ename) ∧ shid = 2 }',
            '{ ename | seasons(snum, shid, sname) ∧ episodes(enum, _, shid, ename) ∧ shid = 2 }',
            '{ ename | seasons(snum, shid, sname) ∧ episodes(__, snum, shid, ename) ∧ shid = 2 }',
            '{ ename | seasons(snum, shid, sname) ∧ episodes(_, __, shid, ename) ∧ shid = 2 }'
        ]:
            root = DCParser.parse_query(query)
            assert con.execute_dc(root) == [
                ('Show 2 / Season 1 / Episode 1',),
                ('Show 2 / Season 1 / Episode 2',),
                ('Show 2 / Season 1 / Episode 3',),
                ('Show 2 / Season 2 / Episode 1',),
                ('Show 2 / Season 2 / Episode 2',),
                ('Show 2 / Season 2 / Episode 3',),
                ('Show 2 / Season 2 / Episode 4',)
            ]

        # reused underscores in a single relation
        for query in [
            '{ ename | seasons(snum, shid, sname) ∧ episodes(_, _, shid, ename) ∧ shid = 2 }'
        ]:
            root = DCParser.parse_query(query)
            assert con.execute_dc(root) == [
                ('Show 2 / Season 1 / Episode 1',),
                ('Show 2 / Season 1 / Episode 2',),
                ('Show 2 / Season 1 / Episode 3',),
                ('Show 2 / Season 2 / Episode 1',),
                ('Show 2 / Season 2 / Episode 2',),
                ('Show 2 / Season 2 / Episode 3',),
                ('Show 2 / Season 2 / Episode 4',)
            ]

        # reused underscores in two different relations
        for query in [
            '{ ename | seasons(_, shid, _) ∧ episodes(_, _, shid, ename) ∧ shid = 2 }',
            '{ ename | seasons(_, shid, __) ∧ episodes(_, __, shid, ename) ∧ shid = 2 }'
        ]:
            root = DCParser.parse_query(query)
            assert con.execute_dc(root) == [
                ('Show 2 / Season 1 / Episode 1',),
                ('Show 2 / Season 1 / Episode 2',),
                ('Show 2 / Season 1 / Episode 3',),
                ('Show 2 / Season 2 / Episode 1',),
                ('Show 2 / Season 2 / Episode 2',),
                ('Show 2 / Season 2 / Episode 3',),
                ('Show 2 / Season 2 / Episode 4',)
            ]
