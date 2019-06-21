var mongoose = require('mongoose')
var Schema = mongoose.Schema

var SociolinguisticSchema = new Schema (
    {
        pt:{type:variablesSchema, required: true},
        en:{type:variablesSchema, required: true},
    }
)

var KeywordSchema = new Schema (
    {
        type_prejudice:{type: String, required: true},
        sociolinguistic_variables:{type: SociolinguisticSchema, required: true}
    }
)

module.exports = mongoose.model('Keywords', FicheiroSchema, 'keywords')