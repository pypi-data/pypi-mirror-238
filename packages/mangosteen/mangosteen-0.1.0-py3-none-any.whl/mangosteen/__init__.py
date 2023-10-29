from flask import Blueprint

# bp = Blueprint('webui', __name__, template_folder='templates', static_folder='static', static_url_path='/static') 


# from .routes import WebUIView

# from .mangosteen_base import MangosteenBlueprint
# from .routes import WebUIView

zbp = Blueprint( 
                    name='webui',
                    import_name=__name__,  
                    url_prefix='/', 
                    template_folder='templates', 
                    static_folder='static', 
                    static_url_path='/' 
                )

    # def __init__( self, blueprint_name, blueprint_module, route_class, url_prefix='/', template_folder='templates', static_folder='static', static_url_path='/static' ):
    #     self._bp = Blueprint(   name=blueprint_name, 
    #                             import_name=blueprint_module, 
    #                             static_folder=static_folder,
    #                             static_url_path=static_url_path,
    #                             template_folder=template_folder,
    #                             url_prefix=url_prefix  )

    #     self._route_class = route_class

    # def get_blueprint(self):
    #     return self._bp

    # def get_view(self):
    #     return self._route_class 
                