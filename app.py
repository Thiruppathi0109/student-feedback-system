from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///feedback.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ---------------- MODELS ----------------
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    faculty = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<Course {self.name}>"


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(120), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comments = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    course = db.relationship('Course', backref='feedbacks')


# ---------------- ROUTES ----------------
@app.route('/')
def index():
    courses = Course.query.all()
    return render_template('index.html', courses=courses)


@app.route('/submit', methods=['GET', 'POST'])
def submit_feedback():
    courses = Course.query.all()
    if request.method == 'POST':
        student_name = request.form.get('student_name', '').strip()
        course_id = request.form.get('course_id')
        rating = request.form.get('rating')
        comments = request.form.get('comments', '').strip()

        if not student_name or not course_id or not rating:
            flash('Please fill all required fields.', 'error')
            return redirect(url_for('submit_feedback'))

        feedback = Feedback(
            student_name=student_name,
            course_id=int(course_id),
            rating=int(rating),
            comments=comments,
        )
        db.session.add(feedback)
        db.session.commit()
        flash('Feedback submitted successfully!', 'success')
        return redirect(url_for('submit_feedback'))

    return render_template('submit_feedback.html', courses=courses)


@app.route('/admin')
def admin():
    course_filter = request.args.get('course_id', type=int)
    query = Feedback.query
    if course_filter:
        query = query.filter_by(course_id=course_filter)
    feedbacks = query.order_by(Feedback.created_at.desc()).all()
    courses = Course.query.all()

    avg_ratings = {}
    for c in courses:
        ratings = [f.rating for f in c.feedbacks]
        avg_ratings[c.id] = round(sum(ratings) / len(ratings), 2) if ratings else None

    return render_template(
        'admin.html', feedbacks=feedbacks, courses=courses,
        avg_ratings=avg_ratings, selected_course=course_filter
    )


@app.route('/admin/delete/<int:feedback_id>', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    db.session.delete(feedback)
    db.session.commit()
    flash('Feedback deleted.', 'success')
    return redirect(url_for('admin'))


# health check endpoint - useful for CI/CD & deployment platforms
@app.route('/health')
def health():
    return {'status': 'ok'}, 200


def seed_data():
    """Add a few sample courses if DB is empty."""
    if Course.query.count() == 0:
        sample_courses = [
            Course(name='Data Structures', faculty='Dr. Meena'),
            Course(name='Operating Systems', faculty='Prof. Karthik'),
            Course(name='Web Development', faculty='Dr. Anitha'),
        ]
        db.session.add_all(sample_courses)
        db.session.commit()


with app.app_context():
    db.create_all()
    seed_data()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
