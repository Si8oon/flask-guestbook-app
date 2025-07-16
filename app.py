from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 🧠 Load and save functions
def load_entries():
    entries = []
    try:
        with open("guestbook.txt", "r") as f:
            for i, line in enumerate(f):
                name, message = line.strip().split("|")
                entries.append({"id": i, "name": name, "message": message})
    except FileNotFoundError:
        pass
    return entries

def save_entries(entries):
    with open("guestbook.txt", "w") as f:
        for entry in entries:
            f.write(f"{entry['name']}|{entry['message']}\n")

# 🏠 Home page with form
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        message = request.form.get("message")
        if name and message:
            entries = load_entries()
            entries.append({"name": name, "message": message})
            save_entries(entries)
            return redirect(url_for("entries_page"))
    return render_template("index.html")

# 📃 Show all entries
@app.route("/entries")
def entries_page():
    entries = load_entries()
    return render_template("entries.html", entries=entries)

# ❌ Delete an entry
@app.route("/delete/<int:entry_id>")
def delete_entry(entry_id):
    entries = load_entries()
    if 0 <= entry_id < len(entries):
        entries.pop(entry_id)
        save_entries(entries)
    return redirect(url_for("entries_page"))

# ✏️ Edit an entry
@app.route("/edit/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    entries = load_entries()
    if request.method == "POST":
        new_name = request.form.get("name")
        new_message = request.form.get("message")
        if new_name and new_message:
            entries[entry_id] = {"id": entry_id, "name": new_name, "message": new_message}
            save_entries(entries)
            return redirect(url_for("entries_page"))
    entry = entries[entry_id]
    return render_template("edit.html", entry=entry)

if __name__ == "__main__":
    app.run(debug=True)
