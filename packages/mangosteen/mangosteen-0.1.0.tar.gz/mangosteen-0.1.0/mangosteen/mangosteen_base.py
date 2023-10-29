import inspect, json

########################################################################################################################
########################################################################################################################
class MangosteenBase:
	def __init__(self, app=None, logger=None):
		self.logger = logger
		self.app = app
		self.debug = False

	def get_callee_str(self):
		callee = inspect.stack()[2]
		callee_file = callee.filename[ callee.filename.rfind('/'): ]

		ret_str = f"{callee_file }:{callee.lineno}:{callee.function}:" 
		# breakpoint()
		return ret_str

	def log_debug(self, message): 
		if self.logger: self.logger.debug( message, stack_level=2)
		else: print( "DEBUG:" + message )

	def log_error(self, message, stack_level=2):
		if self.logger: self.logger.error( message, stack_level)
		else: print( "ERROR:" + message )

	def log_info(self, message):
		if self.logger: self.logger.info( message, stack_level=2)
		else: print( "INFO:" + message )

	def log_warning(self, message):
		if self.logger: self.logger.warning( message, stack_level=2)
		else: print( "WARNING:" + message )

# ########################################################################################################################
# ########################################################################################################################
# class MangosteenBlueprint():
#     def __init__( self, blueprint_name, blueprint_module, route_class, url_prefix='/', template_folder='templates', static_folder='static', static_url_path='/static' ):
#         self._bp = Blueprint(   name=blueprint_name, 
#                                 import_name=blueprint_module, 
#                                 static_folder=static_folder,
#                                 static_url_path=static_url_path,
#                                 template_folder=template_folder,
#                                 url_prefix=url_prefix  )

#         self._route_class = route_class

#     def get_blueprint(self):
#         return self._bp

#     def get_view(self):
#         return self._route_class 
