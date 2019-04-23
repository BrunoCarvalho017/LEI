var express = require('express');
var fs = require('fs');
var path = require('path')
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
  res.send('respond with a resource');
});

router.get('/getFiles/:tipo',function(req,res,next){
  var listFiles
  var tipoEmURL = (req.params.tipo)
  var folderPath

  if(tipoEmURL == 'youtube')
    folderPath = '../../Extratos/'+tipoEmURL+'/fase2'
  else
    folderPath = '../../Extratos/'+tipoEmURL

  var listFiles = fs.readdirSync(folderPath);

  /*fs.readdirSync(folderPath).forEach(file=>{
    console.log(file);
  })*/

  console.log(listFiles);
  //res.render('fileSelect',{files: listFiles});
});

module.exports = router;
