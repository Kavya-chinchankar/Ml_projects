from flask import Flask, render_template,request,redirect,url_for
import sqlite3
import pickle
import numpy as np
import os 

currentdirectory = os.path.dirname(os.path.abspath(__file__))

# con = sqlite3.connect('rext.db')
# cr=con.cursor()

connection = sqlite3.connect(currentdirectory + "file.db")   
cursor = connection.cursor()


popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_score.pkl','rb'))

app = Flask(__name__)


@app.route('/')
def home():
     return render_template('home.html')

@app.route('/explore')
def explore():
     return render_template('login.html')

@app.route('/login')
def login():
     return render_template('login.html')

@app.route('/register')
def register():
     return render_template('register.html')

@app.route('/enter')
def enter():
     return render_template('index.html')

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


cursor.execute("create table if not exists sign_up( id integer primary key,fname TEXT,lname TEXT,email TEXT,username TEXT,password TEXT)")

# @app.route('/sign_up', methods=['POST','GET'])
# def sign_up():
#     if request.method == 'POST':
#         con = sqlite3.connect('file.db')
#         cr=con.cursor()

#         fname=request.form['fname'] 
#         lname=request.form['lname'] 
#         email=request.form['email'] 
#         username=request.form['uname'] 
#         password=request.form['password']  
#         print(fname,lname,email,username,password)
#         List=[fname,lname,email,username,password]
#         cr.execute("insert into sign_up(fname,lname,email,username,password) values(?,?,?,?,?,?)",List)
#         con.commit()
#         return render_template('home.html')
#     return render_template('home.html')


@app.route('/sign_up', methods=['POST'])
def sign_up():
    if request.method == 'POST':

        fname=request.form['fname'] 
        lname=request.form['lname'] 
        email=request.form['email'] 
        username=request.form['username'] 
        password=request.form['password'] 

        connection = sqlite3.connect(currentdirectory + "file.db")   
        cursor = connection.cursor()
      
        query1 = "INSERT INTO sign_up VALUES('{fn}',{ln},{e},{user},{passw})".format(fn = fname, ln = lname, e = email, user = username, passw = password )

        connection.commit()

        return render_template('home.html')
    else:
        return render_template('home.html')


@app.route('/sign_in', methods=['POST'])
def sign_in():
    try:
        if request.method == 'POST':
            username=request.form['username'] 
            password=request.form['password']

            connection = sqlite3.connect(currentdirectory + "file.db")   
            cursor = connection.cursor()
       
            query1 = "SELECT * from sign_up WHERE  username = {user},{passw}".format(user = username, passw = password)
            result = cursor.execute(query1)
            result = result.fetchall()[0][0]

            return render_template('index.html', result=result)
        
    except:
        return render_template('home.html', msg="enterd wrong username or password")
    return render_template('home.html')

    




# @app.route('/sign_in', methods=['POST','GET'])
# def sign_in():
#     if request.method == 'POST':
#         con = sqlite3.connect('file.db')
#         cr=con.cursor()
#         username=request.form['username']
#         password=request.form['password']
#         print("username,password")
#         cr.execute("select * from sign_up where username = '"+username+"' and password = '"+password+"'")    
#         result = cr.fetchall()
#         if result:
#             cr.execute("select * from sign_up") 
#             value =cr.fetchall()
#             print(value)
#             return render_template('index.html', value=value)
#         else:
#             return render_template('home.html', msg="enterd wrong username or password")
#     return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_ratings'].values)
                           )



@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)