from flask import Flask, request
from flask_restx import Api, Resource, fields
from config import DevConfig
from models import Recipe
from exts import db
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)
migrate = Migrate(app,db)
api = Api(app, doc='/docs')

# Model (Serializer)
recipe_model = api.model(
    "Recipe",
    {
        "id": fields.Integer(),
        "title": fields.String(),
        "description": fields.String()
    }
)

@api.route('/hello')
class HelloResource(Resource):
    def get(self):
        return {"message": "Hello world!"}
    
@api.route('/recipes')
class RecipesResource(Resource):
    @api.marshal_list_with(recipe_model)
    def get(self):
        """Return all recipes"""
        recipes = Recipe.query.all()
        return recipes

    @api.marshal_with(recipe_model)
    def post(self):
        """Create a new recipe"""
        data = request.get_json()
        new_recipe = Recipe(
            title=data.get("title"),
            description=data.get("description")
        )
        new_recipe.save()
        return new_recipe, 201

@api.route('/recipe/<int:id>')  # Make it a dynamic route
class RecipeResource(Resource):
    @api.marshal_with(recipe_model)
    def get(self, id):
        """Get a specific recipe by ID"""
        recipe = Recipe.query.get_or_404(id)  # Returns 404 if not found
        return recipe

    @api.marshal_with(recipe_model)
    def put(self, id):
        """Update a recipe"""
        recipe = Recipe.query.get_or_404(id)
        data = request.get_json()
        recipe.update(
            title=data.get("title"),
            description=data.get("description")
        )
        return recipe

    def delete(self, id):
        """Delete a recipe"""
        recipe = Recipe.query.get_or_404(id)
        recipe.delete()
        return {"message": "Recipe deleted successfully"}, 200
    

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Recipe': Recipe}

if __name__ == '__main__':
    app.run(debug=True)
