 
 
    // import ValidationHelper from '/webui/static/zjs/validation_helper.js'; //
    import WCEltParent from  "/webui/mangosteen/mangosteen/static/zwc/wc_elt_parent.js" 
 
    

    // var wc_form_ref_instance = customElements.get('wc-form-main');
    export default class WCHidden extends WCEltParent { 
        define_template(){
            return  ` 
            <div class="field">
                    <input  id="si_field" class="sck_field input" name="[placeholder::id]" 
                            type="hidden" value="[placeholder::value]">
            </div>  
            `;
        }

        constructor(){
            super(  {"class":"" , "label":"", "name":""}, ["id", "value"]);   
        } 
        //************************************************************************************
        //Setup the defaults and events
        connectedCallback(){     
             super.connectedCallback(); 
        } 
        init_component(){} 
 
    }
 

     
    window.customElements.define('wc-hidden', WCHidden);  
