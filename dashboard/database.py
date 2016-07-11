from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///dashboard.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()



# team information
teams = {}

def read_config(conf_file='./usr.list'):
    with open(conf_file) as f:
        team_name = ''
        for s in f.readlines():
            s = s.strip('\n')
            if s.startswith('['):
                s = s.strip('[')
                s = s.strip(']')
                teams.update({s: []})
                team_name = s
            else:
                if len(team_name) < 1:
                    raise
                if s:
                    teams[team_name].append(s)


# Populating user from config
def populat_user_from_config():
    '''
        return a list of Team users
    '''
    import models

    model_users = []
    for t in teams:
        for u in teams[t]:
            u.strip()
            user = models.User()
            user.name = u.split(':')[0].strip()
            user.user_id = u.split(':')[1].strip()
            user.email = 'fake@test.com'
            model_users.append(user)

    return model_users

# Populating team from config
def populat_team_from_config():
    '''
        return a list of Team modle
    '''
    import models

    model_teams = []
    for t in teams:
        model_t = models.Team()
        model_t.name = t
        for u in teams[t]:
            u.strip()
            user = models.User()
            user.name = u.split(':')[0].strip()
            user.user_id = u.split(':')[1].strip()
            user.email = 'fake@test.com'
            model_t.users.append(user)

        model_teams.append(model_t)

    return model_teams



def init_db():
    import models
    # read config for user informations
    read_config()

    # Creating tables
    Base.metadata.create_all(bind=engine)

    # Populating Release table
    release = models.Release()
    release.name = 'All'
    db_session.add(release)

    release = models.Release()
    release.name = 'Newton'
    db_session.add(release)

    release = models.Release()
    release.name = 'Mitaka'
    db_session.add(release)

    release = models.Release()
    release.name = 'Liberty'
    db_session.add(release)

    release = models.Release()
    release.name = 'Kilo'
    db_session.add(release)

    release = models.Release()
    release.name = 'Juno'
    db_session.add(release)

    release = models.Release()
    release.name = 'Icehouse'
    db_session.add(release)

    release = models.Release()
    release.name = 'Havana'
    db_session.add(release)

    release = models.Release()
    release.name = 'Grizzly'
    db_session.add(release)

    release = models.Release()
    release.name = 'Folsom'
    db_session.add(release)

    release = models.Release()
    release.name = 'Essex'
    db_session.add(release)

    release = models.Release()
    release.name = 'Diablo'
    db_session.add(release)

    release = models.Release()
    release.name = 'Cactus'
    db_session.add(release)

    release = models.Release()
    release.name = 'Bexar'
    db_session.add(release)

    release = models.Release()
    release.name = 'Austin'
    db_session.add(release)
    db_session.commit()

    # Populating User table
    for usr in populat_user_from_config():
        db_session.add(usr)

    db_session.commit()

    # fake team intel
    team_intel = models.Team()
    team_intel.name = 'Intel'
    user = models.User()
    user.name = 'intel'
    user.user_id = 'intel'
    user.email = 'intel@intel.com'
    team_intel.users.append(user)

    db_session.add(team_intel)
    db_session.commit()

    # Populating team from config
    for team in populat_team_from_config():
        db_session.add(team)

    db_session.commit()

    report = models.CustomReport()
    report.name = 'Test'
    report.description = 'Test description'
    report.url = ('bla')
    db_session.add(report)
    db_session.commit()

if __name__ == "__main__":
    read_config()
    print populat_user_from_config()
    print populat_team_from_config()
