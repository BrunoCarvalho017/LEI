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
  var folderPath = '../../../Extratos/'+tipoEmURL

  fs.readdirSync(folderPath).forEach(file=>{
    console.log(file);
  })

  console.log(listFiles);
  //res.render('fileSelect',{files: listFiles});
});

module.exports = router;
