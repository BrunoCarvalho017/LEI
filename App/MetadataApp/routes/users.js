var express = require('express');
var fs = require('fs');
var path = require('path');
var router = express.Router();
var formidable = require('formidable')
const {PythonShell} = require("python-shell");
//const metadata = require('../metadata.json');
var axios = require('axios')

var metadata;

router.post('/submitMeta', (req,res) => {
  var form = new formidable.IncomingForm()
  form.parse(req, (erro,fields,files)=>{
    metadata['cmc']=fields.cmc
    metadata['lang']=fields.lang
    metadata['date_p']=fields.date_p
    metadata['date_e']=fields.date_e
    metadata['title_type']=fields.title_type
    metadata['url_type']=fields.url_type
    metadata['setting']=fields.setting
    metadata['platform']=fields.platform
    metadata['extract_file_type']=fields.extract_file_type
    metadata['sorce_type']=fields.source_type
    metadata['cpo']=fields.cpo
   
    json = JSON.stringify(metadata); //convert it back to json
    fs.writeFile('metadata.json', json, 'utf8', (err) => {
      if (err) throw err;
      console.log('Data written to file');
      res.redirect('/')
    }); 
  })

})

router.post('/compile', (req, res) => {
  var form = new formidable.IncomingForm()
  form.parse(req, (erro,fields,files)=>{
      var fenviado = files.ficheiro.path
    
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

              //Leitura do metadata (refresshing do ficheiro metadata;) 
            try {
              let rawdata = fs.readFileSync('metadata.json');  
              metadata = JSON.parse(rawdata);  
              console.log(metadata)
            } catch (err) {
              console.error(err)
            }

              res.render('metadataSubmission',{prints: results, kws: metadata.kws, svs: metadata.svs });
            });
          }
          else{
              console.log('Ocorreu erro no rename')
              res.end()
          }
      })
  })  
})

router.get('/projeto',function(req,res,next){
      res.render('projeto');
});

router.get('/utilizar',function(req,res,next){
  res.render('utilizar');
});

router.get('/grupo',function(req,res,next){
  res.render('grupo');
});



router.get('/getFiles/:tipo',function(req,res,next){
  var tipoEmURL = (req.params.tipo)
  res.render('fileSelect',{tipo: tipoEmURL});
});

router.get('/visualizacao/:id',function(req,res,next){
  axios.get('http://localhost:3000/api/'+req.params.id)
  .then(ficheiro => res.render('visualizacao', {ficheiro: ficheiro.data}))
  .catch(erro => {
      console.log('Erro na consulta do evento: ' + erro)
      res.render('index')})
});


router.get('/listavisualizacao',function(req,res,next){
  axios.get('http://localhost:3000/api/')
  .then(ficheiro => res.render('listaderesults', {ficheiro: ficheiro.data}))
  .catch(erro => {
      console.log('Erro na consulta do evento: ' + erro)
      res.render('index')})
});

module.exports = router;
