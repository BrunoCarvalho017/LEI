var mongoose = require('mongoose')
var Schema = mongoose.Schema

var FicheiroSchema = new Schema (
    {
        title:{type: String, required: true},
        plataform: {type: String, required: true},
        url: {type: String, required: true},
        numberPosts:{type: String, required: true},
        keywords:{type: String, required: true},
        socioLingVar:{type: String, required: true}
    }
)

module.exports = mongoose.model('Ficheiros', FicheiroSchema, '//nome da cena')