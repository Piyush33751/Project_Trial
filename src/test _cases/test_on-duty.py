# tests/test_on_duty_query.py
import pytest
from sqlalchemy import create_engine, text

# Your original SQL (kept verbatim; run in setup)
CREATE_TABLE_SQL = """
CREATE TABLE firefighters_info (
    name VARCHAR(50),
    area VARCHAR(50),
    status VARCHAR(20),
    password VARCHAR(10)
);
"""

INSERT_ROWS_SQL = """
INSERT INTO firefighters_info (name, area, status, password) VALUES
('Sam Ng', 'Yishun', 'On-Duty', '1234'),
('Jayden Tan', 'Jurong', 'On-Duty', '1234'),
('Javier Liew', 'Serangoon', 'On-Duty', '1234'),
('Nikhil', 'Harbourfront', 'On-Duty', '1234'),
('Kayden Koo', 'Tampines', 'On-Duty', '1234'),
('Ben Chen', 'Canberra', 'On-Duty', '1234'),
('Ali', 'Bedok', 'Off-Duty', '1234'),
('Irfan', 'Pioneer', 'Off-Duty', '1234'),
('Kester Kwan', 'Tiong Bahru', 'Off-Duty', '1234'),
('Dennis Ho', 'Yew Tee', 'Off-duty', '1234');
"""

SELECT_ON_DUTY_SQL = """
SELECT * FROM firefighters_info
WHERE status = 'On-Duty';
"""

@pytest.fixture()
def conn():
    """
    In-memory SQLite DB for the test. We run your SQL to create the table
    and seed the exact rows provided.
    """
    engine = create_engine("sqlite:///:memory:", future=True)
    with engine.begin() as conn:
        # run DDL + seed data
        conn.exec_driver_sql(CREATE_TABLE_SQL)
        conn.exec_driver_sql(INSERT_ROWS_SQL)
    # yield a new connection in autocommit mode for the assertions
    with engine.connect() as c:
        yield c

def test_select_only_on_duty_returns_expected_names(conn):
    # Execute your exact SELECT
    rows = conn.execute(text(SELECT_ON_DUTY_SQL)).fetchall()

    # Expect 6 on-duty records (the last row is 'Off-duty' with lowercase 'd')
    assert len(rows) == 6

    # Column order is (name, area, status, password) per your CREATE TABLE
    names = {r[0] for r in rows}
    assert names == {
        "Sam Ng",
        "Jayden Tan",
        "Javier Liew",
        "Nikhil",
        "Kayden Koo",
        "Ben Chen",
    }

    # Ensure Off-Duty folks are not present
    off_duty_names = {"Ali", "Irfan", "Kester Kwan", "Dennis Ho"}
    assert names.isdisjoint(off_duty_names)

def test_case_sensitivity_note(conn):
    """
    Optional: show that the query is case-sensitive on the literal.
    'Off-duty' (lowercase d) is not matched by 'On-Duty', so it's fine here.
    This test just documents behavior and protects against accidental changes.
    """
    off_duty_all = conn.execute(
        text("SELECT name, status FROM firefighters_info WHERE status LIKE '%Off%'")
    ).fetchall()
    # We should see 3 'Off-Duty' + 1 'Off-duty'
    statuses = [s for _, s in off_duty_all]
    assert statuses.count("Off-Duty") == 3
    assert statuses.count("Off-duty") == 1
