from datetime import datetime
from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///journal.db'
db = SQLAlchemy(app)

class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        entry = request.form['journal_entry']
        new_entry = JournalEntry(entry=entry)
        db.session.add(new_entry)
        db.session.commit()
        return 'Journal entry submitted!'
    else:
        return render_template('index.html')

@app.route('/export')
def export_entries():
    entries = JournalEntry.query.all()
    filename = 'journal_entries.txt'
    with open(filename, 'w') as file:
        for entry in entries:
            file.write(f'{entry.date}\n\n{entry.entry}\n\n')
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
