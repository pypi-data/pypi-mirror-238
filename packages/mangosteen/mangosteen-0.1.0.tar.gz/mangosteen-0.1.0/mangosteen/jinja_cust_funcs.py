import json , re

from flask import url_for, current_app
# from flask_wtf import csrf_token
# from zohavi.zcommon import Utils


##############################################################################################################


class JCFunc:

	CSRF_TOKEN_NAME = "_csrf_token"

	def get_csrf_token_name():
		return JCFunc.CSRF_TOKEN_NAME

	def set_csrf_token(myapp, class_name):
		# breakpoint()
		csrf_str  = f'<wc-hidden id = "{JCFunc.CSRF_TOKEN_NAME}" name="{JCFunc.CSRF_TOKEN_NAME}" '  
		csrf_str += f'value="{current_app.jinja_env.globals["csrf_token"]() }"'
		csrf_str += f'class="{class_name}" ></wc-hidden>'
		return 	csrf_str
				
			 	

	def load_template_funcions(jinja_env):
		for method in dir(JCFunc):
			if method.startswith('__') is False:
				jinja_env.globals[ 'jc_' + method] = getattr(JCFunc, method)


	######################################################################################################
	# Test function
	def test():
		return "hello JCFunc world"

	def defaulter(value, default):
		return value if value else default
	# def breakpoint():
	# 	breakpoint()


	def breakpoint(data):
		breakpoint()

	######################################################################################################
	# Helper function 
	def dict_to_json_str(inp_dict, field_list):
		ret_json = {}

		for field in field_list:
			if field in inp_dict: ret_json[field] = inp_dict[field]

		return json.dumps( ret_json )
		# pass

	######################################################################################################
	# Helper function 
	def list_dict_to_json_str(inp_list, field_list):
		ret_json = []

		for item in inp_list:
			item_dict = {}
			for field in field_list:
				if field in item: item_dict[field] = item[field]
			if item_dict: ret_json.append( item_dict )

		return json.dumps( ret_json )
		# pass
	
	######################################################################################################
	# Take an existing list or dict, and then convert the field names from A to B
	def translate_obj(obj, field_mapping, field_inserts ): 
		new_obj = None

		if not obj: return []	

		if isinstance(obj, list):
			new_obj = []
			for item in obj:	#Look through each of the rows
				curr_row = {}

				for field in item:
					if field in field_mapping:	#for each of the field mapping - "field" = original field
						curr_row[ field_mapping[field] ] = item[ field ]
					else:
						curr_row[ field ] = item[ field ]

				# if field_inserts: breakpoint() 
				for curr_insert in field_inserts:	#Go through each of the insert items
					search_match = True
					for search_item in curr_insert["search"]:	#check if the search criteria matches.  if so, then add it to the item
					 	if not ( search_item in item and item[search_item] == curr_insert["search"][ search_item ] ) :
					 		search_match = False

					if search_match:  curr_row.update (    curr_insert[ "insert" ]  )
							
				new_obj.append( curr_row )

		else:
			raise Exception( 'error')
		# print( json.dumps( new_obj ) )
		# print('deondone')
		return json.dumps( new_obj )
		# return json.dumps( obj )
		# breakpoint()
	######################################################################################################
	# Helper function for set_elt_attribs() to render each attribute in a HTML tag
	def concat_dirs(base_dir, *sub_dirs):
		new_dir = base_dir;
		for curr_sub_dir in sub_dirs :
			if curr_sub_dir:
				# logger.debug(f"adding {new_dir} + {curr_sub_dir} ")
				add_sub_dir = curr_sub_dir	
				if curr_sub_dir[0] == '/': curr_sub_dir = curr_sub_dir[1:]

				if new_dir[-1] == "/": 
					new_dir += curr_sub_dir
				else:  
					new_dir += "/" + curr_sub_dir
		if new_dir and new_dir[-1] != "/":
			new_dir += "/"

		# logger.debug("returning adding:" + new_dir)
		return new_dir


	######################################################################################################
	# Helper function for set_elt_attribs() to render each attribute in a HTML tag
	def _set_elt_attribs_print_str(item, data_value ): 
		if isinstance(data_value, dict):
			# print( f"####:{data_value}")
			return f" {item}='{ json.dumps(data_value) }' "
		return f' {item}="{data_value}" '

	

	######################################################################################################
	# Set the attributes of a HTML tag where **defaults_dict will be added if no entry in the field provided
	def set_elt_attribs(field, **defaults_dict ):
		attrib_str = "" 
		for item in defaults_dict:
			if item in field: 
				attrib_str += JCFunc._set_elt_attribs_print_str( item, field[item] )
			else:
				attrib_str += JCFunc._set_elt_attribs_print_str( item, defaults_dict[item] )   

		print( f"****:{attrib_str}")
		return attrib_str
	
	# {"class":"" , "message_type=opt[error,info,warn,success]":"", "message_header":"", "message":""}, ["id"]);   
	######################################################################################################
	def fill_message( message_data:dict, overrides:dict={} ):		
		attrib_str = ""

		attrib_str += f'id="{ 				JCFunc._fill_attribs_get_attrib_value( message_data, "id", overrides) }"  ' 
		attrib_str += f'class="{ 			JCFunc._fill_attribs_get_attrib_value( message_data, "class", overrides) }"  ' 
		attrib_str += f'message_type="{ 	JCFunc._fill_attribs_get_attrib_value( message_data, "message_type", overrides) }"  ' 
		attrib_str += f'message_header="{ 	JCFunc._fill_attribs_get_attrib_value( message_data, "message_header", overrides) }"  ' 
		attrib_str += f'message="{ 			JCFunc._fill_attribs_get_attrib_value( message_data, "message", overrides) }"  ' 
			
		return attrib_str
	
	######################################################################################################
	def fill_attribs( attrib_type: str, table_obj:str, field_id:str, data_ui: dict, data_value: any=None, overrides:dict={} ):
		attrib_filler_func = {
								'wc-input': JCFunc._fill_attribs_wc_input_text
		}
		# breakpoint()
		if attrib_type in attrib_filler_func: return attrib_filler_func[attrib_type](table_obj, field_id, data_ui, data_value, overrides)
		return f"ERROR: ATTRIB_TYPE [{attrib_type}] not found"

	######################################################################################################
	def _fill_attribs_wc_input_text(table_obj:str, field_id:str, data_ui: dict, data_value: any, overrides:dict) -> str:
		# breakpoint()
		field_schema = data_ui.get_field_schema( table_obj ,  field_id )
		if not field_schema:
			raise ValueError( f"Either table object:[{table_obj}] or field id[{field_id}] not found in the web data ui schema passed.  Check JSON schema and Jinja template entry for match")
		
		attrib_str =  f'id="{ field_id }"  ' 
		attrib_str += f'placeholder="{ JCFunc._fill_attribs_get_attrib_value( field_schema, "placeholder", overrides) }"  ' 
		attrib_str += f'label="{  JCFunc._fill_attribs_get_attrib_value( field_schema, "label", overrides) }" '
		attrib_str += f'message_err="{  JCFunc._fill_attribs_get_attrib_value( field_schema, "message_err", overrides) }" '
		attrib_str += f'type="{  JCFunc._fill_attribs_get_attrib_value( field_schema, "type", overrides) }" '
		attrib_str += f"validation='{  JCFunc._fill_attribs_get_attrib_value( field_schema, 'validation', overrides) }' " 	
		if data_value: attrib_str += f'value="{ data_value }" '

		return attrib_str

	######################################################################################################
	def _fill_attribs_get_attrib_value(   field_schema:dict, field_str:str, overrides:dict) -> str:
		field_value = ""
		if field_str in overrides:	#try to get from override first if present
			field_value = overrides[ field_str ]
		elif field_str == "validation": #if validation then use a json value-pair entry to validation field
			comma = ""
			for key in field_schema.get('validation',{} ).keys():
				comma += f'"{key}":"{ field_schema["validation"][key]}" ,'
			if comma: field_value += "{" + comma[:-1] + "}"
			# breakpoint()
		else:  #catch all - add the value from the database
			field_value = field_schema.get( field_str, "")
		return field_value

	######################################################################################################
	# 
	# <wc-input-text id="si_env_authsite_name"  class="ck_grp_elt" placeholder="Add site title"  label="Site Name"  validation='{"text_min_len":3}', message_err="Site name at least 3 characters" , value='defaultxx'   >
    #         </wc-input-text> 
	
	
					#   +
					#  f'validation='{"text_min_len":3}', message_err="Site name at least 3 characters" , value='defaultxx'   

	######################################################################################################
	# expand the url from the config files
	# scenario 1: url_for:member.home
	# scenario 2: url_for:members.home?var1=abc 
	# scenario 3: url_for:members.home?var1=abc&var2=xyz
	# scenario 3: url_for:members.home?var1=abc&var2=[data_field] abd data_table is a hash containing key 'data_field'
	def extract_url_from_config_str(urlStr, data_table = None):
		strTokens = re.split("[:\?]", urlStr )		#split into two parts, first bit into main link, then param
		arg_hash = {}

		if( len(strTokens) > 2):					#if we have parameters
			arg_list = re.split("[=&]", strTokens[2] )	#split each parameter

			#create dictionary.  arg_list[::2] = every seond item, arg_list[1::2]  = every first item
			arg_hash = dict( zip( arg_list[::2], arg_list[1::2] ) ) 

			if data_table:			#if we have data to replace
				for key in arg_hash:
					if arg_hash[key].startswith("[") and arg_hash[key].endswith("]"):	#if we have a bracked item
						arg_hash[key] = data_table.get(arg_hash[key][1:-1], arg_hash[key])	#check if key exists in table
	 
		return strTokens[1], arg_hash


	######################################################################################################
	# Custom Template Function: try to convert url_string
	def render_url(urlStr, data_table = None):

		if 'url_for' in urlStr:
			# strTokens = urlStr.split(":")
			# logger.debug("Tokens:" + str(strTokens))
			(link, args) = JCFunc.extract_url_from_config_str( urlStr, data_table )

			return url_for( link , **args)
		else:
			return  urlStr

	######################################################################################################
	# Custom Template Function: try to get url string, if not exist, return blank
	def url_for_lazy(urlStr ):

		try:
			return url_for( urlStr );
		except Exception as e:
			# logger.debug(f"URL converstaion failed:{urlStr}")
			return ""
		 
	 ######################################################################################################
	# enable creation of lists using the SET command under JINJA
	def make_list(*list_items): 
		return list_items

		
	
