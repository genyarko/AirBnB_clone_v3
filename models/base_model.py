#!/usr/bin/python3
"""
Contains class BaseModel
"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage, place, state, city, amenity
import hashlib

@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id=None):
    """Gets all places"""
    if city_id is None:
        abort(404)

    res = []
    for i in storage.all("Place").values():
        res.append(i.to_dict())

    return jsonify(res)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id=None):
    """Gets a place"""
    s = storage.get("Place", place_id)
    if s is None:
        abort(404)
    else:
        return jsonify(s.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id=None):
    """Deletes a place"""
    s = storage.get("Place", place_id)
    if s is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id=None):
    """Create a place"""
    checker = set()
    for i in storage.all("City").values():
        finder.add(i.id)
    if city_id not in checker:
        abort(404)

    s = request.get_json(silent=True)
    if s is None:
        abort(400, "Not a JSON")

    user = s.get("user_id")
    if user is None:
        abort(400, "Missing user_id")
    checker = set()
    for i in storage.all("User").values():
        checker.add(i.id)
    if user not in checker:
        abort(404)

    if "name" not in s.keys():
        abort(400, "Missing name")

    s["city_id"] = city_id
    new_s = places.Place(**s)
    storage.new(new_s)
    storage.save()
    return jsonify(new_s.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id=None):
    """Update a place"""
    obj = storage.get("Place", place_id)
    if obj is None:
        abort(404)

    s = request.get_json(silent=True)
    if s is None:
        abort(400, "Not a JSON")
    else:
        for k, v in s.items():
            if k in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
                pass
            else:
                setattr(obj, k, v)
        storage.save()
        res = obj.to_dict()
        return jsonify(res), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Searches for places based on JSON in request body"""
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")

    states = req.get("states", [])
    cities = req.get("cities", [])
    amenities = req.get("amenities", [])

    if not states and not cities and not amenities:
        res = [p.to_dict(include_password=True) for p in storage.all("Place").values()]
        return jsonify(res)

    res = []
    for s in states:
        state_obj = storage.get("State", s)
        if state_obj is not None:
            for c in state_obj.cities:
                if c.id not in cities:
                    cities.append(c.id)

    for c in cities:
        city_obj = storage.get("City", c)
        if city_obj is not None:
            for p in city_obj.places:
                if p not in res:
                    res.append(p)

    if amenities:
        res = [p for p in res if all(a in p.amenities for a in amenities)]

    res = [p.to_dict(include_password=True) for p in res]
    return jsonify(res)


class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    if models.storage_t == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, include_password=False):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        new_dict.pop('_sa_instance_state', None)
        if not include_password:
            new_dict.pop('password', None)
        return new_dict

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)


class User(BaseModel):
    """The User class, which inherits from BaseModel"""
    if models.storage_t == "db":
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
    else:
        email = ""
        password = ""

    def __init__(self, *args, **kwargs):
        """Initialization of the user"""
        super().__init__(*args, **kwargs)
        if kwargs.get("password", None) is not None:
            self.password = hashlib.md5(kwargs["password"].encode()).hexdigest()

    def update_password(self, password):
        """Updates the user's password"""
        self.password = hashlib.md5(password.encode()).hexdigest()
