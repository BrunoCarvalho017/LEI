var express = require('express');
var axios = require('axios')
var router = express.Router();

/* GET lista de ficheiros analisados*/
router.get('/', function(req, res) {
    axios.get('http://localhost:3001/api/ficheiros/')
         .then(ficheiros => {
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
            res.render('files/visualizacao', {ficheiro: ficheiro.data})
            console.log(ficheiro.data)
        })
})

/* POST create a ficheiro */
router.post('/', function(req, res) {
})


module.exports = router;