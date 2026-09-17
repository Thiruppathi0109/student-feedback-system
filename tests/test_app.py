import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db, Course, Feedback  # noqa: E402


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        c = Course(name='Test Course', faculty='Test Faculty')
        db.session.add(c)
        db.session.commit()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_health(client):
    res = client.get('/health')
    assert res.status_code == 200
    assert res.get_json()['status'] == 'ok'


def test_index_loads(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b'Student Feedback System' in res.data


def test_submit_feedback_get(client):
    res = client.get('/submit')
    assert res.status_code == 200


def test_submit_feedback_post(client):
    course = Course.query.first()
    res = client.post('/submit', data={
        'student_name': 'Yuvraj',
        'course_id': course.id,
        'rating': '5',
        'comments': 'Great course!'
    }, follow_redirects=True)
    assert res.status_code == 200
    assert Feedback.query.count() == 1


def test_admin_page(client):
    res = client.get('/admin')
    assert res.status_code == 200
