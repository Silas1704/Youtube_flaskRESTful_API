from flask import Flask 
from flask_restful import Api ,Resource, abort, reqparse,fields,marshal_with
from flask_sqlalchemy import SQLAlchemy
#this is server that offers an API

#create flask app and connect it with api
app=Flask(__name__)
api=Api(app)
app.config['SQLAlchemy_DATABASE_URI']='sqllite:///database.db'
db=SQLAlchemy(app)

class VideoModel(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    views=db.Column(db.Integer,nullable=False)
    likes=db.Column(db.Integer,nullable=False)

    def __repr__(self):
         return f"Video(name = {name},views={views},likes={likes})"




db.create_all() #intialse database after creating model


#reqparse is validation lib
video_put_args=reqparse.RequestParser()
video_put_args.add_argument("name",type=str,help="Name of the video",required=True)
video_put_args.add_argument("likes",type=int,help="likes of the video",required=True)
video_put_args.add_argument("views",type=int,help="views of the video",required=True)

video_update_args=reqparse.RequestParser()
video_update_args.add_argument("name",type=str,help="NEW Name of the video")
video_update_args.add_argument("likes",type=int,help=" NEW likes of the video")
video_update_args.add_argument("views",type=int,help="NEW views of the video")


#fields used to serialize in json format(attributes of the resource)
resource_fields={
    'id':fields.Integer,
    'name':fields.String,
    'views':fields.Integer,
    'likes':fields.Integer
}


#define the resource and the methods that u want to happen on this resource
class Video(Resource):
    @marshal_with(resource_fields)
    def get(self,video_id):#retrieve data from server
        result=VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404,message="could not find video of that id")
        return result
    
    @marshal_with(resource_fields)
    def patch(self,video_id):
        args= video_update_args.parse_args()
        video=VideoModel.query.filter_by(id=video_id).first()
        if not video:
           abort(404,message="video doesnt exits,cannot update")
        if args['name']:
           video.name=args['name']
        if args['views']:
           video.views=args['views']
        if args['likes']:
           video.likes=args['likes']
        
      
        db.session.commit()
        
        return video,200
       
       

    @marshal_with(resource_fields)
    def put(self,video_id):#update existing data on server
        args=video_put_args.parse_args()
        result=VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409,message="video id taken")

        video=VideoModel(id=video_id,name=args['name'],views=args['views'],likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video,201
    
    

    #delete existing data on server
    @marshal_with(resource_fields)
    def delete(self,video_id):
       video=VideoModel.query.filter_by(id=video_id).first()
       if not video:
           abort(404,message="video not found")
       
       db.session.delete(video)
       db.session.commit()
       return '',204
        
 
    
api.add_resource(Video,"/video/<int:video_id>")

#start flask app and server.debug only in testing env
if __name__=="__main__":
    app.run(debug=True)
