let table_config = selecionar_configuracao_tabela()

iniciarTabela(table_config)

function iniciarTabela(table_config){
    jQuery('table[name="tables"]').bootstrapTable(table_config) //div table procurar name = tables
}


function selecionar_configuracao_tabela(){
    let $form = jQuery('form[name="form-tables"]')

    let select_table_option = $form.find('select').val()

    let config_padrao = {
        search: true,
        pagination: true, //gerar opção de mudar de página
        sidePagination: 'server',
        toggle: 'table',
        pageSize: 5,
        queryParams: function(p) {
            return {
                search: p.search, //PESQUISAR do bootstrap-table
                sort: p.sort,
                order: p.order,
                limit: parseInt(p.limit),
                offset: parseInt(p.offset)
            };
        },
    }

    let table_options = {
        'users': {
            url: window.location.origin + '/user/tabela-user/',
            columns:[{
                    field: 'name',
                    title: 'Nome'
                },{
                    field: 'type',
                    title: 'Tipo de Acesso'
                },{
                    field: 'email',
                    title: 'Email'
                },{
                    title: 'Ações',
                    align: 'center',
                    formatter: acoesUsuario
                }
            ]
        },
        'beneficioDataAPI': {
            
        }
    }


    return {
        ...config_padrao,
        ...table_options[select_table_option]
    }
}

function acoesUsuario(value, row, index){
    // lista de botões de ações que sera renderizada na tabela
    let buttons = []

    //cria o botão para trocar o tipo de acesso do usuário ('admin' ou 'user')

    let btn_atualizar_tipo_usuario =  '';

    if(row.type === 'user'){//user da tabela do type user MONGODB
        btn_atualizar_tipo_usuario = '<button type="button" class="btn btn-outline-primary mr-2" onclick="atualizar_tipo_usuario(\''+ row._id +'\', \'admin\')">'+
                                        '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-person-bounding-box" fill="currentColor" xmlns="http://www.w3.org/2000/svg">'+
                                            '<path fill-rule="evenodd" d="M1.5 1a.5.5 0 0 0-.5.5v3a.5.5 0 0 1-1 0v-3A1.5 1.5 0 0 1 1.5 0h3a.5.5 0 0 1 0 1h-3zM11 .5a.5.5 0 0 1 .5-.5h3A1.5 1.5 0 0 1 16 1.5v3a.5.5 0 0 1-1 0v-3a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 1-.5-.5zM.5 11a.5.5 0 0 1 .5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 1 0 1h-3A1.5 1.5 0 0 1 0 14.5v-3a.5.5 0 0 1 .5-.5zm15 0a.5.5 0 0 1 .5.5v3a1.5 1.5 0 0 1-1.5 1.5h-3a.5.5 0 0 1 0-1h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 1 .5-.5z"/>'+
                                            '<path fill-rule="evenodd" d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H3zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>'+
                                        '</svg>'+
                                    '</button>'
        
    }else{
        btn_atualizar_tipo_usuario = '<button type="button" class="btn btn-outline-primary mr-2" onclick="atualizar_tipo_usuario(\''+ row._id +'\', \'user\')">'+
                                        '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-person-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">'+
                                            '<path fill-rule="evenodd" d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H3zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>'+
                                        '</svg>'+
                                    '</button>'
    }
    
    //cria o botão para habilitar ou desabilitar o acesso de um usuário ao sistema
    let btn_habilitar_desabilar_usuario = ''

    if(row.ativo){
        btn_habilitar_desabilar_usuario = '<button type="button" class="btn btn-outline-danger" onclick="disabilitar_ou_habilitar_usuario(\'' + row._id + '\', false)">'+
                                                '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-person-x-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">'+
                                                    '<path fill-rule="evenodd" d="M1 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H1zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm6.146-2.854a.5.5 0 0 1 .708 0L14 6.293l1.146-1.147a.5.5 0 0 1 .708.708L14.707 7l1.147 1.146a.5.5 0 0 1-.708.708L14 7.707l-1.146 1.147a.5.5 0 0 1-.708-.708L13.293 7l-1.147-1.146a.5.5 0 0 1 0-.708z"></path>'+
                                                '</svg>'+
                                            '</button>'
    }else{
        btn_habilitar_desabilar_usuario = '<button type="button" class="btn btn-outline-danger" onclick="disabilitar_ou_habilitar_usuario(\'' + row._id + '\', true)">'+
                                                '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-person-plus-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">'+
                                                    '<path fill-rule="evenodd" d="M1 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H1zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm7.5-3a.5.5 0 0 1 .5.5V7h1.5a.5.5 0 0 1 0 1H14v1.5a.5.5 0 0 1-1 0V8h-1.5a.5.5 0 0 1 0-1H13V5.5a.5.5 0 0 1 .5-.5z"/>'+
                                                '</svg>'+
                                            '</button>'
    }   

    //adiciona os botões a lista de botões de acão  
    buttons.push(btn_atualizar_tipo_usuario, btn_habilitar_desabilar_usuario)

    return buttons.join('')
}

function atualizar_tipo_usuario(user_id, tipo){
    jQuery.ajax // faz a request do servidor linkar front-back
    ({
        url: "/user/tornar-admin/",
        type: "PUT",
        dataType: "json",
        data: {
            user_id: user_id,
            tipo: tipo
        },
        success: function(resp)
        {
            jQuery('table[name="tables"]').bootstrapTable('refresh');
        },
        error: function(resp)
        {
            $msg.text(resp.responseJSON.msg).attr("class","msg error");           

        }  
    });
}

function disabilitar_ou_habilitar_usuario(user_id, ativo){
    jQuery.ajax // faz a request do servidor linkar front-back
    ({
        url: "/user/desativar/",
        type: "PUT",
        dataType: "json",
        data: {
            user_id: user_id,
            ativo: ativo
        },
        success: function(resp)
        {
            jQuery('table[name="tables"]').bootstrapTable('refresh');
        },
        error: function(resp)
        {
            $msg.text(resp.responseJSON.msg).attr("class","msg error");           

        }  
    });
}

function export_json(){

    let $form = jQuery('form[name="form-tables"]')

    let select_table_option = $form.find('select').val()//procura tag select: pega valor dela (string)

    jQuery.ajax // faz a request do servidor linkar front-back
    ({
        url: "/user/exporta-colecao/" + select_table_option,
        type: "GET",
        dataType: "json",
        success: function(resp)
        {  
            
            window.location.href = window.location.origin +'/download-file/' + resp.filename
            
        },
        error: function(resp)
        {
            $msg.text(resp.responseJSON.msg).attr("class","msg error");  

        }  
    });
}
    