var express = require('express');
var router = express.Router();
var KeywordsController = require('../../controller/keywordController');


router.get('/', function(req, res) {
    KeywordsController.listaPreconceito()
        .then(dados => res.jsonp(dados))
        .catch(erro => res.status(500).send("ERROR na listagem" + erro))
});

router.post('/', function(req, res) {
    KeywordsController.inserePrejudice(req.params,req.body)
        .then(dados => res.jsonp(dados))
        .catch(erro => res.status(500).send("ERROR na listagem" + erro))
});

router.get('/:id', function(req, res) {
    KeywordsController.listaVars(req.params.id)
        .then(dados => res.jsonp(dados))
        .catch(erro => res.status(500).send("ERROR na listagem" + erro))
});

router.post('/:id', function(req, res) {
    KeywordsController.insereVar(req.params,req.body)
        .then(dados => res.jsonp(dados))
        .catch(erro => res.status(500).send("ERROR na listagem" + erro))
});

router.get('/:id/:id2/pt', function(req, res) {
    KeywordsController.getKeywordByIdPt(req.params.id)
        .then(dados => res.jsonp(dados))
        .catch(erro => res.status(500).send("ERROR na listagem" + erro))
});

router.get('/:id/:id2/en', function(req, res) {
    KeywordsController.getKeywordByIdEn(req.params.id)
        .then(dados => res.jsonp(dados))
        .catch(erro => res.status(500).send("ERROR na listagem" + erro))
});

router.post('/:id/:id2', function(req, res) {
    console.log(req)
    KeywordsController.adicionaKeyword(req.params,req.body)
    .then(dados=> res.jsonp(dados))
    .catch(erro=> res.status(500).send('Erro na inserção [KEYWORDS]: ' + erro));
});

module.exports = router;