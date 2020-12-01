jQuery("form[name=esqueciSenha_form]").submit(function(e)
{
    let $form = jQuery(this) //$variavel internalet $error= $form.find(".error") //vai no form e procura a tag html que tenha class = "error", pode carregar todas as tags q tiverem essa classe (tipo error* coringa)
    let $msg= $form.find(".msg")
    var data = $form.serialize(); // variavel global, vai oegar todos os inputs do form e criar chave-valor

    let button =  $form.find('input[type="submit"]')

    $msg.attr("class","loading")//carrega automaticamente a classe

    button.prop('disabled',true)

    jQuery.ajax // faz a request do servidor linkar front-back
    ({
        url: "/user/esqueciSenha/",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp)
        {
            $msg.text(resp.msg).attr("class","msg sucess");
            button.prop('disabled',false)
        },
        error: function(resp)
        {
            $msg.text(resp.responseJSON.msg).attr("class","msg error");
        }
        
    })
    
    e.preventDefault();
});
