var express = require('express');
var fs = require('fs');
var path = require('path')
var router = express.Router();
var formidable = require('formidable')
const {PythonShell} = require("python-shell");


router.post('/compile', (req, res) => {
  var form = new formidable.IncomingForm()
  form.parse(req, (erro,fields,files)=>{
      var fenviado = files.ficheiro.path
      /*
      var caminho =fields.caminho
      var tipo = fields.tipo
      console.log("POST [tipo]:"+tipo)
      console.log("POST [caminho]:"+caminho)
      */
      var tipo = fields.tipo
      console.log("POST [tipo]:"+tipo)
      var fnovo = './public/uploaded/'+files.ficheiro.name
      console.log("POST [fnovo]:"+fnovo)
      
      fs.rename(fenviado, fnovo, erro => {
          if(!erro){
            let options = {
              mode: 'text',
              pythonPath: '/usr/bin/python3',
              pythonOptions: ['-u'], // get print results in real-time
              scriptPath: './public/pyscripts',
              args: [tipo,fnovo,'./public/uploaded/keywords_pt.json']
            };
             
            PythonShell.run('analisador.py', options, function (err, results) {
              if (err) throw err;
              // results is an array consisting of messages collected during execution
              console.log('results: %j', results);
              res.redirect('/')
            });
          }
          else{
              console.log('Ocorreu erro no rename')
              res.end()
          }
      })
  })  
})

router.get('/getFiles/:tipo',function(req,res,next){
  var tipoEmURL = (req.params.tipo)
  /*var listFiles
  var tipoEmURL = (req.params.tipo)
  var folderPath = '../../Extratos/'+tipoEmURL

  var listFiles = fs.readdirSync(folderPath);
  */
  /*fs.readdirSync(folderPath).forEach(file=>{
    console.log(file);
  })*/

  //console.log(listFiles);
  res.render('fileSelect',{tipo: tipoEmURL});
});


module.exports = router;
