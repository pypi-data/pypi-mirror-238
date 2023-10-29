import C_UTIL, {C_UI, C_AJAX } from '/webui/mangosteen/mangosteen/static/zjs/common_utils.js'; //


export default class WCTable_GUI    { 

    constructor( dom_ref, inp, evt_icon_clicked_fn){
        this._shadowRoot = dom_ref;
        this._evt_icon_clicked_fn = evt_icon_clicked_fn
        this._inp = inp 
        
    }

    init( data_twin ){
        this.init_modal(this._inp.columns);
        // this.init_submit_button_action()


        this.create_table( this._inp.columns )
        // this.create_table( this._inp.columns );

        // this.init_table_data(this._inp.data)
        this.init_table_data( this._inp.columns, data_twin , this._inp.action_icons ) //[pseudo_id]) //this._inp.data)
        this.add_table_row_item_events()
    }
    //************************************************************************************
    //Add events to table cells
    add_table_row_item_events(  ){
        var this_obj = this;
        this._shadowRoot.querySelectorAll('.sc_icon_clickable').forEach(item =>{
            item.addEventListener( 'click',  (event)=> this_obj._evt_icon_clicked_fn(event) );  
        });
        
    }

    
    //************************************************************************************
        //Update teh default settings per field once shadowdom is setup
    create_table(columns){
        var table_str = "<tr>"; 
        var this_obj = this;
        columns.forEach( function( elt){
            table_str += `<th `;
            table_str += this_obj.add_table_attrb_class_list( elt, ['class', 'id'] )
            table_str += this_obj.add_attribute( 'width', elt );

            if( elt['hidden'] ){  table_str += ' style="display:none;" ' }

            table_str += `>${elt.col_label}</th>`; 
        });
        table_str += `</tr>`;
        if(columns){ 
            this._shadowRoot.getElementById('si_thead').innerHTML = table_str; 
        }else{ 
            this._shadowRoot.getElementById('si_thead').innerHTML = ""; 
        }
    }

    //************************************************************************************
    //Add attribute element
    add_attribute(search_attribute_name, attribute_data_obj, write_attrib_name){
        if( search_attribute_name in attribute_data_obj){
            var new_attrib_name = ( write_attrib_name ? write_attrib_name : search_attribute_name )
            return `${new_attrib_name}='${attribute_data_obj[search_attribute_name]}' `
        }
        return "";
    }

    //************************************************************************************
    //Add html-attrib class items where the value comes from attrib_data_obj and the lookup
    //value comes from class_key_list
    add_table_attrb_class_list( attrib_data_obj, class_key_list, additional_class_list){
        var class_str = ""
        class_key_list.forEach( function(elt){
            if( elt in attrib_data_obj     ){ class_str += attrib_data_obj[ elt ] + " "; }
        });

        if( additional_class_list){
            additional_class_list.forEach( function(class_item){ class_str += class_item + " "; });    
        }
        
        return 'class ="' + class_str +'" '
    }

    //************************************************************************************
    init_table_data(cols, data, action_icons){
        var table_str = ""; 
        var this_obj = this;
        // debugger
        for( var key in data){
            table_str += this_obj.init_table_data_row( cols, data[key], key, 'id', action_icons) //, row_no )
        }
        // data.forEach( function( data_row){ //}, row_no ){
        //     table_str += this_obj.init_table_data_row( this_obj._inp.columns, data_row, 'id') //, row_no )
        // });
        this._shadowRoot.getElementById('si_tbody').innerHTML = table_str; 
        // this.add_table_row_item_events()
    }

    //************************************************************************************
    init_table_data_row(cols, row_data, pseudo_id, key_field_name, action_icons){ //}, row_no){
        var this_obj = this;
        var row_str = "";

        
        row_str += `<tr `;
        row_str += this_obj.add_table_attrb_class_list( row_data, ['class'],  ['has-text-centered', 'sck_data_row'] )
        row_str += `data-pseudo_id="${ pseudo_id }" `
        
        row_str += ">"
        cols.forEach( function( col){
            var data_cell = C_UTIL.search_list_dict_key_value( row_data, key_field_name , col[ 'id' ] );
            
            row_str += `<td `
            row_str += this_obj.add_attribute( 'width', col ) 
            row_str += `data-pseudo_id="${ pseudo_id }" `
            
            if( col['hidden'] ){  row_str += ' style="display:none;" ' }
            if( data_cell ){  //in case this is a static cell - 
                if( 'data-value' in data_cell){ row_str += `data-value="${ data_cell['data-value'] }"`
                }else{  row_str += `data-value="${ data_cell['value']}"` }    
                row_str += this_obj.add_attribute( 'validation', data_cell, 'data-validation' )
                // row_str += this_obj.add_table_attrb_class_list( data_cell, [ key_field_name ] ) 
            }
            row_str += this_obj.add_table_attrb_class_list( col, [ key_field_name ] )
 
            //set background color
            if(  String( col['key_field']).toLowerCase() == 'true'){ row_str += `class="sc_cell_bg_key_color" ` }
            row_str += '>'

            if( col['type'] == 'actions'){
                row_str += this_obj._init_table_cell_add_actions( col, action_icons, pseudo_id );//row_no );
            }else if( data_cell ){
                row_str += this_obj._shadowRoot.querySelector('#si_modal').get_field_display_value(data_cell.id,data_cell.value)
            } 
            row_str += '</td>'
        });

        row_str += `</tr>`;

        return row_str;
    }

    //************************************************************************************
    // Add any icon elements in a table cell
    //example: "icons":[ {"icon_class":"fa-edit", "class_key":"ck_env_edit", "data-value":"3"},
    //                   {"icon_class":"fa-trash", "class_key":"ck_env_delete", "data-value":"3"}] }
    _init_table_cell_add_actions( col_entry, action_icons, pseudo_id){ //row_no ){
        var cell_str = "";
        var this_obj = this;
        // debugger;
        col_entry.actions.forEach( function(action_item ){

            // var icon_class = search_list_dict_key_value( this_obj._inp.action_icons, 'action', action_item )

            cell_str += `<a href="#" ` 
            cell_str += `data-action="${action_item}" ` 
            // cell_str += `data-row_no="${row_no}" `
            cell_str += `data-pseudo_id="${pseudo_id}" `
            cell_str += `class="sc_icon_clickable" >`
            cell_str += `<i class="${ action_icons[action_item] }"></i>`
            cell_str += `</a>`
            // debugger
        });
        
        return cell_str; 
    }


    //************************************************************************************
    init_modal(columns){
        var this_obj = this;
        var field_list = []
        // debugger;
        for( var col_index in columns){
            const elt = columns[col_index ]
            if( elt.editable == "true" || elt.hidden == "true"){
                var field_data = {}
                field_data.type = this_obj._init_modal_get_field_type(elt)
                field_data.label = elt.col_label;
                field_data.id = elt.id; 
                // debugger;
                field_data.validation = elt.validation;

                if( "field_params" in elt){  //If there are further parameters - e.g. lookup fields
                    // debugger;
                    for( var param_field in elt.field_params){
                        const param_name = elt.field_params[ param_field ]
                        field_data[ param_field ] = this._inp.field_params[ param_name  ]
                    }
                }
                field_list.push( field_data );
            }
        };
        this._shadowRoot.querySelector('#si_modal').fields = field_list;
    }

    //************************************************************************************
    _init_modal_get_field_type(elt){
        if( elt.hidden  == "true" ){ return 'hidden'; }
        return ( typeof elt.type  === 'undefined' ? 'input': elt.type );    
    }

    
}