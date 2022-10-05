"""Flask app for Cupcakes"""
from flask import Flask, render_template, request, jsonify

from models import db, connect_db, Cupcake


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SECRET_KEY'] = "OH-SECRET"



connect_db(app)



@app.route('/')
def show_cakes():
    return render_template('base.html')


@app.route('/api/cupcakes', methods=["GET"])
def list_cupcakes():
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)




@app.route('/api/cupcakes/<int:id>', methods=['GET'])
def get_cupcakes(id):
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())



@app.route('/api/cupcakes', methods=['POST'])
def create_cupcakes():
    

    cupcake = Cupcake(
        flavor = request.json['flavor'], 
        rating = request.json['rating'], 
        size = request.json['size'],
        image=request.json['image'] or None)

    db.session.add(cupcake)
    db.commit()
    
    response_json = jsonify(cupcake=cupcake.serialize())
    return (response_json, 201)


@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcakes(id):
    cupcake = Cupcake.query.get_or_404(id)

    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('iamge', cupcake.image)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcakes(id):
    cupcake = Cupcake.query.get_or_404(id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="deleted")


