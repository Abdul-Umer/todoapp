from flask import Flask, render_template, request,redirect,url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "my_secretkey"

# MySQL Configuration (✅ FIXED config keys)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'tododb'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/task/create', methods=['GET', 'POST'])
def createtask():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        tid = request.form['tid']
        name = request.form['name']
        status = request.form['status']
        priority = request.form['priority']

        cur.execute("INSERT INTO task (tid, name, status, priority) VALUES (%s, %s, %s, %s)",(tid, name, status, priority))
        mysql.connection.commit()

        cur.close()
        return "Task Added Successfully!"

    cur.execute("SELECT * FROM task")
    task = cur.fetchall()
    cur.close()

    return render_template("createtask.html", tasks=task)

@app.route('/task/update/<int:tid>',methods=['POST','GET'])
def update_task(tid):
    cur=mysql.connection.cursor()
    if request.method=='POST':
        name=request.form['name']
        status=request.form['status']
        priority=request.form['priority']

        cur.execute("update task set name=%s,status=%s,priority=%s where tid=%s",(name,status,priority,tid,))
        mysql.connection.commit()
        cur.close()
        return "Changes Done Successful"
    
    cur.execute("Select * from task where tid=%s",(tid,))
    task=cur.fetchone()
    cur.close()
    if task:
        return render_template("edittask.html",task=task)
    else:
        return "Task not found",404

@app.route('/task/delete/<int:tid>',methods=['GET','POST'])
def deletetask(tid):
    cur=mysql.connection.cursor()
    cur.execute("select * from task where tid=%s",(tid,))
    task=cur.fetchone()
    if request.method=='POST':
        if task:
            cur.execute("Delete from task where tid=%s",(tid,))
            mysql.connection.commit()
            task_name=task[1]
            cur.close()
            return f"Task {task_name} deleted successfully"
        else:
            cur.close()
            return "Task not found",404 
    cur.close()
    if task:
        return render_template('deletetask.html',task=task)
    else:
        return f'Task not found',404
    

    
@app.route('/task/viewtasks',methods=['POST','GET'])
def view_tasks():
    cur=mysql.connection.cursor()
    cur.execute("Select * from task")
    tasks=cur.fetchall()
    if tasks:
        return render_template('viewtasks.html',tasks=tasks)
    else:
        return f"No task found",404

@app.route('/task/complete')
def completedTasks():
    status='complete'
    cur=mysql.connection.cursor()
    cur.execute("Select name,status from task where status=%s ",(status,))
    tasks=cur.fetchall()
    if tasks:
        return render_template("completedTasks.html",tasks=tasks)
    else:
        return f"No task",404



@app.route('/add/<int:a>,<int:b>,<int:c>')
def add(a,b,c):
    return str(a)+str(b)+str(c)

if __name__ == "__main__":
    app.run(debug=True)
