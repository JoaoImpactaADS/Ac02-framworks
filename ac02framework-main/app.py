import os
from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL


mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'senha123'
app.config['MYSQL_DATABASE_DB'] = 'teste'
app.config['MYSQL_DATABASE_HOST'] = '172.17.0.7'
#app.config['MYSQL_DATABASE_HOST'] = '172.17.0.7'
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _endereco = request.form['inputEndereco']

        print(_name)
        print(_email)
        print(_endereco)

        # validate the received values
        if _name and _email and _endereco:
            
            # All Good, let's call MySQL
            
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_endereco = _endereco
            cursor.callproc('sp_createUser',(_name,_email,_hashed_endereco))
            data = cursor.fetchall()
            print(data);

            if len(data) == 0:
                conn.commit()
            else:
                return json.dumps({'error':str(data[0])})

            return render_template('signup2.html', posts=data)
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()

@app.route('/list',methods=['POST','GET'])
def list():
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute ('select user_name from tbl_user')
            data = cursor.fetchall()
            print(data[0]);

            conn.commit()
            return render_template('signup2.html', datas=data)

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


    docker -compose up -d # Baixa o banco e roda junto com o aódigo
    docker exec -it /bin.bash id_container_banco


