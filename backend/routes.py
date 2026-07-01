from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data),200

    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if data:
        for picture in data:
            if picture.get("id") == id:
                return jsonify(picture)
        
        return {"message": "Picture not found"},404
    else:
        return {"message": "Internal server error"}, 500 


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    pic_data = request.get_json()
    if pic_data:
        pid = pic_data["id"]

        for pic in data:
            if pic.get("id") == pid:
                return {"Message": f"picture with id {pic['id']} already present"},302
        
        data.append(pic_data)
        return {"Message": "picture added", "id": pid},201
    else:
        return {"message": "Internal server error"}, 500 

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    pic_data = request.get_json()
    if pic_data:

        for i in range(len(data)):
            pic = data[i]
            if pic.get("id") == id:
                data[i] = pic_data
                return {"message": "picture updated"},200
        return {"message": "picture not found"},404
    else:
        return {"message": "Internal server error"}, 500 

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    pid = id

    if pid:
        for pic in data:
            if pic.get("id") == pid:
                data.remove(pic)
                res = make_response()
                res.status_code =204
                return res
        return {"message": "picture not found"},404
    else:
        return {"message":"Internal server error"},500
