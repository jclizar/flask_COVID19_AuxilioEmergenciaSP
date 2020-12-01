
jQuery(document).ready(function(){
    carregar_grafio_por_mes([0,0,0,0,0,0,0,0,0,0,0,0]);
    carregar_grafio_por_mes_pie([0,1]);
});

function carregar_graficos(){
    let municiopio_id = jQuery('select[name="municipio"]').val()

    jQuery.ajax // faz a request do servidor linkar front-back
    ({
        url: "/api/municipio/" + municiopio_id,
        type: "GET",
        dataType: "json",
        success: function(resp)
        {
            change_grafio('grafico-por-mes', 'chart1',resp.beneficiados_por_mes)
            change_grafio('grafico-total', 'chart2',resp.media_beneficiados)
        },
        error: function(resp)
        {
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
        
    })
}

function carregar_grafio_por_mes(data){
    let grafico_por_mes = document.getElementById('grafico-por-mes').getContext('2d');

    let myChart1 = new Chart(grafico_por_mes, 
        {
            type: 'bar',
            data: {
                labels: ['JAN','FEV','MAR','ABR','MAI','JUN','JUL','AGO','SET','OUT','NOV','DEZ'],
                datasets: [{
                    label: 'quantidade',
                    data: data,
                    backgroundColor:'rgba(255, 159, 64, 1)',
                    borderColor: 'rgba(255, 159, 64, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                title: {
                    display: true,
                    text: 'Beneficiados - Auxílio Emergencial',
                    //fontColor: 'white',
                    fontSize: 20
                },
                legend:
                {
                    display: false,
                    labels:
                    {
                        // This more specific font property overrides the global property
                        fontColor: 'white',
                        fontSize: 20
                        
                    }
                },
                scales:
                {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });

}

function change_grafio(canvas_id, div_canvas, data){
    jQuery('#'+canvas_id).remove()

    jQuery("div."+div_canvas).append('<canvas id="'+canvas_id+'"></canvas>')

    selecionar_grafico = {
        'grafico-por-mes': carregar_grafio_por_mes,
        'grafico-total': carregar_grafio_por_mes_pie
    }

    selecionar_grafico[canvas_id](data)
}

function carregar_grafio_por_mes_pie(data){
   let canvas_grafico_total = document.getElementById('grafico-total').getContext('2d');

   let porcentegem = Math.round(data[0]/(data[1]+data[0])*100);
   // And for a doughnut chart
   // And for a doughnut chart
    let myChart2= new Chart(canvas_grafico_total,
    {
        type:"doughnut",
        data:
        {
            labels:["Beneciados","População Município"],
            datasets:
            [
                {
                    data: data,
                    borderColor: ['rgba(255, 159, 64, 1)',"rgba(255, 255, 255, 1)"],
                    backgroundColor:['rgba(255, 159, 64, 1)',"rgba(255, 255, 255, 1)"]
                }
            ]
        },
        options:
        {
            title:
            {
                display: true,
                text:'Média de beneficiados: '+ porcentegem +'%',
                //fontColor: 'white',
                fontSize: 20
            },
        },
    }) 
}

