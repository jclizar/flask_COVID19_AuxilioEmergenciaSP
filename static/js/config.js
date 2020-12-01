function deleteUser(){
    
    let $form = jQuery(this)
    let $msg= $form.find(".msg");


    jQuery.ajax // faz a request do servidor linkar front-back
    ({
        url: "/user/configDelete/",
        type: "DELETE",
        dataType: "json",
        success: function(resp)
        {
            window.location.href="/"
        },
        error: function(resp)
        {
            $msg.text(resp.responseJSON.msg).attr("class","msg error");           

        }  
    });
}

function habilitarEditar(){
    let $form = jQuery("form[name=config_form]");
    let $form_input = $form.find('input');
    let $btn_salvar = $form.find('button[name="save"]');
    let $btn_deletar = $form.find('button[name="del"]');
    let $msg= $form.find(".msg");

    $form_input.each((index, input) => {
        if(input.disabled && input.name != 'email'){

            $btn_deletar.prop('disabled', true); //obj jquery
            $btn_salvar.prop('disabled', false); //obj jquery
            input.disabled = false;//js
        }else{
            $form.trigger("reset");
            $btn_deletar.prop('disabled', false); //obj jquery
            $btn_salvar.prop('disabled', true); //obj jquery
            
            input.disabled = true;//js

            $msg.html('')
        }
    });
}

function updateSalvar(){
    let $form = jQuery("form[name=config_form]");
    let $msg= $form.find(".msg");

    jQuery.ajax // faz a request do servidor linkar front-back
    ({
        url: "/user/configSave/",
        type: "PUT",
        dataType: "json",
        data: $form.serialize(), //input >json
        success: function(resp)
        {
            $msg.text(resp.msg).attr("class","msg sucess");
        },
        error: function(resp)
        {
            $msg.text(resp.responseJSON.msg).attr("class","msg error");
        }  
    });

}
