var express = require('express');
var router = express.Router();
var Ficheiros = require('../controller/ficheirocontroller');

router.get('/', function(req, res) {
    Ficheiros.NomeFicheiros()
        .then(dados => res.jsonp(dados))
        .catch(erro => res.status(500).send("ERROR na listagem" + erro))
});

router.get('/:id',function(req, res) {
    Ficheiros.ficheiro(req.params.id)
        .then(dados => res.jsonp(dados))
        .catch(erro => res.status(500).send("ERROR na consulta" + erro))
});

module.exports = router;