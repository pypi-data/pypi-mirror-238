    
    import C_UTIL, {C_UI} from '/webui/mangosteen/mangosteen/static/zjs/common_utils.js'; 

    import ValidationHelper from '/webui/mangosteen/mangosteen/static/zjs/validation_helper.js'; //
    import WCEltParent from  "/webui/mangosteen/mangosteen/static/zwc/wc_elt_parent.js" 
    import WCModal from  "/webui/mangosteen/mangosteen/static/zwc/wc_modal.js" 
    import WCButton from  "/webui/mangosteen/mangosteen/static/zwc/wc_button.js" 
    
    import WCTable_Updater from "/webui/mangosteen/mangosteen/static/zwc/wc_table_updater.js" 
    import WCTable_GUI from "/webui/mangosteen/mangosteen/static/zwc/wc_table_gui.js" 
     
 
    export default class WCTable extends WCEltParent { 
        define_template_globals(){
            return `:host{ 
                        --table_header_cell_color: var(--background_cat3_color);
                        --table_header_text_color: var(--light_text_color_cat1);

                        --table_cell_bg_key_color: var(--background_cat2_color);
                    }`
        }

        define_template(){
            var add_button_html = ""
            var submit_button_html = ""

            var template_str = ""
            if( this._inp.add_row ){
                add_button_html = `<div class="container mt-2 mb-2 level-right">
                                        <div class="level-item has-text-centered"> 
                                            <p class="control "> 
                                                <wc-button id="si_add_row" label="[placeholder::add_row]" active_class="is-success" > </wc-button>  
                                            </p>  
                                        </div>
                                    </div>`;
            } 

            if( this._inp.submit_method == "manual"){
                submit_button_html = `<div class="container mt-2 mb-2 level-right">
                                        <div class="level-item has-text-centered"> 
                                            <p class="control "> 
                                                <wc-button id="si_submit" label="Save" active_class="is-success"  > </wc-button>  
                                                <wc-button id="si_cancel" label="Cancel" active_class="is-danger" > </wc-button>  
                                            </p>  
                                        </div>
                                    </div>`;
            }
            template_str = super.define_template() + `   
                        <style>
                                ${this.define_template_globals()}

                                .sc_cell_validation_failed{  
                                    background-image: linear-gradient(225deg, red, red 10px, transparent 10px, transparent);
                                    color: red; 
                                }

                                .sc_cell_bg_key_color{
                                    background-color: var(--table_cell_bg_key_color);
                                    color: var(--light_text_color_cat1);
                                    font-weight: bold;
                                }
                                .sc_cell_disabled{
                                    background-color: grey
                                }

                                .table thead th{ /*over ride bulma setting */
                                    background-color: var(--table_header_cell_color);
                                    color: var(--table_header_text_color);
                                }
                        </style>

                        <div class="container">
                            ${ add_button_html }

                            <table id="si_field" class="table is-bordered is-striped is-hoverable is-fullwidth">
                                <thead id="si_thead"  >
                                  <!--
                                      <tr>
                                        <th width="20%" class="sc_table_header">Env</th>
                                        <th width="60%" class="sc_table_header">URL</th>
                                        <th width="20%" class="sc_table_header">Port</th>
                                      </tr>
                                  -->
                                </thead>
                                <tbody id="si_tbody">
                                    <!--
                                        <tr>
                                            <td  > Dev </td>
                                            <td class="sck_validation " data-validation="required|is_url" data-validation_msg="Must include a URL"  contenteditable> </td>
                                            <td class="sck_validation "  data-validation="required|num_gte:1000|num_lte:9999" data-validation_msg="Must include a 4 digit port number"  contenteditable> </td>
                                        </tr>
                                    -->
                                </tbody>
                            </table>
                            ${ submit_button_html }
                        </div>` +
            this.define_template_modal();

            return template_str;
        }

        define_template_modal(){
            return ` <wc-modal id="si_modal" title="Edit"
                                fields='[]'> 
                    </wc-modal>`;
               
        }
        // columns='[
        //       {"col_label":"Name", "key":"ck_env_name" },
        //       {"col_label":"Description", "key":"ck_env_desc" },
        //       {"col_label":"Code", "key":"ck_env_code" },
        //       {"col_label":"Action", "key":"ck_env_action" }
        // ]'

        // data='[ {"row_no":1, "data-id":"1",   
        //                               "row":[  {"key":"ck_env_name", "value":"Dev", "data-value":"dev", "data-id":"1",     
        //                               "cell_key_color":"true"},
        //                               {"key":"ck_env_desc", "value":"Development"},
        //                               {"key":"ck_env_code", "value":"dev"},
        //                               {"key":"ck_env_action", 
        //                                          "icons":[ {"icon":"fa-edit", "class_key":"ck_env_edit", "data-value":"1"},
        //                                                    {"icon":"fa-trash", "class_key":"ck_env_delete", "data-value":"1"}] }
        //                             ] },
        //         {"row_no":2, "data-id":"2", 
        //                               "row":[  {"key":"ck_env_name", "value":"Dev", "data-value":"dev", "data-id":"2" ,    
        //                               "cell_key_color":"true"},
        //                               {"key":"ck_env_desc", "value":"Development"},
        //                               {"key":"ck_env_code", "value":"dev"},
        //                               {"key":"ck_env_action", 
        //                                          "icons":[ {"icon":"fa-edit", "class_key":"ck_env_edit", "data-value":"2"},
        //                                                    {"icon":"fa-trash", "class_key":"ck_env_delete", "data-value":"2"}] }
        //                             ] },

        constructor(){
            super( {"add_row":"", "data=json":"[]", "field_params=json":"", 
                    "url_submit_bulk":"",
                    "url_submit_on_add":"",  "url_submit_on_edit":"", "url_submit_on_del":"", "submit_hidden_data=json":"",
                    "popup_messages=json":"", "class":"", "submit_method":"", 
                    "action_icons=json":'{"edit":"fas fa-edit","delete":"fas fa-trash"}'}, ["columns=json", "id"]);   

            this._updater = new WCTable_Updater( this._inp.columns, this._inp.url_submit_bulk, this._inp.submit_method, this._inp.popup_messages )

            this._renderer = new WCTable_GUI( this.shadowRoot, this._inp, this.evt_icon_clicked.bind(this) )
            
        } 

        //************************************************************************************
        connectedCallback(){     
            
            super.connectedCallback(); 

            this.validate_schema_submit_hidden_data()
            this.validate_schema_popup_messages()
            this.validate_schema_columns()
            this.validate_schema_column_params()
            this.validate_schema_data();
            
        } 

        

        //************************************************************************************
        //Update teh default settings per field once shadowdom is setup
        init_component(){
            var this_obj = this;
            this.log('initing')
            this.init_data()
            // this.init_modal(this._inp.columns);
            this.init_submit_button_action()
            
            this._renderer.init( this._data_twin )

            this._modal_ref = this.shadowRoot.querySelector('#si_modal')

            var add_row_elt = this.shadowRoot.querySelector('#si_add_row')
            if( add_row_elt){
                add_row_elt.addEventListener('click', this.evt_add_row_clicked.bind(this) );
            }
            // this.init_modal( this._inp.columns);
        }

        // init_submit_button_action(){
        //     var this_obj = this;
        //     var button_elt = this.shadowRoot.querySelector('#si_submit');
        //     if( button_elt){
        //         button_elt.addEventListener('wc_click', function( event ){ 
        //             if( !this_obj._updater.is_empty() ){
        //                 this_obj._updater.submit(   function(success_data){
        //                     this_obj.trigger_custom_event( success_data, 'submit_success');
        //                     this_obj._updater.clear_queue()
        //                 },
        //                 function(fail_data){ 
        //                     this_obj.trigger_custom_event( fail_data, 'submit_failed');
        //                 } );  
        //             }else{
        //                 C_UI.popup_fail( 'no data to svae' ); 
        //             }
                    
        //         });
        //     }
        // }

        //************************************************************************************
        init_data(){
            var this_obj = this;
            this._data_twin = {}
            this._inp.data.forEach( function(item, index){
                item.forEach( function(col){
                    if( ! col['data-value']){ col['data-value'] = col['value'] }
                });
                this_obj._data_twin[  index ] = item
                // item['pseudo_id'] = index;
            });
            // debugger;
        }
        
        // //************************************************************************************
        // init_modal(columns){
        //     var this_obj = this;
        //     var field_list = []
        //     // debugger;
        //     for( var col_index in columns){
        //         const elt = columns[col_index ]
        //         if( elt.editable == "true" || elt.hidden == "true"){
        //             var field_data = {}
        //             field_data.type = this_obj._init_modal_get_field_type(elt)
        //             field_data.label = elt.col_label;
        //             field_data.id = elt.id;
        //             field_data.validation = elt.validation;

        //             if( "field_params" in elt){  //If there are further parameters - e.g. lookup fields
        //                 // debugger;
        //                 for( var param_field in elt.field_params){
        //                     const param_name = elt.field_params[ param_field ]
        //                     field_data[ param_field ] = this._inp.field_params[ param_name  ]
        //                 }
        //             }
        //             field_list.push( field_data );
        //         }
        //     };
        //     this.shadowRoot.querySelector('#si_modal').fields = field_list;
        // }

        // //************************************************************************************
        // _init_modal_get_field_type(elt){
        //     if( elt.hidden  == "true" ){ return 'hidden'; }
        //     return ( typeof elt.type  === 'undefined' ? 'input': elt.type );    
        // }
        
        

        //************************************************************************************
        //Delete row from table
        delete_row(pseudo_id){ //row_no){
            // debugger
            var curr_data_row = this._data_twin[pseudo_id] //this.#data_twin_get_row( pseudo_id)  //this._inp.data[ row_no ]

            // var table_row = this.shadowRoot.querySelector(`tr[data-row_no='${row_no}']`)
            var table_row = this.shadowRoot.querySelector(`tr[data-pseudo_id='${pseudo_id}']`)
            table_row.parentNode.removeChild(table_row);
            
            this._updater.del( curr_data_row )
            
            // delete this._inp.data[  row_no  ] 
            delete this._data_twin[pseudo_id]
        }

        // //************************************************************************************
        // //Add events to table cells
        // add_table_row_item_events(){
        //     this.shadowRoot.querySelectorAll('.sc_icon_clickable').forEach(item =>{
        //         item.addEventListener( 'click',  (event)=> this.evt_icon_clicked(event) );  
        //     });
            
        // }
        
        //************************************************************************************
        //Add events to table cells
        evt_add_row_clicked(event){
            this._modal_ref.show( null, null, this.callback_row_add.bind(this) );
        }
        //************************************************************************************
        //Add events to table cells
        evt_icon_clicked(event){ 
            // this.log('clicked')
            // debugger;
            var elt = event.target.parentElement

            if( elt.dataset['action'] == 'edit' ){
                // this.edit_row_entry( event.path[1].dataset['row_no'] )
                this.edit_row_entry( elt.dataset['pseudo_id'] )
                
            }else if( elt.dataset['action'] == 'delete' ){
                // this.delete_row( event.path[1].dataset['row_no'] )
                this.delete_row( elt.dataset['pseudo_id'] )
            }

            // debugger;
            var new_event = new CustomEvent( 'table_icon_click', { detail: {this:this, 
                                                                            elt:elt, 
                                                                            id:elt.dataset['id'], 
                                                                            value:elt.dataset['value'],
                                                                            // row_no:event.path[1].dataset['row_no'],  }}); 
                                                                            pseudo_id:elt.dataset['pseudo_id'],  }}); 
            this.dispatchEvent(new_event , { bubbles:true, component:true} ); 
        }

        // //************************************************************************************
        // #data_twin_get_row( pseudo_id){
        //     var return_data = null 
        //     this._inp.data.every( function(item){
        //         if( item.pseudo_id == pseudo_id){
        //             return_data = item;
        //             return false;   //Break out of the loop since item found
        //         }
        //         return true //continue to next iteration
        //     } );
        //     if( return_data ){ return return_data; }
        //     throw `Coul not find row with pseudo_id [${pseudo_id}]`
        // }
        //************************************************************************************
        //edit row number (zero index entry)
        edit_row_entry(pseudo_id) { //row_no){
            var curr_data_row = this._data_twin[pseudo_id] // this.#data_twin_get_row( pseudo_id) // _inp.data[ row_no ]
            // debugger;
            // this._modal_ref.show( curr_data_row, {'row_no':row_no}, this.callback_row_edited.bind(this) );
            this._modal_ref.show( curr_data_row, {'pseudo_id':pseudo_id}, this.callback_row_edited.bind(this) );
            this.log( 'showed modal')
            
        }


        //************************************************************************************
        // Called from the modal popup to add new entry
        callback_row_add(action,  ref_data,  new_data){
            // debugger;
            // this.log()
            var full_data = new_data;
            if( this._inp.submit_hidden_data){ 
                if( new_data){
                    full_data = new_data.concat( this._inp.submit_hidden_data ) 
                }
            }
            console.log('adding')
            console.log( JSON.stringify( full_data) )
            if( action == this._modal_ref.C_SAVE){ 
                
                this._callback_row_add_post_submit_updates(full_data)
                this._updater.add(  full_data)
            }
        }

        //************************************************************************************
        _callback_row_add_post_submit_updates(full_data){
            var key_value_temp = 'NEW_' + Date.now(); 
            //Find the key field(s)
            this._inp.columns.forEach( function(col){
                if( col.key_field ){
                    full_data.forEach( function( data_item){
                        if( data_item.id == col.id ){
                            data_item.value = key_value_temp
                        }
                    }); 
                }
            });
            // debugger;
            var tbody_ref = this.shadowRoot.getElementById('si_tbody')
            var new_pseudo_id = tbody_ref.childNodes.length

            this._callback_row_add_update_table(tbody_ref, full_data, new_pseudo_id);
            this._callback_row_add_update_data_twin(full_data, new_pseudo_id);
            this._renderer.add_table_row_item_events()
        }

        //************************************************************************************
        _callback_row_add_update_data_twin(new_data, new_pseudo_id){
            //Update the internal data records
            var inp_new_data_temp = []
            new_data.forEach( function(elt){
                
                var new_data_rec = {}
                new_data_rec['id'] = elt.id
                new_data_rec['value'] = elt.value
                new_data_rec['data-value'] = elt.value
                if( 'data-value' in elt ){
                    new_data_rec['data-value'] = elt['data-value']    
                }
                inp_new_data_temp.push( new_data_rec )
            });
            // this._inp.data.push( inp_new_data_temp )
            this._data_twin[ new_pseudo_id ] = inp_new_data_temp
        }
        //************************************************************************************
        _callback_row_add_update_table(tbody_ref, new_data, new_pseudo_id){
            var table_str = "";
            // var tbody_ref = this.shadowRoot.getElementById('si_tbody')
            // var new_row_no = tbody_ref.childNodes.length
            //Update the table row
            table_str += this._renderer.init_table_data_row( this._inp.columns, new_data, new_pseudo_id, 'id', this._inp.action_icons  )
            tbody_ref.innerHTML = tbody_ref.innerHTML + table_str;
            tbody_ref.childNodes[ tbody_ref.childNodes.length -1 ].querySelector('.sc_icon_clickable').addEventListener( 'click',  (event)=> this.evt_icon_clicked(event) ); 
        }

        //************************************************************************************
        //edit row number (zero index entry)
        callback_row_edited(action, ref_data, new_data){
            var this_obj = this;
            var full_data = new_data;
            if( this._inp.submit_hidden_data){ 
                if( new_data){
                    full_data = new_data.concat( this._inp.submit_hidden_data ) 
                }
            }
             
            if(action == this._modal_ref.C_SAVE ){
                console.log( JSON.stringify( full_data) )

                this._updater.edit(    full_data )
                this._update_row_values( ref_data['pseudo_id'], full_data)
                
                
            }
        }
        
        //************************************************************************************
        _update_row_values( pseudo_id, new_data ){
            var this_obj = this;
            // var row_elt = this.shadowRoot.querySelectorAll('tr.sck_data_row')[ ref_data['row_no'] ]
            var row_elt = this.shadowRoot.querySelector(`tr[data-pseudo_id='${ pseudo_id }']` ) //find table row entry
            
            for( const elt_key in new_data){ //loop through and udpate values
                var new_data_item = new_data[ elt_key ]
                
                this_obj._update_row_values_update_data_twin( pseudo_id, new_data_item)
                
                //update the httml
                var html_elt = row_elt.querySelector('.' + new_data_item.id )  
                if(html_elt){   //If this is a default hidden field from [submit_hidden_data] tehre may not be an html element
                    html_elt.innerHTML = new_data_item.display_value;
                    html_elt.dataset['value'] = new_data_item.value;
                }
            };
        }

        //************************************************************************************
        _update_row_values_update_data_twin( pseudo_id, new_data_item ){
            var inp_data_fields = this._data_twin[  pseudo_id  ] //reference the data values and update them for future ref
            
            var item_found = false
            for( const input_data_key  in inp_data_fields){
                if( inp_data_fields[ input_data_key ].id == new_data_item.id ){
                    inp_data_fields[ input_data_key ].value = new_data_item.value 
                    item_found = true
                }
            };

            if( ! item_found){  
                // debugger;
                inp_data_fields.push( {'id':new_data_item.id, 'value':new_data_item.display_value, 'data-value':new_data_item.value  })
            }
        }

        //************************************************************************************
        init_submit_button_action(){
            var this_obj = this;
            var button_elt = this.shadowRoot.querySelector('#si_submit');
            if( button_elt){
                button_elt.addEventListener('wc_click', function( event ){ 
                    if( !this_obj._updater.is_empty() ){
                        this_obj._updater.submit(   function(success_data){
                            this_obj.trigger_custom_event( success_data, 'submit_success');
                            this_obj._updater.clear_queue()
                        },
                        function(fail_data){ 
                            this_obj.trigger_custom_event( fail_data, 'submit_failed');
                        } );  
                    }else{
                        C_UI.popup_fail( 'no data to svae' ); 
                    }
                    
                });
            }
        }

        // //************************************************************************************
        // //Add attribute element
        // add_attribute(search_attribute_name, attribute_data_obj, write_attrib_name){
        //     if( search_attribute_name in attribute_data_obj){
        //         var new_attrib_name = ( write_attrib_name ? write_attrib_name : search_attribute_name )
        //         return `${new_attrib_name}='${attribute_data_obj[search_attribute_name]}' `
        //     }
        //     return "";
        // }

        // //************************************************************************************
        // add_table_attrb_class_list( attrib_data_obj, class_key_list, additional_class_list){
        //     var class_str = ""
        //     class_key_list.forEach( function(elt){
        //         if( elt in attrib_data_obj     ){ class_str += attrib_data_obj[ elt ] + " "; }
        //     });

        //     if( additional_class_list){
        //         additional_class_list.forEach( function(class_item){ class_str += class_item + " "; });    
        //     }
            
        //     return 'class ="' + class_str +'" '
        // }

        // //************************************************************************************
        // init_table_data(cols, data){
        //     var table_str = ""; 
        //     var this_obj = this;
        //     // debugger
        //     for( var key in data){
        //         table_str += this_obj.init_table_data_row( this_obj._inp.columns, data[key], key, 'id') //, row_no )
        //     }
        //     // data.forEach( function( data_row){ //}, row_no ){
        //     //     table_str += this_obj.init_table_data_row( this_obj._inp.columns, data_row, 'id') //, row_no )
        //     // });
        //     this.shadowRoot.getElementById('si_tbody').innerHTML = table_str; 
        //     this.add_table_row_item_events()
        // }

        
        // //************************************************************************************
        // init_table_data_row(cols, row_data, pseudo_id, key_field_name){ //}, row_no){
        //     var this_obj = this;
        //     var row_str = "";

        //     row_str += `<tr `;
        //     row_str += this_obj.add_table_attrb_class_list( row_data, ['class'],  ['has-text-centered', 'sck_data_row'] )
        //     // row_str += `data-row_no="${row_no}" `
        //     row_str += `data-pseudo_id="${ pseudo_id }" `
            
        //     // row_str += this_obj.add_attribute( 'data-row_no', row_data )  
        //     // debugger;
            
        //     row_str += ">"
        //     cols.forEach( function( col){
        //         var data_cell = C_UTIL.search_list_dict_key_value( row_data, key_field_name , col[ 'id' ] );
                
        //         row_str += `<td `
        //         row_str += this_obj.add_attribute( 'width', col )
        //         // row_str += `data-row_no="${row_no}" `
        //         row_str += `data-pseudo_id="${ pseudo_id }" `
                
        //         if( col['hidden'] ){  row_str += ' style="display:none;" ' }
        //         if( data_cell ){  //in case this is a static cell - 
        //             if( 'data-value' in data_cell){ row_str += `data-value="${ data_cell['data-value'] }"`
        //             }else{  row_str += `data-value="${ data_cell['value']}"` }    

        //             row_str += this_obj.add_attribute( 'validation', data_cell, 'data-validation' )

        //             row_str += this_obj.add_table_attrb_class_list( data_cell, [ key_field_name ] ) 
        //         }

        //         // if( 'validation')


        //         //set background color
        //         if(  String( col['key_field']).toLowerCase() == 'true'){ row_str += `class="sc_cell_bg_key_color" ` }
        //         row_str += '>'

        //         if( col['type'] == 'actions'){
        //             row_str += this_obj._init_table_cell_add_actions( col, pseudo_id );//row_no );
        //         }else if( data_cell ){
        //             row_str += this_obj.shadowRoot.querySelector('#si_modal').get_field_display_value(data_cell.id,data_cell.value)
        //         } 
        //         row_str += '</td>'
        //     });

        //     row_str += `</tr>`;

        //     return row_str;
        // }

        // //************************************************************************************
        // // Add any icon elements in a table cell
        // //example: "icons":[ {"icon_class":"fa-edit", "class_key":"ck_env_edit", "data-value":"3"},
        // //                   {"icon_class":"fa-trash", "class_key":"ck_env_delete", "data-value":"3"}] }
        // _init_table_cell_add_actions( col_entry, pseudo_id){ //row_no ){
        //     var cell_str = "";
        //     var this_obj = this;
        //     // debugger;
        //     col_entry.actions.forEach( function(action_item ){

        //         // var icon_class = search_list_dict_key_value( this_obj._inp.action_icons, 'action', action_item )

        //         cell_str += `<a href="#" ` 
        //         cell_str += `data-action="${action_item}" ` 
        //         // cell_str += `data-row_no="${row_no}" `
        //         cell_str += `data-pseudo_id="${pseudo_id}" `
        //         cell_str += `class="sc_icon_clickable" >`
        //         cell_str += `<i class="${ this_obj._inp.action_icons[ action_item ] }"></i>`
        //         cell_str += `</a>`
        //         // debugger
        //     });
            
        //     return cell_str; 
        // }



        // //************************************************************************************
        // //Update teh default settings per field once shadowdom is setup
        // create_table(columns){
        //     var table_str = "<tr>"; 
        //     var this_obj = this;
        //     columns.forEach( function( elt){
        //         table_str += `<th `;
        //         table_str += this_obj.add_table_attrb_class_list( elt, ['class', 'id'] )
        //         table_str += this_obj.add_attribute( 'width', elt );

        //         if( elt['hidden'] ){  table_str += ' style="display:none;" ' }

        //         table_str += `>${elt.col_label}</th>`; 
        //     });
        //     table_str += `</tr>`;
        //     if(columns){ 
        //         this.shadowRoot.getElementById('si_thead').innerHTML = table_str; 
        //     }else{ 
        //         this.shadowRoot.getElementById('si_thead').innerHTML = ""; 
        //     }
        // }


        //************************************************************************************
        // columns='[
        //              {"col_label":"ID", "id":"si_env_id", "editable":"false", "hidden":"true","key_field":"true"},
        //              {"col_label":"Name", "id":"si_env_name", "editable":"true"},
        //              {"col_label":"Description", "id":"si_env_desc", "editable":"true" },
        //              {"col_label":"Code", "id":"si_env_code", "editable":"true", "validation":{"text_min_len":4}  },
        //              {"col_label":"Action", "id":"si_env_action", "type":"actions", "data-key":"ck_env_edit", "actions":["edit","delete"] }
        //   ]'
        validate_schema_columns(){
            const schema = {
                type: "array",
                items: {
                            type: "object",
                            properties:{
                                            col_label   : {type: "string"},
                                            id          : {type: "string"},
                                            editable    : { "$ref": "#/definitions/bool_type"},
                                            hidden      : { "$ref": "#/definitions/bool_type"},
                                            type        : { type: "string", enum: ["input", "hidden", "select", "checkbox", "actions"] },
                                            "data-key"  : {type: "string"},
                                            actions     : { type: "array", items: {  type: "string"  } },
                                            key_field   : { "$ref": "#/definitions/bool_type"},
                                            field_params       : { type: "object", properties:{  list: { type: "string"} } },
                                            validation : {
                                                            type            : "object",
                                                            properties:{
                                                                            text_min_len    : {type: "number"},
                                                                            text_max_len    : {type: "number"},
                                                                            text_num_gte    : {type: "number"},
                                                                            text_num_lte    : {type: "number"},
                                                                            required        : { "$ref": "#/definitions/bool_type"} }
                                            }
                                        },
                            required: ["col_label", "id"]
                        },
                definitions: {
                    bool_type: {    type: "string",
                                    enum: ["false","true"] }
                }
            } 
            this.validate_inp_json_schema( 'columns', this._inp.columns, schema )
        }

        //************************************************************************************
        // param='{
        //    "file_type_list":{"log":"Log", "base":"Base Directory", "app":"App Directory",  "def":"Library Directory", "resdef":"Resource  Directory"}
        //}'
        //************************************************************************************
        validate_schema_column_params(){
            const schema = {
                type: "object",
                properties: {}
            }
            this.validate_inp_json_schema( 'field_params', this._inp.field_params, schema )
        }

        //************************************************************************************
        // data='[ [    {"id":"si_env_id", "value":"1" },
        //              {"id":"si_env_name", "value":"Dev", "data-value":"1" },
        //              {"id":"si_env_desc", "value":"Development"},
        //              {"id":"si_env_code", "value":"dev"}  ] ]
        validate_schema_data(){
            const schema = {
                type: "array",
                items: {
                            type: "array",
                            items: {
                                        type: "object",
                                        properties:{
                                            id          : {type: "string"},
                                            value       : {},
                                            "data-value": {type: "string"}
                                        },
                                        required: ["id", "value"]
                                    }
                        }
            }

            this.validate_inp_json_schema( 'data', this._inp.data, schema )
        }
        //************************************************************************************
        // submit_hidden_data='{"id":"si_env_id", "value":"{{env_data.id}}" }' 
        validate_schema_submit_hidden_data(){
            const schema = {
                type: "object",
                properties: {
                  id    : {type: "string"},
                  value : {type: "string"}
                },
                required: ["id", "value"],
                additionalProperties: false
              }
            this.validate_inp_json_schema( 'submit_hidden_data', this._inp.submit_hidden_data, schema )
        }

        //************************************************************************************
        // popup_messages='{    "add_success":"added", "add_fail":"failed to add", 
        //                      "edit_success":"edited", "edit_fail":"failed to edit", 
        //                      "del_success":"deleted", "del_fail":"failed to delete" }'
        validate_schema_popup_messages(){
            const schema = {
                type: "object",
                properties: {
                    add_success     : {type: "string"},
                    add_fail        : {type: "string"},
                    edit_success    : {type: "string"},
                    edit_fail       : {type: "string"},
                    del_success     : {type: "string"},
                    del_fail        : {type: "string"}

                },
                required: ["add_success", "add_fail","edit_success", "edit_fail", "del_success", "del_fail"],
                additionalProperties: false
              }
            this.validate_inp_json_schema( 'popup_messages', this._inp.popup_messages, schema )
        }

        // //************************************************************************************
        // // check schema
        // #validate_inp_json_schema( attribute_name, attribute_value, schema){
        //     if(attribute_value){
        //         const validate = this.ajv.compile(schema)
        //         const valid = validate( attribute_value )
        //         if (!valid){
        //             // debugger;
        //             throw `Failed validation of json for ${this._inp.id} '${attribute_name}':: [${ JSON.stringify(validate.errors)}]`;
        //         }
        //     }
        //     return true;
        // }

        is_debug(){ return false; } 

    }

    window.customElements.define('wc-table', WCTable);



        // //************************************************************************************
        // submit_queue_add(submit_type, data ){
        //     this._submit_queue[ submit_type ].push( data )
        // }

        // _submit_data_auto_bulk_update( ret_data){
        //     if( ret_data.success ){  //If return successfully
                
        //         console.log( JSON.stringify(ret_data) )
        //     }
        // }


        // //************************************************************************************
        // submit_queue_execute(){ 
        //     var this_obj = this

        //     this_obj.submit_data_auto(  this_obj._inp.submit_on_add, add_data, 
        //         this_obj._inp.popup_messages.add_success, 
        //         this_obj._inp.popup_messages.add_fail,
        //         this_obj._submit_data_auto_bulk_update) 
            
        //     // this._submit_queue[  this._SUBMIT_TYPE_ADD ].forEach( function(add_data ){
        //     //     this_obj.submit_data_auto(  this_obj._inp.submit_on_add, add_data, 
        //     //                                 this_obj._inp.popup_messages.add_success, 
        //     //                                 this_obj._inp.popup_messages.add_fail,
        //     //                                 this_obj._submit_data_auto_callback_row_add) 
        //     // } );

        //     // this._submit_queue[  this._SUBMIT_TYPE_EDIT ].forEach( function(edit_data ){
        //     //     this_obj.submit_data_auto(  this_obj._inp.submit_on_edit, edit_data, 
        //     //                                 this_obj._inp.popup_messages.edit_success, 
        //     //                                 this_obj._inp.popup_messages.edit_fail) 
        //     // } );
            
        //     // this._submit_queue[  this._SUBMIT_TYPE_DEL ].forEach( function(del_data ){
        //     //     this_obj.submit_data_auto(  this_obj._inp.submit_on_del, del_data, 
        //     //                                 this_obj._inp.popup_messages.del_success, 
        //     //                                 this_obj._inp.popup_messages.del_fail) 
        //     // } );
        //     // this._submit_queue      
        //     // for (const key of Object.keys( this._submit_queue )) {
        //     //     this._submit_queue[key] = []    // flash each item
        //     //   }
        // }



        // //************************************************************************************
        // submit_data_bulk( url, data, submit_data_bulk_callback){
        //     submit_data_bulk_callback( url, 'submit', data );
        //     C_AJAX.ajax_post( url, data, 
        //         function(success_data){
        //             submit_data_bulk_callback( url, 'success', success_data );
        //             this_ref.trigger_custom_event( success_data, 'submit_success');
        //         },
        //         function(fail_data){
        //             submit_data_bulk_callback( url, 'fail', fail_data );
        //             this_ref.trigger_custom_event( fail_data, 'submit_failed');
        //         } );
        // }

        // //************************************************************************************
        // submit_data_auto( url, data, success_message, fail_message, callback){
        //     var this_ref = this
        //     C_AJAX.ajax_post( url, data, 
        //         function(success_data){
        //             if( success_message  ){ C_UI.popup_success( success_message ); }
        //             if( callback ){ callback( success_data ) }
        //             this_ref.trigger_custom_event( success_data, 'submit_success');
                    
        //         },
        //         function(fail_data){
        //             if( fail_message  ){ C_UI.popup_fail( fail_message ); } 
        //             if( callback ){ callback( fail_data ) }
        //             this_ref.trigger_custom_event( fail_data, 'submit_failed');
        //         } );
        // }

        //** 
        // _submit_data_auto_callback_row_add( ret_data){
        //     if( ret_data.success ){  //If return successfully
                
        //         console.log( JSON.stringify(ret_data) )
        //         // debugger;
        //         // var new_data = [];
        //         // this._inp.columns.forEach(  function( col){
        //         //     var item = {}
        //         //     var db_field_name;
        //         //     item.id = col.id

        //         //     for (const [key, schema_data] of Object.entries( ret_data.schema )) {
        //         //         if( item.id in schema_data.fields){
        //         //             db_field_name = schema_data.fields[ item.id ].field_db;
        //         //         }
        //         //     }

        //         //     item.value = ret_data.data[0][ db_field_name ]
        //         //     new_data.push( item );
        //         // });

        //         // this._callback_row_add_update_table(new_data);
        //         // this._callback_row_add_update_data_twin(new_data);
        //         // this.add_table_row_item_events()
        //     }
        // }