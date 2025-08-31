import types
import pytest

# Import your app module (change this import if your file isn't named app.py)
import app as app_module


@pytest.fixture
def client(monkeypatch):
    """
    - Switch app to TESTING mode
    - Use SQLite in memory instead of MySQL
    - Create tables and seed minimal data
    - Fake render_template to avoid needing real HTML files
    Returns: Flask test client
    """
    flask_app = app_module.app
    db = app_module.db
    Firefighter = app_module.Firefighter

    # Testing config + in-memory DB
    flask_app.testing = True
    flask_app.config.update(
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # Fake render_template to a simple string: "rendered:<template>|data:<csv names>"
    def _fake_render(template_name, **ctx):
        rendered = f"rendered:{template_name}"
        if "data" in ctx and ctx["data"] is not None:
            try:
                names = ",".join([f.name for f in ctx["data"]])
            except Exception:
                names = str(ctx["data"])
            rendered += f"|data:{names}"
        return rendered

    monkeypatch.setattr(app_module, "render_template", _fake_render)

    # Build schema + seed rows
    with flask_app.app_context():
        # make sure engine reflects updated URI
        db.engine.dispose()
        db.drop_all()
        db.create_all()

        # Seed: a few on-duty + off-duty entries
        db.session.add_all([
            Firefighter(name="Sam Ng", area="Yishun",     status="On-Duty",  password="1234"),
            Firefighter(name="Jayden Tan", area="Jurong", status="On-Duty",  password="1234"),
            Firefighter(name="Ali", area="Bedok",         status="Off-Duty", password="1234"),
            Firefighter(name="Irfan", area="Pioneer",     status="Off-Duty", password="1234"),
        ])
        db.session.commit()

    # Return a test client
    client = flask_app.test_client()
    yield client

    # Teardown (clean DB)
    with flask_app.app_context():
        db.session.remove()
        db.drop_all()


# ---- Simple route tests (no DB context required) ----

def test_home_renders(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"rendered:index.html" in resp.data

def test_page2_renders(client):
    resp = client.get("/page2.html")
    assert resp.status_code == 200
    assert b"rendered:page2.html" in resp.data

def test_page3_renders(client):
    resp = client.get("/page3.html")
    assert resp.status_code == 200
    assert b"rendered:page3.html" in resp.data

def test_page4_renders(client):
    resp = client.get("/page4.html")
    assert resp.status_code == 200
    assert b"rendered:page4.html" in resp.data


# ---- DB-backed pages ----

def test_page5_lists_on_duty_only(client):
    resp = client.get("/page5.html")
    assert resp.status_code == 200
    body = resp.data.decode()

    # Our fake renderer includes names after "|data:"
    assert "rendered:page5.html" in body
    assert "|data:" in body

    # On-Duty names present
    assert "Sam Ng" in body
    assert "Jayden Tan" in body

    # Off-Duty names should NOT be in the On-Duty page
    assert "Ali" not in body
    assert "Irfan" not in body


def test_page6_lists_off_duty_only(client):
    resp = client.get("/page6.html")
    assert resp.status_code == 200
    body = resp.data.decode()

    assert "rendered:page6.html" in body
    assert "|data:" in body

    # Off-Duty names present
    assert "Ali" in body
    assert "Irfan" in body

    # On-Duty names should NOT be in the Off-Duty page
    assert "Sam Ng" not in body
    assert "Jayden Tan" not in body
