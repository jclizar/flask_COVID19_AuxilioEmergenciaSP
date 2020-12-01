jQuery("form[name=faleConosco_form").submit(function(e)
{
    let $form = jQuery(this) //$variavel interna
    let $msg= $form.find(".msg") //vai no form e procura a tag html que tenha class = "error", pode carregar todas as tags q tiverem essa classe (tipo error* coringa)
    var form_data = $form.serialize() // variavel global, vai oegar todos os inputs do form e criar chave-valor
    //serialize devolve a query string
    
    
    let button =  $form.find('input[type="submit"]')
    //let loading =  $form.find('.loading')

    //loading.show()

    $msg.attr("class","loading")//carrega automaticamente a classe

    button.prop('disabled',true)

    jQuery.ajax // faz a request do servidor linkar front-back
    ({
        url: "/user/fale-conosco/",
        type: "POST",
        data: form_data,
        dataType: "json",

        success: function(resp)
        {
            $msg.text(resp.msg).attr("class","msg sucess")
            //loading.hide()
            button.prop('disabled',false)
        },
        error: function(resp)
        {
            $msg.text(resp.responseJSON.msg).attr("class","msg error")
            //loading.hide()
            button.prop('disabled',false)
        }
        
    })
    
    e.preventDefault();
});

