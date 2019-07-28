var express = require('express');
var router = express.Router();
var formidable = require('formidable')
var fs = require('fs');
var path = require('path');
const {PythonShell} = require("python-shell");

var youtubeSet=["id","user","date","timestamp","commentText","likes","hasReplies","numberOfReplies","hasKW"]

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Harambe' });
});


module.exports = router;
