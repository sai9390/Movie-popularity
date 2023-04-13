from flask import Flask, render_template, request,flash
import pandas as pd
from flask import Response
import csv
from flask import session
from DBConnection import DBConnection
import sys
from CBMR import movie_recommends
from TargetAudience import audience_prediciton
from MoviePopularity import movie_hit_prediciton

app = Flask(__name__)
app.secret_key = "abc"


cbmrs_list=[]

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signin')
def signin():
    return render_template('user_signin.html')


@app.route('/user_home')
def user_home():
    return render_template('user_home.html')


@app.route('/signup')
def signup():
    return render_template('user_signup.html')





@app.route('/registering',methods =["GET", "POST"])
def registering():
    try:
        name = request.form.get('name')
        uid = request.form.get('uid')
        pwd = request.form.get('pwd')
        email = request.form.get('email')
        mno = request.form.get('mno')

        database = DBConnection.getConnection()
        cursor = database.cursor()
        sql = "select count(*) from register where userid='" + uid + "'"
        cursor.execute(sql)
        res = cursor.fetchone()[0]
        if res > 0:

            return render_template("user_signup.html", messages="User Id already exists..!")

        else:
            sql = "insert into register values(%s,%s,%s,%s,%s)"
            values = (name, uid, pwd, email, mno)
            cursor.execute(sql, values)
            database.commit()

        return render_template("user_signin.html", messages="Registered Successfully..! Login Here.")
    except Exception as e:
        print(e)
    return render_template('user_signin.html')



@app.route("/logincheck",methods =["GET", "POST"])
def userlogin():
        uid = request.form.get("unm")
        pwd = request.form.get("pwd")
        print(uid,pwd)
        database = DBConnection.getConnection()
        cursor = database.cursor()
        sql = "select count(*) from register where userid='" + uid + "' and passwrd='" + pwd + "'"
        cursor.execute(sql)
        res = cursor.fetchone()[0]
        if res > 0:
            session['uid'] = uid

            return render_template("user_home.html")
        else:

            return render_template("user_signin.html",msg="Invalid Credentials")



        return render_template("admin.html")





@app.route('/movie_recommend')
def movie_recommend():
    return render_template('movie_recommends.html')


@app.route('/cbm_recommends', methods=["GET", "POST"])
def cbm_recommends():
    try:
        uid = session['uid']
        movie_content = request.form.get('content')
        cbmr_list=movie_recommends(movie_content)
        session["cbmrs_list"]=cbmr_list

    except Exception as e:
        print(e)

    return render_template('cbmrecommendation_results.html', results=cbmr_list)


@app.route('/movie_popularity')
def movie_popularity():
    results=[]
    cbmr_list=session["cbmrs_list"]

    for cmrelist in cbmr_list:
        movie_name=cmrelist[0]
        print(movie_name)
        print(cmrelist[1])
        hit_prediction=movie_hit_prediciton(movie_name)
        print("pre=",hit_prediction[0])
        hpre=hit_prediction[0]

        if hpre==0:
            result="F"
        elif hpre==1:
            result="A"
        elif hpre == 2:
            result = "AA"
        elif hpre == 3:
            result = "H"
        elif hpre == 4:
            result = "SH"
        else:
           result = "SDH"

        results.append([movie_name,cmrelist[1],cmrelist[2],cmrelist[3],result])


    return render_template('movie_hit_prediction_results.html',results=results)




@app.route('/target_audience')
def target_audience() :
    results=[]
    cbmr_list=session["cbmrs_list"]

    for cmrelist in cbmr_list:
        movie_name=cmrelist[0]
        print(movie_name)
        print(cmrelist[1])
        ta_prediction=audience_prediciton(movie_name)
        print("pre=",ta_prediction[0])
        predict_res=ta_prediction[0]

        if predict_res==1:
            result="Junior"
        elif predict_res==2:
            result="Teenage"
        elif predict_res == 3:
            result = "Mid-age"
        else:
           result = "Senior"

        results.append([movie_name,cmrelist[1],cmrelist[2],cmrelist[3],result])


    return render_template('target_audience_prediction_results.html',results=results)


if __name__ == '__main__':
    app.run(host="localhost", port=1579, debug=True)
