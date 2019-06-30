var express = require('express');
var router = express.Router();
var Football = require('../controllers/football');

router.get('/competitions', async function(req, res, next) {
    var dados = await Football.listCompetitions();
    res.jsonp(dados);
});

router.get('/competitions/:id/seasons', async function(req, res, next) {
    var dados = await Football.listCompetitionSeasons(req.params.id);
    res.jsonp(dados);
});

router.get('/classification/:id', async function(req, res, next) {
    var dados = await Football.listSeasonClassification(req.params.id);
    res.jsonp(dados);
});

router.get('/squad/:id', async function(req, res, next) {
    var dados = await Football.listSeasonSquad(req.params.id);
    res.jsonp(dados);
});
    
router.get('/player/:id', async function(req, res, next) {
    var dados = await  Football.listPlayer(req.params.id);
    res.jsonp(dados);
});

module.exports = router;
