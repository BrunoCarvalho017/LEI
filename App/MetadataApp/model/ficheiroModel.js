var mongoose = require('mongoose')
var Schema = mongoose.Schema

/*var ReplieSchema = new Schema (
    {
        id:{type:String,required:true},
        user:{type:String,required:true},
        commentText:{type:String,required:true},
    }
)
var ComentarioSchema = new Schema (
    {
        id:{type:String, required: true},
        user:{type:String, required: true},
        commentText:{type:String,required: true},
        hasReplies:{type:Boolean,required: true},
        replies:{type:[ReplieSchema],required:false}
    })

 var FicheiroSchema = new Schema (
    {
        title:{type: String, required: true},
        plataform: {type: String, required: true},
        url: {type: String, required: true},
        numberPosts:{type: String, required: true},
        keywords:{type: String, required: true},
        socioLingVar:{type: String, required: true},
        comments:{type:[ComentarioSchema],required:true}
    }*/
var FicheiroSchema = new Schema (
    
        {},{strict: false}

)


module.exports = mongoose.model('Ficheiros', FicheiroSchema, 'ficheiros')