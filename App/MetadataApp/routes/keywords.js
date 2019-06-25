var express = require('express');
var axios = require('axios')
var router = express.Router();

/* GET lista de Keywords analisados*/
router.get('/', function(req, res) {
    axios.get('http://localhost:3001/api/keywords/')
         .then(Keywords => {
             res.render('keywords/keywords', {keywords: Keywords.data})
         })
         .catch(err => {
            res.render('error', {error:err})
        })
});

router.get('/:id', function(req, res) {
    axios.get('http://localhost:3001/api/keywords/'+req.params.id)
         .then(Keywords => {
             res.render('keywords/sociolingual', {keywords: Keywords.data})
         })
         .catch(err => {
            res.render('error', {error:err})
        })
});



router.get('/:id/:id2', function(req, res) {
    axios.all([
        axios.get('http://localhost:3001/api/keywords/'+req.params.id +'/'+ req.params.id2 + '/pt'),
        axios.get('http://localhost:3001/api/keywords/'+req.params.id +'/'+ req.params.id2 + '/en')
      ])
    .then(axios.spread(function (pt, en) {
        res.render('keywords/adicionarkey', {keywordspt : pt.data , keywordsen : en.data ,  aux1 : req.params.id , aux2 : req.params.id2})
    }))
    .catch(err => {
        res.render('error', {error:err})
    })
})


router.post('/:id/:id2', function(req, res) {
    axios.post('http://localhost:3001/api/keywords/'+req.params.id +'/'+ req.params.id2, req.body)
    .then(()=> res.redirect('http://localhost:3001/'))
    .catch(err => {
        console.log('Erro na inserção [Keyword]')
        res.render('error', {error:err})
    })
});





module.exports = router;