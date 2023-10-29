 
 
    import WCEltParent from  "/webui/mangosteen/mangosteen/static/zwc/wc_elt_parent.js" 
 
    

    // var wc_form_ref_instance = customElements.get('wc-form-main');
    export default class WCMessage extends WCEltParent { 
        define_template(){
            var message  =  `<div class="field"> `
            message +=      '<strong>[placeholder::message_header]</strong>'
            message +=      this._inp['message_header'].length >0 && this._inp['message'].length >0 ? '<strong>: </strong>'  : ''
            message +=      "[placeholder::message]"
            message +=  `</div>  `
            return message;
        }

        constructor(){
            super(  {"class":"" , "message_type=opt[error,info,warn,success,]":"", "message_header":"", "message":""}, ["id"]);   
        } 
        //************************************************************************************
        //Setup the defaults and events
        connectedCallback(){     
             super.connectedCallback(); 
        } 
        init_component(){} 
 
    }
 

     
    window.customElements.define('wc-message', WCMessage);  
