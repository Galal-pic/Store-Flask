from exts import db

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(),nullable = False)
    description = db.Column(db.String(),nullable = False)

    def __repr__(self):
        return f'<Recipe {self.title}>'
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self,title,description ):
        self.title = title
        self.description = description
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

#user model

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    def __repr__(self):
        return f'<User {self.username}>'


