from flask import abort
from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from database import db_session
from models import Team
from models import User
from forms import UserForm
from forms import TeamForm
import stackalytics

dashboard = Blueprint('dashboard', __name__)

# Index


@dashboard.route('/', methods=['GET', 'POST'])
def dashboard_index():
    if request.method == 'POST':
        release = request.form.get('release')
        project_type = request.form.get('project_type')
        metric = request.form.get('type')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        team_id = request.form.get('team')
        module = request.form.get('module', 'All')
        # we pass to stackalytics None
        pass_module = None if module == 'all' else module
        team = Team.query.get(team_id)
        list_users = [user.user_id for user in team.users]

        users = stackalytics.get_status_from_users(
             list_users, 'Intel', project_type, release, module=pass_module, start_date=start_date, end_date=end_date)
        # stackalytics dont return user name
        for u in users:
            for usr in team.users:
                if u["user"] == usr.user_id:
                    u['name'] = usr.name
                    break
        return render_template('index.html', users=users, metric=metric,
                               release=release, team_id=team_id,
                               module=module,
                               start_date=start_date, end_date=end_date,
                               project_type=project_type)
    else:
        return render_template('index.html')

# Teams


@dashboard.route('/teams/')
def dashboard_teams():
    teams = Team.query.all()
    return render_template('list_teams.html', teams=teams)


@dashboard.route('/teams/<int:team_id>/edit/', methods=['GET', 'POST'])
def dashboard_edit_team(team_id):
    team = Team.query.get(team_id)
    if team is None:
        abort(404)
    form = TeamForm(request.form, team)
    if request.method == 'POST' and form.validate():
        team.name = form.name.data
        users_in = request.form.getlist('selected-users')
        users_out = request.form.getlist('available-users')

        users = User.query.filter(User.id.in_(users_in)).all()
        for user in users:
            if user not in team.users:
                team.users.append(user)

        users = User.query.filter(User.id.in_(users_out)).all()
        for user in users:
            if user in team.users:
                team.users.remove(user)

        return redirect(url_for('dashboard.dashboard_teams'))
    return render_template('create_team.html', form=form, team_id=team_id)


@dashboard.route('/teams/create/', methods=['GET', 'POST'])
def dashboard_create_team():
    form = TeamForm(request.form)
    if request.method == 'POST' and form.validate():
        team = Team()
        team.name = form.name.data
        user_ids = request.form.getlist('selected-users')
        users = User.query.filter(User.id.in_(user_ids)).all()
        for user in users:
            team.users.append(user)
        db_session.add(team)
        db_session.commit()
        return redirect(url_for('dashboard.dashboard_teams'))
    return render_template('create_team.html', form=form)


# Users


@dashboard.route('/users/', methods=['GET', 'POST'])
def dashboard_users():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        user = User()
        user.name = user_name
        db_session.add(user)
        db_session.commit()

    users = User.query.all()
    return render_template('list_users.html', users=users)


@dashboard.route('/users/create/', methods=['GET', 'POST'])
def dashboard_create_user():
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        user.user_id = form.user_id.data
        user.name = form.name.data
        user.email = form.email.data
        db_session.add(user)
        db_session.commit()
        return redirect(url_for('dashboard.dashboard_users'))
    return render_template('create_user.html', form=form)
