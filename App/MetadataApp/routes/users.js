var express = require('express');
var fs = require('fs');
var path = require('path');
var util = require('util');
var router = express.Router();
var formidable = require('formidable')
const {PythonShell} = require("python-shell");
//const metadata = require('../metadata.json');
var axios = require('axios')

var metadata;


// var validate = require('json-schema').validate;
var Ajv = require('ajv');
var ajv = new Ajv(); // options can be passed, e.g. {allErrors: true}


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
    metadata['source_type']=fields.source_type
    metadata['cpo']=fields.cpo
    metadata['svs']=fields.featured_svs
    metadata['kws']=fields.featured_kws

    console.log(fields)

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
            // Load a schema by which to validate
            fs.readFile('schema.json',function(err,rawdata) {
              if(!err) {
                var schema = JSON.parse(rawdata);
                // Load data file
                fs.readFile(fnovo,function(err,rawdata) {
                  if(!err) {
                    // Parse as JSON
                    var submited_file = JSON.parse(rawdata);

                    var validate = ajv.compile(schema);
                    var valid = validate(submited_file);
                    console.log(valid)

                    if(valid){
                      let options = {
                        mode: 'text',
                        pythonPath: '/usr/bin/python3',
                        pythonOptions: ['-u'], // get print results in real-time
                        scriptPath: './public/pyscripts',
                        args: [tipo,fnovo,'./public/uploaded/keywords_pt.json']
                      };
                      
                      PythonShell.run('analisador.py', options, function (err, results) {
                        if (!err) {
                          // results is an array consisting of messages collected during execution
                          console.log('results: %j', results);

                          let rawdata = fs.readFileSync('metadata.json');  
                          metadata = JSON.parse(rawdata);  
                          console.log(metadata)
                          res.render('metadataSubmission',{prints: results, kws: metadata.kws, svs: metadata.svs });
                        }
                        else{
                          console.log("Erro no analisador")
                          res.render('error',{error: err});
                        }
                      });
                    }
                    else{
                      console.log("Ficheiro não corresponde ao esquema")
                      res.jsonp({success : valid})
                      //res.render('error',{error: err});
                    }
                  }
                  else{
                    // throw err
                    console.log("Erro na leitura do ficheiro")
                    res.render('error',{error: err});
                  }
                });
              }
              else{
                // throw err
                console.log("Erro na leitura do esquema")
                res.render('error',{error: err});
              }
            });
          } 
          else{
              console.log('Ocorreu erro no rename')
              //res.render('error',{error: "Erro no rename!!!"});
              res.end()
          }
      })
  })  
})

router.get('/projeto',function(req,res,next){
      res.render('about/projeto');
});

router.get('/utilizar',function(req,res,next){
  res.render('about/utilizar');
});

router.get('/grupo',function(req,res,next){
  res.render('about/grupo');
});

router.get('/getFiles/:tipo',function(req,res,next){
  var tipoEmURL = (req.params.tipo)
  res.render('fileSelect',{tipo: tipoEmURL});
});





module.exports = router;
