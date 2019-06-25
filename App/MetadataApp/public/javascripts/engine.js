$(()=>{
    $('#submit').click(e => {

        //e.preventDefault()
        
        /*var file = $('select[name=fileOptions]').val()
        var tipo = $('#header').text()
        console.log(tipo)
        console.log(file)
        var url = "http://localhost:3000/users/compile/"+tipo+"/"+file
        */
        /*$.get(url, function(data, status){
            alert("Data: " + data + "\nStatus: " + status);
        });*/
        
        ajaxPost()
    })

    function ajaxPost(){
        
        const file = new FormData()
        file.append('ficheiro',$('#ficheiro')[0].files[0])
        /*
        file.append('tipo',$('#header').text())
        file.append('caminho', $('select[name=fileOptions]').val())
        console.log($('select[name=fileOptions]').val())
        console.log($('#header').text())
        */
        $.ajax({
            type:"POST",
            contentType:false,
            processData:false,
            url:"http://localhost:3001/users/compile",
            data: file,
            mimeType:'multipart/form-data',
            success: p => alert('Ficheiro gravado com sucesso: '+ p),
            error: e => {
                alert('Erro no POST: '+ JSON.stringify(e))
                console.log('ERRO: ' + e)
            }
        })
        $('#ficheiro').val('')
    }

    /* Para remover um evento */
    $('.buttonRemoveFicheiro').click(function(e){
        e.preventDefault()
        if (confirm('De certeza que pretende eliminar este evento?'))
            ajaxDeleteFicheiro($(this))
    })

    function ajaxDeleteFicheiro(element) {
        var url = element.attr('href')
        $.ajax({
            url: url,
            type: 'POST',
            success: () =>{
                element.closest('tr').remove()
            }
        })
    }

    $("#searchFicheiros").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#ficheirosTable tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
})