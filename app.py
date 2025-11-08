from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ✅ Secret key required for flash messages
app.secret_key = "supersecretkey"

# ✅ Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ✅ Initialize Database
db = SQLAlchemy(app)

# ✅ Create Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll = db.Column(db.String(20), nullable=False)
    student_class = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Student {self.name}>"

# 🏠 Home Page – Show All Students
@app.route('/')
def home():
    students = Student.query.all()
    return render_template('index.html', std=students)

# ➕ Add Student
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        student_class = request.form['class']
        email = request.form['email']

        new_student = Student(name=name, roll=roll, student_class=student_class, email=email)
        db.session.add(new_student)
        db.session.commit()

        flash("✅ Student added successfully!", "success")
        return redirect(url_for('home'))
    
    return render_template('add.html')

# ✏️ Edit Student
@app.route('/update/<int:student_id>', methods=['GET', 'POST'])
def update_student(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.roll = request.form['roll']
        student.student_class = request.form['class']
        student.email = request.form['email']
        db.session.commit()

        flash("✏️ Student details updated successfully!", "info")
        return redirect(url_for('home'))
    
    return render_template('update.html', student=student)

# 🗑️ Delete Student
@app.route('/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()

    flash("🗑️ Student deleted successfully!", "danger")
    return redirect(url_for('home'))

# 📄 About Page
@app.route('/about')
def about():
    return render_template('about.html')

# 📞 Contact Page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# 📞 Services Page
@app.route('/services')
def services():
    return render_template('services.html')

# 🚀 Run Flask App
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # ✅ Creates students.db and Student table
    app.run(debug=True)
