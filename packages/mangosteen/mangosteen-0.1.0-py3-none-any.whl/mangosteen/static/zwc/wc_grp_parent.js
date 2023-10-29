import WCRoot from  '/webui/mangosteen/mangosteen/static/zwc/wc_root.js' ;
import WCEltParent from '/webui/mangosteen/mangosteen/static/zwc/wc_elt_parent.js';


export default class WCGroupParent extends WCEltParent  { 
    // constructor(optional_attrib_dict, mandatory_attrib_list) {
    //     // super();  
    //     super( optional_attrib_dict, mandatory_attrib_list) 
        
    // }

    // constructor( ) {
    //     console.log('construct group')
        
    //     super( {"bordered=bool":true, "popup_message_submit_success":"Saved", "popup_message_submit_fail":"Save failed",
    //             "action":"", "submit_data_selector":"","label_cancel":"Cance", "label_save":"Save" },
    //            ["id"]); 
    // }

    // connectedCallback(){     
    //     console.log('construct callback group')
        
    //     super.connectedCallback(); 
    //     this.shadowRoot.querySelector('#sci_site_cancel').addEventListener('wc_click', this.evt_cancel_clicked.bind(this) );
    //     this.shadowRoot.querySelector('#sci_site_save').addEventListener('wc_click', this.evt_save_clicked.bind(this) );
        
    // }

    process_attributes(optional_attrib_dict, mandatory_attrib_list){   //override master function
        super.process_attributes(optional_attrib_dict, mandatory_attrib_list);

        //make sure the search is just within this group
        this._inp.submit_data_selector = "#" + this.id + " " + this._inp.submit_data_selector 
    }


    //####################################################################################################################
    evt_cancel_clicked( event ){
        this._init_values.forEach( function(item){
            item.elt.value = item.orig_value;
        });
    }

    //####################################################################################################################
    evt_process_clicked( event ){
        this._init_values.forEach( function(item){
            item.orig_value = item.elt.value;
        } );
    }
     
    //####################################################################################################################
    init_component(){
        console.log('construct init component group')
        this._init_values = []
        this.get_init_values(  this.childNodes );
    }

    //####################################################################################################################
    get_init_values( child_node_list){
        var this_obj = this; 
        child_node_list.forEach( function(node){
            if( node.childNodes ){
                this_obj.get_init_values(node.childNodes )
            } 
            if( node.classList  &&  node.classList.contains(  this_obj._inp.submit_data_selector)  ){   
                this_obj._init_values.push( { "elt":node, "orig_value":node.value })
 
                
            }
        });

    }
    
    //####################################################################################################################
    hide(){
        this.shadowRoot.querySelector('#si_field').classList.add('is-hidden');
        const event = new CustomEvent('group_disappear', { detail: {this:this  }} );
        this.dispatchEvent(event , { bubbles:true, component:true} ); 
    }

    show(){
        this.shadowRoot.querySelector('#si_field').classList.remove('is-hidden');

        console.log("trigger group appear [0]:" + this.id )
        const event = new CustomEvent('group_appear', { detail: {this:this  }} );
        this.dispatchEvent(event , {bubbles:true,component:true } ); 
        console.log("trigger group appear [1]:" + this.id )
    }
}

// window.customElements.define('wc-group', WCGroup); 



