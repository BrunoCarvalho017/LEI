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
    metadata['source_type']=fields.source_type
    metadata['url']=fields.url
    metadata['platform']=fields.platform
    metadata['post_text']=fields.post_text
    metadata['cpo']=fields.cpo
    metadata['svs']=fields.featured_svs
    metadata['kws']=fields.featured_kws
    metadata['fich']=fields.ficheiro
    metadata['subtitle']=fields.subtitle
    metadata['owner']=fields.owner
    metadata['title']=fields.title
    

    console.log(fields)
    //Construção da string que contém informação sobre keywords
    var keywords= ""
    if(metadata['kws']){
      for(var i =0; i< metadata['kws'].length;i++){
        if(i==0){
          keywords+= metadata['kws'][i]
        }else{
          keywords+=", " + metadata['kws'][i]
        }
      }
    }

    //Construção da string que contém informação sobre variaveis sociolingusiticas
    var socialVar = ""
    if(metadata['svs']){
      for(var j =0; j< metadata['svs'].length;j++){
        if(i==0){
          socialVar+= metadata['svs'][j]
        }else{
          socialVar+=", " + metadata['svs'][j]
        }
      }
    }
  
    var obj
    var file = ''+metadata['fich']
    console.log('Ficheiro: '  + file)
    fs.readFile(file,function(erro,data){
      if(!erro){
        obj = JSON.parse(data);
        //Precisa identificar o que é o listEvents!
        obj.header.keywords=keywords
        obj.header.socioLingVar=socialVar
        obj.header.language=metadata['lang']
        obj.header.datePosted=metadata['date_p']
        obj.header.dateExtraction=metadata['date_e']
        obj.header.plataform=metadata['platform']
        obj.header.scrType=metadata['source_type']
        obj.header.postText=metadata['post_text']
        obj.header.subtitle=metadata['subtitle']
        obj.header.commentsOpen=metadata['cpo']
        obj.header.owner=metadata['owner']
        obj.header.title=metadata['title']
        //obj.header.id=value
        
        
        axios.post('http://localhost:3001/api/ficheiros/', obj)
             .then(dados =>{
                //console.log(dados.data)
              }).catch(erro=>{
                console.log("ERRO no post: " + erro)
              })

        //file remove
        fs.unlink(file, function (err) {
          if (err) throw err;
          console.log('File deleted!');
        });
        
        res.redirect('/')
      }else{
        console.log("Erro a ler o ficheiro")
        res.render('error',{error: erro});
      }
    })
    
  })


})

router.post('/compile', (req, res) => {
  var form = new formidable.IncomingForm()
  form.parse(req, (erro,fields,files)=>{
      var fenviado = files.ficheiro.path

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
                        args: [fnovo]
                      };
                      
                      PythonShell.run('analisador.py', options, function (err, results) {
                        if (!err) {
                          // results is an array consisting of messages collected during execution
                          console.log('results: %j', results);

                          let rawdata = fs.readFileSync('metadata.json');  
                          metadata = JSON.parse(rawdata);  
                          console.log(metadata)
                          res.render('metadataSubmission',{prints: results, kws: metadata.kws, svs: metadata.svs, ficheiro:fnovo, csv:metadata.csv});
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

router.get('/download/tool', (req,res)=>{
    const filePath = path.join(__dirname, "..", "public", "exports", "forJSON-v2.py") 
    res.download(filePath, function(err) {
        console.log(err)
    });
});

router.get('/download/csv/:id', (req,res)=>{
  const filePath = path.join(__dirname, "..", "public", "exports", req.params.id+".xlsx") 
  res.download(filePath, function(err) {
      console.log(err)
  });
});


module.exports = router;
