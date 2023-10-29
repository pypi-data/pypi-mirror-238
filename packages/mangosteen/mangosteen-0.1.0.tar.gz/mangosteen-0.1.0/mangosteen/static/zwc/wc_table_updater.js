import C_UTIL, {C_UI, C_AJAX } from '/webui/mangosteen/mangosteen/static/zjs/common_utils.js'; //


export default class WCTable_Updater    { 

    constructor( column_schema, submit_url_bulk, submit_method, popup_messages){ 
        this._url_bulk = submit_url_bulk
        this._columns = column_schema
        this._submit_method = submit_method

        this._popup_messages = popup_messages
        
        this._submit_queue = []

        this._SUBMIT_TYPE_ADD = "add"
        this._SUBMIT_TYPE_DEL = "del"
        this._SUBMIT_TYPE_EDIT = "edit"

        this.#extract_key_field()

    }

    //**************************************************************************************************
    #extract_key_field(){
        this._key_field = null
        var this_ref = this
        this._columns.every( function(item){
            if( item.key_field == "true"){
                this_ref._key_field = item.id 
                return
            }
        });

        if(! this_ref._key_field ){
            throw `No key field defined in wc-table [columns] list [${ JSON.stringify(this._columns)}]` //if reached this point, then no key field found
        }
    }

    //**************************************************************************************************
    #get_key(data){
        var this_ref = this
        var key_field_found = false 
        var key_field_value = null 

        data.every( function(item){
            if( item.id == this_ref._key_field){
                key_field_value = item.value
                key_field_found = true
                return item.value
            }
        })
        if( ! key_field_found){ throw `In data provided, key field [${this._key_field}] was not found in [${JSON.stringify(data)}]` }
        return key_field_value
    }

    is_empty(){
        if( this._submit_queue.length == 0 ) return true
        return false   
    }

    clear_queue(){
        this._submit_queue = []
    }
    //**************************************************************************************************
    add(data){
        this._submit_queue.push(  { "id": this.#get_key(data), "transaction": this._SUBMIT_TYPE_ADD , "data":data } )
    }

    //**************************************************************************************************
    del(data){
        var index = this.#find_existing_record( data )
        if( index >= 0){ 
            this._submit_queue.splice(index,1)
        }else{
            this._submit_queue.push(  { "id": this.#get_key(data), "transaction": this._SUBMIT_TYPE_DEL , "data":data } )
        }
        
    }

    //**************************************************************************************************
    edit(data){
        
        var index = this.#find_existing_record( data )

        if( index >= 0){ 
            this._submit_queue[index].data = data
            // .push(  { "id": this.#get_key(data), "transaction": this._SUBMIT_TYPE_EDIT , "data":data } )
        }else{
            this._submit_queue.push(  { "id": this.#get_key(data), "transaction": this._SUBMIT_TYPE_EDIT , "data":data } )
        }
         
    
    }

    //**************************************************************************************************
    #find_existing_record(data){
        var update_data_key = ""
        var this_obj = this;
        var ret_index = -1;
        //Get the key value from the data records
        this._columns.filter( function(col_item){ return col_item.key_field == "true"  }).forEach( function(key_col_item){

            data.forEach( function( data_col ){
                if( data_col.id == key_col_item.id ){
                    update_data_key = update_data_key + data_col.value + "#"    //concatenate key value
                }
            });
        });
        
        //find record
        this_obj._submit_queue.forEach( function(submit_item, index){
            var curr_rec_key = ""
            this_obj._columns.filter( function(col_item){ return col_item.key_field == "true"  }).forEach( function(key_col_item){
                submit_item.data.forEach( function( submit_item_col ){
                    if( submit_item_col.id == key_col_item.id ){
                        curr_rec_key = curr_rec_key + submit_item_col.value + "#" 
                    }
                });
            });
            //Check fi keys match:
            if( curr_rec_key == update_data_key){
                ret_index = index
            }
        });

        return ret_index;  //found=
    }

    //************************************************************************************
    submit( success_func, fail_func ){ 
        // var this_ref = this
        // debugger;
        C_AJAX.ajax_post(   this._url_bulk, 
                            this._submit_queue, 
                            function(data){

                                C_UI.popup_success( 'awesome' );
                                success_func(data) 
                            },
                                
                            function(data){
                                C_UI.popup_success( 'not awesome' );
                                fail_func(data)
                            } );
            
    }
 
    
}