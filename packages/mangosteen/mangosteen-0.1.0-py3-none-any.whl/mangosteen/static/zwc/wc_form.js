import WCGroupParent from  '/webui/mangosteen/mangosteen/static/zwc/wc_grp_parent.js' ;


export default class WCForm extends WCGroupParent  { 
    define_template(){
        var button_str = "";

        if( this._inp.button ){
            button_str = `<wc-button id="sci_form_submit" label="[placeholder::button_label]"  > </wc-button>   `
        }
        
        var html_str = super.define_template() + 
                        `   <div class="container">
                                <form id="si_field" name="[placeholder::name]" action="[placeholder::action]" method="[placeholder::method]">
                                    <slot>
                                    </slot>
                                    ${button_str}
                                </form> 
                            </div>`
        return html_str;
    } 

    constructor( ) {
        console.log('construct group')
        
        super( {"submit_data_selector":"", "method":"post", "button=bool":"true", "button_label":"Submit"},
               [ "id", "name", "action"]); 
    }

    connectedCallback(){     
        super.connectedCallback(); 
        var submit_button = this.shadowRoot.querySelector('#sci_form_submit')
            // debugger;
        if(submit_button){
            submit_button.addEventListener('wc_click', this.submit_data_post.bind(this)  );
        }
    }

    submit_data_post(evt){ 
        var this_ref = this  
        console.log('submitting now')
        debugger;
        if( this_ref.is_ready_to_submit() ){  
             this_ref.shadowRoot.querySelector( '#si_field').submit();
             this_ref.evt_process_clicked(evt);
        }else{
            this_ref.trigger_custom_event( data, 'validation_failed');
            throw "***validation failed**"
        } 
    }

}

window.customElements.define('wc-form', WCForm); 



