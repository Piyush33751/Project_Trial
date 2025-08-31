import pytest
from sqlalchemy import create_engine, text, Column, String
from sqlalchemy.orm import declarative_base, Session

# --- Define the same table structure ---
Base = declarative_base()

class Firefighter(Base):
    __tablename__ = "firefighters_info"
    name = Column(String(50), primary_key=True)
    area = Column(String(50))
    status = Column(String(20))
    password = Column(String(10))


@pytest.fixture()
def session():
    """Creates an in-memory SQLite DB with firefighters_info table + sample data"""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        # Insert seed rows
        session.add_all([
            Firefighter(name="Alice", area="North", status="On-Duty", password="123"),
            Firefighter(name="Bob", area="South", status="Off-Duty", password="abc"),
            Firefighter(name="Charlie", area="East", status="Off-Duty", password="xyz"),
        ])
        session.commit()
        yield session


def test_select_off_duty_firefighters(session):
    # Run the same SQL you showed
    result = session.execute(
        text("SELECT * FROM firefighters_info WHERE status = 'Off-Duty';")
    ).fetchall()

    # We expect Bob and Charlie
    names = [row[0] for row in result]  # row[0] = name column
    assert "Bob" in names
    assert "Charlie" in names
    assert "Alice" not in names


def test_select_off_duty_with_orm(session):
    # ORM version of the same query
    off_duty = session.query(Firefighter).filter(Firefighter.status == "Off-Duty").all()

    names = [f.name for f in off_duty]
    assert set(names) == {"Bob", "Charlie"}
