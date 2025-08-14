#app19.py
# インデックスではなくUUID（識別子）でメモを管理
#メモに作成日時（created_at）を追加
#CSV形式で保存・読み込み
from flask import Flask, render_template, request,redirect,flash,url_for
import uuid
from datetime import datetime
import csv
import os

app =Flask(__name__)
app.secret_key ="sercret"  # 任意の文字列（メッセージ保存用）

FILENAME = "data.csv"

def load_notes():
    notes =[]   
    if not os.path.exists(FILENAME):
        return notes
    
    with open(FILENAME, newline='',encoding="utf-8")as csvfile:
        reader = csv.DictReader(csvfile)      
        for row in reader:
                notes.append({
                    "id": row["id"],
                    "name": row["name"],
                    "memo": row["memo"],
                    "created_at": row["created_at"],
                    "priority": row.get("priority", "")        
                })
             
    return notes

def save_notes(notes):
    with open(FILENAME, "w", newline='', encoding="utf-8")as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["id", "name", "memo", "created_at", "priority"])  # ヘッダー
        for note in notes:
            writer.writerow([
                note["id"],
                note["name"],
                note["memo"],
                note["created_at"],
                note.get("priority", "")  # 優先度
            ])
@app.route("/", methods=["GET", "POST"])
def index():

    notes = load_notes() # ← POSTの内側ではなく最初に呼ぶ！

    if request.method == "POST":
        name = request.form["name"].strip()
        memo = request.form["memo"].strip()
        priority = request.form.get("priority","") # 空文字でもOK

        if not name or not memo:
            flash("名前とメモを入力してください")
        else:
            note_id = str(uuid.uuid4())
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # メモ保存の辞書に追加
            notes.append({
                "id" : note_id ,
                "name": name,
                "memo": memo,
                "created_at":created_at,
                "priority": priority
                })
            save_notes(notes)
            flash("メモを保存しました")
            return redirect(url_for("index"))   
    
    
    return render_template("index15.html", notes=notes)

# 🆕 メモの編集フォームを表示
@app.route("/edit/<note_id>", methods=["GET", "POST"])
def edit(note_id):
    notes = load_notes()
    for note in notes:
        if note["id"] == note_id:
            if request.method == "POST":
                note["name"] = request.form["name"] 
                note["memo"] = request.form["memo"]
                note["priority"] = request.form.get("priority", "")
                save_notes(notes)
                flash("メモを更新しました")
                return redirect(url_for("index"))
            return render_template("edit3.html", note=note)
    flash("メモが見つかりません")
    return redirect(url_for("index"))

# メモの削除
@app.route("/delete/<note_id>")
def delete(note_id):
    notes = load_notes()
    updated_notes = [note for note in notes if note["id"] != note_id]
    if len(updated_notes) < len(notes):
        save_notes(updated_notes)
        flash("メモを削除しました")       
    else:
        flash("削除対象のメモが見つかりません")
    return redirect(url_for("index"))

if __name__=="__main__":
    app.run(debug = True)