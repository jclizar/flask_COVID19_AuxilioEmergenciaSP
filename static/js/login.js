jQuery("form[name=login_form").submit(function(e)
{
    let $form = jQuery(this) //$variavel interna
    let $error= $form.find(".error") //vai no form e procura a tag html que tenha class = "error", pode carregar todas as tags q tiverem essa classe (tipo error* coringa)
    var data = $form.serialize(); // variavel global, vai oegar todos os inputs do form e criar chave-valor

    jQuery.ajax // faz a request do servidor linkar front-back
    ({
        url: "/user/login/",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp)
        {
            window.location.href="/menu/";
        },
        error: function(resp)
        {
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
        
    })
    
    e.preventDefault();
});

