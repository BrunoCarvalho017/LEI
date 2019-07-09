var express = require('express');
var router = express.Router();
var formidable = require('formidable')
var fs = require('fs');
var path = require('path');
const {PythonShell} = require("python-shell");

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Harambe' });
});

router.get('/convert', function(req, res, next) {
  res.render('transformador');
});

router.post('/convert/file', function(req, res, next) {
    var form = new formidable.IncomingForm()
    form.parse(req, (erro,fields,files)=>{
        var fenviado = files.ficheiro.path
  
        var fnovo = './public/uploaded/'+files.ficheiro.name
        console.log("POST [fnovo]:"+fnovo)

        fs.rename(fenviado, fnovo, erro => {
          if(!erro){
            let options = {
              mode: 'text',
              pythonPath: '/usr/local/bin/python3',
              pythonOptions: ['-u'], // get print results in real-time
              scriptPath: './public/pyscripts',
              args: [fnovo]
            };
            PythonShell.run('analisador.py', options, function (err, results) {
              if (!err) {
                console.log('results: %j', results);
                res.download();
              }
              else{
                console.log("Erro no tranformador")
                res.render('error',{error: err});
              }
            });
          }else{
            console.log("ERRO")
          }
        })
    })
  
});


module.exports = router;
