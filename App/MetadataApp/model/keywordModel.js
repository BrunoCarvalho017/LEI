var mongoose = require('mongoose')
var Schema = mongoose.Schema





var KeywordSchema = new Schema (
    {
        type_prejudice:{type: String, required: true},
    }
)



module.exports = mongoose.model('Keywords', KeywordSchema, 'keywords')