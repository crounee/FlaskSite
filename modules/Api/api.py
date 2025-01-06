from flask import Flask
from flask_restful import Resource, Api
from flask import Blueprint, Response, request
from ..database import models,session
from sqlalchemy import text

bp = Blueprint('api',__name__)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
    

#Возвращает информацию о всех доступных достижениях
class AllAchievements(Resource):
    def get(self):
        achivments = models.Achivments.query.all()
        description = []
        for achiv in achivments:
            value = {"achivment_id":achiv.achivment_id,
                "achivment_name":achiv.achivment_name,
                "number_of_points":achiv.number_of_points}
            description.append(value)
        return description
    
    def put(self):
        '''Добавить достижение'''
        achivment_name = request.args.get('achivment_name')
        number_of_points = request.args.get('number_of_points')
        
        if achivment_name != None and number_of_points != None:
            newAchivment = models.Achivments(achivment_name = achivment_name,number_of_points = number_of_points)
            session.session.add(newAchivment)
            session.session.commit()
            return 200
        else:
            return 404
        
class AddUserAchievements(Resource):
    #Выдает достижения пользователю с сохранением времени выдачи
    def put(self):
        user_id = request.args.get('user_id')
        achivment_id = request.args.get('achivment_id')

        if user_id != None or achivment_id != None:
            addAchivmentRequest = models.Achivment_recived(user_id = user_id,achivment_id=achivment_id)
            session.session.add(addAchivmentRequest)
            session.session.commit()
            return 200
        else:
            return 404
            
class AddDescriptionAchievements(Resource):
    def put(self):
        #Добавляет описание достижения
        achivment_id = request.args.get('achivment_id')
        description = request.args.get('description')
        language_name = request.args.get('language_name')

        if achivment_id != None and description != None and language_name != None:
            addDescription = models.Description(language_name = language_name,achivment_id = achivment_id,description = description)
            session.session.add(addDescription)
            session.session.commit()
            return 200
        else:
            return 404
        

class StatisticUserMaxAchievements(Resource):
    def get(self):
        #Пользователь с максимальным количеством достижений (штук)
        value = session.session.execute(text("select user_id,count(achivment_id) as max_achivment from achivment_recived group by user_id order by max_achivment desc limit 1"))
        value = value.fetchone()
        return {"user_id":value[0],"achivments_count":value[1]}
        

class StatisticUserSumPoints(Resource):
    def get(self):
        #Пользователь с максимальным количеством очков достижений (баллов суммарно)
        value = session.session.execute(text("select user_id, sum(achivments.number_of_points) as max_points from achivment_recived inner join achivments on achivment_recived.achivment_id = achivments.achivment_id group by user_id order by max_points desc limit 1"))
        value = value.fetchone()
        return {"user_id":value[0],"total_points":value[1]}
        
class StatisticUsersMaximumDifference(Resource):
    def get(self):
        #Пользователи с максимальной разностью очков достижений (разность баллов между пользователями)
        value = session.session.execute(text("""select user_id, (select sum(achivments.number_of_points) as max_points from achivment_recived 
                                            inner join achivments on achivment_recived.achivment_id = achivments.achivment_id
                                            group by user_id order by max_points desc limit 1) - sum(achivments.number_of_points) as value_difference 
                                            from achivment_recived inner join achivments on achivment_recived.achivment_id = achivments.achivment_id
                                            group by user_id order by value_difference desc limit 10"""))
        value = value.fetchall()
        data = []
        for val in value:
            data.append({"user_id":val[0],
                         "points_difference":val[1]})

        return data
    
class StatisticUsersMinDifference(Resource):
    #Пользователи с минимальной разностью очков достижений(разность баллов между пользователями)
    def get(self):
        value = session.session.execute(text("""select user_id, (select sum(achivments.number_of_points) as max_points from achivment_recived 
                                            inner join achivments on achivment_recived.achivment_id = achivments.achivment_id
                                            group by user_id order by max_points desc limit 1) - sum(achivments.number_of_points) as value_difference 
                                            from achivment_recived inner join achivments on achivment_recived.achivment_id = achivments.achivment_id
                                            group by user_id order by value_difference asc limit 10"""))
        value = value.fetchall()
        data = []
        for val in value:
            data.append({"user_id":val[0],
                         "points_difference":val[1]})

        return data
    
class StatisticUsersSevenDaysStreak(Resource):
    #Пользователи, которые получали достижения 7 дней подряд (по дате выдачи, хотя бы одно в каждый из 7 дней)
    def get(self):
        value = session.session.execute(text("""
    SELECT ua1.user_id FROM (select DISTINCT user_id from achivment_recived where DATE(date_of_recived) = CURRENT_DATE - 1) ua1
    INNER JOIN (select DISTINCT user_id from achivment_recived where DATE(date_of_recived) = CURRENT_DATE - 2) ua2 on ua1.user_id = ua2.user_id
    INNER JOIN (select DISTINCT user_id from achivment_recived where DATE(date_of_recived) = CURRENT_DATE - 3) ua3 on ua1.user_id = ua3.user_id
    INNER JOIN (select DISTINCT user_id from achivment_recived where DATE(date_of_recived) = CURRENT_DATE - 4) ua4 on ua1.user_id = ua4.user_id
    INNER JOIN (select DISTINCT user_id from achivment_recived where DATE(date_of_recived) = CURRENT_DATE - 5) ua5 on ua1.user_id = ua5.user_id
    INNER JOIN (select DISTINCT user_id from achivment_recived where DATE(date_of_recived) = CURRENT_DATE - 6) ua6 on ua1.user_id = ua6.user_id
    INNER JOIN (select DISTINCT user_id from achivment_recived where DATE(date_of_recived) = CURRENT_DATE - 7) ua7 on ua1.user_id = ua7.user_id"""))
        value = value.fetchall()
        data = []
        for val in value:
            data.append({"user_id":val[0]})

        return data
    
class UserData(Resource):
    #Возвращает информацию о пользователе
    def get(self):
        user = session.session.query(models.User).filter(models.User.name_user == request.args.get('username'))
        if user.count() > 0:
            return {"user_id":user[0].user_id,
                    "name_user":user[0].name_user,
                    "language_name":user[0].language_name
                    }
        else:
            return 404
        

class AchievementsReceived(Resource):
    #Предоставляет информацию о выданных пользователю достижениях на выбранном пользователем языке
    def get(self):
        user_id = request.args.get("user_id")
        try:
            language_name = session.session.query(models.User).filter(models.User.user_id == user_id)
            language_name = language_name[0].language_name

            achivments_recived = session.session.query(models.Achivment_recived).filter(models.Achivment_recived.user_id == user_id)
            data = []
            for achivment in achivments_recived:
                description = session.session.query(models.Description).filter(models.Description.achivment_id == achivment.achivment_id,
                                                                              models.Description.language_name == language_name)

                if description.count() > 0:
                    description = description[0].description
                else:
                    description = "not found description"

                value = {"achivment_recived_id":achivment.achivment_recived_id,
                        "user_id":achivment.user_id,
                        "achivment_id": achivment.achivment_id,
                        "date_of_recived":achivment.date_of_recived,
                        "description":description
                        }
                data.append(value)
            return data
        except:
            return 404
        
my_api = Api(bp)
my_api.add_resource(HelloWorld,'/hello')
my_api.add_resource(AllAchievements,'/allAchievements')
my_api.add_resource(AddUserAchievements,'/AddUserAchievements')
my_api.add_resource(AddDescriptionAchievements,'/AddDescriptionAchievements')
