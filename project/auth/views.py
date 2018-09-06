from flask import Blueprint, request, jsonify, session, render_template, redirect
# from flask_login import current_user, login_user
from project.models import User
from .forms import RegistrationForm
from project import db

auth_blueprint = Blueprint('auth', __name__, template_folder='./templates')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User()
            print('----------')
            print(dir(form))
            form.populate_obj(user)
            # import code; code.interact(local=dict(globals(), **locals()))
            db.session.add(user)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            raise e


    return render_template('auth/show.html', form=form)

    # if request.method == 'POST':
    #     form = RegistrationForm(request.data)
    #     print(form)

    # print(current_user)
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    # if request.method == 'GET':
    #     return render_template('auth/login.html')
    # else:
    #     return ''
