
import WCGroupParent from  '/webui/mangosteen/mangosteen/static/zwc/wc_grp_parent.js' ;


export default class WCGroup extends WCGroupParent  { 
    define_template(){
        return super.define_template() + ` 
                <div class="container">

                    <div class="m-3 ${ this._inp['bordered']?'box':''} p-3" id="si_field">
                        <slot>
                        </slot>

                        <div class="align_elt_right"> 
                            <p class="control "> 
                                <wc-button id="sci_site_save" label="[placeholder::label_save]" 
                                    action="[placeholder::action]" 
                                    submit_data_selector="[placeholder::submit_data_selector]" 
                                    popup_message_submit_success="[placeholder::popup_message_submit_success]"
                                    popup_message_submit_fail="[placeholder::popup_message_submit_fail]"
                                ></wc-button> 
                                <wc-button id="sci_site_cancel" label="[placeholder::label_cancel]" active_class="none" > </wc-button>   
                            </p>  
                        </div> 
                    </div>   

                </div>`
    } 

    // ******************************************************************************************************************************
    //
    constructor( ) {
        console.log('construct group')
        
        super( {"class":"", "bordered=bool":true, "popup_message_submit_success":"Saved", "popup_message_submit_fail":"Save failed",
                "action":"", "submit_data_selector":"","label_cancel":"Cance", "label_save":"Save" },
               ["id"]); 
    }
    
    // ******************************************************************************************************************************
    //
    connectedCallback(){     
        console.log('construct callback group')
        
        super.connectedCallback(); 
        this.shadowRoot.querySelector('#sci_site_cancel').addEventListener('wc_click', this.evt_cancel_clicked.bind(this) );
        this.shadowRoot.querySelector('#sci_site_save').addEventListener('wc_click', this.evt_process_clicked.bind(this) );
        
    }
}

window.customElements.define('wc-group', WCGroup); 



