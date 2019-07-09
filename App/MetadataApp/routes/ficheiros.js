var express = require('express');
var axios = require('axios')
var fs = require('fs');
var path = require('path');
var util = require('util');
var moment = require('moment');
var router = express.Router();

/* GET lista de ficheiros analisados*/
router.get('/', function(req, res) {
    axios.get('http://localhost:3001/api/ficheiros/')
         .then(ficheiros => {
             console.log(ficheiros.data)
             res.render('files/files', {ficheiros: ficheiros.data})
         })
         .catch(err => {
            res.render('error', {error:err})
        })
});

/* GET ficheiro pelo seu id*/
router.get('/:id', (req,res) => {
    axios.get('http://localhost:3001/api/ficheiros/' + req.params.id)
        .then(ficheiro => {
            console.log(ficheiro.data)
            res.render('files/visualizacao', {ficheiro: ficheiro.data})
        })
});

router.get('/download/:id', (req,res)=>{
    axios.get('http://localhost:3001/api/ficheiros/download/' + req.params.id)
        .then(dados => {
            const time = moment().format('YYYYMMDDhhmmss')
            const filePath = path.join(__dirname, "..", "public", "exports", "json-" + time + ".json")
            var json = JSON.stringify(dados.data,null,'\t')
            fs.writeFile(filePath, json, function (err) {
                if (err) {
                  return res.json(err).status(500);
                }
                else {
                    res.download(filePath, function(err) {
                        console.log(err)
                    });
                }
              });      
    }).catch(err => {
        res.render('error', {error: err})
    })
});

router.post('/delete/:id', (req,res) =>{
    axios.post('http://localhost:3001/api/ficheiros/delete/' + req.params.id)
        .then(ficheiro => {
            
        })
        .catch(err => {
            res.render('error', {error:err})
        })
});

/* POST create a ficheiro */
router.post('/', function(req, res) {
})

module.exports = router;