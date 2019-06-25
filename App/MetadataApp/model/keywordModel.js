var mongoose = require('mongoose')
var Schema = mongoose.Schema

var KeywordSchema = new Schema (
    {}, { strict: false }
)



module.exports = mongoose.model('Keywords', KeywordSchema, 'keywords')