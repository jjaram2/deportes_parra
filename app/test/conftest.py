from app import create_app, db
try:
    import pytest
except ImportError:
    pytest = None

@pytest.fixture
def app_instance():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
  

@pytest.fixture
@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
@pytest.fixture
def user_fixture():
    from app.models.users import Users
    user = Users(nameUser="test_user", passwordUser="test_password")
    db.session.add(user)
    db.session.commit()
    yield user