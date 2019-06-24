var express = require('express');
var router = express.Router();
var FicheirosController = require('../../controller/ficheiroController');


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

router.post('/',function(req,res) {
    FicheirosController.addFicheiro()
});



module.exports = router;