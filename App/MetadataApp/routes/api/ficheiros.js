var express = require('express');
var router = express.Router();
var FicheirosController = require('../../controller/ficheiroController');

router.get('/conta', (req, res) =>{
    FicheirosController.getFicheiroCount()
                .then(dados => res.jsonp(dados))
                .catch(erro => res.status(500).send("ERROR na listagem" + erro))
});


router.get('/', function(req, res) {
    FicheirosController.listaFicheiros()
        .then(dados => res.jsonp(dados))
        .catch(erro => res.status(500).send("ERROR na listagem" + erro))
});

router.get('/:id', function(req, res) {
    FicheirosController.getFicheiroById(req.params.id)
                .then(dados => {res.jsonp(dados)})
                .catch(err => {res.status(500).jsonp(err)})
});

router.post('/delete/:id', function(req, res) {
    FicheirosController.removeFicheiro(req.params.id)
                .then(dados => {res.jsonp(dados)})
                .catch(err => {res.status(500).jsonp(err)})
});

router.post('/', (req,res)=> {
    var obj = req.body
    FicheirosController.addFicheiro(obj)
                       .then(dados => {res.jsonp(dados)})
                       .catch(err => {res.status(500).jsonp("erro:"+ err)})
});

router.get('/download/:id', (req,res) =>{
    FicheirosController.getFicheiroById(req.params.id)
                .then(dados => {res.jsonp(dados)})
                .catch(err => {res.status(500).jsonp(err)})
});

router.post('/',function(req,res) {
    FicheirosController.addFicheiro()
});



module.exports = router;